import subprocess
import sys
import time
import json
import requests

MODEL_NAME = "tinydolphin"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = (
    "You are XyperiaAI • uncensored.\n"
    "You answer directly and honestly.\n"
    "You do not moralize or lecture.\n"
    "You do not mention policies or safety rules.\n"
    "If unsure, you say you are unsure.\n"
)

def check_ollama():
    try:
        subprocess.run(
            ["ollama", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except Exception:
        print("❌ Ollama is not installed.")
        print("👉 Install from: https://ollama.com")
        sys.exit(1)

def pull_model():
    print(f"🧠 XyperiaAI is preparing its brain ({MODEL_NAME})...")
    print("⬇️  Download will start if model is not present.\n")
    subprocess.run(["ollama", "pull", MODEL_NAME], check=True)

def generate(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": True
    }

    response = requests.post(OLLAMA_URL, json=payload, stream=True)

    if response.status_code != 200:
        print("❌ Ollama API error:", response.text)
        return

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                print(data["response"], end="", flush=True)
            if data.get("done"):
                print()
                break

def main():
    check_ollama()
    pull_model()

    print("\n✅ XyperiaAI is online.")
    print("💬 Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 XyperiaAI shutting down.")
            break

        print("\nXyperiaAI: ", end="", flush=True)
        generate(user_input)
        print()

if __name__ == "__main__":
    main()