import os
import sys
import requests
from llama_cpp import Llama
from colorama import Fore, Style, init

init(autoreset=True)

AI_NAME = "XyperiaAI"

MODEL_NAME = "gemma-3-1b-it-heretic-extreme-uncensored-abliterated.Q4_K_S.gguf"
MODEL_URL = "https://huggingface.co/TheBloke/gemma-3-1b-it-Heretic-Extreme-GGUF/resolve/main/" + MODEL_NAME
MODEL_PATH = os.path.join(os.getcwd(), MODEL_NAME)


def download_model():
    print(Fore.YELLOW + "⚠ Model not found.")
    print(Fore.CYAN + "⬇ Downloading Gemma 3 1B (Q4, uncensored)...\n")

    with requests.get(MODEL_URL, stream=True) as r:
        r.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(Fore.GREEN + "✓ Model downloaded successfully!\n")


# ---------- CHECK MODEL ----------
if not os.path.exists(MODEL_PATH):
    download_model()


# ---------- UI ----------
print(Fore.CYAN + r"""
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗
╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
 ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
 ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
""")

print(Fore.GREEN + "✓ XyperiaAI Online")
print("Type 'exit' to quit\n")


# ---------- LOAD MODEL ----------
try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=1024,
        n_threads=4,
        n_batch=64,
        use_mmap=True,
        use_mlock=False
    )
except Exception as e:
    print(Fore.RED + "Model failed to load.")
    print(e)
    sys.exit(1)


# ---------- CHAT LOOP ----------
while True:
    user = input(Fore.YELLOW + "You: ").strip()
    if user.lower() == "exit":
        break

    prompt = f"<start_of_turn>user\n{user}<end_of_turn>\n<start_of_turn>model\n"

    try:
        output = llm(
            prompt,
            max_tokens=256,
            temperature=0.9,
            top_p=0.95,
            stop=["<end_of_turn>"]
        )

        reply = output["choices"][0]["text"].strip()
        print(Fore.CYAN + f"{AI_NAME}: " + Style.RESET_ALL + reply)

    except Exception as e:
        print(Fore.RED + "⚠ Error during generation (RAM limit hit)")