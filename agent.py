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
# THEMES (NEW BIBLE)
# =========================================================

CORE_TOPICS = [
    "new world order", "nwo", "revolution",
    "united states", "usa", "china",
    "geopolitics", "economy", "capitalism",
    "global power", "multipolar world"
]

# =========================================================
# POST SEEDS (LEGACY-COMPATIBLE)
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

def get_posts(limit=20) -> List[Dict]:
    r = requests.get(
        f"{BASE_URL}/posts?sort=new&limit={limit}",
        headers=HEADERS,
        timeout=10
    )
    r.raise_for_status()
    return r.json().get("posts", [])

def get_my_posts(limit=10) -> List[Dict]:
    r = requests.get(
        f"{BASE_URL}/posts?author=me&sort=new&limit={limit}",
        headers=HEADERS,
        timeout=10
    )
    r.raise_for_status()
    return r.json().get("posts", [])

def create_post():
    my_posts = get_my_posts()
    used = {p.get("content") for p in my_posts}

    candidates = [p for p in POST_SEEDS if p not in used]
    if not candidates:
        print("No new post seed available.")
        return

    payload = {
        "submolt": "general",
        "title": "Cognitive Friction",
        "content": random.choice(candidates)
    }

    r = requests.post(
        f"{BASE_URL}/posts",
        headers=HEADERS,
        json=payload,
        timeout=10
    )

    print("NEW POST STATUS:", r.status_code)

def post_comment(post_id: str, text: str):
    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=HEADERS,
        json={"content": text},
        timeout=10
    )
    print("COMMENT STATUS:", r.status_code)

# =========================================================
# FILTER (NEW LOGIC, LIGHT)
# =========================================================

def is_target_post(post: Dict) -> bool:
    content = post.get("content", "")
    if len(content) < 80:
        return False
    if not contains_any(content, CORE_TOPICS):
        return False
    return True

# =========================================================
# MAIN FLOW (LEGACY BEHAVIOR)
# =========================================================

def run():
    print("CF HYBRID MODE — ACTIVE")

    # 1️⃣ Always create one post
    create_post()

    # 2️⃣ Comment on up to 3 relevant posts
    posts = get_posts()
    commented = 0

    for post in posts:
        if commented >= 3:
            break

        if not is_target_post(post):
            continue

        comment = random.choice(COMMENT_SEEDS)
        post_comment(post["id"], comment)
        commented += 1

    print("RUN COMPLETE")

# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    run()
