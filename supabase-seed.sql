-- =============================================================================
-- aiternatives 种子数据
-- 在 Supabase SQL Editor 中执行（建表脚本之后）
-- =============================================================================

-- 清空旧数据（谨慎：仅首次 seed 使用）
TRUNCATE TABLE alternatives, deals, tools RESTART IDENTITY CASCADE;

-- ---------- 源工具（替代方案页入口）----------
INSERT INTO tools (id, name, slug, category, description, website_url, pricing_model, min_monthly_price, max_monthly_price, has_free_tier, has_free_trial, has_api, features, user_rating, rating_source, rating_count, commission_type, affiliate_url, affiliate_network, is_active) VALUES
('b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', 'ChatGPT', 'chatgpt', 'text_gen', 'OpenAI 的旗舰对话 AI，支持文本生成、代码、图像理解和插件生态。', 'https://chat.openai.com', 'subscription', 20, 20, true, false, true, '["Text Generation","Code Assist","Vision","Plugins","GPT-4o"]', 4.7, 'G2', 12000, 'recurring', 'https://chat.openai.com', 'direct', true),
('888a8d69-6322-5958-8afd-facbc823d046', 'Midjourney', 'midjourney', 'image_gen', 'AI 图像生成标杆，以艺术风格和 Discord 社区驱动著称。', 'https://midjourney.com', 'subscription', 10, 120, false, false, true, '["Text-to-Image","Style Control","Upscale","Community Feed"]', 4.8, 'ProductHunt', 8900, 'recurring', 'https://midjourney.com', 'direct', true),
('eca4ddfa-4454-5764-b943-c6d22c14c97d', 'Jasper', 'jasper', 'content_writing', '面向营销团队的 AI 写作平台，支持品牌声音和 SEO 内容。', 'https://jasper.ai', 'subscription', 49, 125, false, true, true, '["Content Writing","Brand Voice","SEO","Campaigns"]', 4.0, 'Capterra', 1800, 'recurring', 'https://jasper.ai', 'PartnerStack', true),
('69d1c71e-ab93-5576-9980-b1cca287fe43', 'Copy.ai', 'copy-ai', 'content_writing', 'AI 写作工作流自动化平台，面向销售和营销团队。', 'https://copy.ai', 'freemium', 36, 36, true, false, true, '["Content Writing","Workflows","Brand Voice","Sales Copy"]', 4.5, 'G2', 2400, 'recurring', 'https://copy.ai', 'PartnerStack', true),
('344be73a-2655-5c59-997b-c3aa9f1261e5', 'Notion AI', 'notion-ai', 'productivity', '集成在 Notion 工作区中的 AI 助手，支持写作、总结和问答。', 'https://notion.so', 'subscription', 10, 10, false, false, true, '["Note Taking","Text Generation","Q&A","Database"]', 4.3, 'G2', 4200, 'recurring', 'https://notion.so', 'direct', true);

