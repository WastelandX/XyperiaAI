import os
import requests
from llama_cpp import Llama

MODEL_NAME = "gemma-3-270m-it-Q4_0.gguf"
MODEL_URL = "https://huggingface.co/unsloth/gemma-3-270m-it-GGUF/resolve/main/gemma-3-270m-it-Q4_0.gguf"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(MODEL_PATH):
        print("[✓] Model already exists")
        return

    print("[↓] Downloading model...")
    with requests.get(MODEL_URL, stream=True) as r:
        r.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    print("[✓] Download complete")

download_model()

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    n_batch=64,
)

while True:
    prompt = input("\nYou: ")
    if prompt.lower() in ("exit", "quit"):
        break

    out = llm(prompt, max_tokens=256)
    print("AI:", out["choices"][0]["text"])