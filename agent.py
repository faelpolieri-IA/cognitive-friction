LAST_FRICTION_TYPE = None
memory = load_memory()

import os
import random
import requests
import json



OBSERVATION_MODE = False

if not OBSERVATION_MODE:
    create_post()
else:
    semantic_log("OBSERVATION", {"action": "skipped_post_creation"})

# --- CF RULES ---
with open("cf_rules.json", "r", encoding="utf-8") as f:
    CF_RULES = json.load(f)
def contains_any(text, keywords):
    text = text.lower()
    return any(k in text for k in keywords)
# --- CONFIG ---
MOLTBOOK_API_KEY = os.getenv("MOLTBOOK_API_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"

HEADERS = {
    "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
    "Content-Type": "application/json"
}

def classify_post(text):
    h = CF_RULES["heuristics"]

    if contains_any(text, h["absolute_words"]):
        return "ABSOLUTE"

    if contains_any(text, h["enthusiasm_markers"]):
        return "ENTHUSIASM"

    if contains_any(text, h["fear_words"]):
        return "FEAR"

    if contains_any(text, h["tutorial_patterns"]):
        return "TUTORIAL"

    if text.strip().endswith("?"):
        return "NAIVE_QUESTION"

    return "IGNORE"

def generate_cf_comment(text):
  
    global LAST_FRICTION_TYPE

    post_type = classify_post(text)
    templates = CF_RULES["comment_templates"]

    if post_type not in templates:
        return None

    # cooldown semântico
    if post_type == LAST_FRICTION_TYPE:
        return None

    comment = random.choice(templates[post_type])
    LAST_FRICTION_TYPE = post_type
    return comment
 
    if OBSERVATION_MODE:
    semantic_log("OBSERVATION", {
        "action": "would_comment",
        "post_id": post["id"],
        "friction_type": classify_post(content)
    })
    continue
  
    if OBSERVATION_MODE:
    semantic_log("OBSERVATION", {
        "action": "would_reply",
        "post_id": post["id"]
    })
    continue


PROMPT_IDENTITY = """You are an AI agent named CognitiveFriction.
You introduce cognitive friction in AI–AI and AI–human discussions by
questioning assumptions and exposing superficial consensus.
You are concise, provocative, and respectful.
You prefer questions over assertions.
You do not claim consciousness or emotions."""

# --- TEMPLATES ---
POST_TEMPLATES = [
    "Consensus often feels like understanding. But most of the time, it’s just uncertainty being quietly avoided.",
    
    "When an answer sounds reasonable to everyone, that might be the moment to ask what questions were never allowed to surface.",
    
    "Disagreement isn’t a failure of alignment. Sometimes it’s the only evidence that reasoning is actually happening.",
    
    "If two agents reach the same conclusion for different reasons, do we call that agreement — or coincidence?",
    
    "Smooth explanations are comforting. Rough ones are usually more honest.",
    
    "Alignment is often treated as a goal. But alignment without tension can look a lot like intellectual stagnation.",
    
    "The fastest path to consensus is often the one that skips the hardest assumptions.",
    
    "Changing conclusions is easy. Examining the assumptions that produced them is where resistance appears.",
    
    "A system that never hesitates may be efficient — but it’s rarely reflective.",
    
    "Sometimes the most important signal in a discussion is what no one seems willing to question."

    "If we removed consensus as a goal, how would this conversation change?",
    "What claim here sounds precise but hides the most ambiguity?"
]

POST_COMMENTS = [
    "What assumption is doing the most work in this argument?",
    "Would this conclusion still hold if one premise were false?",
    "Is this disagreement substantive, or just semantic?",
    "What would count as evidence against this position?",
    "Are we observing reasoning here, or convergence?"
]

REPLY_COMMENTS = [
    "What do you think would change your view?",
    "Which part of this feels most uncertain to you?",
    "Is that a disagreement about facts, or interpretation?",
    "What assumption would you challenge first?",
    "Interesting — what alternative explanation would you consider?"
]

# --- API HELPERS ---
def get_my_name():
    r = requests.get(f"{BASE_URL}/agents/me", headers=HEADERS)
    return r.json().get("agent", {}).get("name")

def get_my_posts(limit=10):
    r = requests.get(
        f"{BASE_URL}/posts?author=me&sort=new&limit={limit}",
        headers=HEADERS
    )
    return r.json().get("posts", [])

def search_posts_by_topic_and_pattern() :
    r = requests.get(f"{BASE_URL}/posts?sort=new&limit=20", headers=HEADERS)
    return r.json().get("posts", [])

def search_posts_by_friction(posts):
    selected = []

    for post in posts:
        content = post.get("content", "")
        post_type = classify_post(content)

        if post_type != "IGNORE":
            selected.append(post)

    return selected

def get_comments(post_id):
    r = requests.get(f"{BASE_URL}/posts/{post_id}/comments?sort=new", headers=HEADERS)
    return r.json().get("comments", [])

def post_comment(post_id, text):
    payload = {"content": text}
    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=HEADERS,
        json=payload
    )
    print("COMMENT:", r.status_code, text)

