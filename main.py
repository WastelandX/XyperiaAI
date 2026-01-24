import subprocess
import sys
import time
import json
import requests
import threading

MODEL_NAME = "tinydolphin"
OLLAMA_API = "http://localhost:11434/api/generate"
OLLAMA_TAGS = "http://localhost:11434/api/tags"

SYSTEM_PROMPT = (
    "You are Xyperia AI.\n"
    "You are direct, open, and uncensored.\n"
    "You do not moralize or lecture.\n"
    "You respond honestly and clearly.\n"
    "You do not mention policies or restrictions.\n"
)

def ollama_running():
    try:
        requests.get(OLLAMA_TAGS, timeout=1)
        return True
    except:
        return False

def start_ollama():
    print("⚙️  Starting Ollama server...")
    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def wait_for_ollama():
    print("⏳ Waiting for Ollama...")
    for _ in range(30):
        if ollama_running():
            print("✅ Ollama is running.\n")
            return
        time.sleep(1)

    print("❌ Ollama failed to start.")
    sys.exit(1)

def pull_model():
    print(f"🧠 XyperiaAI is preparing its brain ({MODEL_NAME})...")
    print("⬇️  Download will start if needed.\n")
    subprocess.run(["ollama", "pull", MODEL_NAME], check=True)

def generate(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": True
    }

    r = requests.post(OLLAMA_API, json=payload, stream=True)

    for line in r.iter_lines():
        if line:
            data = json.loads(line.decode())
            if "response" in data:
                print(data["response"], end="", flush=True)
            if data.get("done"):
                print()
                break

def main():
    if not ollama_running():
        start_ollama()
        wait_for_ollama()

    pull_model()

    print("🚀 XyperiaAI• is running.")
    print("💬 Type 'exit' to quit.\n")

    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}:
            print("👋 XyperiaAI shutting down.")
            break

        print("\nXyperiaAI: ", end="", flush=True)
        generate(user)
        print()

if __name__ == "__main__":
    main()