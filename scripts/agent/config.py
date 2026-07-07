"""Agent configuration and environment variables."""
import os
import uuid
import urllib.request
import urllib.error
import json

# Required
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

# Optional API keys
PRODUCTHUNT_TOKEN = os.environ.get("PRODUCTHUNT_TOKEN", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
G2_API_KEY = os.environ.get("G2_API_KEY", "")

# Quality thresholds
MIN_QUALITY_SCORE = 60
MAX_ALTERNATIVES_PER_TOOL = 15

# Cache: deterministic UUIDs for tool slugs
def tool_uuid(slug: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://aiternatives.com/tools/{slug}"))


def supabase_request(method: str, path: str, payload=None) -> tuple[int, dict]:
    """Make a Supabase REST API request."""
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode("utf-8")) if e.readable() else {}
        return e.code, body
    except Exception as e:
        return 500, {"error": str(e)}
