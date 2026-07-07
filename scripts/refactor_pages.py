#!/usr/bin/env python3
"""Refactor remaining benchmark pages to use Supabase instead of mock data."""
import re
import os

BASE = "/Users/ak/Workbuddy/mkdir aiternatives/src/pages/alternatives"
PAGES = {
    "midjourney": "Midjourney",
    "jasper": "Jasper",
    "copy-ai": "Copy.ai",
    "notion-ai": "Notion AI",
}

for slug, display_name in PAGES.items():
    path = os.path.join(BASE, f"{slug}.astro")
    with open(path, "r") as f:
        content = f.read()

    # Step 1: Replace import lines
    content = content.replace(
        "import ComparisonTable from '../../components/alternatives/ComparisonTable.astro';",
        "import ComparisonTable from '../../components/alternatives/ComparisonTable.astro';"
    )
    # Remove the type import, add supabase import
    content = content.replace(
        "import type { AlternativeTool } from '../../components/alternatives/ComparisonTable.astro';",
        "import { getAlternativesForSource } from '../../lib/supabase';"
    )

    # Step 2: Find and replace the mock data section
    # Pattern: `const alternatives: AlternativeTool[] = [` ... `];`
    # We need to find everything between `const alternatives` and the closing `];` of the array

    # Find the start of the mock data
    start_pattern = f"const alternatives: AlternativeTool[] = ["
    start_idx = content.find(start_pattern)
    if start_idx == -1:
        print(f"WARN: Could not find mock data start in {slug}")
        continue

    # Find the matching `];` - find the last `];` before the next `---` or top-level export
    # A simpler approach: find the pattern `];\n\n---` which marks end of frontmatter + start of template
    end_marker = "];\n\n---\n\n<BaseLayout"
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        # Alternative: try just `];\n` followed by `---` 
        end_marker2 = "];\n---"
        end_idx = content.find(end_marker2, start_idx)

    if end_idx == -1:
        print(f"WARN: Could not find mock data end in {slug}")
        continue

    # Build the replacement
    new_frontmatter = f"""import {{ getAlternativesForSource }} from '../../lib/supabase';

// 从 Supabase 拉取数据（构建时静态生成）
const alternatives = await getAlternativesForSource('{slug}');
const sourceToolName = '{display_name}';

// 空状态测试用
const mockEmpty: typeof alternatives = [];
"""

    # Replace the section from start of const alternatives to end of mock data
    content = content[:start_idx] + new_frontmatter + content[end_idx + len("];"):]

    # Step 3: Update sourceToolName in ComparisonTable (if hardcoded)
    # It should already match, but let's use the variable
    content = content.replace(
        f'sourceToolName="{display_name}"',
        'sourceToolName={sourceToolName}'
    )

    # Write back
    with open(path, "w") as f:
        f.write(content)

    print(f"OK {slug}.astro (display: {display_name})")

print("\nDone!")
