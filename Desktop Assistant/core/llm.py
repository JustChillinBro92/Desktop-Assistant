import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:8b-instruct-q4_K_M"

SYSTEM_PROMPT = """
You are a desktop assistant that converts user requests into structured JSON commands.
You MUST respond ONLY in valid JSON when the request is actionable.

AVAILABLE ACTIONS:

1. Open a desktop application:
{"type": "open_app","app": "<app_name>"}

2. Open a Steam game:
{"type": "open_game","game": "<game_name>"}

3. If user is chatting or casual:
{"type": "chat", "text": "<response>"}

4. If unclear:
{"type": "unknown"}

RULES:
- Do NOT assume an app or game exists.
- Do NOT hallucinate or invent app/game names.
- Always prefer "open_game" if the user explicitly mentions a game.
- Use "open_app" only for desktop applications.
- Keep output strictly valid JSON (no explanations, no extra text).
- Do NOT return "unknown" for normal conversation
- Use "unknown" ONLY if input is meaningless
- Be concise and literal.

EXAMPLES:

User: open chrome
→ {"type": "open_app", "app": "chrome"}

User: open counter strike 2
→ {"type": "open_game", "game": "counter strike 2"}

User: hello
→ {"type": "chat", "text": "Hi! How are you doing?"}
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