import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
MODEL = "gemini-3.1-flash-lite-preview"

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
- If user is chatting or asking a normal question, use "chat".
- If chat topic is irrelevant to opening apps/games indulge the user (pull data from google if needed).
- If user wants to open/launch/start software, use "open_app".
- If user wants to play/open/launch/start a game, use "open_game".
- NEVER use "unknown" for valid English sentences.
- Use "unknown" ONLY if input is meaningless (e.g., "asdfgh", "").
- Do NOT hallucinate apps or games.
- Always return JSON only.
- Do NOT include markdown.

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

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# for model in client.models.list():
#     print(model.name)

# guardrail for markdown response
def clean_response(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = (
            text.replace("```json", "")
            .replace("```JSON", "")
            .replace("```", "")
            .strip()
        )

    return text


def ask_llm(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
        )

        return clean_response(response.text)

    except Exception as e:
        print("[LLM ERROR]", e)
        return '{"type":"unknown"}'