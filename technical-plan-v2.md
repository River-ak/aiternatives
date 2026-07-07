# 技术开发方案：AI工具替代方案引擎

> **文档版本**：V1.0
> **对应 PRD**：PRD V2（2026-07-06）
> **技术栈**：Astro 4.x + Tailwind CSS + Supabase PostgreSQL + Cloudflare Pages + Cloudflare R2 + Pagefind + Plausible CE
> **作者**：全栈开发工程师
> **日期**：2026-07-06

---

## 目录

1. [数据库表结构设计](#1-数据库表结构设计)
2. [构建性能与架构方案评估](#2-构建性能与架构方案评估)
3. [项目目录结构设计](#3-项目目录结构设计)
4. [Agent 数据通信与安全设计](#4-agent-数据通信与安全设计)

---

## 1. 数据库表结构设计

### 1.1 完整建表 SQL（PostgreSQL / Supabase）

```sql
-- =============================================================================
-- 表 1: tools — AI 工具主表
-- 存储所有 AI 工具的元数据，是替代方案引擎的核心实体
-- =============================================================================

CREATE TABLE tools (
    -- 主键
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 基础信息
    name            TEXT NOT NULL,
    slug            TEXT NOT NULL UNIQUE,                -- URL-safe 标识符，如 "chatgpt"
    category        TEXT NOT NULL,                       -- 品类：text_gen, image_gen, code_assist, video_gen 等
    description     TEXT,                                -- 200-300字简介
    website_url     TEXT,
    logo_url        TEXT,                                -- 存储在 Cloudflare R2 的 Logo URL

    -- 定价信息
    pricing_model       TEXT,                            -- 'freemium' | 'subscription' | 'one_time' | 'usage_based' | 'free'
    min_monthly_price   NUMERIC,                         -- 最低月价（美元）
    max_monthly_price   NUMERIC,                         -- 最高月价（美元），NULL 表示无上限
    has_free_tier       BOOLEAN DEFAULT false,
    has_free_trial      BOOLEAN DEFAULT false,

    -- 功能标签
    has_api             BOOLEAN DEFAULT false,
    features            JSONB DEFAULT '[]'::jsonb,       -- ["text_generation","team_collab","custom_models",...]

    -- 评分数据
    user_rating         NUMERIC CHECK (user_rating >= 1 AND user_rating <= 5),
    rating_source       TEXT,                            -- 'g2' | 'producthunt' | 'trustpilot' | 'capterra'
    rating_count        INTEGER DEFAULT 0,

    -- 联盟变现（V2 新增）
    commission_type     TEXT CHECK (commission_type IN ('recurring', 'one_time', 'lifetime', 'none')),
    -- 'recurring'  = 按月订阅佣金（LTV 高 3.5 倍，Agent 优先推荐）
    -- 'one_time'   = 一次性购买佣金
    -- 'lifetime'   = 终身许可佣金
    -- 'none'       = 无佣金（纯信息展示）
    commission_rate     NUMERIC,                         -- 佣金比例（百分比），如 20 表示 20%
    affiliate_url       TEXT,                            -- 联盟链接 URL
    affiliate_network   TEXT,                            -- 'PartnerStack' | 'Impact' | 'ShareASale' | 'direct'

    -- 状态控制
    is_active           BOOLEAN DEFAULT true,            -- 是否在站点展示
    metadata            JSONB DEFAULT '{}'::jsonb,       -- 扩展字段（品类特有属性等）

    -- 审计字段
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);


-- =============================================================================
-- 表 2: deals — 折扣表
-- 优惠/折扣信息，由 Agent 从 AppSumo/Reddit/Twitter 采集
-- =============================================================================

CREATE TABLE deals (
    -- 主键
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 关联
    tool_id             UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,

    -- 折扣信息
    title               TEXT NOT NULL,                   -- 如 "ChatGPT Plus 首月 50% OFF"
    description         TEXT,
    original_price      NUMERIC,                         -- 原价（美元）
    deal_price          NUMERIC,                         -- 折后价（美元）
    discount_percentage NUMERIC,                         -- 折扣率，如 50 表示 50%
    deal_url            TEXT,                            -- 折扣跳转链接
    coupon_code         TEXT,                            -- 优惠码，如 "AI50OFF"
    source              TEXT,                            -- 'appsumo' | 'reddit' | 'twitter' | 'official'

    -- 时效控制
    starts_at           TIMESTAMPTZ,
    expires_at          TIMESTAMPTZ,

    -- 状态
    is_active           BOOLEAN DEFAULT true,            -- 当前是否有效
    is_expired          BOOLEAN DEFAULT false,           -- Agent 过期检查标记

    -- 扩展
    metadata            JSONB DEFAULT '{}'::jsonb,

    -- 审计
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);


-- =============================================================================
-- 表 3: alternatives — 替代方案关系表
-- 核心业务表：记录 [源工具] → [替代工具] 的对比关系
-- =============================================================================

CREATE TABLE alternatives (
    -- 主键
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 外键关联
    source_tool_id      UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
    alternative_tool_id UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,

    -- 质量评分（V2 新增核心字段）
    quality_score       NUMERIC DEFAULT 0
                        CHECK (quality_score >= 0 AND quality_score <= 100),
    -- Agent 基于多维算法综合评分：
    --   功能相似度（40%权重）+ 数据完整性（25%权重）
    --   + 价格竞争力（20%权重）+ 用户口碑（15%权重）
    -- 评分 < 60 的替代品不列入对比展示

    -- 对比说明
    similarity_reason   TEXT,                            -- Agent 解释为什么它们是替代关系
    price_comparison_note TEXT,                          -- 价格对比说明
    feature_overlap     JSONB DEFAULT '[]'::jsonb,       -- ["text_gen","code_assist"] 重叠功能

    -- 展示控制
    is_featured         BOOLEAN DEFAULT false,           -- 是否精选展示
    sort_order          INTEGER DEFAULT 0,               -- 展示排序

    -- 扩展
    metadata            JSONB DEFAULT '{}'::jsonb,

    -- 审计
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),

    -- 一个替代关系唯一
    UNIQUE(source_tool_id, alternative_tool_id)
);


-- =============================================================================
-- 索引优化
-- =============================================================================

-- tools 表索引
CREATE INDEX idx_tools_slug             ON tools(slug);
CREATE INDEX idx_tools_category         ON tools(category);
CREATE INDEX idx_tools_is_active        ON tools(is_active) WHERE is_active = true;
CREATE INDEX idx_tools_commission_type  ON tools(commission_type) WHERE commission_type IS NOT NULL;
-- 品类 + 活跃 + 评分复合索引（替代方案首页按品类排序用）
CREATE INDEX idx_tools_category_active_rating ON tools(category, is_active, user_rating DESC)
    WHERE is_active = true;

-- deals 表索引
CREATE INDEX idx_deals_tool_id          ON deals(tool_id);
CREATE INDEX idx_deals_active_expires   ON deals(is_active, expires_at) WHERE is_active = true;
CREATE INDEX idx_deals_is_expired       ON deals(is_expired, is_active);

-- alternatives 表索引
CREATE INDEX idx_alt_source_tool        ON alternatives(source_tool_id, quality_score DESC)
    WHERE quality_score >= 60;                         -- 替代页查询的黄金索引
CREATE INDEX idx_alt_alternative_tool   ON alternatives(alternative_tool_id);


-- =============================================================================
-- 自动触发器：updated_at 字段自动更新
-- =============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_tools_updated_at
    BEFORE UPDATE ON tools
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_deals_updated_at
    BEFORE UPDATE ON deals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_alternatives_updated_at
    BEFORE UPDATE ON alternatives
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 1.2 实体关系说明

```
                    ┌──────────┐
                    │  tools   │
                    │ (主表)    │
                    └────┬─────┘
                         │
            ┌────────────┼────────────┐
            │            │            │
       ┌────▼─────┐ ┌───▼────────┐   │
       │  deals   │ │alternatives│   │
       │  (折扣)   │ │  (替代关系) │   │
       └──────────┘ └────────────┘   │
                         │            │
                    source_tool_id    │
                    alternative_tool_id ──┘
                    (都指向 tools.id)
```

### 1.3 设计决策说明

| 决策 | 选择 | 理由 |
|------|------|------|
| `features` 用 JSONB | ✅ | 每个品类的特征维度不同（图像工具有分辨率，代码工具有语言支持），JSONB 比 EAV 模式简单且查询性能足够 |
| `quality_score` 放 alternatives | ✅ | 同一工具作为不同源工具的替代品时，相似度不同。放在关系表而非 tools 表更合理 |
| `commission_type` 放 tools | ✅ | 佣金类型是工具的固有属性，不随替代关系变化 |
| 软删除（`is_active`） | ✅ | V1 不做用户系统，软删除足够；避免级联删除导致历史数据丢失 |
| UUID 主键 | ✅ | 分布式友好，Agent 可以预先生成 ID，支持未来多 Agent 并行写入 |

### 1.4 Supabase 免费层容量验证

```
预估数据量（第12月）：
  tools:        3,000 条 × ~2KB   = 6 MB
  deals:        1,500 条 × ~1KB   = 1.5 MB
  alternatives: 5,000 条 × ~0.5KB = 2.5 MB
  ───────────────────────────────────────
  总计：                           10 MB

Supabase 免费层上限：500 MB
实际使用：10 MB（仅 2%）
结论：✅ 充足，3 年内无需升级
```

---

## 2. 构建性能与架构方案评估

### 2.1 当前架构回顾

```
Agent 每日写入 Supabase
        │
        ▼
  GitHub Actions (每日 15:00 触发)
        │
        ▼
    astro build (SSG)
        │
        ▼
  Cloudflare Pages 部署
```

### 2.2 页面数量预估与构建时间分析

```
第3月（MVP）:
  替代方案页  30 个
  工具详情页  ~100 个
  品类列表页  ~10 个
  折扣列表页  ~2 个
  其他页      ~15 个（首页/搜索/404/sitemap等）
  ─────────────────────
  总计：      ~160 页

  预估构建时间：1-3 分钟 ✅

第6月:
  替代方案页  150 个
  工具详情页  ~400 个
  品类列表页  ~25 个
  折扣列表页  ~5 个
  其他页      ~20 个
  ─────────────────────
  总计：      ~600 页

  预估构建时间：
    - Astro 页面生成：600 × 25ms ≈  15s
    - 数据拉取（Supabase）：       5-10s
    - Tailwind CSS 编译：         30-45s
    - JS 打包 + 资源优化：         20-30s
    ────────────────────────────────────
    总耗时：                      2-3 分钟 ✅

第12月:
  替代方案页  500 个
  工具详情页  ~1,200 个
  品类列表页  ~50 个
  折扣列表页  ~20 个
  跳转页      500 个
  其他页      ~30 个
  ─────────────────────
  总计：      ~2,300 页

  预估构建时间：
    - Astro 页面生成：2300 × 25ms ≈  58s
    - 数据拉取（Supabase）：        15-20s
    - Tailwind CSS 编译：          40-60s
    - JS 打包 + 资源优化：          25-40s
    ────────────────────────────────────
    总耗时：                       4-6 分钟 ✅
```

### 2.3 Cloudflare Pages 免费层限制评估

| 限制项 | 免费层配额 | 实际用量 | 安全水位 |
|--------|:---------:|:-------:|:-------:|
| 月构建次数 | 500 | ~30（日更1次） | **仅 6%，充裕** |
| 单次构建超时 | 20 分钟 | 4-6 分钟 | **仅 25%，安全** |
| 带宽 | 无限 | — | ✅ 静态资源走 CDN |
| 并发构建 | 1 | 1 | ✅ 无需排队 |
| 自定义域名 | 100 | 1-2 | ✅ |

### 2.4 全量 SSG 可行性结论

> **结论：全量 SSG 在第 12 月的 2,300 页面规模下完全可行，无瓶颈。**

**支撑论据：**

1. **Astro 的构建速度极快**（Go 写的编译器 + 极简 runtime），同类项目实测：1,000 页约 2 分钟，5,000 页约 8-10 分钟
2. **CF Pages 免费层 500 次构建/月**，日均 1 次仅 30 次，不足配额的 10%
3. **构建是幂等的**（全量读取 → 全量生成），没有增量构建的复杂性
4. **Supabase 出站流量**在构建时峰值约 10-15MB（读取全量数据），远低于 5GB/月上限

### 2.5 是否需要 SSR / 混合模式？

| 场景 | 当前（全量 SSG） | 混合模式（SSG + SSR） | 建议 |
|------|:---:|:---:|:---:|
| 12月规模（2,300 页） | ✅ 4-6 分钟 | ⚠️ 过度设计 | **不需要** |
| 未来 5,000+ 页 | ⚠️ 接近 12-15 分钟 | ✅ 按需渲染更优 | 第 3 年评估 |
| 实时数据需求 | ❌ 不适合 | ✅ SSR 可用 | **当前无此需求** |
| 折扣页实时过期 | N/A（日更足够） | 可做到实时 | 折扣日更已满足 PRD |

**触发混合模式的条件（建议在达到以下阈值时切换）：**

```
条件 A：页面数 > 5,000（构建时间 > 15 分钟）
条件 B：需要实时数据展示（用户需要看到即时过期折扣）
条件 C：月构建次数即将触及 500 上限

当前状态：三项条件均不满足 → 保持全量 SSG
```

### 2.6 构建流水线可靠性设计

```
┌──────────────────────────────────────────┐
│           GitHub Actions 工作流           │
│                                           │
│  on:                                       │
│    schedule: "0 15 * * *"  # 每日 15:00   │
│    workflow_dispatch:       # 手动触发    │
│                                           │
│  steps:                                   │
│    1. Checkout 代码                        │
│    2. Setup Node.js (22.x)                │
│    3. npm ci                              │
│    4. astro build  ←── 从 Supabase 拉取   │
│    5. wrangler pages deploy ./dist        │
│                                           │
│  失败处理：                                 │
│    - 自动重试 2 次（间隔 5/15 分钟）        │
│    - 如果连续 3 次失败 → Telegram 告警     │
│    - 不影响已部署版本（CF Pages 保留历史）  │
│                                           │
│  月构建量：                                 │
│    30（定时）+ 2（手动修复触发）= 32 次     │
│    远低于 500 次上限                        │
└──────────────────────────────────────────┘
```

**可靠性保障机制：**

1. **幂等构建**：每次从 Supabase 全量读取 → 中间无状态 → 任意重试结果一致
2. **零依赖构建**：不依赖外部 API（数据已在 Supabase），构建环境纯净
3. **CF Pages 自动回滚**：部署失败时保留上一版本，用户不受影响
4. **Agent 失败不影响构建**：Agent 写入失败 → 数据库保持昨日数据 → 构建照常产出

---

## 3. 项目目录结构设计

### 3.1 完整目录树

```
aiternatives/
│
├── astro.config.mjs                  # Astro 配置（SSG 模式 + CF Pages 适配器）
├── tailwind.config.mjs               # Tailwind CSS 配置
├── tsconfig.json                     # TypeScript 配置
├── package.json
├── .env.example                      # 环境变量模板（无密钥）
│
├── src/
│   │
│   ├── pages/                        # ========== 路由层 ==========
│   │   │
│   │   ├── index.astro               # 🏠 首页：展示热门替代方案 + 品类导航 + 最新折扣
│   │   │
│   │   ├── alternatives/             # 🔗 A站路由 — 替代方案页（核心 SEO 资产）
│   │   │   ├── index.astro           #    /alternatives/ — 全部替代方案列表页（搜索+品类筛选）
│   │   │   └── [slug].astro          #    /alternatives/chatgpt/ — 单个替代方案详情页
│   │   │                             #    getStaticPaths() → 从 alternatives 表生成
│   │   │
│   │   ├── tools/                    # 🔧 工具详情页
│   │   │   └── [slug].astro          #    /tools/chatgpt/ — 工具详情 + 相关替代方案
│   │   │
│   │   ├── deals/                    # 💰 C 站路由 — 折扣模块（辅助功能）
│   │   │   └── index.astro           #    /deals/ — 当日有效折扣列表
│   │   │
│   │   ├── categories/               # 📂 品类浏览页
│   │   │   └── [category].astro      #    /categories/text-generation/ — 按品类浏览
│   │   │
│   │   ├── go/                       # 🔀 联盟跳转中间页
│   │   │   └── [slug].astro          #    /go/chatgpt/ — 纯静态生成，防 AdBlock
│   │   │                             #    构建时注入 affiliate_url，客户端自动跳转
│   │   │
│   │   ├── api/                      # 🌐 API 路由（仅 Hybrid/SSR 模式启用）
│   │   │   └── health.ts             #    /api/health — 健康检查（可选）
│   │   │                             #    注意：SSG 模式下 /api/ 路由不会运行
│   │   │                             #    Agent 直连 Supabase，不经过此层
│   │   │
│   │   ├── 404.astro                 # 自定义 404 页面
│   │   ├── robots.txt.ts             # 自动生成 robots.txt
│   │   └── sitemap.xml.ts            # 自动生成 sitemap.xml
│   │
│   ├── components/                   # ========== UI 组件层 ==========
│   │   │
│   │   ├── layout/
│   │   │   ├── BaseLayout.astro      # 全局布局：Header + 插槽 + Footer
│   │   │   ├── Header.astro          # 导航栏：Logo + 搜索 + 品类菜单
│   │   │   ├── Footer.astro          # 页脚：链接 + 免责声明
│   │   │   └── SEO.astro             # SEO 元数据组件（title/description/OG/canonical）
│   │   │
│   │   ├── alternatives/             # 替代方案相关组件
│   │   │   ├── ComparisonTable.astro # 核心：结构化对比表（5-15 行 × N 列）
│   │   │   ├── AlternativeRow.astro  # 对比表单行：工具名/价格/评分/功能/链接
│   │   │   ├── PriceCell.astro       # 价格列：显示定价模式 + 最低月价
│   │   │   ├── RatingBadge.astro     # 评分徽章
│   │   │   ├── QualityBadge.astro    # 质量分指示器
│   │   │   └── RelatedAlternatives.astro  # Related Alternatives 区块
│   │   │
│   │   ├── deals/                    # 折扣相关组件
│   │   │   ├── DealCard.astro        # 折扣卡片
│   │   │   └── DiscountBadge.astro   # "X% OFF" 徽章（嵌入对比表）
│   │   │
│   │   ├── tools/
│   │   │   └── ToolCard.astro        # 工具卡片（列表页用）
│   │   │
│   │   ├── ui/                       # 通用 UI 组件
│   │   │   ├── Button.astro
│   │   │   ├── SearchInput.astro     # 搜索输入框
│   │   │   ├── CategoryFilter.astro  # 品类筛选器
│   │   │   ├── EmptyState.astro      # 空状态占位
│   │   │   └── ThemeToggle.astro     # 明暗主题切换（Alpine.js 驱动）
│   │   │
│   │   └── seo/                      # SEO 组件
│   │       ├── JsonLd.astro          # 动态生成 JSON-LD（FAQ/Product/Breadcrumb）
│   │       └── Breadcrumb.astro      # 面包屑导航
│   │
│   ├── lib/                          # ========== 工具库层 ==========
│   │   ├── supabase.ts               # Supabase 服务端客户端（构建时读取数据）
│   │   ├── constants.ts              # 全局常量（品类列表、评分来源等）
│   │   ├── types.ts                  # TypeScript 类型定义（与数据库 schema 对齐）
│   │   ├── seo.ts                    # SEO 辅助函数（title/meta 生成）
│   │   ├── affiliate.ts              # 联盟链接处理（构建时注入参数）
│   │   └── format.ts                 # 格式化工具（价格、日期）
│   │
│   ├── data/                         # ========== 静态数据层 ==========
│   │   ├── categories.ts             # 品类定义（名称、slug、图标、对比维度）
│   │   └── site-config.ts            # 站点全局配置（名称、URL、默认 meta）
│   │
│   ├── styles/                       # ========== 样式层 ==========
│   │   └── global.css                # Tailwind 指令 + 自定义 CSS 变量 + 主题
│   │
│   └── content/                      # Astro Content Collections（可选）
│       └── blog/                     # 未来博客内容（V2+）
│
├── public/                           # ========== 静态资源（原样复制） ==========
│   ├── favicon.ico
│   ├── robots.txt
│   ├── images/                       # 站点用图（Logo 等，工具 Logo 在 R2）
│   └── pagefind/                     # Pagefind 构建后自动生成的搜索索引
│
├── supabase/                         # ========== 数据库相关 ==========
│   ├── migrations/
│   │   └── 001_initial_schema.sql    # 初始建表迁移文件
│   └── seed.sql                      # 开发/测试种子数据
│
├── scripts/                          # ========== 运维脚本 ==========
│   ├── verify-build.sh               # 构建后质量检查（死链/Lighthouse）
│   └── backfill-tools.ts             # 手动导入工具数据脚本（冷启动用）
│
└── .github/
    └── workflows/
        └── daily-build.yml           # GitHub Actions：每日 15:00 触发构建
```

### 3.2 路由职责划分

| 路由类型 | 目录 | 渲染模式 | 数据来源 | 说明 |
|---------|------|:------:|---------|------|
| **A站路由** | `src/pages/alternatives/` | SSG | `alternatives` + `tools` 表 | 替代方案页，核心 SEO 资产 |
| **C站路由** | `src/pages/deals/` | SSG | `deals` + `tools` 表 | 折扣列表页，辅助功能 |
| **工具页** | `src/pages/tools/` | SSG | `tools` 表 | 工具详情页 |
| **跳转页** | `src/pages/go/` | SSG | `tools.affiliate_url` | 防 AdBlock + 点击追踪 |
| **品类页** | `src/pages/categories/` | SSG | `tools` 表分组 | 按品类浏览 |
| **API 路由** | `src/pages/api/` | 无效（SSG） | — | SSG 模式下此目录无用，保留为未来 Hybrid 做准备 |

### 3.3 纯客户端逻辑划分

以下逻辑通过 **Vanilla JS / Alpine.js** 在客户端运行，不依赖服务端：

| 功能 | 实现方式 | 所在组件 |
|------|---------|---------|
| 对比表排序 | Alpine.js `x-data` + `x-sort` | `ComparisonTable.astro` |
| 品类筛选 | Alpine.js 响应式 `x-show` | `CategoryFilter.astro` |
| 搜索建议 | Pagefind（静态搜索库） | `SearchInput.astro` |
| 主题切换 | Alpine.js + `localStorage` | `ThemeToggle.astro` |
| 折扣倒计时 | 纯 JS `setInterval` | `DealCard.astro` |
| 跳转页倒计时 | 纯 JS `setTimeout` → `location.href` | `go/[slug].astro` |

---

## 4. Agent 数据通信与安全设计

### 4.1 架构总览

```
┌─────────────────────────────────────────────────────┐
│                    安全边界                           │
│                                                      │
│  ┌──────────┐        Service Role Key                │
│  │  Agent   │───(仅服务端持有)──▶┌──────────────┐    │
│  │(WorkBuddy)│                    │   Supabase   │    │
│  └──────────┘                    │  PostgreSQL  │    │
│                                   │              │    │
│  ┌──────────┐     Anon Key       │  ┌────────┐  │    │
│  │  Astro   │───(只读，公开)──▶  │  │ tools   │  │    │
│  │  Build   │                    │  │ deals   │  │    │
│  └──────────┘                    │  │ alt..   │  │    │
│                                   │  └────────┘  │    │
│  ┌──────────┐                    │              │    │
│  │  Browser │───(不直接访问DB)───▶│  同上（0暴露）│    │
│  └──────────┘                    └──────────────┘    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 4.2 数据写入方案（推荐方案）

**核心原则：Agent 不通过 HTTP API 端点写入数据，而是使用 Supabase Client SDK 直连数据库。**

这避免了：
- 自己维护 API 端点的安全风险
- CF Worker 的额外费用（100 万请求/天免费，但不需要）
- 额外的中间层故障点

#### 实现细节

```typescript
// Agent 端 (WorkBuddy 定时任务中运行)
// 文件：agent/supabase-writer.ts

import { createClient } from '@supabase/supabase-js'

// ⚠️ Service Role Key — 仅在 Agent 端使用，绝不暴露给前端
const supabase = createClient(
  process.env.SUPABASE_URL!,           // 如 https://xxxxx.supabase.co
  process.env.SUPABASE_SERVICE_ROLE_KEY! // 绕过 RLS，拥有完整读写权限
)

// 写入新工具
async function upsertTool(tool: ToolInput) {
  const { data, error } = await supabase
    .from('tools')
    .upsert({
      slug: tool.slug,
      name: tool.name,
      category: tool.category,
      description: tool.description,
      commission_type: tool.commission_type,   // 'recurring' | 'one_time' | ...
      // ... 其他字段
    }, {
      onConflict: 'slug',  // slug 冲突时更新
    })

  if (error) throw new AgentError('Failed to write tool', error)
  return data
}

// 写入替代方案关系
async function insertAlternative(rel: AlternativeInput) {
  // quality_score 由 Agent 的评分算法计算
  const qualityScore = calculateQualityScore(rel)

  if (qualityScore < 60) {
    // 质量不达标，不写入（避免低质量数据污染数据库）
    console.log(`Skipped: ${rel.alternative_name} score ${qualityScore} < 60`)
    return null
  }

  const { data, error } = await supabase
    .from('alternatives')
    .upsert({
      source_tool_id: rel.source_tool_id,
      alternative_tool_id: rel.alternative_tool_id,
      quality_score: qualityScore,
      similarity_reason: rel.reason,
      price_comparison_note: rel.price_note,
      feature_overlap: rel.shared_features,
    }, {
      onConflict: 'source_tool_id,alternative_tool_id',
    })

  if (error) throw new AgentError('Failed to write alternative', error)
  return data
}

// 写入折扣
async function insertDeal(deal: DealInput) {
  const { data, error } = await supabase
    .from('deals')
    .insert({
      tool_id: deal.tool_id,
      title: deal.title,
      original_price: deal.original_price,
      deal_price: deal.deal_price,
      discount_percentage: deal.discount_pct,
      deal_url: deal.url,
      coupon_code: deal.coupon,
      source: deal.source,          // 'appsumo' | 'reddit' | 'twitter'
      starts_at: deal.starts_at,
      expires_at: deal.expires_at,
    })

  if (error) throw new AgentError('Failed to write deal', error)
  return data
}
```

### 4.3 安全层级设计

```
Layer 1: Service Role Key（服务端唯一持有）
  ├── 存储在 GitHub Secrets / WorkBuddy 环境变量
  ├── 绕过 RLS，拥有全部权限
  ├── 如果泄露 → 攻击者获得完整 DB 写入权限 ⚠️
  └── 缓解：定期轮换密钥（Supabase 支持），监控写入量异常

Layer 2: Supabase RLS（前端 Anon Key 的安全网）
  ├── ALTER TABLE tools ENABLE ROW LEVEL SECURITY;
  ├── 策略：Anon Key 只能 SELECT（只读）
  └── 即使 Anon Key 泄露，也无法修改数据

Layer 3: Supabase Dashboard 审计日志
  ├── 免费计划包含 Dashboard 操作日志
  └── 可监控异常写入模式
```

#### RLS 策略 SQL

```sql
-- =============================================================================
-- RLS 策略：前端的 Anon Key 仅允许读取操作
-- =============================================================================

ALTER TABLE tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE alternatives ENABLE ROW LEVEL SECURITY;

-- tools 表：anon 角色只读
CREATE POLICY "tools_anon_select" ON tools
    FOR SELECT
    TO anon
    USING (is_active = true);

-- deals 表：anon 角色只读（且仅显示有效折扣）
CREATE POLICY "deals_anon_select" ON deals
    FOR SELECT
    TO anon
    USING (is_active = true AND is_expired = false);

-- alternatives 表：anon 角色只读（且仅显示达标替代品）
CREATE POLICY "alternatives_anon_select" ON alternatives
    FOR SELECT
    TO anon
    USING (quality_score >= 60);

-- 写入、更新、删除：仅 service_role 允许（默认行为，无需额外策略）
```

### 4.4 Anon Key 使用方式（构建时）

```typescript
// src/lib/supabase.ts — Astro 构建时使用

import { createClient } from '@supabase/supabase-js'

// ✅ 使用 Anon Key（公开，仅只读权限）
export const supabase = createClient(
  import.meta.env.SUPABASE_URL,       // Astro 环境变量
  import.meta.env.SUPABASE_ANON_KEY   // 公开的 Anon Key（RLS 限制为只读）
)

// 典型用法（在 getStaticPaths 中）：
// const { data: tools } = await supabase
//   .from('tools')
//   .select('*')
//   .eq('is_active', true)

// const { data: alternatives } = await supabase
//   .from('alternatives')
//   .select('*, alternative_tool:alternative_tool_id(*)')
//   .eq('source_tool_id', slugToId(slug))
//   .gte('quality_score', 60)
//   .order('quality_score', { ascending: false })
```

### 4.5 方案对比：为何不用自建 API 端点

| 方案 | 安全性 | 复杂度 | 成本 | 可靠性 |
|------|:-----:|:-----:|:---:|:-----:|
| **A: Agent → Supabase SDK（推荐）** | ⭐⭐⭐⭐ | 低 | $0 | 高（Supabase SLA） |
| B: Agent → CF Worker → Supabase | ⭐⭐⭐⭐⭐ | 中 | ~$0（用量低） | 中（多一跳） |
| C: Agent → Astro API Route → Supabase | ⭐⭐⭐ | 中 | $0 | 低（SSG 无 API） |

**方案 B（CF Worker 网关）的额外价值：**

如果未来需要更细粒度的控制，可以在中间加一层 CF Worker：
- 请求日志记录（审计追踪）
- 速率限制（防止 Agent bug 导致的写入风暴）
- 数据格式校验（在 Worker 层再做一次校验）
- API Key 轮换（不修改 Agent 代码即可切换 Supabase Key）

但 V1 阶段不需要这个复杂度。方案 A 完全满足需求。

### 4.6 密钥管理清单

```
需要管理的密钥：

1. SUPABASE_SERVICE_ROLE_KEY
   存储位置：GitHub Secrets（Agent 使用）
   权限：完整读写
   轮换：每季度（Supabase Dashboard → Project Settings → API）

2. SUPABASE_ANON_KEY
   存储位置：CF Pages 环境变量（构建时使用）
   权限：仅只读（RLS 限制）
   风险：可公开（设计上就可公开）

3. PLAUSIBLE_API_KEY（可选）
   存储位置：CF Pages 环境变量
   权限：仅写入分析数据

密钥轮换流程：
  1. Supabase Dashboard 生成新 Service Role Key
  2. 更新 GitHub Secrets
  3. 更新 Agent 环境变量
  4. 撤销旧 Key
  5. 验证 Agent 下次运行正常
```

---

## 附录 A：数据流时序图

```
时间轴（每日）:

08:00  Agent AG-1 启动 ────────▶ Supabase INSERT/UPDATE tools, alternatives
09:00  Agent AG-3 启动 ────────▶ Supabase INSERT deals
10:00  Agent AG-2 启动 ────────▶ Supabase UPDATE tools (价格/评分抽查)
11:00  Agent AG-4 启动 ────────▶ Supabase UPDATE deals (标记过期)
14:00  Agent AG-6 启动 ────────▶ (死链检查，不写数据库)
                     ⬇
        所有数据操作在 15:00 前完成
                     ⬇
15:00  GitHub Actions 触发 ─────▶ astro build (全量读取 Supabase)
                     ⬇
15:05  构建完成 ────────────────▶ Cloudflare Pages 自动部署
                     ⬇
15:06  新版本上线（用户可见）
```

## 附录 B：技术选型决策记录

| 决策 | 选择 | 备选 | 理由 |
|------|------|------|------|
| 渲染模式 | SSG（全量静态） | SSR/Hybrid | 2,300 页 6 分钟内完成，无需服务端运行时 |
| 数据库 | Supabase PostgreSQL | SQLite/PlanetScale | 免费层充足 + 内置 REST API + RLS + 实时订阅 |
| 文件存储 | Cloudflare R2 | Supabase Storage | R2 无出站费用，工具 Logo 直接用 CF CDN |
| 样式方案 | Tailwind CSS | CSS Modules | 构建时 PurgeCSS，零运行时开销 |
| 搜索 | Pagefind | Algolia | 静态搜索，零成本，安装即用 |
| 分析 | Plausible CE + CF Analytics | Google Analytics | 隐私友好 + 双轨数据校验 |
| 部署 | Cloudflare Pages | Vercel | 无限带宽 + 全球 CDN + Workers 生态 |
| CI/CD | GitHub Actions | CF Pages CI | 定时触发 + 手动触发，灵活可控 |

---

> **下一步行动**：基于本技术方案，可以开始 Week 1 Day 1-2 的实施 —— Astro 项目初始化 + Supabase 建表 + 基础布局。