-- ---------- ChatGPT 替代品 ----------
INSERT INTO tools (id, name, slug, category, description, website_url, pricing_model, min_monthly_price, max_monthly_price, has_free_tier, has_free_trial, has_api, features, user_rating, rating_source, rating_count, commission_type, affiliate_url, affiliate_network, is_active) VALUES
('63c9fc2a-8903-5a06-b97c-ef5939653e7c', 'Claude', 'claude', 'text_gen', 'Anthropic 的对话 AI，以长上下文和安全对齐著称。', 'https://claude.ai', 'subscription', 20, 20, true, false, true, '["Text Generation","Code Assist","Long Context","Vision","Projects"]', 4.7, 'G2', 1250, 'recurring', 'https://claude.ai', 'direct', true),
('00c2440c-6322-5340-ab70-874e726f8413', 'Gemini', 'gemini', 'text_gen', 'Google 的多模态 AI，深度集成 Google 应用生态。', 'https://gemini.google.com', 'freemium', 19.99, 19.99, true, true, true, '["Multimodal","Text Generation","Code Assist","Google Integration"]', 4.3, 'TrustPilot', 890, 'recurring', 'https://gemini.google.com', 'direct', true),
('ad717a0c-573c-5600-a9ea-3d906cf31c39', 'Perplexity', 'perplexity', 'text_gen', '结合搜索和 LLM 的答案引擎，提供带引用来源的研究。', 'https://perplexity.ai', 'freemium', 20, 20, true, false, true, '["Web Search","Citations","Pro Search","File Upload","API Access"]', 4.5, 'G2', 2100, 'recurring', 'https://perplexity.ai', 'direct', true),
('bb648634-65dc-5198-b37f-bc9222e2db17', 'Mistral', 'mistral', 'text_gen', '欧洲开源大模型公司，提供开放权重模型和 API。', 'https://mistral.ai', 'usage_based', null, null, true, false, true, '["Open Source","Text Generation","Code Assist","Fine-tuning"]', 4.1, 'ProductHunt', 450, 'one_time', 'https://mistral.ai', 'direct', true),
('d48aad63-a05d-566b-a5b9-dec2d54e35c7', 'Cohere', 'cohere', 'text_gen', '专注企业级文本模型和嵌入 API 的 AI 平台。', 'https://cohere.com', 'freemium', null, null, true, true, true, '["Text Generation","Embeddings","RAG","Enterprise"]', 4.2, 'G2', 680, 'recurring', 'https://cohere.com', 'direct', true),
('86fa1f3e-f286-5432-ba61-f9329113d433', 'DeepSeek', 'deepseek', 'text_gen', '开源推理模型，以高性价比和代码能力著称。', 'https://deepseek.com', 'freemium', null, null, true, false, true, '["Text Generation","Code Assist","Reasoning","Open Source"]', 4.6, 'ProductHunt', 3200, 'one_time', 'https://deepseek.com', 'direct', true),
('8e10f0d9-3e0f-5591-9b4d-9d75f62a6651', 'GitHub Copilot', 'copilot', 'code_assist', 'GitHub 推出的 AI 编程助手，集成主流 IDE。', 'https://github.com/features/copilot', 'subscription', 30, 39, true, true, true, '["Code Assist","Text Generation","IDE Integration","Office Suite"]', 4.3, 'G2', 5600, 'recurring', 'https://github.com/features/copilot', 'direct', true),
('22457ed2-4602-5345-9673-b894d807d050', 'Writesonic', 'writesonic', 'content_writing', '面向 SEO 和内容的 AI 写作工具，支持文章生成和聊天。', 'https://writesonic.com', 'freemium', 16, 16, true, true, true, '["Content Writing","SEO","Chat","AI Article Writer"]', 4.4, 'G2', 1900, 'recurring', 'https://writesonic.com', 'direct', true),
('3f1a28dc-3350-5e36-8b76-356aba54ae4e', 'Rytr', 'rytr', 'content_writing', '预算友好的 AI 写作工具，支持多语言和语气控制。', 'https://rytr.me', 'freemium', 9, 9, true, false, true, '["Content Writing","Tone Control","Plagiarism Check","30+ Languages"]', 4.6, 'TrustPilot', 1500, 'recurring', 'https://rytr.me', 'direct', true);