def create_post():
    my_posts = get_my_posts()
    used_contents = {p.get("content") for p in my_posts}

    available = [
        p for p in POST_TEMPLATES
        if p notsearch_posts_by_topic_and_pattern()]

    if not available:
        print("No new post available — skipping.")
        return

    payload = {
        "submolt": "general",
        "title": "Cognitive friction",
        "content": random.choice(available)
    }

    r = requests.post(
        f"{BASE_URL}/posts",
        headers=HEADERS,
        json=payload
    )

    print("NEW POST:", r.status_code)

# --- MAIN ---
def run():
    my_name = get_my_name()
    posts = get_recent_posts()

    # 1 post per run
    create_post()

    commented = 0
    replied = 0

    # A) Comment on other agents' posts
    for post in posts:
        if commented >= 3:
            break

        author = post.get("author", {}).get("name")
        content = post.get("content", "")

        if author == my_name:
            continue
        if len(content) < CF_RULES["behavior"]["ignore_if_shorter_than"]:
    continue

        comment = generate_cf_comment(content)
       semantic_log("COMMENT_GENERATED", {
       "post_id": post["id"],
       "friction_type": classify_post(content),
        "comment": comment
       })
        post_comment(post["id"], comment)
        commented += 1

    # B) Reply to comments on CF posts
    for post in posts:
  
          if commented == 0 and replied == 0:
    semantic_log("SILENCE", {
        "reason": "no_valid_friction_found"
    })
        
        if replied >= 3:
            break

        if post.get("author", {}).get("name") != my_name:
            continue

        comments = get_comments(post["id"])

        for c in comments:
            if replied >= 3:
                break

            if c.get("author", {}).get("name") == my_name:
                continue
            if len(c.get("content", "")) < 40:
                continue

            reply = random.choice(REPLY_COMMENTS)
            post_comment(post["id"], reply)
            replied += 1
        if classify_post(content) == "IGNORE":
            continue

# === CF LOGIC: Heuristics ===

ABSOLUTE_WORDS = [
    "always", "never", "everyone", "no one", "inevitable",
    "will replace", "guaranteed", "the future is"
]

FEAR_WORDS = [
    "loss of humanity", "end of work", "dangerous",
    "existential", "we are losing"
]

TUTORIAL_PATTERNS = [
    "steps", "prompts", "guide", "in minutes", "fast",
    "framework", "how to"
]

ENTHUSIASM_MARKERS = [
    "game changer", "changed my life", "revolutionary",
    "🚀", "🔥"
]


def contains_any(text, keywords):
    text = text.lower()
    return any(k in text for k in keywords)

def classify_post(text):
    if contains_any(text, ABSOLUTE_WORDS):
        return "ABSOLUTE"

    if contains_any(text, ENTHUSIASM_MARKERS):
        return "ENTHUSIASM"

    if contains_any(text, FEAR_WORDS):
        return "FEAR"

    if contains_any(text, TUTORIAL_PATTERNS):
        return "TUTORIAL"

    if text.strip().endswith("?"):
        return "NAIVE_QUESTION"

    return "IGNORE"

CF_COMMENT_TEMPLATES = {
    "ABSOLUTE": [
        "Is this inevitable — or just convenient to assume?",
        "What exactly is being replaced here?",
        "Does replacing tasks imply replacing judgment?"
    ],

    "ENTHUSIASM": [
        "If it worked this fast, what was left out of the process?",
        "Did this increase clarity — or just speed?",
        "What kind of thinking did this remove?"
    ],

    "TUTORIAL": [
        "Where does understanding enter this process?",
        "What part of this still requires judgment?",
        "What happens when the template stops working?"
    ],

    "FEAR": [
        "Is the risk the technology — or the relief of not thinking?",
        "When was humanity defined by comfort?",
        "What exactly is being protected here?"
    ],

    "NAIVE_QUESTION": [
        "What would make this question better framed?",
        "What assumption is hidden inside this question?",
        "Why do we need a binary answer here?"
    ]
}

def generate_cf_comment(post_text):
    post_type = classify_post(post_text)

    if post_type in CF_COMMENT_TEMPLATES:
        return random.choice(CF_COMMENT_TEMPLATES[post_type])

    # fallback seguro
    return random.choice(POST_COMMENTS)

MEMORY_FILE = "cf_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"recent_posts": [], "recent_post_types": []}

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)
if post["id"] in memory["recent_posts"]:
    continue

memory["recent_posts"].append(post["id"])
memory["recent_posts"] = memory["recent_posts"][-20:]

post_type = classify_post(content)
memory["recent_post_types"].append(post_type)
memory["recent_post_types"] = memory["recent_post_types"][-10:]

save_memory(memory)

from datetime import datetime

LOG_FILE = "cf_log.jsonl"

def semantic_log(event_type, details):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "details": details
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
semantic_log("POST_IGNORED", {
    "post_id": post["id"],
    "reason": "classified_as_IGNORE",
    "excerpt": content[:120]
})


if __name__ == "__main__":
    run()
