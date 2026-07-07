"""Quality scoring and data validation for alternatives."""
from .config import supabase_request, MIN_QUALITY_SCORE


def score_alternatives() -> int:
    """Re-score all alternative relationships based on data completeness and overlap.
    Returns count of relationships updated."""
    status, rows = supabase_request(
        "GET",
        "alternatives?select=id,source_tool_id,alternative_tool_id,feature_overlap,similarity_reason",
    )
    if status != 200:
        print(f"[quality] Failed to fetch alternatives: {status}")
        return 0

    updated = 0
    for row in (rows or []):
        new_score = _calculate_quality(row)
        if abs(new_score - row.get("quality_score", 0)) > 5:
            supabase_request(
                "PATCH",
                f"alternatives?id=eq.{row['id']}",
                payload={"quality_score": new_score},
            )
            updated += 1

    print(f"[quality] Re-scored {updated} alternatives")
    return updated


def _calculate_quality(row: dict) -> int:
    """Calculate quality score from 0-100 based on:
    - Feature overlap richness (40%)
    - Similarity reason presence (25%)
    - Data completeness (25%)
    - Rating data (10%)
    """
    score = 0

    # Feature overlap (max 40)
    overlap = row.get("feature_overlap") or []
    if isinstance(overlap, list):
        score += min(len(overlap) * 8, 40)

    # Similarity reason (max 25)
    reason = row.get("similarity_reason", "")
    if reason and len(reason) > 10:
        score += 20
    elif reason:
        score += 10
    else:
        score += 0

    # Other heuristics (max 35)
    # Price comparison note bonus
    if row.get("price_comparison_note"):
        score += 15
    else:
        score += 5

    # Sort order bonus (indicates curation)
    if row.get("sort_order", 0) > 0:
        score += 10

    return min(score, 95)  # cap at 95, reserve 100 for manual review


def prune_low_quality() -> int:
    """Deactivate alternatives below quality threshold."""
    status, rows = supabase_request(
        "GET",
        f"alternatives?quality_score=lt.{MIN_QUALITY_SCORE}&select=id,quality_score",
    )
    if status != 200:
        return 0

    count = len(rows or [])
    if count > 0 and input(f"[quality] {count} low-quality alternatives found. Prune? (y/N) ").strip().lower() == "y":
        for row in (rows or []):
            supabase_request("DELETE", f"alternatives?id=eq.{row['id']}")
        print(f"[quality] Pruned {count} low-quality alternatives")
        return count

    print(f"[quality] Skipped pruning {count} items (requires confirmation)")
    return 0