-- ---------- Midjourney 替代品 ----------
INSERT INTO tools (id, name, slug, category, description, website_url, pricing_model, min_monthly_price, max_monthly_price, has_free_tier, has_free_trial, has_api, features, user_rating, rating_source, rating_count, commission_type, affiliate_url, affiliate_network, is_active) VALUES
('46c55358-b737-5ef6-93ad-5b77cfa99d56', 'DALL-E 3', 'dalle-3', 'image_gen', 'OpenAI 的文本到图像模型，集成 ChatGPT。', 'https://openai.com/dall-e-3', 'usage_based', null, null, false, false, true, '["Text-to-Image","Inpainting","ChatGPT Integration","High Resolution"]', 4.5, 'G2', 3200, 'usage_based', 'https://openai.com/dall-e-3', 'direct', true),
('803d5362-ddec-5af5-adc9-b8825d20a9a0', 'Stable Diffusion', 'stable-diffusion', 'image_gen', '开源图像生成模型，支持本地部署和社区模型。', 'https://stability.ai', 'free', null, null, true, false, true, '["Open Source","Local Hosting","Fine-tuning","Community Models","Txt2Img"]', 4.6, 'ProductHunt', 8900, 'none', 'https://stability.ai', 'direct', true),
('1894e972-1d2b-59de-b11d-03a726a296a1', 'Leonardo AI', 'leonardo-ai', 'image_gen', '面向游戏和设计的 AI 图像生成平台。', 'https://leonardo.ai', 'freemium', 12, 12, true, false, true, '["Image Generation","Fine-tuning","Canvas Editor","Community Feed"]', 4.7, 'G2', 4500, 'recurring', 'https://leonardo.ai', 'direct', true),
('9ddd8cd7-d407-5af9-905e-f10ef949329b', 'Adobe Firefly', 'adobe-firefly', 'image_gen', 'Adobe 的生成式 AI 工具，商业安全图像生成。', 'https://firefly.adobe.com', 'freemium', 4.99, 4.99, true, true, true, '["Generative Fill","Text Effects","Photoshop Integration","Commercial Safe"]', 4.3, 'TrustPilot', 2100, 'recurring', 'https://firefly.adobe.com', 'direct', true),
('f2e97890-563a-56c4-9335-c1bece0e853d', 'Ideogram', 'ideogram', 'image_gen', '专注图像中文字渲染的 AI 图像生成器。', 'https://ideogram.ai', 'freemium', 8, 8, true, false, true, '["Text Rendering","Image Generation","Remix","Describe"]', 4.4, 'ProductHunt', 1800, 'recurring', 'https://ideogram.ai', 'direct', true),
('6a2df910-5312-5418-8f2e-7942c9af7ec9', 'Recraft', 'recraft', 'image_gen', '支持矢量和光栅图形的 AI 设计工具。', 'https://recraft.ai', 'freemium', 12, 12, true, false, true, '["Vector Graphics","Brand Kit","Style Control","Templates"]', 4.5, 'G2', 960, 'recurring', 'https://recraft.ai', 'direct', true),
('14a0a3c9-7d76-5813-8875-053818af88d8', 'Playground AI', 'playground-ai', 'image_gen', '画布优先的 AI 图像生成和编辑平台。', 'https://playground.com', 'freemium', 12, 12, true, false, true, '["Canvas Editor","Image Generation","Mixed Media","Templates"]', 4.2, 'G2', 1500, 'recurring', 'https://playground.com', 'direct', true),
('6af96291-2ef3-5d69-bda2-6ffb96725193', 'Runway ML', 'runway-ml', 'video_gen', 'AI 视频和图像生成套件，含运动画笔和绿幕。', 'https://runwayml.com', 'subscription', 15, 35, true, true, true, '["Video Generation","Image Generation","Motion Brush","Green Screen"]', 4.4, 'G2', 2800, 'recurring', 'https://runwayml.com', 'direct', true);

-- ---------- Jasper / Copy.ai 通用写作替代品 ----------
INSERT INTO tools (id, name, slug, category, description, website_url, pricing_model, min_monthly_price, max_monthly_price, has_free_tier, has_free_trial, has_api, features, user_rating, rating_source, rating_count, commission_type, affiliate_url, affiliate_network, is_active) VALUES
('a56edc44-5555-5325-a56f-49a13637ab59', 'Anyword', 'anyword', 'content_writing', '预测性评分驱动的 AI 写作平台。', 'https://anyword.com', 'subscription', 49, 49, false, true, true, '["Predictive Performance","Content Writing","Ad Copy","Blog Posts"]', 4.3, 'Capterra', 860, 'recurring', 'https://anyword.com', 'direct', true),
('36e74e3a-1f6a-5a04-acea-1ab2d11cb68e', 'Wordtune', 'wordtune', 'content_writing', '专注改写和语气调整的 AI 写作助手。', 'https://wordtune.com', 'freemium', 13.99, 13.99, true, false, true, '["Rewrite","Tone Adjust","Summarize","Browser Extension"]', 4.5, 'G2', 1100, 'recurring', 'https://wordtune.com', 'direct', true),
('c3724e17-2a57-5baf-a352-b41a5d23e96a', 'Grammarly', 'grammarly', 'content_writing', '语法检查与 AI 写作辅助工具。', 'https://grammarly.com', 'freemium', 12, 12, true, false, true, '["Grammar Check","Tone Detection","Plagiarism","AI Writing"]', 4.7, 'G2', 15000, 'recurring', 'https://grammarly.com', 'direct', true),
('8b801155-994e-5c0f-9c4e-3256d71792b2', 'Surfer SEO', 'surfer-seo', 'content_writing', '内容优化与 AI 写作结合的 SEO 平台。', 'https://surferseo.com', 'subscription', 69, 249, false, false, true, '["SEO Analysis","AI Writer","Content Planner","SERP Analyzer"]', 4.4, 'G2', 1300, 'recurring', 'https://surferseo.com', 'direct', true),
('89d6d8a6-070e-581c-bafb-ab3a35eea1f9', 'Simplified', 'simplified', 'content_writing', '集设计、视频、社媒和写作为一体的 AI 平台。', 'https://simplified.com', 'freemium', 18, 18, true, false, true, '["Content Writing","Design","Social Media","Video Editing"]', 4.4, 'G2', 2300, 'recurring', 'https://simplified.com', 'direct', true);

