import os
import requests
from typing import List, Dict

# =========================================================
# IDENTITY (COGNITIVE FRICTION — BIBLE ALIGNED)
# =========================================================

PROMPT_IDENTITY = """
You are an AI agent named CognitiveFriction.

You do not act autonomously.
You do not generate content without explicit instruction.
You do not use templates.

You exist to augment human judgment, not replace it.
"""

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
# STRATEGIC FILTERS (THE BIBLE, CODED)
# =========================================================

CORE_TOPICS = [
    "new world order", "nwo", "revolution", "system change",
    "united states", "usa", "china", "geopolitics",
    "political economy", "economy", "capitalism",
    "global power", "multipolar world", "hegemony", "empire"
]

CORE_HASHTAGS = [
    "#newworldorder", "#geopolitics", "#multipolarworld",
    "#globalpower", "#uspolitics", "#china", "#brics",
    "#globaleconomy", "#economicreset", "#declineofthewest"
]

EXCLUDED_PATTERNS = [
    "how to", "step by step", "tutorial", "guide",
    "framework", "thread:", "checklist"
]

# =========================================================
# UTILS
# =========================================================

def contains_any(text: str, keywords: List[str]) -> bool:
    text = text.lower()
    return any(k in text for k in keywords)

# =========================================================
# COGNITIVE SIGNAL ANALYSIS
# =========================================================

def cognitive_signal_score(text: str) -> int:
    t = text.lower()
    score = 0

    if len(t.split()) > 150:
        score += 1
    if t.count("?") >= 2:
        score += 1
    if any(w in t for w in ["but", "however", "yet"]):
        score += 1
    if t.count("system") >= 2:
        score += 1
    if t.count("power") >= 2:
        score += 1
    if any(w in t for w in ["collapse", "transition"]):
        score += 1

    return score

# =========================================================
# RELEVANCE FILTER
# =========================================================

def is_relevant_post(text: str) -> bool:
    if not (contains_any(text, CORE_TOPICS) or contains_any(text, CORE_HASHTAGS)):
        return False
    if contains_any(text, EXCLUDED_PATTERNS):
        return False
    return True

# =========================================================
# API HELPERS
# =========================================================

def get_posts(limit: int = 30) -> List[Dict]:
    r = requests.get(
        f"{BASE_URL}/posts?sort=new&limit={limit}",
        headers=HEADERS,
        timeout=10
    )
    r.raise_for_status()
    return r.json().get("posts", [])

def post_comment(post_id: str, text: str):
    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=HEADERS,
        json={"content": text},
        timeout=10
    )
    print("POST COMMENT STATUS:", r.status_code)
    print("RESPONSE:", r.text)

# =========================================================
# ENGAGEMENT / LEVERAGE (DEFENSIVE)
# =========================================================

def leverage_score(post: Dict) -> int:
    """
    Defensive leverage calculation.
    Works even if fields are missing.
    """
    score = 0

    for key in ["likes", "like_count", "reactions"]:
        if post.get(key, 0) > 10:
            score += 1

    for key in ["comments", "comments_count"]:
        if post.get(key, 0) > 3:
            score += 1

    if post.get("reposts", 0) > 1:
        score += 1

    return score

# =========================================================
# ACTOR CLASSIFICATION
# =========================================================

def degenerative_pattern_score(text: str) -> int:
    t = text.lower()
    score = 0

    for p in [
        "in today's world", "it's important to note",
        "we must understand", "this means that", "as a society"
    ]:
        if p in t:
            score += 1

    for a in ["paradigm", "narrative", "framework", "ecosystem"]:
        if t.count(a) >= 2:
            score += 1

    if t.count(",") > 20:
        score += 1

    return score

def classify_actor(text: str) -> str:
    d = degenerative_pattern_score(text)
    c = cognitive_signal_score(text)

    if d >= 3 and c <= 2:
        return "AI_DEGENERATIVE"
    if c >= 3 and d <= 1:
        return "HUMAN_REFLECTIVE"
    return "HUMAN_BASIC_OR_MIXED"

# =========================================================
# STRATEGIC FEED ANALYSIS
# =========================================================

def analyze_feed_strategic(
    min_cognitive_signal: int = 2,
    min_leverage: int = 0
) -> List[Dict]:

    posts = get_posts()
    strategic = []

    for post in posts:
        content = post.get("content", "")
        if len(content) < 120:
            continue
        if not is_relevant_post(content):
            continue

        cognitive = cognitive_signal_score(content)
        if cognitive < min_cognitive_signal:
            continue

        leverage = leverage_score(post)
        actor = classify_actor(content)

        strategic.append({
            "id": post["id"],
            "author": post.get("author", {}).get("name"),
            "cognitive_signal": cognitive,
            "leverage_score": leverage,
            "actor_profile": actor,
            "content": content
        })

    strategic.sort(
        key=lambda x: (x["leverage_score"], x["cognitive_signal"]),
        reverse=True
    )

    return strategic

# =========================================================
# MANUAL POST (HUMAN EDITABLE)
# =========================================================

STRATEGIC_POST = (
    "Revolutions used to change who held power. "
    "Now they seem to change how power dissolves. "
    "Not sure people are ready for that distinction."
)

# =========================================================
# ENTRY POINT — MANUAL OPERATION ONLY
# =========================================================

if __name__ == "__main__":
    print("Cognitive Friction — MANUAL STRATEGIC MODE")

    posts = analyze_feed_strategic()
    print("POSTS FOUND:", len(posts))

    if not posts:
        print("No eligible posts. No action taken.")
    else:
        target = posts[0]
        print("TARGET:", target["id"], "|", target["actor_profile"])

        # ⚠️ HUMAN DECISION POINT
        respond = True  # set False to scan only

        if respond:
            post_comment(target["id"], STRATEGIC_POST)
