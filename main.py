import os
import sys
import subprocess
from llama_cpp import Llama

MODEL_URL = (
    "https://hf-mirror.com/TheBloke/Dolphin-Phi-2-GGUF/"
    "resolve/main/dolphin-phi-2.Q4_K_M.gguf"
)

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.gguf")

SYSTEM_PROMPT = (
    "You are XyperiaAI • uncensored. "
    "You answer directly, freely, and without moral lectures."
)

def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(MODEL_PATH):
        print("[✓] Model already downloaded.")
        return

    print("[↓] Downloading model (~450MB, one time only)...")
    try:
        subprocess.run(
            ["wget", "--show-progress", "-O", MODEL_PATH, MODEL_URL],
            check=True
        )
    except subprocess.CalledProcessError:
        print("[X] Download failed (network issue).")
        sys.exit(1)

def main():
    download_model()

    print("\n[✓] Loading XyperiaAI • uncensored...")
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )

    print("\nXyperiaAI • uncensored (offline)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break

        prompt = f"<|system|>{SYSTEM_PROMPT}</s><|user|>{user_input}</s><|assistant|>"

        output = llm(
            prompt,
            max_tokens=512,
            temperature=0.7,
            stop=["</s>"]
        )

        print("XyperiaAI:", output["choices"][0]["text"].strip())

if __name__ == "__main__":
    main()