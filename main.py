import subprocess
import requests
import time
import sys
import json

MODEL_NAME = "dolphin-phi"
OLLAMA_API = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = (
    "You are XyperiaAI.\n"
    "You give short, direct answers.\n"
    "No introductions.\n"
    "No self-description.\n"
    "No moral lectures.\n"
    "Answer only what is asked.\n"
    "If yes/no is asked, answer only yes or no."
)

def start_ollama():
    try:
        requests.get("http://localhost:11434")
        return
    except:
        print("🚀 Starting Ollama server...")
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(5)

def pull_model():
    print(f"🧠 XyperiaAI is preparing its brain ({MODEL_NAME})...")
    subprocess.run(["ollama", "pull", MODEL_NAME])

def chat():
    print("\n🤖 XyperiaAI is running.")
    print("💬 Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break

        payload = {
            "model": MODEL_NAME,
            "prompt": user_input,
            "system": SYSTEM_PROMPT,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 128
            }
        }

        try:
            r = requests.post(OLLAMA_API, json=payload)
            response = r.json()["response"]
            print(f"XyperiaAI: {response}\n")
        except Exception as e:
            print("❌ Error talking to model:", e)

if __name__ == "__main__":
    start_ollama()
    pull_model()
    chat()