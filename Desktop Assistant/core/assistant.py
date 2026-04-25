from core.llm import ask_llm
from core.parser import parse_response
from core.app_resolver import open_something


def run_assistant():
    print("")
    print("+--------------------------------------------+")
    print("| AI Assistant Started (type 'exit' to quit) |")
    print("+--------------------------------------------+\n")

    while True:
        user_input = input("You: ").strip()
        print("")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = ask_llm(user_input)
        # print("LLM:", response)

        command = parse_response(response)

        # -----------------------
        # ACTION HANDLER
        # -----------------------
        if isinstance(command, dict) and command.get("type") in ["open_app", "open_game"]:
            open_something(command)

        # -----------------------
        # CHAT HANDLER
        # -----------------------
        elif isinstance(command, dict) and command.get("type") == "chat":
            print("AI:", command.get("text", ""), "\n")

        elif isinstance(command, dict) and command.get("type") == "unknown":
            print("\nAI: I didn't understand that.", "\n")

        else:
            print("\nAI: I didn't understand that.", "\n")
