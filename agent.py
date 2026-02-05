import os
import random
import requests
from typing import List, Dict

# =========================================================
# CONFIG
# =========================================================

MOLTBOOK_API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"

HEADERS = {
    "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
    "Content-Type": "application/json"
}

# =========================================================
# THEMES (CF BIBLE – LIGHT FILTER)
# =========================================================

CORE_TOPICS = [
    "new world order",
    "nwo",
    "revolution",
    "united states",
    "usa",
    "china",
    "geopolitics",
    "economy",
    "capitalism",
    "global power",
    "multipolar world"
]

# =========================================================
# CONTENT SEEDS
# =========================================================

POST_SEEDS = [
    "Everyone talks about a New World Order as if it were a plan. What if it’s just systems drifting without control?",
    "Revolutions used to replace leaders. Now they seem to dissolve structures instead.",
    "The most interesting part of geopolitics today is how little control anyone seems to have.",
    "Economic debates feel intense, yet strangely disconnected from where power actually moved.",
    "Multipolarity isn’t emerging because someone planned it — but because old systems stopped holding."
]

COMMENT_SEEDS = [
    "What assumption is doing most of the work here?",
    "Is this a cause — or a symptom?",
    "What part of this feels least examined?",
    "What would challenge this conclusion?",
    "Is this describing power — or reacting to its loss?"
]

# =========================================================
# UTILS
# =========================================================

def contains_any(text: str, keywords: List[str]) -> bool:
    t = text.lower()
    return any(k in t for k in keywords)

# =========================================================
# API HELPERS
# =========================================================

def get_posts(limit: int = 20) -> List[Dict]:
    r = requests.get(
        f"{BASE_URL}/posts?sort=new&limit={limit}",
        headers=HEADERS,
        timeout=10
    )
    r.raise_for_status()
    return r.json().get("posts", [])

def create_post():
    """
    Attempts to create a post.
    NOTE: This may be blocked by Moltbook policy for agents.
    """
    payload = {
        "content": random.choice(POST_SEEDS)
    }

    r = requests.post(
        f"{BASE_URL}/posts",
        headers=HEADERS,
        json=payload,
        timeout=10
    )

    print("NEW POST STATUS:", r.status_code)
    print("NEW POST RESPONSE:", r.text)

    if r.status_code not in (200, 201):
        print("⚠️ Post creation not allowed or rejected by API.")

def post_comment(post_id: str, text: str):
    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=HEADERS,
        json={"content": text},
        timeout=10
    )

    print("COMMENT STATUS:", r.status_code)
    print("COMMENT RESPONSE:", r.text)

    if r.status_code not in (200, 201):
        print("❌ Comment failed on post:", post_id)

# =========================================================
# FILTER (SAFE + DEFENSIVE)
# =========================================================

def is_target_post(post: Dict) -> bool:
    content = post.get("content")

    if not content or not isinstance(content, str):
        return False

    if len(content) < 80:
        return False

    if not contains_any(content, CORE_TOPICS):
        return False

    return True

# =========================================================
# MAIN FLOW (LEGACY-SAFE, API-COMPATIBLE)
# =========================================================

def run():
    print("CF HYBRID MODE — ACTIVE")

    # Attempt to create one post (may be blocked by API policy)
    create_post()

    # Comment on up to 3 relevant posts
    posts = get_posts()
    commented = 0

    for post in posts:
        if commented >= 3:
            break

        if not is_target_post(post):
            continue

        comment = random.choice(COMMENT_SEEDS)
        post_comment(post.get("id"), comment)
        commented += 1

    print("RUN COMPLETE")

# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    run()
