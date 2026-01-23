import os
import sys
import urllib.request

MODEL_DIR = "models"
MODEL_NAME = "model.gguf"

MODEL_URL = (
    "https://huggingface.co/TheBloke/dolphin-phi-2-GGUF/resolve/main/"
    "dolphin-phi-2.Q4_K_M.gguf"
)

MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)
MIN_SIZE_MB = 300  # sanity check

def mb(size):
    return size / (1024 * 1024)

def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(MODEL_PATH):
        size = mb(os.path.getsize(MODEL_PATH))
        if size > MIN_SIZE_MB:
            print(f"[✓] Model already exists ({size:.1f} MB)")
            return
        else:
            print("[!] Corrupted model found, re-downloading…")
            os.remove(MODEL_PATH)

    print("[↓] Downloading model (this may take time)...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

    size = mb(os.path.getsize(MODEL_PATH))
    if size < MIN_SIZE_MB:
        print("[✗] Download failed (file too small)")
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

    print("\n🔥 XyperiaAI (uncensored-ish) ready")
    print("Type 'exit' to quit\n")

    while True:
        user = input("You > ").strip()
        if user.lower() in ("exit", "quit"):
            break

        output = llm(
            user,
            max_tokens=256,
            stop=["You >"],
        )

        print("AI >", output["choices"][0]["text"].strip())


if __name__ == "__main__":
    download_model()
    run_ai()