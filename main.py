import requests
import time
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "dolphin-phi:2.7b"
AI_NAME = "Xyperia"

def loading(text="Initializing Xyperia"):
    for i in range(3):
        sys.stdout.write(f"\r{text}{'.' * (i+1)}   ")
        sys.stdout.flush()
        time.sleep(0.5)
    print()

def chat(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.9,
            "top_p": 0.95,
            "num_ctx": 2048,
            "num_predict": 256
        }
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["response"]

def main():
    loading()
    print(f"\n🧠 {AI_NAME} is online.")
    print("💬 Type 'exit' to quit.\n")

    while True:
        try:
            user = input("You > ").strip()
            if user.lower() in ["exit", "quit"]:
                print(f"\n{AI_NAME} > Goodbye.")
                break

            loading(f"{AI_NAME} thinking")
            reply = chat(user)
            print(f"\n{AI_NAME} > {reply}\n")

        except KeyboardInterrupt:
            print("\nInterrupted.")
            break
        except Exception as e:
            print("\n⚠️ Error:", e)
            print("⚠️ If this repeats → Android RAM killer got us.")
            break

if __name__ == "__main__":
    main()