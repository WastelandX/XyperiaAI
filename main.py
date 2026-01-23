import os
import sys
import requests
from llama_cpp import Llama

# ================= CONFIG =================

AI_NAME = "XpreaAI | uncensored edition. Fine tuned llma model.   Made by Act"

MODEL_URL = (
    "https://huggingface.co/unsloth/gemma-3-270m-it-GGUF/"
    "resolve/main/gemma-3-270m-it-Q4_0.gguf"
)

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "gemma-3-270m-it-Q4_0.gguf")

# ==========================================


def download_model():
    if os.path.exists(MODEL_PATH):
        return

    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"{AI_NAME} is downloading required files...\n")

    with requests.get(MODEL_URL, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0

        with open(MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total) * 100
                    print(f"\rDownloading: {percent:.1f}%", end="")

    print("\nDownload complete.\n")


def load_model():
    print(f"{AI_NAME} is initializing...\n")
    return Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        verbose=False,
    )


def chat_loop(llm):
    print(f"{AI_NAME} is online.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("\nGoodbye.")
                break

            prompt = f"User: {user_input}\nAssistant:"

            output = llm(
                prompt,
                max_tokens=256,
                temperature=0.9,
                top_p=0.95,
                stop=["User:"],
            )

            response = output["choices"][0]["text"].strip()
            print(f"{AI_NAME}: {response}\n")

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break


def main():
    download_model()
    llm = load_model()
    chat_loop(llm)


if __name__ == "__main__":
    main()