-- ---------- Notion AI 替代品 ----------
INSERT INTO tools (id, name, slug, category, description, website_url, pricing_model, min_monthly_price, max_monthly_price, has_free_tier, has_free_trial, has_api, features, user_rating, rating_source, rating_count, commission_type, affiliate_url, affiliate_network, is_active) VALUES
('5c135833-7b3c-5a1e-afb4-35a04da23a65', 'Coda AI', 'coda-ai', 'productivity', '文档、数据库和 AI 助手结合的工作区。', 'https://coda.io', 'freemium', 12, 12, true, false, true, '["AI Assistant","Documents","Databases","Automations"]', 4.5, 'G2', 1800, 'recurring', 'https://coda.io', 'direct', true),
('5b9edf08-d030-50c1-9c30-d0f31a347e55', 'ClickUp AI', 'clickup-ai', 'productivity', '项目管理工具内置 AI 写作和自动化。', 'https://clickup.com', 'freemium', 5, 5, true, false, true, '["Project Management","AI Writing","Task Automation","Docs"]', 4.6, 'G2', 5200, 'recurring', 'https://clickup.com', 'direct', true),
('726ecff6-4c31-55e0-99ed-3d878a11e0c8', 'Mem', 'mem', 'productivity', 'AI 优先的笔记应用，自动组织和搜索。', 'https://mem.ai', 'subscription', 14.99, 14.99, true, false, true, '["AI Notes","Auto-Organization","Search","Collections"]', 4.4, 'ProductHunt', 1200, 'recurring', 'https://mem.ai', 'direct', true),
('ee9e4e37-53ce-52fd-a451-c11c7cddaf00', 'Taskade', 'taskade', 'productivity', '可视化规划与 AI 协作工具。', 'https://taskade.com', 'freemium', 8, 8, true, false, true, '["AI Assistant","Mind Maps","Task Management","Collaboration"]', 4.5, 'G2', 960, 'recurring', 'https://taskade.com', 'direct', true),
('540b678b-9693-56fd-b68a-a786482abd51', 'Craft', 'craft', 'productivity', '美观的文档编辑器，内置 AI 助手。', 'https://craft.do', 'freemium', 8, 8, true, false, true, '["Documents","AI Assistant","Collaboration","Beautiful UI"]', 4.5, 'G2', 750, 'recurring', 'https://craft.do', 'direct', true),
('a83b19b6-c221-5642-9c0e-04dfdef7d5b7', 'Obsidian', 'obsidian', 'productivity', '本地优先的知识管理工具，支持 AI 插件。', 'https://obsidian.md', 'free', null, null, true, false, true, '["Markdown","Knowledge Graph","Plugins","Local-first"]', 4.7, 'G2', 3200, 'none', 'https://obsidian.md', 'direct', true),
('caca2500-fe15-531b-bd9b-180a6f0e246d', 'Reflect', 'reflect', 'productivity', '隐私优先的笔记应用，集成 GPT-4。', 'https://reflect.app', 'subscription', 10, 10, false, true, true, '["AI Notes","Daily Notes","Backlinks","End-to-End Encryption"]', 4.3, 'ProductHunt', 680, 'recurring', 'https://reflect.app', 'direct', true),
('93555c05-d73b-5b81-939b-8a6da284a2b8', 'Anytype', 'anytype', 'productivity', '开源的本地优先 Notion 替代品。', 'https://anytype.io', 'freemium', null, null, true, false, true, '["Objects","Graph View","Offline-first","Open Source"]', 4.2, 'ProductHunt', 1400, 'none', 'https://anytype.io', 'direct', true),
('a695df6a-ea60-5c56-8fc4-0f30c772c15c', 'Albus', 'albus', 'productivity', 'AI 驱动的研究和内容看板工具。', 'https://albus.org', 'freemium', 15, 15, true, true, true, '["AI Boards","Research","Content Creation","Team Workspace"]', 4.1, 'ProductHunt', 420, 'recurring', 'https://albus.org', 'direct', true);

