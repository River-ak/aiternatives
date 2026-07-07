import { createClient } from '@supabase/supabase-js';
import type { AlternativeTool } from '../components/alternatives/ComparisonTable.astro';

const supabaseUrl = import.meta.env.SUPABASE_URL;
const supabaseServiceKey = import.meta.env.SUPABASE_SERVICE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
  throw new Error(
    'Missing Supabase credentials. Set SUPABASE_URL and SUPABASE_SERVICE_KEY in your environment.'
  );
}

export const supabase = createClient(supabaseUrl, supabaseServiceKey, {
  auth: {
    autoRefreshToken: false,
    persistSession: false,
  },
});

export interface SupabaseAlternativeRow {
  id: string;
  name: string;
  slug: string;
  logo_url: string | null;
  pricing_model: string;
  min_monthly_price: number | null;
  has_free_tier: boolean;
  has_free_trial: boolean;
  features: string[];
  user_rating: number | null;
  rating_source: string | null;
  rating_count: number;
  affiliate_url: string;
  discount_percentage?: number | null;
  similarity_reason?: string | null;
}

export async function getAlternativesForSource(
  sourceSlug: string
): Promise<AlternativeTool[]> {
  // 1. 获取源工具 ID
  const { data: sourceTool, error: sourceError } = await supabase
    .from('tools')
    .select('id')
    .eq('slug', sourceSlug)
    .eq('is_active', true)
    .single();

  if (sourceError || !sourceTool) {
    console.error(`Source tool not found: ${sourceSlug}`, sourceError);
    return [];
  }

  // 2. 获取替代方案（质量分 ≥ 60）
  const { data: rows, error } = await supabase
    .from('alternatives')
    .select(
      `
      quality_score,
      similarity_reason,
      price_comparison_note,
      feature_overlap,
      alternative_tool_id,
      alternative_tools:alternative_tool_id (
        name,
        slug,
        logo_url,
        pricing_model,
        min_monthly_price,
        has_free_tier,
        has_free_trial,
        features,
        user_rating,
        rating_source,
        rating_count,
        affiliate_url
      )
    `
    )
    .eq('source_tool_id', sourceTool.id)
    .gte('quality_score', 60)
    .order('sort_order', { ascending: true })
    .order('quality_score', { ascending: false });

  if (error) {
    console.error(`Failed to fetch alternatives for ${sourceSlug}:`, error);
    return [];
  }

  return (rows || [])
    .map((row: any): AlternativeTool | null => {
      const tool = row.alternative_tools as SupabaseAlternativeRow | null;
      if (!tool) return null;
      return {
        name: tool.name,
        slug: tool.slug,
        logoUrl: tool.logo_url,
        pricingModel: tool.pricing_model as AlternativeTool['pricingModel'],
        minMonthlyPrice: tool.min_monthly_price,
        hasFreeTier: tool.has_free_tier,
        hasFreeTrial: tool.has_free_trial,
        features: row.feature_overlap || tool.features || [],
        userRating: tool.user_rating,
        ratingSource: tool.rating_source,
        ratingCount: tool.rating_count,
        affiliateUrl: tool.affiliate_url,
        discountPercentage: row.discount_percentage ?? null,
        similarityReason: row.similarity_reason || '',
      };
    })
    .filter((item): item is AlternativeTool => item !== null);
}

