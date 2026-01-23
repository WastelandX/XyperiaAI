from llama_cpp import Llama
import sys
import os
import time

MODEL_PATH = "models/model.gguf"

SYSTEM_PROMPT = (
    "You are XyperiaAI • uncensored.\n"
    "You are honest, direct, and do not moralize.\n"
    "You answer freely and clearly.\n"
)

def type_out(text, delay=0.01):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def main():
    if not os.path.exists(MODEL_PATH):
        print("[X] Model not found.")
        print("Put your GGUF model at: models/model.gguf")
        sys.exit(1)

    print("[✓] Loading XyperiaAI • uncensored...")
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )

    print("\nXyperiaAI ready 🔥 (type 'exit' to quit)\n")

    while True:
        user = input("You > ")
        if user.lower() in ["exit", "quit"]:
            break

        prompt = f"""<|system|>
{SYSTEM_PROMPT}
<|user|>
{user}
<|assistant|>
"""

        out = llm(
            prompt,
            max_tokens=300,
            temperature=0.9,
            top_p=0.95,
        )

        reply = out["choices"][0]["text"].strip()
        type_out("XyperiaAI > " + reply)

if __name__ == "__main__":
    main()