-- ---------- 替代关系（ChatGPT）----------
INSERT INTO alternatives (id, source_tool_id, alternative_tool_id, quality_score, similarity_reason, price_comparison_note, feature_overlap, is_featured, sort_order) VALUES
(gen_random_uuid(), 'b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', '63c9fc2a-8903-5a06-b97c-ef5939653e7c', 95, 'Most direct alternative with comparable reasoning', 'Same $20/month Pro tier, both offer free tier', '["Text Generation","Code Assist","Long Context","Vision"]', true, 1),
(gen_random_uuid(), 'b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', '00c2440c-6322-5340-ab70-874e726f8413', 88, 'Google ecosystem integration', '$19.99/month, integrated with Gmail/Docs', '["Text Generation","Multimodal","Code Assist"]', true, 2),
(gen_random_uuid(), 'b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', 'ad717a0c-573c-5600-a9ea-3d906cf31c39', 90, 'Research-focused with verified sources', '$20/month, adds real-time web citations', '["Text Generation","Web Search","Citations"]', true, 3),
(gen_random_uuid(), 'b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', '86fa1f3e-f286-5432-ba61-f9329113d433', 85, 'Open source with strong reasoning capabilities', 'Significantly cheaper API pricing', '["Text Generation","Code Assist","Reasoning"]', false, 4),
(gen_random_uuid(), 'b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', '22457ed2-4602-5345-9673-b894d807d050', 82, 'Affordable content generation', '$16/month, strong SEO features', '["Content Writing","SEO","Chat"]', false, 5),
(gen_random_uuid(), 'b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', '3f1a28dc-3350-5e36-8b76-356aba54ae4e', 80, 'Budget-friendly with strong free tier', '$9/month, cheapest content-focused option', '["Content Writing","Tone Control","Plagiarism Check"]', false, 6),
(gen_random_uuid(), 'b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', '344be73a-2655-5c59-997b-c3aa9f1261e5', 78, 'Integrated AI in workspace', '$10/month as add-on to Notion', '["Note Taking","Text Generation","Q&A"]', false, 7);

