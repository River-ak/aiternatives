-- =============================================================================
-- aiternatives 数据库完整建表脚本
-- 在 Supabase SQL Editor 中粘贴执行：
-- https://supabase.com/dashboard/project/wqzttprkmkpzqrqjdouw/sql/new
-- =============================================================================

-- 表 1: tools — AI 工具主表
CREATE TABLE tools (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    slug            TEXT NOT NULL UNIQUE,
    category        TEXT NOT NULL,
    description     TEXT,
    website_url     TEXT,
    logo_url        TEXT,
    pricing_model       TEXT,
    min_monthly_price   NUMERIC,
    max_monthly_price   NUMERIC,
    has_free_tier       BOOLEAN DEFAULT false,
    has_free_trial      BOOLEAN DEFAULT false,
    has_api             BOOLEAN DEFAULT false,
    features            JSONB DEFAULT '[]'::jsonb,
    user_rating         NUMERIC CHECK (user_rating >= 1 AND user_rating <= 5),
    rating_source       TEXT,
    rating_count        INTEGER DEFAULT 0,
    commission_type     TEXT CHECK (commission_type IN ('recurring', 'one_time', 'lifetime', 'none')),
    commission_rate     NUMERIC,
    affiliate_url       TEXT,
    affiliate_network   TEXT,
    is_active           BOOLEAN DEFAULT true,
    metadata            JSONB DEFAULT '{}'::jsonb,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- 表 2: deals — 折扣表
CREATE TABLE deals (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_id             UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
    title               TEXT NOT NULL,
    description         TEXT,
    original_price      NUMERIC,
    deal_price          NUMERIC,
    discount_percentage NUMERIC,
    deal_url            TEXT,
    coupon_code         TEXT,
    source              TEXT,
    starts_at           TIMESTAMPTZ,
    expires_at          TIMESTAMPTZ,
    is_active           BOOLEAN DEFAULT true,
    is_expired          BOOLEAN DEFAULT false,
    metadata            JSONB DEFAULT '{}'::jsonb,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- 表 3: alternatives — 替代方案关系表
CREATE TABLE alternatives (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_tool_id      UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
    alternative_tool_id UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
    quality_score       NUMERIC DEFAULT 0 CHECK (quality_score >= 0 AND quality_score <= 100),
    similarity_reason   TEXT,
    price_comparison_note TEXT,
    feature_overlap     JSONB DEFAULT '[]'::jsonb,
    is_featured         BOOLEAN DEFAULT false,
    sort_order          INTEGER DEFAULT 0,
    metadata            JSONB DEFAULT '{}'::jsonb,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source_tool_id, alternative_tool_id)
);

-- 索引
CREATE INDEX idx_tools_slug             ON tools(slug);
CREATE INDEX idx_tools_category         ON tools(category);
CREATE INDEX idx_tools_is_active        ON tools(is_active) WHERE is_active = true;
CREATE INDEX idx_tools_commission_type  ON tools(commission_type) WHERE commission_type IS NOT NULL;
CREATE INDEX idx_tools_category_active_rating ON tools(category, is_active, user_rating DESC) WHERE is_active = true;

CREATE INDEX idx_deals_tool_id          ON deals(tool_id);
CREATE INDEX idx_deals_active_expires   ON deals(is_active, expires_at) WHERE is_active = true;
CREATE INDEX idx_deals_is_expired       ON deals(is_expired, is_active);

CREATE INDEX idx_alt_source_tool        ON alternatives(source_tool_id, quality_score DESC) WHERE quality_score >= 60;
CREATE INDEX idx_alt_alternative_tool   ON alternatives(alternative_tool_id);

-- 自动触发器：updated_at 自动更新
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_tools_updated_at
    BEFORE UPDATE ON tools FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_deals_updated_at
    BEFORE UPDATE ON deals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_alternatives_updated_at
    BEFORE UPDATE ON alternatives FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- RLS 策略：公开只读 + Service Key 全权限（Agent 使用）
ALTER TABLE tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE alternatives ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read access" ON tools FOR SELECT USING (is_active = true);
CREATE POLICY "Public read access" ON deals FOR SELECT USING (is_active = true);
CREATE POLICY "Public read access" ON alternatives FOR SELECT USING (true);

-- 验证
SELECT '✅ 建表完成' AS status;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;
