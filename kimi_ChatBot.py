#!/usr/bin/env python3
"""
OpenRouter + Mimo-v2-flash chat bot with private knowledge
"""
import os
from openai import OpenAI
import csv, io
# ---------- config ----------
API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
    default_headers={"HTTP-Referer": "https://localhost", "X-Title": "mimo-chat"},
)
MODEL = "xiaomi/mimo-v2-flash:free"

# ---------- load knowledge ----------


# ---------- load CSV ----------
try:
    with open("sailings.csv", newline='', encoding="utf-8") as f:
        rows = list(csv.DictReader(f))          # first line = column names
    KNOWLEDGE = "\n".join(
        " | ".join(str(v) for v in row.values()) for row in rows
    )
except FileNotFoundError:
    KNOWLEDGE = ""

SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Use ONLY the information below to answer user questions. "
    "If the info isn't mentioned, say 'I don't know'.\n\n"
    f"--- BEGIN KNOWLEDGE ---\n{KNOWLEDGE}\n--- END KNOWLEDGE ---"
)
# ----------------------------

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def ask_mimo(prompt: str) -> str:
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        extra_body={"reasoning": {"enabled": True}},
    )
    assistant_msg = resp.choices[0].message
    messages.append(
        {
            "role": "assistant",
            "content": assistant_msg.content,
            "reasoning_details": getattr(assistant_msg, "reasoning_details", None),
        }
    )
    return assistant_msg.content

def chat_loop():
    print("Mimo chat ready (type 'quit' or 'exit' to stop)\n")
    try:
        while True:
            user = input("> ").strip()
            if user.lower() in {"quit", "exit"}:
                print("bye")
                break
            if not user:
                continue
            print(ask_mimo(user), "\n")
    except KeyboardInterrupt:
        print("\nbye")

if __name__ == "__main__":
    chat_loop()