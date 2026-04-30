from core.assistant import run_assistant
from voice.live_agent import start_voice_agent

if __name__ == "__main__":
    try:
        mode = input("\nChoose mode: text or voice (t/v): ").lower().strip()

        if mode == "v":
            start_voice_agent()
        elif mode == 't': 
            run_assistant()
        else:
            print("Invalid option!\n")

    except KeyboardInterrupt:
        print("\nApplication Closed!\n")
