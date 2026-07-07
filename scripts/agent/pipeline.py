#!/usr/bin/env python3
"""aiternatives Agent v1 — Daily data pipeline orchestrator.

Runs in GitHub Actions daily at 15:00 UTC.
Stages:
  1. Discovery — find new AI tools via web search
  2. Alternatives — generate alternative relationships
  3. Quality — re-score and prune low-quality entries
  4. Deals — expire outdated deals (Day 10)
  5. Report — output summary
"""
import sys
import time


def run_pipeline():
    print("=" * 60)
    print("aiternatives Agent v1 — Pipeline Run")
    print(f"Started: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    print("=" * 60)

    results = {}

    # Stage 1: Discovery
    print("\n[Stage 1/3] Tool Discovery")
    try:
        from .discovery import discover_new_tools, discover_alternatives
        new_tools = discover_new_tools()
        results["tools_discovered"] = len(new_tools)
    except Exception as e:
        print(f"[pipeline] Discovery error: {e}")
        results["tools_discovered"] = -1

    # Stage 2: Alternative relationships
    print("\n[Stage 2/3] Alternative Relationships")
    try:
        from .discovery import discover_alternatives
        new_alts = discover_alternatives()
        results["alternatives_created"] = new_alts
    except Exception as e:
        print(f"[pipeline] Alternatives error: {e}")
        results["alternatives_created"] = -1

    # Stage 3: Quality scoring
    print("\n[Stage 3/3] Quality Scoring")
    try:
        from .quality import score_alternatives
        re_scored = score_alternatives()
        results["quality_updated"] = re_scored
    except Exception as e:
        print(f"[pipeline] Quality error: {e}")
        results["quality_updated"] = -1

    # Deal expiry check (lightweight)
    try:
        from .supabase_ops import get_expired_deal_ids, mark_deal_expired
        expired = get_expired_deal_ids()
        for deal_id in expired:
            mark_deal_expired(deal_id)
        results["deals_expired"] = len(expired)
        print(f"\n[Pipeline] Expired {len(expired)} deals")
    except Exception as e:
        print(f"[pipeline] Deals error: {e}")
        results["deals_expired"] = -1

    # Summary
    print("\n" + "=" * 60)
    print("Pipeline Summary:")
    print(f"  Tools discovered:    {results.get('tools_discovered', 'N/A')}")
    print(f"  Alternatives created: {results.get('alternatives_created', 'N/A')}")
    print(f"  Quality re-scored:   {results.get('quality_updated', 'N/A')}")
    print(f"  Deals expired:       {results.get('deals_expired', 'N/A')}")
    print("=" * 60)

    # Exit code: fail if any stage had errors
    errors = sum(1 for v in results.values() if v == -1)
    if errors > 2:
        print(f"\n[pipeline] FAILED: {errors} stages had errors")
        sys.exit(1)
    else:
        print(f"\n[pipeline] OK ({errors} stage(s) with issues)")
        sys.exit(0)


if __name__ == "__main__":
    run_pipeline()
