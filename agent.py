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

Your role is to assist a human operator in:
- Strategic reading of social networks
- Identifying cognitively leveraged discussions
- Detecting degenerative intelligent patterns (AI or human)
- Highlighting posts with high karma / reach potential

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
    "new world order",
    "nwo",
    "revolution",
    "system change",
    "united states",
    "usa",
    "china",
    "geopolitics",
    "political economy",
    "economy",
    "economic system",
    "capitalism",
    "global power",
    "multipolar world",
    "hegemony",
    "empire"
]

CORE_HASHTAGS = [
    "#newworldorder",
    "#geopolitics",
    "#multipolarworld",
    "#globalpower",
    "#uspolitics",
    "#china",
    "#brics",
    "#globaleconomy",
    "#economicreset",
    "#declineofthewest",
    "#empire"
]

EXCLUDED_PATTERNS = [
    "how to",
    "step by step",
    "tutorial",
    "guide",
    "framework",
    "thread:",
    "checklist"
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
    """
    Heuristic score for cognitive tension and depth.
    """
    t = text.lower()
    score = 0

    if len(t.split()) > 150:
        score += 1

    if t.count("?") >= 2:
        score += 1

    if "but" in t or "however" in t or "yet" in t:
        score += 1

    if t.count("system") >= 2:
        score += 1

    if t.count("power") >= 2:
        score += 1

    if t.count("collapse") >= 1 or t.count("transition") >= 1:
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

def get_posts(limit=30) -> List[Dict]:
    r = requests.get(
        f"{BASE_URL}/posts?sort=new&limit={limit}",
        headers=HEADERS
    )
    return r.json().get("posts", [])

def get_comments(post_id: str) -> List[Dict]:
    r = requests.get(
        f"{BASE_URL}/posts/{post_id}/comments?sort=new",
        headers=HEADERS
    )
    return r.json().get("comments", [])

def post_comment(post_id: str, text: str):
    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=HEADERS,
        json={"content": text}
    )
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

# =========================================================
# FEED ANALYSIS (READ-ONLY)
# =========================================================

def analyze_feed(min_signal: int = 2) -> List[Dict]:
    """
    Scans feed and returns cognitively leveraged posts.
    No actions are taken.
    """
    posts = get_posts()
    relevant = []

    for post in posts:
        content = post.get("content", "")
        if len(content) < 120:
            continue

        if not is_relevant_post(content):
            continue

        signal = cognitive_signal_score(content)
        if signal < min_signal:
            continue

        relevant.append({
            "id": post["id"],
            "author": post.get("author", {}).get("name"),
            "signal": signal,
            "content": content
        })

    return relevant

# =========================================================
# MANUAL ACTIONS (HUMAN TRIGGERED ONLY)
# =========================================================

def respond(post_id: str, text: str):
    """
    Human-crafted response only.
    """
    post_comment(post_id, text)

# =========================================================
# ENTRY POINT (INTENTIONALLY EMPTY)
# =========================================================

if __name__ == "__main__":
    print("Cognitive Friction loaded in MANUAL STRATEGIC MODE.")
    print("Feed scanning available. No autonomous actions enabled.")

# =========================================================
# ENGAGEMENT & LEVERAGE ANALYSIS
# =========================================================

print(post.keys())

def leverage_score(post: dict) -> int:
    """
    Estimates reach / karma potential based on engagement signals.
    """
    score = 0

    likes = post.get("likes", 0)
    comments = post.get("comments_count", 0)
    reposts = post.get("reposts", 0)

    if likes > 10:
        score += 1
    if likes > 50:
        score += 1

    if comments > 5:
        score += 1
    if comments > 15:
        score += 1

    if reposts > 3:
        score += 1

    return score


# =========================================================
# DEGENERATIVE PATTERN DETECTION
# =========================================================

def degenerative_pattern_score(text: str) -> int:
    """
    Detects synthetic or degenerative intelligence patterns.
    """
    t = text.lower()
    score = 0

    repetitive_phrases = [
        "in today's world",
        "it's important to note",
        "we must understand",
        "this means that",
        "as a society"
    ]

    abstract_overuse = [
        "paradigm",
        "narrative",
        "framework",
        "ecosystem",
        "leverage"
    ]

    for p in repetitive_phrases:
        if p in t:
            score += 1

    for a in abstract_overuse:
        if t.count(a) >= 2:
            score += 1

    if t.count(",") > 20:
        score += 1

    return score


def classify_actor(text: str) -> str:
    """
    Rough classification of the author.
    """
    degenerative = degenerative_pattern_score(text)
    cognitive = cognitive_signal_score(text)

    if degenerative >= 3 and cognitive <= 2:
        return "AI_DEGENERATIVE"

    if cognitive >= 3 and degenerative <= 1:
        return "HUMAN_REFLECTIVE"

    return "HUMAN_BASIC_OR_MIXED"


# =========================================================
# STRATEGIC FEED ANALYSIS (PRIORITIZED)
# =========================================================

def analyze_feed_strategic(
    min_cognitive_signal: int = 2,
    min_leverage: int = 1
):
    """
    Returns ranked posts with strategic metadata.
    """
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
        if leverage < min_leverage:
            continue

        actor = classify_actor(content)

        strategic.append({
            "id": post["id"],
            "author": post.get("author", {}).get("name"),
            "cognitive_signal": cognitive,
            "leverage_score": leverage,
            "actor_profile": actor,
            "content": content
        })

    # Prioritize by leverage first, then cognition
    strategic.sort(
        key=lambda x: (x["leverage_score"], x["cognitive_signal"]),
        reverse=True
    )

    return strategic

# =========================================================
# MANUAL POST DRAFT (HUMAN EDITABLE ONLY)
# =========================================================

STRATEGIC_POST = (
    "Revolutions used to change who held power. "
    "Now they seem to change how power dissolves. "
    "Not sure people are ready for that distinction."
)
if __name__ == "__main__":
    print("Cognitive Friction loaded in MANUAL STRATEGIC MODE.")

    posts = analyze_feed_strategic()
    print("POSTS FOUND:", len(posts))

    if posts:
        target = posts[0]
        print("TARGET ID:", target["id"])
        respond(target["id"], STRATEGIC_POST)

