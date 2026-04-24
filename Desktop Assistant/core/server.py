import subprocess
import requests
import atexit
import time

ollama_process = None

def is_running():
    try:
        requests.get("http://localhost:11434", timeout=1)
        return True
    except:
        return False
    
def start_server():
    global ollama_process

    if is_running():
        print("[OK] Ollama already running!")
        return
    
    print("[START] Launching Ollama Server...")
    ollama_process = subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for Ollama to accept requests before continuing.
    for _ in range(30):
        if is_running():
            print("[OK] Ollama server is ready")
            return
        time.sleep(1)

    print("[ERROR] Ollama did not become ready within 30 seconds")

def stop_server():
    global ollama_process

    if ollama_process:
        print("[STOP] Shutting down Ollama...")
        ollama_process.terminate()
        ollama_process = None
    
# atexit.register(stop_server)