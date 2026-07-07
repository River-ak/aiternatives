#!/usr/bin/env python3
"""Standalone runner for the aiternatives Agent pipeline.

Usage:
    python3 scripts/run_agent.py
Requires env vars: SUPABASE_URL, SUPABASE_SERVICE_KEY
"""
import sys
import os

# Add scripts directory to path so relative imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from agent.pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()
