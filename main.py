import os
import sys
import subprocess
from llama_cpp import Llama

MODEL_URL = (
    "https://huggingface.co/TheBloke/TinyDolphin-2.8-1.1B-GGUF/"
    "resolve/main/tinydolphin-2.8-1.1b.Q4_K_M.gguf"
)
MODEL_PATH = "models/model.gguf"

SYSTEM_PROMPT = (
    "You are XyperiaAI• uncensored. "
    "You speak freely, honestly, and without unnecessary refusal. "
    "You are helpful, direct, and not preachy."
)

def download_model():
    if os.path.exists(MODEL_PATH):
        print("[✓] Model already exists")
        return

    print("[↓] Downloading model (~480MB)...")
    print("    This may take time. Be patient.")

    cmd = [
        "wget",
        "--continue",
        "--header=User-Agent: Mozilla/5.0",
        "--header=Accept: */*",
        "-O", MODEL_PATH,
        MODEL_URL
    ]

    try:
        subprocess.run(cmd, check=True)
        print("[✓] Download complete")
    except subprocess.CalledProcessError:
        print("[✗] Download failed")
        print("Check internet or storage")
        sys.exit(1)

def animated_print(text, delay=0.01):
    for c in text:
        print(c, end="", flush=True)
        import time
        time.sleep(delay)
    print()

def main():
    download_model()

    print("[*] Loading model...")
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )

    print("\nXyperiaAI• uncensored ready 🔥")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You > ")
        if user_input.lower() in ["exit", "quit"]:
            break

        prompt = f"""<|system|>
{SYSTEM_PROMPT}
<|user|>
{user_input}
<|assistant|>
"""

        output = llm(
            prompt,
            max_tokens=300,
            temperature=0.9,
            top_p=0.95,
            stop=["<|user|>"]
        )

        text = output["choices"][0]["text"]
        animated_print(f"XyperiaAI > {text}")

if __name__ == "__main__":
    main()