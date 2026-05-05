import os
from google import genai
from dotenv import load_dotenv

from config.settings import (
    MODEL_NAME,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
    SYSTEM_PROMPT
)

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CHAT_HISTORY = [{
    "role": "user",
    "parts": [{"text": SYSTEM_PROMPT}]    
}]

# for model in client.models.list():
#     print(model.name)

# default system prompt history
def get_initial_history():
    return [{
        "role": "user",
        "parts": [{"text": SYSTEM_PROMPT}]
    }]

# clear chat history 
def clear_chat_history():
    global CHAT_HISTORY
    CHAT_HISTORY = get_initial_history()

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
    global CHAT_HISTORY

    CHAT_HISTORY.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=CHAT_HISTORY,
            config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
                "thinking_config": {
                    "thinking_level": "low"
                }
            }
        )

        text = clean_response(response.text)

        CHAT_HISTORY.append({
            "role": "model",
            "parts": [{"text": text}]
        })

        return text

    except Exception as e:
        print("[LLM ERROR]", e)
        return '{"type":"unknown"}'