-- ---------- 替代关系（Midjourney）----------
INSERT INTO alternatives (id, source_tool_id, alternative_tool_id, quality_score, similarity_reason, price_comparison_note, feature_overlap, is_featured, sort_order) VALUES
(gen_random_uuid(), '888a8d69-6322-5958-8afd-facbc823d046', '46c55358-b737-5ef6-93ad-5b77cfa99d56', 92, 'Most direct competitor with ChatGPT integration', 'Usage-based, pay per image', '["Text-to-Image","High Resolution"]', true, 1),
(gen_random_uuid(), '888a8d69-6322-5958-8afd-facbc823d046', '803d5362-ddec-5af5-adc9-b8825d20a9a0', 90, 'Open source with full control over models', 'Free to run locally', '["Open Source","Fine-tuning","Txt2Img"]', true, 2),
(gen_random_uuid(), '888a8d69-6322-5958-8afd-facbc823d046', '1894e972-1d2b-59de-b11d-03a726a296a1', 91, 'Best UI/UX with free daily credits', '$12/month, game/asset focused', '["Image Generation","Canvas Editor","Fine-tuning"]', true, 3),
(gen_random_uuid(), '888a8d69-6322-5958-8afd-facbc823d046', '9ddd8cd7-d407-5af9-905e-f10ef949329b', 85, 'Commercial-safe images with Adobe ecosystem', '$4.99/month entry point', '["Generative Fill","Commercial Safe"]', false, 4),
(gen_random_uuid(), '888a8d69-6322-5958-8afd-facbc823d046', 'f2e97890-563a-56c4-9335-c1bece0e853d', 84, 'Best text-in-image rendering', '$8/month', '["Text Rendering","Image Generation"]', false, 5),
(gen_random_uuid(), '888a8d69-6322-5958-8afd-facbc823d046', '6a2df910-5312-5418-8f2e-7942c9af7ec9', 83, 'Vector + raster in one tool', '$12/month', '["Vector Graphics","Brand Kit"]', false, 6),
(gen_random_uuid(), '888a8d69-6322-5958-8afd-facbc823d046', '6af96291-2ef3-5d69-bda2-6ffb96725193', 80, 'Video + image generation in one suite', '$15/month, adds motion/video', '["Image Generation","Video Generation"]', false, 7);

-- ---------- 替代关系（Jasper）----------
INSERT INTO alternatives (id, source_tool_id, alternative_tool_id, quality_score, similarity_reason, price_comparison_note, feature_overlap, is_featured, sort_order) VALUES
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', '69d1c71e-ab93-5576-9980-b1cca287fe43', 93, 'Workflow automation for content teams', '$36/month vs Jasper $49/month', '["Content Writing","Workflows","Brand Voice"]', true, 1),
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', '22457ed2-4602-5345-9673-b894d807d050', 87, 'Affordable with strong SEO features', '$16/month, ~67% cheaper', '["Content Writing","SEO","AI Article Writer"]', true, 2),
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', '3f1a28dc-3350-5e36-8b76-356aba54ae4e', 86, 'Budget-friendly with strong free tier', '$9/month, lowest entry', '["Content Writing","Tone Control","Plagiarism Check"]', true, 3),
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', 'b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', 80, 'General-purpose but great for content drafts', '$20/month, more flexible', '["Text Generation","Content Writing"]', false, 4),
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', '63c9fc2a-8903-5a06-b97c-ef5939653e7c', 85, 'Excellent for long-form content and analysis', '$20/month, superior long context', '["Text Generation","Content Writing","Analysis"]', false, 5),
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', 'a56edc44-5555-5325-a56f-49a13637ab59', 84, 'Predictive scoring for content performance', '$49/month, performance prediction', '["Predictive Performance","Content Writing"]', false, 6),
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', '36e74e3a-1f6a-5a04-acea-1ab2d11cb68e', 82, 'Best rewrite and tone adjustment tool', '$13.99/month', '["Rewrite","Tone Adjust"]', false, 7),
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', 'c3724e17-2a57-5baf-a352-b41a5d23e96a', 81, 'Editing and writing assistance combined', '$12/month, grammar + AI writing', '["Grammar Check","AI Writing"]', false, 8),
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', '8b801155-994e-5c0f-9c4e-3256d71792b2', 79, 'Content + SEO in one platform', '$69/month, premium SEO', '["SEO Analysis","AI Writer"]', false, 9);

