import json

def parse_response(text):
    text = text.strip()

    # try JSON first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "type": "chat", 
            "text": text
        }