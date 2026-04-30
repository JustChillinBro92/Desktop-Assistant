from core.llm import ask_llm
from core.parser import parse_response
from core.app_resolver import open_something


def run_user_message(user_input):
    response = ask_llm(user_input)
    # print("LLM:", response)

    command = parse_response(response)

    # -----------------------
    # ACTION HANDLER
    # -----------------------
    if isinstance(command, dict) and command.get("type") in ["open_app", "open_game"]:
        open_something(command)
        return {
            "type": command.get('type'),
            "message": f"Opening {command.get('app') or command.get('game')}"
        }

    # -----------------------
    # CHAT HANDLER
    # -----------------------
    elif isinstance(command, dict) and command.get("type") == "chat":
        print("AI:", command.get("text", ""), "\n")
        return {
            "type": command.get('type'),
            "message": f"{command.get('text', "")}"
        }

    else:
        print("\nAI: I didn't understand that.", "\n")
        return {
            "type": "unknown",
            "message": "I didn't understand that."
        }


def run_assistant():
    print("")
    print("+----------------------------------------------+")
    print("| AI Assistant Started ( type 'exit' to quit ) |")
    print("+----------------------------------------------+\n")

    while True:
        user_input = input("You: ").strip()
        print("")

        if user_input.lower() in ["exit", "quit"]:
            break
        
        run_user_message(user_input)