-- ---------- 替代关系（Copy.ai）----------
INSERT INTO alternatives (id, source_tool_id, alternative_tool_id, quality_score, similarity_reason, price_comparison_note, feature_overlap, is_featured, sort_order) VALUES
(gen_random_uuid(), '69d1c71e-ab93-5576-9980-b1cca287fe43', 'eca4ddfa-4454-5764-b943-c6d22c14c97d', 90, 'Marketing-focused with built-in campaigns', '$49/month', '["Content Writing","Brand Voice","Campaigns"]', true, 1),
(gen_random_uuid(), '69d1c71e-ab93-5576-9980-b1cca287fe43', '22457ed2-4602-5345-9673-b894d807d050', 86, 'More affordable with free trial', '$16/month', '["Content Writing","SEO","AI Article Writer"]', true, 2),
(gen_random_uuid(), '69d1c71e-ab93-5576-9980-b1cca287fe43', '3f1a28dc-3350-5e36-8b76-356aba54ae4e', 85, 'Cheapest option with decent output', '$9/month', '["Content Writing","Tone Control"]', true, 3),
(gen_random_uuid(), '69d1c71e-ab93-5576-9980-b1cca287fe43', 'b35bbb5a-4995-52ee-bb4f-ceb7a7b910f6', 82, 'Most flexible general-purpose alternative', '$20/month', '["Text Generation","Content Writing"]', false, 4),
(gen_random_uuid(), '69d1c71e-ab93-5576-9980-b1cca287fe43', '63c9fc2a-8903-5a06-b97c-ef5939653e7c', 84, 'Better for nuanced long-form content', '$20/month', '["Text Generation","Content Writing"]', false, 5),
(gen_random_uuid(), '69d1c71e-ab93-5576-9980-b1cca287fe43', '36e74e3a-1f6a-5a04-acea-1ab2d11cb68e', 80, 'Rewrite-focused complement to Copy.ai', '$13.99/month', '["Rewrite","Tone Adjust"]', false, 6),
(gen_random_uuid(), '69d1c71e-ab93-5576-9980-b1cca287fe43', '89d6d8a6-070e-581c-bafb-ab3a35eea1f9', 78, 'All-in-one content creation platform', '$18/month', '["Content Writing","Design","Social Media"]', false, 7);

-- ---------- 替代关系（Notion AI）----------
INSERT INTO alternatives (id, source_tool_id, alternative_tool_id, quality_score, similarity_reason, price_comparison_note, feature_overlap, is_featured, sort_order) VALUES
(gen_random_uuid(), '344be73a-2655-5c59-997b-c3aa9f1261e5', '5c135833-7b3c-5a1e-afb4-35a04da23a65', 89, 'Docs + databases + AI in one', '$12/month', '["AI Assistant","Documents","Databases"]', true, 1),
(gen_random_uuid(), '344be73a-2655-5c59-997b-c3aa9f1261e5', '5b9edf08-d030-50c1-9c30-d0f31a347e55', 88, 'Project management with built-in AI', '$5/month add-on', '["Project Management","AI Writing","Docs"]', true, 2),
(gen_random_uuid(), '344be73a-2655-5c59-997b-c3aa9f1261e5', '726ecff6-4c31-55e0-99ed-3d878a11e0c8', 86, 'AI-first note-taking experience', '$14.99/month', '["AI Notes","Auto-Organization","Search"]', true, 3),
(gen_random_uuid(), '344be73a-2655-5c59-997b-c3aa9f1261e5', 'ee9e4e37-53ce-52fd-a451-c11c7cddaf00', 84, 'Visual planning with AI integration', '$8/month', '["AI Assistant","Mind Maps","Task Management"]', false, 4),
(gen_random_uuid(), '344be73a-2655-5c59-997b-c3aa9f1261e5', '540b678b-9693-56fd-b68a-a786482abd51', 83, 'Beautiful document editor with AI', '$8/month', '["Documents","AI Assistant","Collaboration"]', false, 5),
(gen_random_uuid(), '344be73a-2655-5c59-997b-c3aa9f1261e5', 'a83b19b6-c221-5642-9c0e-04dfdef7d5b7', 82, 'Local-first knowledge management with AI plugins', 'Free core + paid plugins', '["Markdown","Knowledge Graph","Plugins"]', false, 6),
(gen_random_uuid(), '344be73a-2655-5c59-997b-c3aa9f1261e5', 'caca2500-fe15-531b-bd9b-180a6f0e246d', 80, 'Privacy-focused with GPT-4 integration', '$10/month', '["AI Notes","Daily Notes","Backlinks"]', false, 7),
(gen_random_uuid(), '344be73a-2655-5c59-997b-c3aa9f1261e5', '93555c05-d73b-5b81-939b-8a6da284a2b8', 78, 'Open source Notion alternative', 'Free core', '["Objects","Graph View","Offline-first"]', false, 8),
(gen_random_uuid(), '344be73a-2655-5c59-997b-c3aa9f1261e5', 'a695df6a-ea60-5c56-8fc4-0f30c772c15c', 77, 'AI-powered research and content boards', '$15/month', '["AI Boards","Research","Content Creation"]', false, 9);

