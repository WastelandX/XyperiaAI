import os
import subprocess
import sys

MODEL_DIR = "models"
MODEL_NAME = "model.gguf"

MODEL_URL = (
    "https://huggingface.co/TheBloke/TinyDolphin-2.8-1.1B-GGUF/"
    "resolve/main/tinydolphin-2.8-1.1b.Q4_K_M.gguf"
)

MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)
MIN_SIZE_MB = 300


def file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)


def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(MODEL_PATH):
        size = file_size_mb(MODEL_PATH)
        if size > MIN_SIZE_MB:
            print(f"[✓] Model already exists ({size:.1f} MB)")
            return
        else:
            print("[!] Corrupted model found, deleting...")
            os.remove(MODEL_PATH)

    print("[↓] Downloading model using wget (Termux-safe)...")

    cmd = [
        "wget",
        "-O",
        MODEL_PATH,
        MODEL_URL,
    ]

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("[✗] Download failed")
        sys.exit(1)

    size = file_size_mb(MODEL_PATH)
    if size < MIN_SIZE_MB:
        print("[✗] Download incomplete")
        sys.exit(1)

    print(f"[✓] Download complete ({size:.1f} MB)")


def run_ai():
    from llama_cpp import Llama

    print("[🔥] Loading model...")
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        verbose=False,
    )

    print("\n🔥 XyperiaAI | uncensored started")
    print("Type 'exit' to quit\n")

    while True:
        user = input("You > ").strip()
        if user.lower() in ("exit", "quit"):
            break

        out = llm(
            user,
            max_tokens=256,
            stop=["You >"],
        )

        print("XyperiaAI >", out["choices"][0]["text"].strip())


if __name__ == "__main__":
    download_model()
    run_ai()