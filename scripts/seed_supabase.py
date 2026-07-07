#!/usr/bin/env python3
"""Seed Supabase with aiternatives mock data."""
import json
import os
import uuid
import urllib.request
import urllib.error

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://wqzttprkmkpzqrqjdouw.supabase.co")
SUPABASE_SERVICE_KEY = os.environ.get(
    "SUPABASE_SERVICE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxenR0cHJrbWtwenFycWpkb3V3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MzQzMDY0NywiZXhwIjoyMDk5MDA2NjQ3fQ.2OQCfzrbcHdRf8o2C9rxBDVZkdezf6wJlVR3cVFSPs8",
)

HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}


def ns_uuid(slug: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://aiternatives.com/tools/{slug}"))


SOURCE_TOOLS = [
    {
        "id": ns_uuid("chatgpt"),
        "name": "ChatGPT",
        "slug": "chatgpt",
        "category": "text_gen",
        "description": "OpenAI 的旗舰对话 AI，支持文本生成、代码、图像理解和插件生态。",
        "website_url": "https://chat.openai.com",
        "pricing_model": "subscription",
        "min_monthly_price": 20,
        "max_monthly_price": 20,
        "has_free_tier": True,
        "has_free_trial": False,
        "has_api": True,
        "features": ["Text Generation", "Code Assist", "Vision", "Plugins", "GPT-4o"],
        "user_rating": 4.7,
        "rating_source": "G2",
        "rating_count": 12000,
        "commission_type": "recurring",
        "affiliate_url": "https://chat.openai.com",
        "affiliate_network": "direct",
        "is_active": True,
    },
    {
        "id": ns_uuid("midjourney"),
        "name": "Midjourney",
        "slug": "midjourney",
        "category": "image_gen",
        "description": "AI 图像生成标杆，以艺术风格和 Discord 社区驱动著称。",
        "website_url": "https://midjourney.com",
        "pricing_model": "subscription",
        "min_monthly_price": 10,
        "max_monthly_price": 120,
        "has_free_tier": False,
        "has_free_trial": False,
        "has_api": True,
        "features": ["Text-to-Image", "Style Control", "Upscale", "Community Feed"],
        "user_rating": 4.8,
        "rating_source": "ProductHunt",
        "rating_count": 8900,
        "commission_type": "recurring",
        "affiliate_url": "https://midjourney.com",
        "affiliate_network": "direct",
        "is_active": True,
    },
    {
        "id": ns_uuid("jasper"),
        "name": "Jasper",
        "slug": "jasper",
        "category": "content_writing",
        "description": "面向营销团队的 AI 写作平台，支持品牌声音和 SEO 内容。",
        "website_url": "https://jasper.ai",
        "pricing_model": "subscription",
        "min_monthly_price": 49,
        "max_monthly_price": 125,
        "has_free_tier": False,
        "has_free_trial": True,
        "has_api": True,
        "features": ["Content Writing", "Brand Voice", "SEO", "Campaigns"],
        "user_rating": 4.0,
        "rating_source": "Capterra",
        "rating_count": 1800,
        "commission_type": "recurring",
        "affiliate_url": "https://jasper.ai",
        "affiliate_network": "PartnerStack",
        "is_active": True,
    },
    {
        "id": ns_uuid("copy-ai"),
        "name": "Copy.ai",
        "slug": "copy-ai",
        "category": "content_writing",
        "description": "AI 写作工作流自动化平台，面向销售和营销团队。",
        "website_url": "https://copy.ai",
        "pricing_model": "freemium",
        "min_monthly_price": 36,
        "max_monthly_price": 36,
        "has_free_tier": True,
        "has_free_trial": False,
        "has_api": True,
        "features": ["Content Writing", "Workflows", "Brand Voice", "Sales Copy"],
        "user_rating": 4.5,
        "rating_source": "G2",
        "rating_count": 2400,
        "commission_type": "recurring",
        "affiliate_url": "https://copy.ai",
        "affiliate_network": "PartnerStack",
        "is_active": True,
    },
    {
        "id": ns_uuid("notion-ai"),
        "name": "Notion AI",
        "slug": "notion-ai",
        "category": "productivity",
        "description": "集成在 Notion 工作区中的 AI 助手，支持写作、总结和问答。",
        "website_url": "https://notion.so",
        "pricing_model": "subscription",
        "min_monthly_price": 10,
        "max_monthly_price": 10,
        "has_free_tier": False,
        "has_free_trial": False,
        "has_api": True,
        "features": ["Note Taking", "Text Generation", "Q&A", "Database"],
        "user_rating": 4.3,
        "rating_source": "G2",
        "rating_count": 4200,
        "commission_type": "recurring",
        "affiliate_url": "https://notion.so",
        "affiliate_network": "direct",
        "is_active": True,
    },
]

ALTERNATIVE_TOOLS = [
    # ChatGPT alternatives
    {"id": ns_uuid("claude"), "name": "Claude", "slug": "claude", "category": "text_gen", "description": "Anthropic 的对话 AI，以长上下文和安全对齐著称。", "website_url": "https://claude.ai", "pricing_model": "subscription", "min_monthly_price": 20, "max_monthly_price": 20, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Text Generation", "Code Assist", "Long Context", "Vision", "Projects"], "user_rating": 4.7, "rating_source": "G2", "rating_count": 1250, "commission_type": "recurring", "affiliate_url": "https://claude.ai", "affiliate_network": "direct"},
    {"id": ns_uuid("gemini"), "name": "Gemini", "slug": "gemini", "category": "text_gen", "description": "Google 的多模态 AI，深度集成 Google 应用生态。", "website_url": "https://gemini.google.com", "pricing_model": "freemium", "min_monthly_price": 19.99, "max_monthly_price": 19.99, "has_free_tier": True, "has_free_trial": True, "has_api": True, "features": ["Multimodal", "Text Generation", "Code Assist", "Google Integration"], "user_rating": 4.3, "rating_source": "TrustPilot", "rating_count": 890, "commission_type": "recurring", "affiliate_url": "https://gemini.google.com", "affiliate_network": "direct"},
    {"id": ns_uuid("perplexity"), "name": "Perplexity", "slug": "perplexity", "category": "text_gen", "description": "结合搜索和 LLM 的答案引擎，提供带引用来源的研究。", "website_url": "https://perplexity.ai", "pricing_model": "freemium", "min_monthly_price": 20, "max_monthly_price": 20, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Web Search", "Citations", "Pro Search", "File Upload", "API Access"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 2100, "commission_type": "recurring", "affiliate_url": "https://perplexity.ai", "affiliate_network": "direct"},
    {"id": ns_uuid("mistral"), "name": "Mistral", "slug": "mistral", "category": "text_gen", "description": "欧洲开源大模型公司，提供开放权重模型和 API。", "website_url": "https://mistral.ai", "pricing_model": "usage_based", "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Open Source", "Text Generation", "Code Assist", "Fine-tuning"], "user_rating": 4.1, "rating_source": "ProductHunt", "rating_count": 450, "commission_type": "one_time", "affiliate_url": "https://mistral.ai", "affiliate_network": "direct"},
    {"id": ns_uuid("cohere"), "name": "Cohere", "slug": "cohere", "category": "text_gen", "description": "专注企业级文本模型和嵌入 API 的 AI 平台。", "website_url": "https://cohere.com", "pricing_model": "freemium", "has_free_tier": True, "has_free_trial": True, "has_api": True, "features": ["Text Generation", "Embeddings", "RAG", "Enterprise"], "user_rating": 4.2, "rating_source": "G2", "rating_count": 680, "commission_type": "recurring", "affiliate_url": "https://cohere.com", "affiliate_network": "direct"},
    {"id": ns_uuid("deepseek"), "name": "DeepSeek", "slug": "deepseek", "category": "text_gen", "description": "开源推理模型，以高性价比和代码能力著称。", "website_url": "https://deepseek.com", "pricing_model": "freemium", "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Text Generation", "Code Assist", "Reasoning", "Open Source"], "user_rating": 4.6, "rating_source": "ProductHunt", "rating_count": 3200, "commission_type": "one_time", "affiliate_url": "https://deepseek.com", "affiliate_network": "direct"},
    {"id": ns_uuid("copilot"), "name": "GitHub Copilot", "slug": "copilot", "category": "code_assist", "description": "GitHub 推出的 AI 编程助手，集成主流 IDE。", "website_url": "https://github.com/features/copilot", "pricing_model": "subscription", "min_monthly_price": 30, "max_monthly_price": 39, "has_free_tier": True, "has_free_trial": True, "has_api": True, "features": ["Code Assist", "Text Generation", "IDE Integration", "Office Suite"], "user_rating": 4.3, "rating_source": "G2", "rating_count": 5600, "commission_type": "recurring", "affiliate_url": "https://github.com/features/copilot", "affiliate_network": "direct"},
    {"id": ns_uuid("writesonic"), "name": "Writesonic", "slug": "writesonic", "category": "content_writing", "description": "面向 SEO 和内容的 AI 写作工具，支持文章生成和聊天。", "website_url": "https://writesonic.com", "pricing_model": "freemium", "min_monthly_price": 16, "max_monthly_price": 16, "has_free_tier": True, "has_free_trial": True, "has_api": True, "features": ["Content Writing", "SEO", "Chat", "AI Article Writer"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 1900, "commission_type": "recurring", "affiliate_url": "https://writesonic.com", "affiliate_network": "direct"},
    {"id": ns_uuid("rytr"), "name": "Rytr", "slug": "rytr", "category": "content_writing", "description": "预算友好的 AI 写作工具，支持多语言和语气控制。", "website_url": "https://rytr.me", "pricing_model": "freemium", "min_monthly_price": 9, "max_monthly_price": 9, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Content Writing", "Tone Control", "Plagiarism Check", "30+ Languages"], "user_rating": 4.6, "rating_source": "TrustPilot", "rating_count": 1500, "commission_type": "recurring", "affiliate_url": "https://rytr.me", "affiliate_network": "direct"},
    # Midjourney alternatives
    {"id": ns_uuid("dalle-3"), "name": "DALL-E 3", "slug": "dalle-3", "category": "image_gen", "description": "OpenAI 的文本到图像模型，集成 ChatGPT。", "website_url": "https://openai.com/dall-e-3", "pricing_model": "usage_based", "has_free_tier": False, "has_free_trial": False, "has_api": True, "features": ["Text-to-Image", "Inpainting", "ChatGPT Integration", "High Resolution"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 3200, "commission_type": "none", "affiliate_url": "https://openai.com/dall-e-3", "affiliate_network": "direct"},
    {"id": ns_uuid("stable-diffusion"), "name": "Stable Diffusion", "slug": "stable-diffusion", "category": "image_gen", "description": "开源图像生成模型，支持本地部署和社区模型。", "website_url": "https://stability.ai", "pricing_model": "free", "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Open Source", "Local Hosting", "Fine-tuning", "Community Models", "Txt2Img"], "user_rating": 4.6, "rating_source": "ProductHunt", "rating_count": 8900, "commission_type": "none", "affiliate_url": "https://stability.ai", "affiliate_network": "direct"},
    {"id": ns_uuid("leonardo-ai"), "name": "Leonardo AI", "slug": "leonardo-ai", "category": "image_gen", "description": "面向游戏和设计的 AI 图像生成平台。", "website_url": "https://leonardo.ai", "pricing_model": "freemium", "min_monthly_price": 12, "max_monthly_price": 12, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Image Generation", "Fine-tuning", "Canvas Editor", "Community Feed"], "user_rating": 4.7, "rating_source": "G2", "rating_count": 4500, "commission_type": "recurring", "affiliate_url": "https://leonardo.ai", "affiliate_network": "direct"},
    {"id": ns_uuid("adobe-firefly"), "name": "Adobe Firefly", "slug": "adobe-firefly", "category": "image_gen", "description": "Adobe 的生成式 AI 工具，商业安全图像生成。", "website_url": "https://firefly.adobe.com", "pricing_model": "freemium", "min_monthly_price": 4.99, "max_monthly_price": 4.99, "has_free_tier": True, "has_free_trial": True, "has_api": True, "features": ["Generative Fill", "Text Effects", "Photoshop Integration", "Commercial Safe"], "user_rating": 4.3, "rating_source": "TrustPilot", "rating_count": 2100, "commission_type": "recurring", "affiliate_url": "https://firefly.adobe.com", "affiliate_network": "direct"},
    {"id": ns_uuid("ideogram"), "name": "Ideogram", "slug": "ideogram", "category": "image_gen", "description": "专注图像中文字渲染的 AI 图像生成器。", "website_url": "https://ideogram.ai", "pricing_model": "freemium", "min_monthly_price": 8, "max_monthly_price": 8, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Text Rendering", "Image Generation", "Remix", "Describe"], "user_rating": 4.4, "rating_source": "ProductHunt", "rating_count": 1800, "commission_type": "recurring", "affiliate_url": "https://ideogram.ai", "affiliate_network": "direct"},
    {"id": ns_uuid("recraft"), "name": "Recraft", "slug": "recraft", "category": "image_gen", "description": "支持矢量和光栅图形的 AI 设计工具。", "website_url": "https://recraft.ai", "pricing_model": "freemium", "min_monthly_price": 12, "max_monthly_price": 12, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Vector Graphics", "Brand Kit", "Style Control", "Templates"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 960, "commission_type": "recurring", "affiliate_url": "https://recraft.ai", "affiliate_network": "direct"},
    {"id": ns_uuid("playground-ai"), "name": "Playground AI", "slug": "playground-ai", "category": "image_gen", "description": "画布优先的 AI 图像生成和编辑平台。", "website_url": "https://playground.com", "pricing_model": "freemium", "min_monthly_price": 12, "max_monthly_price": 12, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Canvas Editor", "Image Generation", "Mixed Media", "Templates"], "user_rating": 4.2, "rating_source": "G2", "rating_count": 1500, "commission_type": "recurring", "affiliate_url": "https://playground.com", "affiliate_network": "direct"},
    {"id": ns_uuid("runway-ml"), "name": "Runway ML", "slug": "runway-ml", "category": "video_gen", "description": "AI 视频和图像生成套件，含运动画笔和绿幕。", "website_url": "https://runwayml.com", "pricing_model": "subscription", "min_monthly_price": 15, "max_monthly_price": 35, "has_free_tier": True, "has_free_trial": True, "has_api": True, "features": ["Video Generation", "Image Generation", "Motion Brush", "Green Screen"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 2800, "commission_type": "recurring", "affiliate_url": "https://runwayml.com", "affiliate_network": "direct"},
    # Writing alternatives
    {"id": ns_uuid("anyword"), "name": "Anyword", "slug": "anyword", "category": "content_writing", "description": "预测性评分驱动的 AI 写作平台。", "website_url": "https://anyword.com", "pricing_model": "subscription", "min_monthly_price": 49, "max_monthly_price": 49, "has_free_tier": False, "has_free_trial": True, "has_api": True, "features": ["Predictive Performance", "Content Writing", "Ad Copy", "Blog Posts"], "user_rating": 4.3, "rating_source": "Capterra", "rating_count": 860, "commission_type": "recurring", "affiliate_url": "https://anyword.com", "affiliate_network": "direct"},
    {"id": ns_uuid("wordtune"), "name": "Wordtune", "slug": "wordtune", "category": "content_writing", "description": "专注改写和语气调整的 AI 写作助手。", "website_url": "https://wordtune.com", "pricing_model": "freemium", "min_monthly_price": 13.99, "max_monthly_price": 13.99, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Rewrite", "Tone Adjust", "Summarize", "Browser Extension"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 1100, "commission_type": "recurring", "affiliate_url": "https://wordtune.com", "affiliate_network": "direct"},
    {"id": ns_uuid("grammarly"), "name": "Grammarly", "slug": "grammarly", "category": "content_writing", "description": "语法检查与 AI 写作辅助工具。", "website_url": "https://grammarly.com", "pricing_model": "freemium", "min_monthly_price": 12, "max_monthly_price": 12, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Grammar Check", "Tone Detection", "Plagiarism", "AI Writing"], "user_rating": 4.7, "rating_source": "G2", "rating_count": 15000, "commission_type": "recurring", "affiliate_url": "https://grammarly.com", "affiliate_network": "direct"},
    {"id": ns_uuid("surfer-seo"), "name": "Surfer SEO", "slug": "surfer-seo", "category": "content_writing", "description": "内容优化与 AI 写作结合的 SEO 平台。", "website_url": "https://surferseo.com", "pricing_model": "subscription", "min_monthly_price": 69, "max_monthly_price": 249, "has_free_tier": False, "has_free_trial": False, "has_api": True, "features": ["SEO Analysis", "AI Writer", "Content Planner", "SERP Analyzer"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 1300, "commission_type": "recurring", "affiliate_url": "https://surferseo.com", "affiliate_network": "direct"},
    {"id": ns_uuid("simplified"), "name": "Simplified", "slug": "simplified", "category": "content_writing", "description": "集设计、视频、社媒和写作为一体的 AI 平台。", "website_url": "https://simplified.com", "pricing_model": "freemium", "min_monthly_price": 18, "max_monthly_price": 18, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Content Writing", "Design", "Social Media", "Video Editing"], "user_rating": 4.4, "rating_source": "G2", "rating_count": 2300, "commission_type": "recurring", "affiliate_url": "https://simplified.com", "affiliate_network": "direct"},
    # Notion AI alternatives
    {"id": ns_uuid("coda-ai"), "name": "Coda AI", "slug": "coda-ai", "category": "productivity", "description": "文档、数据库和 AI 助手结合的工作区。", "website_url": "https://coda.io", "pricing_model": "freemium", "min_monthly_price": 12, "max_monthly_price": 12, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["AI Assistant", "Documents", "Databases", "Automations"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 1800, "commission_type": "recurring", "affiliate_url": "https://coda.io", "affiliate_network": "direct"},
    {"id": ns_uuid("clickup-ai"), "name": "ClickUp AI", "slug": "clickup-ai", "category": "productivity", "description": "项目管理工具内置 AI 写作和自动化。", "website_url": "https://clickup.com", "pricing_model": "freemium", "min_monthly_price": 5, "max_monthly_price": 5, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Project Management", "AI Writing", "Task Automation", "Docs"], "user_rating": 4.6, "rating_source": "G2", "rating_count": 5200, "commission_type": "recurring", "affiliate_url": "https://clickup.com", "affiliate_network": "direct"},
    {"id": ns_uuid("mem"), "name": "Mem", "slug": "mem", "category": "productivity", "description": "AI 优先的笔记应用，自动组织和搜索。", "website_url": "https://mem.ai", "pricing_model": "subscription", "min_monthly_price": 14.99, "max_monthly_price": 14.99, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["AI Notes", "Auto-Organization", "Search", "Collections"], "user_rating": 4.4, "rating_source": "ProductHunt", "rating_count": 1200, "commission_type": "recurring", "affiliate_url": "https://mem.ai", "affiliate_network": "direct"},
    {"id": ns_uuid("taskade"), "name": "Taskade", "slug": "taskade", "category": "productivity", "description": "可视化规划与 AI 协作工具。", "website_url": "https://taskade.com", "pricing_model": "freemium", "min_monthly_price": 8, "max_monthly_price": 8, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["AI Assistant", "Mind Maps", "Task Management", "Collaboration"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 960, "commission_type": "recurring", "affiliate_url": "https://taskade.com", "affiliate_network": "direct"},
    {"id": ns_uuid("craft"), "name": "Craft", "slug": "craft", "category": "productivity", "description": "美观的文档编辑器，内置 AI 助手。", "website_url": "https://craft.do", "pricing_model": "freemium", "min_monthly_price": 8, "max_monthly_price": 8, "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Documents", "AI Assistant", "Collaboration", "Beautiful UI"], "user_rating": 4.5, "rating_source": "G2", "rating_count": 750, "commission_type": "recurring", "affiliate_url": "https://craft.do", "affiliate_network": "direct"},
    {"id": ns_uuid("obsidian"), "name": "Obsidian", "slug": "obsidian", "category": "productivity", "description": "本地优先的知识管理工具，支持 AI 插件。", "website_url": "https://obsidian.md", "pricing_model": "free", "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Markdown", "Knowledge Graph", "Plugins", "Local-first"], "user_rating": 4.7, "rating_source": "G2", "rating_count": 3200, "commission_type": "none", "affiliate_url": "https://obsidian.md", "affiliate_network": "direct"},
    {"id": ns_uuid("reflect"), "name": "Reflect", "slug": "reflect", "category": "productivity", "description": "隐私优先的笔记应用，集成 GPT-4。", "website_url": "https://reflect.app", "pricing_model": "subscription", "min_monthly_price": 10, "max_monthly_price": 10, "has_free_tier": False, "has_free_trial": True, "has_api": True, "features": ["AI Notes", "Daily Notes", "Backlinks", "End-to-End Encryption"], "user_rating": 4.3, "rating_source": "ProductHunt", "rating_count": 680, "commission_type": "recurring", "affiliate_url": "https://reflect.app", "affiliate_network": "direct"},
    {"id": ns_uuid("anytype"), "name": "Anytype", "slug": "anytype", "category": "productivity", "description": "开源的本地优先 Notion 替代品。", "website_url": "https://anytype.io", "pricing_model": "freemium", "has_free_tier": True, "has_free_trial": False, "has_api": True, "features": ["Objects", "Graph View", "Offline-first", "Open Source"], "user_rating": 4.2, "rating_source": "ProductHunt", "rating_count": 1400, "commission_type": "none", "affiliate_url": "https://anytype.io", "affiliate_network": "direct"},
    {"id": ns_uuid("albus"), "name": "Albus", "slug": "albus", "category": "productivity", "description": "AI 驱动的研究和内容看板工具。", "website_url": "https://albus.org", "pricing_model": "freemium", "min_monthly_price": 15, "max_monthly_price": 15, "has_free_tier": True, "has_free_trial": True, "has_api": True, "features": ["AI Boards", "Research", "Content Creation", "Team Workspace"], "user_rating": 4.1, "rating_source": "ProductHunt", "rating_count": 420, "commission_type": "recurring", "affiliate_url": "https://albus.org", "affiliate_network": "direct"},
]

ALL_TOOLS = SOURCE_TOOLS + ALTERNATIVE_TOOLS

# Normalize keys for batch insert: all rows must share the same keys
TOOL_KEYS = [
    "id", "name", "slug", "category", "description", "website_url", "logo_url",
    "pricing_model", "min_monthly_price", "max_monthly_price", "has_free_tier",
    "has_free_trial", "has_api", "features", "user_rating", "rating_source",
    "rating_count", "commission_type", "commission_rate", "affiliate_url",
    "affiliate_network", "is_active", "metadata",
]


def normalize_tool(t: dict) -> dict:
    return {k: t.get(k) for k in TOOL_KEYS}


ALL_TOOLS = [normalize_tool(t) for t in ALL_TOOLS]


def http(method: str, path: str, payload=None, extra_headers=None):
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    headers = dict(HEADERS)
    if extra_headers:
        headers.update(extra_headers)
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode("utf-8")[:500]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")[:500]


def seed_table(table: str, rows: list):
    status, body = http("POST", table, rows)
    if status not in (200, 201):
        print(f"FAILED {table}: {status} {body}")
        return False
    print(f"OK {table}: inserted {len(rows)} rows")
    return True


def main():
    # Clean existing data
    for table, filter_q in [
        ("alternatives", "id=not.is.null"),
        ("deals", "is_active=eq.true"),
        ("tools", "is_active=eq.true"),
    ]:
        path = f"{table}?{filter_q}" if filter_q else table
        status, body = http("DELETE", path, extra_headers={"Prefer": "return=minimal"})
        if status not in (200, 204):
            print(f"WARN truncate {table}: {status} {body}")

    seed_table("tools", ALL_TOOLS)

    # Build slug -> id lookup
    slug_to_id = {t["slug"]: t["id"] for t in ALL_TOOLS}

    alternatives = [
        # ChatGPT
        {"source_tool_id": slug_to_id["chatgpt"], "alternative_tool_id": slug_to_id["claude"], "quality_score": 95, "similarity_reason": "Most direct alternative with comparable reasoning", "price_comparison_note": "Same $20/month Pro tier, both offer free tier", "feature_overlap": ["Text Generation", "Code Assist", "Long Context", "Vision"], "is_featured": True, "sort_order": 1},
        {"source_tool_id": slug_to_id["chatgpt"], "alternative_tool_id": slug_to_id["gemini"], "quality_score": 88, "similarity_reason": "Google ecosystem integration", "price_comparison_note": "$19.99/month, integrated with Gmail/Docs", "feature_overlap": ["Text Generation", "Multimodal", "Code Assist"], "is_featured": True, "sort_order": 2},
        {"source_tool_id": slug_to_id["chatgpt"], "alternative_tool_id": slug_to_id["perplexity"], "quality_score": 90, "similarity_reason": "Research-focused with verified sources", "price_comparison_note": "$20/month, adds real-time web citations", "feature_overlap": ["Text Generation", "Web Search", "Citations"], "is_featured": True, "sort_order": 3},
        {"source_tool_id": slug_to_id["chatgpt"], "alternative_tool_id": slug_to_id["deepseek"], "quality_score": 85, "similarity_reason": "Open source with strong reasoning capabilities", "price_comparison_note": "Significantly cheaper API pricing", "feature_overlap": ["Text Generation", "Code Assist", "Reasoning"], "is_featured": False, "sort_order": 4},
        {"source_tool_id": slug_to_id["chatgpt"], "alternative_tool_id": slug_to_id["writesonic"], "quality_score": 82, "similarity_reason": "Affordable content generation", "price_comparison_note": "$16/month, strong SEO features", "feature_overlap": ["Content Writing", "SEO", "Chat"], "is_featured": False, "sort_order": 5},
        {"source_tool_id": slug_to_id["chatgpt"], "alternative_tool_id": slug_to_id["rytr"], "quality_score": 80, "similarity_reason": "Budget-friendly with strong free tier", "price_comparison_note": "$9/month, cheapest content-focused option", "feature_overlap": ["Content Writing", "Tone Control", "Plagiarism Check"], "is_featured": False, "sort_order": 6},
        {"source_tool_id": slug_to_id["chatgpt"], "alternative_tool_id": slug_to_id["notion-ai"], "quality_score": 78, "similarity_reason": "Integrated AI in workspace", "price_comparison_note": "$10/month as add-on to Notion", "feature_overlap": ["Note Taking", "Text Generation", "Q&A"], "is_featured": False, "sort_order": 7},
        # Midjourney
        {"source_tool_id": slug_to_id["midjourney"], "alternative_tool_id": slug_to_id["dalle-3"], "quality_score": 92, "similarity_reason": "Most direct competitor with ChatGPT integration", "price_comparison_note": "Usage-based, pay per image", "feature_overlap": ["Text-to-Image", "High Resolution"], "is_featured": True, "sort_order": 1},
        {"source_tool_id": slug_to_id["midjourney"], "alternative_tool_id": slug_to_id["stable-diffusion"], "quality_score": 90, "similarity_reason": "Open source with full control over models", "price_comparison_note": "Free to run locally", "feature_overlap": ["Open Source", "Fine-tuning", "Txt2Img"], "is_featured": True, "sort_order": 2},
        {"source_tool_id": slug_to_id["midjourney"], "alternative_tool_id": slug_to_id["leonardo-ai"], "quality_score": 91, "similarity_reason": "Best UI/UX with free daily credits", "price_comparison_note": "$12/month, game/asset focused", "feature_overlap": ["Image Generation", "Canvas Editor", "Fine-tuning"], "is_featured": True, "sort_order": 3},
        {"source_tool_id": slug_to_id["midjourney"], "alternative_tool_id": slug_to_id["adobe-firefly"], "quality_score": 85, "similarity_reason": "Commercial-safe images with Adobe ecosystem", "price_comparison_note": "$4.99/month entry point", "feature_overlap": ["Generative Fill", "Commercial Safe"], "is_featured": False, "sort_order": 4},
        {"source_tool_id": slug_to_id["midjourney"], "alternative_tool_id": slug_to_id["ideogram"], "quality_score": 84, "similarity_reason": "Best text-in-image rendering", "price_comparison_note": "$8/month", "feature_overlap": ["Text Rendering", "Image Generation"], "is_featured": False, "sort_order": 5},
        {"source_tool_id": slug_to_id["midjourney"], "alternative_tool_id": slug_to_id["recraft"], "quality_score": 83, "similarity_reason": "Vector + raster in one tool", "price_comparison_note": "$12/month", "feature_overlap": ["Vector Graphics", "Brand Kit"], "is_featured": False, "sort_order": 6},
        {"source_tool_id": slug_to_id["midjourney"], "alternative_tool_id": slug_to_id["runway-ml"], "quality_score": 80, "similarity_reason": "Video + image generation in one suite", "price_comparison_note": "$15/month, adds motion/video", "feature_overlap": ["Image Generation", "Video Generation"], "is_featured": False, "sort_order": 7},
        # Jasper
        {"source_tool_id": slug_to_id["jasper"], "alternative_tool_id": slug_to_id["copy-ai"], "quality_score": 93, "similarity_reason": "Workflow automation for content teams", "price_comparison_note": "$36/month vs Jasper $49/month", "feature_overlap": ["Content Writing", "Workflows", "Brand Voice"], "is_featured": True, "sort_order": 1},
        {"source_tool_id": slug_to_id["jasper"], "alternative_tool_id": slug_to_id["writesonic"], "quality_score": 87, "similarity_reason": "Affordable with strong SEO features", "price_comparison_note": "$16/month, ~67% cheaper", "feature_overlap": ["Content Writing", "SEO", "AI Article Writer"], "is_featured": True, "sort_order": 2},
        {"source_tool_id": slug_to_id["jasper"], "alternative_tool_id": slug_to_id["rytr"], "quality_score": 86, "similarity_reason": "Budget-friendly with strong free tier", "price_comparison_note": "$9/month, lowest entry", "feature_overlap": ["Content Writing", "Tone Control", "Plagiarism Check"], "is_featured": True, "sort_order": 3},
        {"source_tool_id": slug_to_id["jasper"], "alternative_tool_id": slug_to_id["chatgpt"], "quality_score": 80, "similarity_reason": "General-purpose but great for content drafts", "price_comparison_note": "$20/month, more flexible", "feature_overlap": ["Text Generation", "Content Writing"], "is_featured": False, "sort_order": 4},
        {"source_tool_id": slug_to_id["jasper"], "alternative_tool_id": slug_to_id["claude"], "quality_score": 85, "similarity_reason": "Excellent for long-form content and analysis", "price_comparison_note": "$20/month, superior long context", "feature_overlap": ["Text Generation", "Content Writing", "Analysis"], "is_featured": False, "sort_order": 5},
        {"source_tool_id": slug_to_id["jasper"], "alternative_tool_id": slug_to_id["anyword"], "quality_score": 84, "similarity_reason": "Predictive scoring for content performance", "price_comparison_note": "$49/month, performance prediction", "feature_overlap": ["Predictive Performance", "Content Writing"], "is_featured": False, "sort_order": 6},
        {"source_tool_id": slug_to_id["jasper"], "alternative_tool_id": slug_to_id["wordtune"], "quality_score": 82, "similarity_reason": "Best rewrite and tone adjustment tool", "price_comparison_note": "$13.99/month", "feature_overlap": ["Rewrite", "Tone Adjust"], "is_featured": False, "sort_order": 7},
        {"source_tool_id": slug_to_id["jasper"], "alternative_tool_id": slug_to_id["grammarly"], "quality_score": 81, "similarity_reason": "Editing and writing assistance combined", "price_comparison_note": "$12/month, grammar + AI writing", "feature_overlap": ["Grammar Check", "AI Writing"], "is_featured": False, "sort_order": 8},
        {"source_tool_id": slug_to_id["jasper"], "alternative_tool_id": slug_to_id["surfer-seo"], "quality_score": 79, "similarity_reason": "Content + SEO in one platform", "price_comparison_note": "$69/month, premium SEO", "feature_overlap": ["SEO Analysis", "AI Writer"], "is_featured": False, "sort_order": 9},
        # Copy.ai
        {"source_tool_id": slug_to_id["copy-ai"], "alternative_tool_id": slug_to_id["jasper"], "quality_score": 90, "similarity_reason": "Marketing-focused with built-in campaigns", "price_comparison_note": "$49/month", "feature_overlap": ["Content Writing", "Brand Voice", "Campaigns"], "is_featured": True, "sort_order": 1},
        {"source_tool_id": slug_to_id["copy-ai"], "alternative_tool_id": slug_to_id["writesonic"], "quality_score": 86, "similarity_reason": "More affordable with free trial", "price_comparison_note": "$16/month", "feature_overlap": ["Content Writing", "SEO", "AI Article Writer"], "is_featured": True, "sort_order": 2},
        {"source_tool_id": slug_to_id["copy-ai"], "alternative_tool_id": slug_to_id["rytr"], "quality_score": 85, "similarity_reason": "Cheapest option with decent output", "price_comparison_note": "$9/month", "feature_overlap": ["Content Writing", "Tone Control"], "is_featured": True, "sort_order": 3},
        {"source_tool_id": slug_to_id["copy-ai"], "alternative_tool_id": slug_to_id["chatgpt"], "quality_score": 82, "similarity_reason": "Most flexible general-purpose alternative", "price_comparison_note": "$20/month", "feature_overlap": ["Text Generation", "Content Writing"], "is_featured": False, "sort_order": 4},
        {"source_tool_id": slug_to_id["copy-ai"], "alternative_tool_id": slug_to_id["claude"], "quality_score": 84, "similarity_reason": "Better for nuanced long-form content", "price_comparison_note": "$20/month", "feature_overlap": ["Text Generation", "Content Writing"], "is_featured": False, "sort_order": 5},
        {"source_tool_id": slug_to_id["copy-ai"], "alternative_tool_id": slug_to_id["wordtune"], "quality_score": 80, "similarity_reason": "Rewrite-focused complement to Copy.ai", "price_comparison_note": "$13.99/month", "feature_overlap": ["Rewrite", "Tone Adjust"], "is_featured": False, "sort_order": 6},
        {"source_tool_id": slug_to_id["copy-ai"], "alternative_tool_id": slug_to_id["simplified"], "quality_score": 78, "similarity_reason": "All-in-one content creation platform", "price_comparison_note": "$18/month", "feature_overlap": ["Content Writing", "Design", "Social Media"], "is_featured": False, "sort_order": 7},
        # Notion AI
        {"source_tool_id": slug_to_id["notion-ai"], "alternative_tool_id": slug_to_id["coda-ai"], "quality_score": 89, "similarity_reason": "Docs + databases + AI in one", "price_comparison_note": "$12/month", "feature_overlap": ["AI Assistant", "Documents", "Databases"], "is_featured": True, "sort_order": 1},
        {"source_tool_id": slug_to_id["notion-ai"], "alternative_tool_id": slug_to_id["clickup-ai"], "quality_score": 88, "similarity_reason": "Project management with built-in AI", "price_comparison_note": "$5/month add-on", "feature_overlap": ["Project Management", "AI Writing", "Docs"], "is_featured": True, "sort_order": 2},
        {"source_tool_id": slug_to_id["notion-ai"], "alternative_tool_id": slug_to_id["mem"], "quality_score": 86, "similarity_reason": "AI-first note-taking experience", "price_comparison_note": "$14.99/month", "feature_overlap": ["AI Notes", "Auto-Organization", "Search"], "is_featured": True, "sort_order": 3},
        {"source_tool_id": slug_to_id["notion-ai"], "alternative_tool_id": slug_to_id["taskade"], "quality_score": 84, "similarity_reason": "Visual planning with AI integration", "price_comparison_note": "$8/month", "feature_overlap": ["AI Assistant", "Mind Maps", "Task Management"], "is_featured": False, "sort_order": 4},
        {"source_tool_id": slug_to_id["notion-ai"], "alternative_tool_id": slug_to_id["craft"], "quality_score": 83, "similarity_reason": "Beautiful document editor with AI", "price_comparison_note": "$8/month", "feature_overlap": ["Documents", "AI Assistant", "Collaboration"], "is_featured": False, "sort_order": 5},
        {"source_tool_id": slug_to_id["notion-ai"], "alternative_tool_id": slug_to_id["obsidian"], "quality_score": 82, "similarity_reason": "Local-first knowledge management with AI plugins", "price_comparison_note": "Free core + paid plugins", "feature_overlap": ["Markdown", "Knowledge Graph", "Plugins"], "is_featured": False, "sort_order": 6},
        {"source_tool_id": slug_to_id["notion-ai"], "alternative_tool_id": slug_to_id["reflect"], "quality_score": 80, "similarity_reason": "Privacy-focused with GPT-4 integration", "price_comparison_note": "$10/month", "feature_overlap": ["AI Notes", "Daily Notes", "Backlinks"], "is_featured": False, "sort_order": 7},
        {"source_tool_id": slug_to_id["notion-ai"], "alternative_tool_id": slug_to_id["anytype"], "quality_score": 78, "similarity_reason": "Open source Notion alternative", "price_comparison_note": "Free core", "feature_overlap": ["Objects", "Graph View", "Offline-first"], "is_featured": False, "sort_order": 8},
        {"source_tool_id": slug_to_id["notion-ai"], "alternative_tool_id": slug_to_id["albus"], "quality_score": 77, "similarity_reason": "AI-powered research and content boards", "price_comparison_note": "$15/month", "feature_overlap": ["AI Boards", "Research", "Content Creation"], "is_featured": False, "sort_order": 9},
    ]

    seed_table("alternatives", alternatives)

    deals = [
        {"tool_id": slug_to_id["perplexity"], "title": "Perplexity Pro 首年 50% OFF", "description": "Perplexity Pro 年费订阅半价优惠", "original_price": 200, "deal_price": 100, "discount_percentage": 50, "deal_url": "https://perplexity.ai/pro", "coupon_code": "PRO50", "source": "official", "is_active": True},
        {"tool_id": slug_to_id["deepseek"], "title": "DeepSeek API 充值 30% 返现", "description": "API 充值限时返现活动", "original_price": 100, "deal_price": 70, "discount_percentage": 30, "deal_url": "https://deepseek.com", "coupon_code": "API30", "source": "official", "is_active": True},
        {"tool_id": slug_to_id["jasper"], "title": "Jasper 首月 25% OFF", "description": "新用户首月订阅优惠", "original_price": 49, "deal_price": 36.75, "discount_percentage": 25, "deal_url": "https://jasper.ai", "coupon_code": "JASPER25", "source": "official", "is_active": True},
        {"tool_id": slug_to_id["rytr"], "title": "Rytr 年付 40% OFF", "description": "年付方案限时优惠", "original_price": 108, "deal_price": 64.8, "discount_percentage": 40, "deal_url": "https://rytr.me", "coupon_code": "RYTR40", "source": "official", "is_active": True},
        {"tool_id": slug_to_id["leonardo-ai"], "title": "Leonardo AI 年付 25% OFF", "description": "年度订阅优惠", "original_price": 144, "deal_price": 108, "discount_percentage": 25, "deal_url": "https://leonardo.ai", "coupon_code": "LEO25", "source": "official", "is_active": True},
        {"tool_id": slug_to_id["recraft"], "title": "Recraft 首月 30% OFF", "description": "新用户订阅优惠", "original_price": 12, "deal_price": 8.4, "discount_percentage": 30, "deal_url": "https://recraft.ai", "coupon_code": "RC30", "source": "official", "is_active": True},
        {"tool_id": slug_to_id["wordtune"], "title": "Wordtune 年付 20% OFF", "description": "年度订阅优惠", "original_price": 119.88, "deal_price": 95.9, "discount_percentage": 20, "deal_url": "https://wordtune.com", "coupon_code": "WT20", "source": "official", "is_active": True},
        {"tool_id": slug_to_id["clickup-ai"], "title": "ClickUp AI 加购 20% OFF", "description": "ClickUp Unlimited + AI 加购优惠", "original_price": 5, "deal_price": 4, "discount_percentage": 20, "deal_url": "https://clickup.com", "coupon_code": "AI20", "source": "official", "is_active": True},
        {"tool_id": slug_to_id["taskade"], "title": "Taskade 年付 30% OFF", "description": "年度订阅限时优惠", "original_price": 96, "deal_price": 67.2, "discount_percentage": 30, "deal_url": "https://taskade.com", "coupon_code": "TASK30", "source": "official", "is_active": True},
        {"tool_id": slug_to_id["albus"], "title": "Albus 首年 50% OFF", "description": "早期用户优惠", "original_price": 180, "deal_price": 90, "discount_percentage": 50, "deal_url": "https://albus.org", "coupon_code": "ALBUS50", "source": "official", "is_active": True},
    ]

    seed_table("deals", deals)


if __name__ == "__main__":
    main()