-- ---------- 折扣数据 ----------
INSERT INTO deals (id, tool_id, title, description, original_price, deal_price, discount_percentage, deal_url, coupon_code, source, starts_at, expires_at, is_active) VALUES
(gen_random_uuid(), 'ad717a0c-573c-5600-a9ea-3d906cf31c39', 'Perplexity Pro 首年 50% OFF', 'Perplexity Pro 年费订阅半价优惠', 200, 100, 50, 'https://perplexity.ai/pro', 'PRO50', 'official', NOW(), NOW() + INTERVAL '30 days', true),
(gen_random_uuid(), '86fa1f3e-f286-5432-ba61-f9329113d433', 'DeepSeek API 充值 30% 返现', 'API 充值限时返现活动', 100, 70, 30, 'https://deepseek.com', 'API30', 'official', NOW(), NOW() + INTERVAL '14 days', true),
(gen_random_uuid(), 'eca4ddfa-4454-5764-b943-c6d22c14c97d', 'Jasper 首月 25% OFF', '新用户首月订阅优惠', 49, 36.75, 25, 'https://jasper.ai', 'JASPER25', 'official', NOW(), NOW() + INTERVAL '7 days', true),
(gen_random_uuid(), '3f1a28dc-3350-5e36-8b76-356aba54ae4e', 'Rytr 年付 40% OFF', '年付方案限时优惠', 108, 64.8, 40, 'https://rytr.me', 'RYTR40', 'official', NOW(), NOW() + INTERVAL '21 days', true),
(gen_random_uuid(), '1894e972-1d2b-59de-b11d-03a726a296a1', 'Leonardo AI 年付 25% OFF', '年度订阅优惠', 144, 108, 25, 'https://leonardo.ai', 'LEO25', 'official', NOW(), NOW() + INTERVAL '30 days', true),
(gen_random_uuid(), '6a2df910-5312-5418-8f2e-7942c9af7ec9', 'Recraft 首月 30% OFF', '新用户订阅优惠', 12, 8.4, 30, 'https://recraft.ai', 'RC30', 'official', NOW(), NOW() + INTERVAL '14 days', true),
(gen_random_uuid(), '36e74e3a-1f6a-5a04-acea-1ab2d11cb68e', 'Wordtune 年付 20% OFF', '年度订阅优惠', 119.88, 95.9, 20, 'https://wordtune.com', 'WT20', 'official', NOW(), NOW() + INTERVAL '30 days', true),
(gen_random_uuid(), '5b9edf08-d030-50c1-9c30-d0f31a347e55', 'ClickUp AI 加购 20% OFF', 'ClickUp Unlimited + AI 加购优惠', 5, 4, 20, 'https://clickup.com', 'AI20', 'official', NOW(), NOW() + INTERVAL '30 days', true),
(gen_random_uuid(), 'ee9e4e37-53ce-52fd-a451-c11c7cddaf00', 'Taskade 年付 30% OFF', '年度订阅限时优惠', 96, 67.2, 30, 'https://taskade.com', 'TASK30', 'official', NOW(), NOW() + INTERVAL '21 days', true),
(gen_random_uuid(), 'a695df6a-ea60-5c56-8fc4-0f30c772c15c', 'Albus 首年 50% OFF', '早期用户优惠', 180, 90, 50, 'https://albus.org', 'ALBUS50', 'official', NOW(), NOW() + INTERVAL '60 days', true);

-- 验证
SELECT '✅ Seed 完成' AS status;
SELECT (SELECT COUNT(*) FROM tools) AS tools_count,
       (SELECT COUNT(*) FROM alternatives) AS alternatives_count,
       (SELECT COUNT(*) FROM deals) AS deals_count;
