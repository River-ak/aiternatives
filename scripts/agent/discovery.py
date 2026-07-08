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
    # === Text Gen Expansion ===
    {"name": "HuggingChat", "slug": "huggingchat", "category": "text_gen", "description": "Hugging Face 推出的开源 LLM 聊天界面，支持多种模型切换。", "website_url": "https://huggingface.co/chat", "pricing_model": "free", "has_free_tier": True, "has_api": True, "features": ["Open Source", "Multi-Model", "Chat", "API Access"], "user_rating": 4.2, "rating_source": "ProductHunt", "rating_count": 1200},
    {"name": "Character.AI", "slug": "character-ai", "category": "text_gen", "description": "角色扮演 AI 聊天平台，支持自定义 AI 角色和对话。", "website_url": "https://character.ai", "pricing_model": "freemium", "min_monthly_price": 9.99, "has_free_tier": True, "features": ["Roleplay", "Custom Characters", "Chat", "Voice"], "user_rating": 4.6, "rating_source": "G2", "rating_count": 5600},
    {"name": "JanitorAI", "slug": "janitorai", "category": "text_gen", "description": "AI 角色扮演与聊天机器人平台，面向创意写作。", "website_url": "https://janitorai.com", "pricing_model": "freemium", "has_free_tier": True, "features": ["Roleplay", "Character Creation", "Creative Writing"], "user_rating": 3.8, "rating_source": "ProductHunt", "rating_count": 800},
    {"name": "Phind", "slug": "phind", "category": "text_gen", "description": "面向开发者的 AI 搜索引擎，实时联网获取技术答案。", "website_url": "https://phind.com", "pricing_model": "freemium", "min_monthly_price": 20, "has_free_tier": True, "features": ["Code Search", "Technical Q&A", "Citations", "Multi-Model"], "user_rating": 4.5, "rating_source": "ProductHunt", "rating_count": 1600},
    {"name": "YouChat", "slug": "youchat", "category": "text_gen", "description": "You.com 的 AI 聊天助手，集成实时搜索和多模态。", "website_url": "https://you.com", "pricing_model": "freemium", "min_monthly_price": 14.99, "has_free_tier": True, "features": ["Web Search", "Chat", "Image Generation", "File Upload"], "user_rating": 4.1, "rating_source": "ProductHunt", "rating_count": 950},
    {"name": "NovelAI", "slug": "novelai", "category": "text_gen", "description": "面向小说创作者的 AI 故事生成与图像生成平台。", "website_url": "https://novelai.net", "pricing_model": "subscription", "min_monthly_price": 10, "features": ["Story Generation", "Text-to-Image", "Custom Models", "Memory System"], "user_rating": 4.3, "rating_source": "ProductHunt", "rating_count": 1100},
    {"name": "FreedomGPT", "slug": "freedomgpt", "category": "text_gen", "description": "本地运行的私密 AI 助手，无需联网。", "website_url": "https://freedomgpt.com", "pricing_model": "free", "has_free_tier": True, "features": ["Local Hosting", "Private", "Offline", "Multiple Models"], "user_rating": 3.9, "rating_source": "ProductHunt", "rating_count": 670},
    # === Image Gen Expansion ===
    {"name": "Clipdrop", "slug": "clipdrop", "category": "image_gen", "description": "Stability AI 推出的图像编辑套件，支持背景去除和图像增强。", "website_url": "https://clipdrop.co", "pricing_model": "freemium", "min_monthly_price": 11, "has_free_tier": True, "features": ["Background Removal", "Upscale", "Re-light", "Cleanup"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 1900},
    {"name": "Artbreeder", "slug": "artbreeder", "category": "image_gen", "description": "图像混合和进化工具，通过交叉生成新图像。", "website_url": "https://artbreeder.com", "pricing_model": "freemium", "min_monthly_price": 8.99, "has_free_tier": True, "features": ["Image Mixing", "Face Generation", "Landscape", "Community"], "user_rating": 4.3, "rating_source": "ProductHunt", "rating_count": 2800},
    {"name": "Remove.bg AI", "slug": "remove-bg-ai", "category": "image_gen", "description": "AI 背景去除工具，批量处理产品图片。", "website_url": "https://remove.bg", "pricing_model": "usage_based", "has_free_tier": True, "has_api": True, "features": ["Background Removal", "Batch Process", "API", "Integration"], "user_rating": 4.8, "rating_source": "G2", "rating_count": 3200},
    {"name": "Deep Dream", "slug": "deep-dream", "category": "image_gen", "description": "经典的 AI 图像艺术生成器，以迷幻风格著称。", "website_url": "https://deepdreamgenerator.com", "pricing_model": "freemium", "has_free_tier": True, "features": ["Style Transfer", "Deep Dream", "Texture Synthesis", "AI Art"], "user_rating": 4.1, "rating_source": "ProductHunt", "rating_count": 2100},
    # === Code Assist Expansion ===
    {"name": "Tabnine", "slug": "tabnine", "category": "code_assist", "description": "AI 代码补全工具，支持本地模型保护代码隐私。", "website_url": "https://tabnine.com", "pricing_model": "freemium", "min_monthly_price": 12, "has_free_tier": True, "has_free_trial": True, "features": ["Code Completion", "Local Model", "Privacy", "IDE Plugin"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 3400},
    {"name": "Codeium", "slug": "codeium", "category": "code_assist", "description": "免费 AI 代码补全工具，支持 70+ 语言和 40+ IDE。", "website_url": "https://codeium.com", "pricing_model": "freemium", "min_monthly_price": 15, "has_free_tier": True, "features": ["Code Completion", "Chat", "Multi-IDE", "Context Awareness"], "user_rating": 4.6, "rating_source": "G2", "rating_count": 4100},
    {"name": "Replit AI", "slug": "replit-ai", "category": "code_assist", "description": "在线 IDE 内置 AI 编程助手，支持一键部署。", "website_url": "https://replit.com", "pricing_model": "freemium", "min_monthly_price": 25, "has_free_tier": True, "has_free_trial": True, "features": ["Code Generation", "Debugging", "Online IDE", "Deploy"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 5200},
    {"name": "Sourcegraph Cody", "slug": "cody", "category": "code_assist", "description": "基于代码库上下文的 AI 编程助手，理解整个仓库。", "website_url": "https://sourcegraph.com", "pricing_model": "freemium", "min_monthly_price": 9, "has_free_tier": True, "has_free_trial": True, "features": ["Codebase Context", "Code Generation", "Code Review", "Auto-Fix"], "user_rating": 4.3, "rating_source": "ProductHunt", "rating_count": 1500},
    # === Content Writing Expansion ===
    {"name": "QuillBot", "slug": "quillbot", "category": "content_writing", "description": "AI 改写和摘要工具，支持学术和商务写作。", "website_url": "https://quillbot.com", "pricing_model": "freemium", "min_monthly_price": 9.95, "has_free_tier": True, "features": ["Paraphrase", "Grammar Check", "Summarizer", "Citation"], "user_rating": 4.6, "rating_source": "G2", "rating_count": 2800},
    {"name": "Hemingway AI", "slug": "hemingway-ai", "category": "content_writing", "description": "AI 辅助简化写作——让内容更清晰简洁。", "website_url": "https://hemingwayapp.com", "pricing_model": "one_time", "min_monthly_price": 19.99, "features": ["Readability", "Simplicity", "Tone", "Grammar"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 1900},
    {"name": "Typefully", "slug": "typefully", "category": "content_writing", "description": "Twitter/LinkedIn 内容创作和排期工具，内置 AI 助手。", "website_url": "https://typefully.com", "pricing_model": "freemium", "min_monthly_price": 12.5, "has_free_tier": True, "features": ["Thread Writing", "Scheduling", "AI Rewrite", "Analytics"], "user_rating": 4.7, "rating_source": "ProductHunt", "rating_count": 2200},
    {"name": "LongShot AI", "slug": "longshot-ai", "category": "content_writing", "description": "面向长文章和 SEO 博客的 AI 写作工具。", "website_url": "https://longshot.ai", "pricing_model": "subscription", "min_monthly_price": 19, "has_free_tier": True, "has_free_trial": True, "features": ["SEO Content", "Long-form", "Research", "Fact Check"], "user_rating": 4.3, "rating_source": "G2", "rating_count": 1200},
    # === Productivity Expansion ===
    {"name": "Elicit", "slug": "elicit", "category": "productivity", "description": "AI 研究助手，自动分析学术论文和提取关键发现。", "website_url": "https://elicit.com", "pricing_model": "freemium", "min_monthly_price": 10, "has_free_tier": True, "features": ["Research", "Paper Analysis", "Data Extraction", "Literature Review"], "user_rating": 4.6, "rating_source": "ProductHunt", "rating_count": 1800},
    {"name": "Tome", "slug": "tome", "category": "productivity", "description": "AI 故事讲述和演示文稿生成器，自动生成视觉叙事。", "website_url": "https://tome.app", "pricing_model": "freemium", "min_monthly_price": 16, "has_free_tier": True, "features": ["AI Presentations", "Storytelling", "Templates", "Media Integration"], "user_rating": 4.5, "rating_source": "ProductHunt", "rating_count": 3400},
    {"name": "Napkin AI", "slug": "napkin-ai", "category": "productivity", "description": "将文字自动转化为信息图表的 AI 可视化工具。", "website_url": "https://napkin.ai", "pricing_model": "freemium", "has_free_tier": True, "features": ["Text-to-Visual", "Infographics", "Diagrams", "Charts"], "user_rating": 4.8, "rating_source": "ProductHunt", "rating_count": 4300},
    {"name": "Alter", "slug": "alter-ai", "category": "productivity", "description": "AI 个人成长教练，提供行为改变和目标追踪。", "website_url": "https://alter.ai", "pricing_model": "subscription", "min_monthly_price": 29, "has_free_tier": False, "has_free_trial": True, "features": ["Coaching", "Goal Tracking", "Behavior Change", "AI Insights"], "user_rating": 4.0, "rating_source": "ProductHunt", "rating_count": 520},
    # === Video Gen Expansion ===
    {"name": "Synthesia", "slug": "synthesia", "category": "video_gen", "description": "企业级 AI 虚拟人视频生成平台，140+ 语言。", "website_url": "https://synthesia.io", "pricing_model": "subscription", "min_monthly_price": 22, "has_free_tier": False, "has_free_trial": True, "features": ["AI Avatars", "140+ Languages", "Templates", "Enterprise"], "user_rating": 4.7, "rating_source": "G2", "rating_count": 4100},
    {"name": "Pictory", "slug": "pictory", "category": "video_gen", "description": "AI 视频编辑和文字转视频工具，面向营销内容。", "website_url": "https://pictory.ai", "pricing_model": "subscription", "min_monthly_price": 19, "has_free_tier": True, "has_free_trial": False, "features": ["Blog-to-Video", "Captioning", "Editing", "Stock Footage"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 2800},
    {"name": "Descript", "slug": "descript", "category": "video_gen", "description": "AI 视频和播客编辑工具，像编辑文档一样编辑视频。", "website_url": "https://descript.com", "pricing_model": "freemium", "min_monthly_price": 24, "has_free_tier": True, "has_free_trial": True, "features": ["Text-Based Editing", "Transcription", "Screen Recording", "AI Voices"], "user_rating": 4.6, "rating_source": "G2", "rating_count": 6200},
    # === Audio / Voice ===
    {"name": "ElevenLabs", "slug": "elevenlabs", "category": "text_gen", "description": "最先进的 AI 语音合成和克隆平台，支持 29 种语言。", "website_url": "https://elevenlabs.io", "pricing_model": "freemium", "min_monthly_price": 5, "has_free_tier": True, "has_api": True, "features": ["Voice Cloning", "TTS", "29 Languages", "Fine-tuning"], "user_rating": 4.7, "rating_source": "ProductHunt", "rating_count": 5200},
    {"name": "Murf AI", "slug": "murf-ai", "category": "text_gen", "description": "AI 配音和语音合成工作室，面向视频和播客。", "website_url": "https://murf.ai", "pricing_model": "freemium", "min_monthly_price": 19, "has_free_tier": True, "has_free_trial": False, "features": ["AI Voiceover", "Templates", "Voice Customization", "Multilingual"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 2100},
    {"name": "Rask AI", "slug": "rask-ai", "category": "video_gen", "description": "AI 视频翻译和本地化工具，语音克隆 + 唇形同步。", "website_url": "https://rask.ai", "pricing_model": "subscription", "min_monthly_price": 49, "has_free_tier": False, "has_free_trial": True, "features": ["Video Translation", "Lip Sync", "Voice Cloning", "130+ Languages"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 1200},
    # === Design ===
    {"name": "Canva AI", "slug": "canva-ai", "category": "image_gen", "description": "Canva 内置的 AI 设计助手：Magic Design、文字生成图片等。", "website_url": "https://canva.com", "pricing_model": "freemium", "min_monthly_price": 12.99, "has_free_tier": True, "has_free_trial": True, "features": ["Magic Design", "Text-to-Image", "Background Remover", "Templates"], "user_rating": 4.7, "rating_source": "G2", "rating_count": 18000},
    {"name": "Uizard", "slug": "uizard", "category": "productivity", "description": "AI 驱动的 UI 设计工具，将草图转化为可交互原型。", "website_url": "https://uizard.io", "pricing_model": "freemium", "min_monthly_price": 12, "has_free_tier": True, "has_free_trial": True, "features": ["Sketch-to-UI", "Wireframe", "Prototype", "Templates"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 1500},
    # === Data / Analytics ===
    {"name": "Julius AI", "slug": "julius-ai", "category": "productivity", "description": "AI 数据分析助手，用自然语言分析 CSV/Excel 数据。", "website_url": "https://julius.ai", "pricing_model": "freemium", "min_monthly_price": 20, "has_free_tier": True, "has_free_trial": True, "features": ["Data Analysis", "Chart Generation", "CSV/Excel", "Statistics"], "user_rating": 4.6, "rating_source": "ProductHunt", "rating_count": 3200},
    {"name": "Rows", "slug": "rows-ai", "category": "productivity", "description": "内置 AI 分析助手的电子表格工具。", "website_url": "https://rows.com", "pricing_model": "freemium", "min_monthly_price": 8, "has_free_tier": True, "has_free_trial": True, "features": ["AI Spreadsheet", "Data Import", "Chart", "API Integration"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 1800},
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
        {"slugs": ["claude", "gemini", "perplexity", "deepseek", "mistral", "groq", "poe", "huggingchat", "character-ai", "phind", "youchat", "novelai", "elevenlabs", "murf-ai"], "reason": "Text generation and chat AI alternatives"},
    ],
    "image_gen": [
        {"slugs": ["stable-diffusion", "dalle-3", "leonardo-ai", "adobe-firefly", "ideogram", "flux-ai", "krea-ai", "clipdrop", "artbreeder", "canva-ai", "remove-bg-ai"], "reason": "AI image generation and editing alternatives"},
    ],
    "code_assist": [
        {"slugs": ["copilot", "cursor", "windsurf", "tabnine", "codeium", "replit-ai", "cody", "phind"], "reason": "AI code generation and developer tools"},
    ],
    "content_writing": [
        {"slugs": ["writesonic", "rytr", "jasper", "copy-ai", "anyword", "grammarly", "wordtune", "sudowrite", "quillbot", "hemingway-ai", "typefully", "longshot-ai"], "reason": "AI content writing and editing tools"},
    ],
    "productivity": [
        {"slugs": ["notion-ai", "coda-ai", "clickup-ai", "mem", "taskade", "craft", "obsidian", "gamma", "elicit", "tome", "napkin-ai", "julius-ai", "rows-ai", "uizard"], "reason": "AI productivity and workspace tools"},
    ],
    "video_gen": [
        {"slugs": ["runway-ml", "pika", "heygen", "synthesia", "pictory", "descript", "rask-ai"], "reason": "AI video generation and editing tools"},
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
