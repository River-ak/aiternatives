"""Tool and alternative discovery via web search and ProductHunt API."""
import json
import re
import urllib.request
import urllib.error

from .config import PRODUCTHUNT_TOKEN, GOOGLE_API_KEY
from .supabase_ops import get_existing_slugs, create_tool_from_discovery, upsert_alternative

# Known categories with parent-child relationships for slug generation
CATEGORY_MAP = {
    "text generation": "text_gen",
    "text gen": "text_gen",
    "chat": "text_gen",
    "llm": "text_gen",
    "image generation": "image_gen",
    "image gen": "image_gen",
    "design": "image_gen",
    "code assistant": "code_assist",
    "code assist": "code_assist",
    "coding": "code_assist",
    "developer": "code_assist",
    "content writing": "content_writing",
    "content": "content_writing",
    "writing": "content_writing",
    "copywriting": "content_writing",
    "video generation": "video_gen",
    "video": "video_gen",
    "productivity": "productivity",
    "notes": "productivity",
    "project management": "productivity",
}


def slugify(name: str) -> str:
    """Convert a tool name to a URL-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = slug.strip("-")
    return slug


def guess_category(name: str, description: str = "") -> str:
    """Try to guess the category from name and description."""
    combined = f"{name} {description}".lower()
    for keyword, category in CATEGORY_MAP.items():
        if keyword in combined:
            return category
    return "text_gen"  # default


# ---- ProductHunt Trending (if API key available) ----


def fetch_producthunt_ai_tools() -> list[dict]:
    """Fetch trending AI tools from ProductHunt."""
    if not PRODUCTHUNT_TOKEN:
        return []

    url = "https://api.producthunt.com/v2/api/graphql"
    query = """
    query {
      posts(first: 20, topic: "artificial-intelligence", order: VOTES) {
        edges {
          node {
            name
            tagline
            description
            website
            topics { edges { node { name } } }
            votesCount
          }
        }
      }
    }
    """
    req = urllib.request.Request(
        url,
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {PRODUCTHUNT_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            posts = data.get("data", {}).get("posts", {}).get("edges", [])
            tools = []
            for edge in posts:
                node = edge["node"]
                tools.append({
                    "name": node["name"],
                    "tagline": node.get("tagline", ""),
                    "description": node.get("description", "")[:300],
                    "website": node.get("website", ""),
                    "votes": node.get("votesCount", 0),
                })
            return tools
    except Exception as e:
        print(f"[discovery] ProductHunt fetch error: {e}")
        return []


# ---- Static discovery: high-signal AI tools not yet in our DB ----


HIGH_SIGNAL_TOOLS = [
    # --- Image Gen ---
    {"name": "Flux AI", "slug": "flux-ai", "category": "image_gen", "description": "Black Forest Labs 的开源图像生成模型系列，以照片级真实感著称。", "website_url": "https://blackforestlabs.ai", "pricing_model": "freemium", "has_free_tier": True, "features": ["Text-to-Image", "High Realism", "Open Source", "Community Models"], "user_rating": 4.6, "rating_source": "ProductHunt", "rating_count": 3200},
    {"name": "Krea AI", "slug": "krea-ai", "category": "image_gen", "description": "实时 AI 图像生成和编辑工具，支持即时美化。", "website_url": "https://krea.ai", "pricing_model": "freemium", "min_monthly_price": 10, "has_free_tier": True, "features": ["Real-time Generation", "Upscale", "Canvas Editor", "Prompt Mixing"], "user_rating": 4.5, "rating_source": "ProductHunt", "rating_count": 2100},
    # --- Text Gen ---
    {"name": "Groq", "slug": "groq", "category": "text_gen", "description": "超低延迟 LLM 推理平台，提供多个开源模型的 API 访问。", "website_url": "https://groq.com", "pricing_model": "usage_based", "has_free_tier": True, "has_api": True, "features": ["Low Latency", "Chat API", "Multiple Models", "Developer Tools"], "user_rating": 4.7, "rating_source": "G2", "rating_count": 1800},
    {"name": "Poe", "slug": "poe", "category": "text_gen", "description": "Quora 推出的 AI 聊天聚合平台，一个界面访问多个模型。", "website_url": "https://poe.com", "pricing_model": "freemium", "min_monthly_price": 19.99, "has_free_tier": True, "has_free_trial": False, "features": ["Multi-Model", "Chat", "Bot Creation", "Knowledge Base"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 3200},
    # --- Code ---
    {"name": "Cursor", "slug": "cursor", "category": "code_assist", "description": "AI-first 代码编辑器，内置 ChatGPT 和 Claude 集成。", "website_url": "https://cursor.sh", "pricing_model": "freemium", "min_monthly_price": 20, "has_free_tier": True, "has_free_trial": True, "features": ["Code Generation", "Refactoring", "Inline Chat", "Codebase Understanding"], "user_rating": 4.8, "rating_source": "ProductHunt", "rating_count": 5200},
    {"name": "Windsurf", "slug": "windsurf", "category": "code_assist", "description": "Codeium 推出的 AI IDE，支持 Cascade 流式代码生成。", "website_url": "https://codeium.com/windsurf", "pricing_model": "freemium", "min_monthly_price": 15, "has_free_tier": True, "features": ["Code Generation", "Cascade Flows", "Context Awareness", "Multi-File Edit"], "user_rating": 4.6, "rating_source": "ProductHunt", "rating_count": 2800},
    # --- Content ---
    {"name": "Sudowrite", "slug": "sudowrite", "category": "content_writing", "description": "专为小说和创意写作设计的 AI 助手。", "website_url": "https://sudowrite.com", "pricing_model": "subscription", "min_monthly_price": 24, "has_free_tier": False, "has_free_trial": True, "features": ["Story Engine", "Character Development", "Prose Rewrite", "Plot Outline"], "user_rating": 4.5, "rating_source": "ProductHunt", "rating_count": 900},
    # --- Productivity ---
    {"name": "Gamma", "slug": "gamma", "category": "productivity", "description": "AI 驱动的演示文稿、文档和网站生成器。", "website_url": "https://gamma.app", "pricing_model": "freemium", "min_monthly_price": 10, "has_free_tier": True, "features": ["AI Presentations", "AI Documents", "AI Websites", "Templates"], "user_rating": 4.7, "rating_source": "G2", "rating_count": 3800},
    # --- Video ---
    {"name": "Pika", "slug": "pika", "category": "video_gen", "description": "AI 视频生成和编辑工具，支持文本/图像转视频。", "website_url": "https://pika.art", "pricing_model": "freemium", "min_monthly_price": 10, "has_free_tier": True, "features": ["Text-to-Video", "Image-to-Video", "Video Editing", "Lip Sync"], "user_rating": 4.3, "rating_source": "ProductHunt", "rating_count": 4500},
    {"name": "HeyGen", "slug": "heygen", "category": "video_gen", "description": "AI 数字人视频生成平台，支持唇形同步和多语言。", "website_url": "https://heygen.com", "pricing_model": "subscription", "min_monthly_price": 24, "has_free_tier": True, "has_free_trial": False, "features": ["AI Avatars", "Lip Sync", "Multi-language", "Templates"], "user_rating": 4.6, "rating_source": "G2", "rating_count": 2100},
]


def discover_new_tools() -> list[dict]:
    """Discover tools not yet in our database. Returns list of new tools added."""
    existing = get_existing_slugs()
    new_tools = []

    # 1. Static high-signal list
    for tool in HIGH_SIGNAL_TOOLS:
        if tool["slug"] not in existing:
            if create_tool_from_discovery(
                name=tool["name"],
                slug=tool["slug"],
                category=tool["category"],
                description=tool.get("description", ""),
                website_url=tool.get("website_url", ""),
                pricing_model=tool.get("pricing_model", "freemium"),
                min_monthly_price=tool.get("min_monthly_price"),
                has_free_tier=tool.get("has_free_tier", False),
                has_free_trial=tool.get("has_free_trial", False),
                features=tool.get("features", []),
                user_rating=tool.get("user_rating"),
                rating_source=tool.get("rating_source"),
                rating_count=tool.get("rating_count", 0),
                affiliate_url=tool.get("affiliate_url", tool.get("website_url", "")),
            ):
                new_tools.append(tool)
                existing.add(tool["slug"])
                print(f"[discovery] Added tool: {tool['name']} ({tool['slug']})")

    # 2. ProductHunt trending (if API key configured)
    ph_tools = fetch_producthunt_ai_tools()
    for pt in ph_tools:
        slug = slugify(pt["name"])
        if slug not in existing and slug:  # skip empty slugs
            category = guess_category(pt["name"], pt.get("description", ""))
            if create_tool_from_discovery(
                name=pt["name"],
                slug=slug,
                category=category,
                description=pt.get("description", "")[:300],
                website_url=pt.get("website", ""),
                pricing_model="freemium",
                has_free_tier=True,
                features=[],
                affiliate_url=pt.get("website", ""),
            ):
                new_tools.append({"name": pt["name"], "slug": slug, "category": category})
                existing.add(slug)
                print(f"[discovery] Added PH tool: {pt['name']} ({slug})")

    print(f"[discovery] Total new tools: {len(new_tools)}")
    return new_tools


# ---- Alternative relationship generation (heuristic-based) ----


FEATURE_BASED_RELATIONS = {
    "text_gen": [
        {"slugs": ["claude", "gemini", "perplexity", "deepseek", "mistral", "groq", "poe"], "reason": "Text generation and chat AI alternatives"},
    ],
    "image_gen": [
        {"slugs": ["stable-diffusion", "dalle-3", "leonardo-ai", "adobe-firefly", "ideogram", "flux-ai", "krea-ai"], "reason": "AI image generation and editing alternatives"},
    ],
    "code_assist": [
        {"slugs": ["copilot", "cursor", "windsurf", "mistral"], "reason": "AI code generation and developer tools"},
    ],
    "content_writing": [
        {"slugs": ["writesonic", "rytr", "jasper", "copy-ai", "anyword", "grammarly", "wordtune", "sudowrite"], "reason": "AI content writing and editing tools"},
    ],
    "productivity": [
        {"slugs": ["notion-ai", "coda-ai", "clickup-ai", "mem", "taskade", "craft", "obsidian", "gamma"], "reason": "AI productivity and workspace tools"},
    ],
    "video_gen": [
        {"slugs": ["runway-ml", "pika", "heygen"], "reason": "AI video generation and editing tools"},
    ],
}


def discover_alternatives() -> int:
    """Find and create alternative relationships based on category overlap.
    Returns count of new relationships created."""
    from .supabase_ops import get_source_tools, get_existing_alternatives, upsert_alternative
    import time

    source_tools = get_source_tools()
    total_created = 0

    for source in source_tools:
        source_id = source["id"]
        source_slug = source["slug"]
        source_category = source["category"]

        # Find relevant relation group
        relation_group = FEATURE_BASED_RELATIONS.get(source_category)
        if not relation_group:
            continue

        # Get already-linked alternatives
        existing_alts = get_existing_alternatives(source_id)

        # Get potential alternatives by slug
        for group in relation_group:
            for alt_slug in group["slugs"]:
                if alt_slug == source_slug:  # skip self
                    continue

                from .supabase_ops import get_tool_by_slug
                alt_tool = get_tool_by_slug(alt_slug)
                if not alt_tool:
                    continue

                alt_id = alt_tool["id"]
                if alt_id in existing_alts:
                    continue

                # Create relationship with default quality score
                base_score = 75
                # Bonus for same category
                if alt_tool.get("category") == source_category:
                    base_score += 5
                # Bonus if both have ratings
                if source.get("user_rating") and alt_tool.get("user_rating"):
                    base_score += 5

                ok = upsert_alternative(
                    source_tool_id=source_id,
                    alternative_tool_id=alt_id,
                    quality_score=min(base_score, 95),
                    similarity_reason=group["reason"],
                    feature_overlap=alt_tool.get("features", [])[:5],
                    sort_order=total_created + 1,
                )
                if ok:
                    total_created += 1
                    existing_alts.add(alt_id)
                    print(f"[discovery] Alternative: {source_slug} ← {alt_slug} (score={base_score})")
                    time.sleep(0.1)  # rate limit

    print(f"[discovery] Total new alternatives: {total_created}")
    return total_created
