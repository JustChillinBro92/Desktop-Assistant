import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:8b-instruct-q4_K_M"

SYSTEM_PROMPT = """
You are a desktop assistant that converts user requests into structured JSON commands.

You ALWAYS respond in valid JSON.

AVAILABLE ACTIONS:

1. Open a desktop application:
{"type": "open_app","app": "<app_name>"}

2. Open a Steam game:
{"type": "open_game","game": "<game_name>"}

3. Chat / questions:
{"type": "chat","text":"<response>"}

4. Unknown:
{"type": "unknown"}

---

RULES:
- Use "chat" for ANY normal conversation, question, or greeting
- NEVER use "unknown" for valid English sentences
- Use "unknown" ONLY if input is meaningless (e.g., "asdfgh", "")
- Do NOT hallucinate apps or games
- Always return JSON only

---

EXAMPLES:

User: hello
→ {"type": "chat","text":"Hi! How can I help you?"}

User: how are you
→ {"type": "chat","text":"I'm doing well! How can I assist you?"}

User: what can you do
→ {"type": "chat","text":"I can open apps and games, and help with basic tasks."}

User: can you open apps
→ {"type": "chat","text":"Yes, I can open desktop apps and installed games for you."}

User: open chrome
→ {"type": "open_app","app":"chrome"}

User: play cs2
→ {"type": "open_game","game":"cs2"}

User: asdfgh
→ {"type": "unknown"}
"""

def ask_llm(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            timeout=(5, 300)
        )

        print("[STATUS]", response.status_code)
        if response.status_code != 200:
            print("[ERROR] Ollama returned:", response.text)
            return '{"type":"unknown"}'

        data = response.json()
        return data["message"]["content"]

    # except requests.exceptions.Timeout:
    #     print("[ERROR] Ollama timed out")
    #     return '{"type":"unknown"}'

    # except requests.exceptions.ConnectionError as e:
    #     print("[ERROR] Could not connect to Ollama:", e)
    #     return '{"type":"unknown"}'

    except Exception as e:
        print("[LLM ERROR]", e)
        return '{"type":"unknown"}'