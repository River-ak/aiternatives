"""Supabase CRUD operations for the Agent pipeline."""
import json
from .config import supabase_request, tool_uuid

# ---- Tool Operations ----


def get_existing_slugs() -> set[str]:
    """Return set of all existing tool slugs in the database."""
    status, data = supabase_request("GET", "tools?select=slug")
    if status != 200:
        return set()
    return {row["slug"] for row in (data or [])}


def get_source_tools() -> list[dict]:
    """Get all active tools that serve as source for alternative pages."""
    status, data = supabase_request(
        "GET",
        "tools?select=id,name,slug,category&is_active=eq.true&order=user_rating.desc",
    )
    if status != 200:
        return []
    return data or []


def get_tool_by_slug(slug: str) -> dict | None:
    """Fetch a single tool by slug."""
    status, data = supabase_request(
        "GET", f"tools?slug=eq.{slug}&select=*&limit=1"
    )
    if status == 200 and data:
        return data[0]
    return None


def upsert_tool(tool: dict) -> bool:
    """Insert or update a tool. Returns True on success."""
    # Ensure required fields have defaults
    tool.setdefault("is_active", True)
    tool.setdefault("has_free_tier", False)
    tool.setdefault("has_free_trial", False)
    tool.setdefault("has_api", False)
    tool.setdefault("features", [])
    tool.setdefault("rating_count", 0)
    tool.setdefault("commission_type", "none")
    tool.setdefault("metadata", {})

    status, body = supabase_request(
        "POST",
        "tools",
        payload=[tool],
    )
    if status == 409:  # Conflict (slug exists) → update
        headers = {
            "apikey": supabase_request.__globals__.get("SUPABASE_SERVICE_KEY", ""),
        }
        status, body = supabase_request(
            "PATCH",
            f"tools?slug=eq.{tool['slug']}",
            payload=tool,
        )
    return status in (200, 201)


def create_tool_from_discovery(
    name: str,
    slug: str,
    category: str,
    description: str = "",
    website_url: str = "",
    pricing_model: str = "freemium",
    min_monthly_price: float | None = None,
    has_free_tier: bool = False,
    has_free_trial: bool = False,
    features: list[str] | None = None,
    user_rating: float | None = None,
    rating_source: str | None = None,
    rating_count: int = 0,
    affiliate_url: str = "",
    **kwargs,
) -> bool:
    """Create a new tool from discovery data."""
    return upsert_tool({
        "id": tool_uuid(slug),
        "name": name,
        "slug": slug,
        "category": category,
        "description": description,
        "website_url": website_url,
        "pricing_model": pricing_model,
        "min_monthly_price": min_monthly_price,
        "has_free_tier": has_free_tier,
        "has_free_trial": has_free_trial,
        "features": features or [],
        "user_rating": user_rating,
        "rating_source": rating_source,
        "rating_count": rating_count,
        "affiliate_url": affiliate_url,
        "commission_type": kwargs.get("commission_type", "none"),
    })


# ---- Alternative Relationship Operations ----


def get_existing_alternatives(source_tool_id: str) -> set[str]:
    """Get set of alternative_tool_id already linked to source_tool_id."""
    status, data = supabase_request(
        "GET",
        f"alternatives?source_tool_id=eq.{source_tool_id}&select=alternative_tool_id",
    )
    if status != 200:
        return set()
    return {row["alternative_tool_id"] for row in (data or [])}


def upsert_alternative(
    source_tool_id: str,
    alternative_tool_id: str,
    quality_score: int = 0,
    similarity_reason: str = "",
    price_comparison_note: str = "",
    feature_overlap: list[str] | None = None,
    sort_order: int = 0,
) -> bool:
    """Insert or update an alternative relationship."""
    row = {
        "source_tool_id": source_tool_id,
        "alternative_tool_id": alternative_tool_id,
        "quality_score": min(max(quality_score, 0), 100),
        "similarity_reason": similarity_reason,
        "price_comparison_note": price_comparison_note,
        "feature_overlap": feature_overlap or [],
        "sort_order": sort_order,
    }
    status, body = supabase_request("POST", "alternatives", payload=[row])
    if status == 409:
        status, body = supabase_request(
            "PATCH",
            f"alternatives?source_tool_id=eq.{source_tool_id}&alternative_tool_id=eq.{alternative_tool_id}",
            payload=row,
        )
    return status in (200, 201)


# ---- Deal Operations ----


def get_expired_deal_ids() -> list[str]:
    """Return IDs of deals past their expiration date."""
    status, data = supabase_request(
        "GET",
        "deals?is_expired=eq.false&is_active=eq.true&expires_at=lt.now()&select=id",
    )
    if status != 200:
        return []
    return [row["id"] for row in (data or [])]


def mark_deal_expired(deal_id: str) -> bool:
    """Mark a deal as expired."""
    status, _ = supabase_request(
        "PATCH",
        f"deals?id=eq.{deal_id}",
        payload={"is_expired": True, "is_active": False},
    )
    return status == 200


def upsert_deal(deal: dict) -> bool:
    """Insert or update a deal."""
    status, body = supabase_request("POST", "deals", payload=[deal])
    if status == 409:
        status, body = supabase_request(
            "PATCH",
            f"deals?id=eq.{deal['id']}",
            payload=deal,
        )
    return status in (200, 201)
