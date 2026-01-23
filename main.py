import subprocess
import sys
import shutil

MODEL_NAME = "dolphin-phi"

def has_ollama():
    return shutil.which("ollama") is not None

def pull_model():
    print(f"[+] Downloading model: {MODEL_NAME}")
    subprocess.run(["ollama", "pull", MODEL_NAME], check=True)

def run_chat():
    print("\n🔥 Dolphin Phi (offline, uncensored-ish)")
    print("Type 'exit' to quit\n")

    while True:
        user = input("You: ")
        if user.lower() in ["exit", "quit"]:
            break

        subprocess.run(
            ["ollama", "run", MODEL_NAME],
            input=user,
            text=True
        )

def main():
    if not has_ollama():
        print("[X] Ollama not found.")
        print("Install it first: https://ollama.com")
        sys.exit(1)

    # Check if model exists
    models = subprocess.check_output(["ollama", "list"]).decode()
    if MODEL_NAME not in models:
        pull_model()

    run_chat()

if __name__ == "__main__":
    main()