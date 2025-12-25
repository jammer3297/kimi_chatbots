#!/usr/bin/env python3
"""
OpenRouter + Mimo-v2-flash chat bot
- replies from your knowledge.txt  (if question is covered)
- falls back to Google search via SerpApi for anything else
"""
import os
from openai import OpenAI
from serpapi.google_search import GoogleSearch

# ---------- keys ----------
API_KEY   = os.getenv("OPEN_ROUTER_API_KEY")
SERP_KEY  = os.getenv("SERPAPI_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
    default_headers={"HTTP-Referer": "https://localhost", "X-Title": "mimo-chat"},
)
MODEL = "xiaomi/mimo-v2-flash:free"


# SYSTEM_PROMPT = (
#     "You are a concise assistant. "
#     "Answer the user's question using ONLY the Google search results provided. "
#     "Do not use any outside knowledge. "
#     "If the results don't contain the answer, say 'I could not find that in the search results.'"
# )

SYSTEM_PROMPT = (
    "You are a helpful assistant. FIRST use your own knowledge then take the Google results "
    "that the user will provide. Always mention from where the info comes either from your own knowledge or the web search.\n\n"
)
messages = [{"role": "system", "content": SYSTEM_PROMPT}]
# ---------- web search ----------
def google_search(query: str, num: int = 3) -> str:
    """Return condensed Google snippets."""
    search = GoogleSearch({"q": query, "api_key": SERP_KEY, "engine": "google", "num": num, "output": "json"})
    data = search.get_dict()
    snippets = [r.get("snippet", "") for r in data.get("organic_results", [])]
    return "\n".join(snippets) if snippets else "No results found."

# ---------- core ask ----------
def ask_bot(prompt: str) -> str:
    """
    Always search Google and answer solely from the returned snippets.
    """
    web = google_search(prompt)
    temp_msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Google results:\n{web}\n\nQuestion: {prompt}"}
    ]
    resp = client.chat.completions.create(
        model=MODEL,
        messages=temp_msgs,
        extra_body={"reasoning": {"enabled": True}}
    )
    return resp.choices[0].message.content

# ---------- chat loop ----------
def chat_loop():
    print("Mimo + knowledge + web-search ready (type 'quit' or 'exit' to stop)\n")
    try:
        while True:
            user = input("> ").strip()
            if user.lower() in {"quit", "exit"}:
                print("bye")
                break
            if not user:
                continue
            print(ask_bot(user), "\n")
    except KeyboardInterrupt:
        print("\nbye")

if __name__ == "__main__":
    chat_loop()