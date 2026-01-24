import os
import subprocess
import time
import requests
from colorama import Fore, Style, init

init(autoreset=True)

MODEL_BASE = "tinydolphin"
MODEL_NAME = "xyperia"
AUTHOR = "ACT"
OLLAMA_URL = "http://127.0.0.1:11434"

# ---------- UTIL ----------

def run(cmd):
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def ollama_running():
    try:
        requests.get(OLLAMA_URL, timeout=1)
        return True
    except:
        return False

# ---------- START OLLAMA ----------

def start_ollama():
    if ollama_running():
        print(Fore.GREEN + "✔ Ollama is running.")
        return

    print(Fore.YELLOW + "⚡ Starting Ollama server...")
    subprocess.Popen(["ollama", "serve"],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    time.sleep(5)

# ---------- MODEL SETUP ----------

def model_exists():
    r = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    return MODEL_NAME in r.stdout

def setup_model():
    if model_exists():
        print(Fore.GREEN + "✔ XyperiaAI model already exists.")
        return

    print(Fore.CYAN + f"⬇ Downloading base model ({MODEL_BASE}) if needed...")
    subprocess.run(["ollama", "pull", MODEL_BASE])

    print(Fore.MAGENTA + "🧠 Creating XyperiaAI model...")

    modelfile = f"""
FROM {MODEL_BASE}

PARAMETER temperature 0.6
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.15
PARAMETER num_ctx 2048

SYSTEM \"\"\"
You are XyperiaAI.

You are concise, intelligent, and stable.
You do not invent identities, names, or personalities.
You never roleplay unless asked.
You do not talk to yourself.
You avoid unnecessary verbosity.

Answer directly and honestly.
Keep replies short unless depth is required.

Author: ACT
\"\"\"
"""

    with open("Modelfile", "w") as f:
        f.write(modelfile.strip())

    subprocess.run(["ollama", "create", MODEL_NAME, "-f", "Modelfile"])
    os.remove("Modelfile")

    print(Fore.GREEN + "✔ XyperiaAI is ready.")

# ---------- CHAT ----------

def chat():
    print(Fore.CYAN + "\n🧠 XyperiaAI Online")
    print(Fore.MAGENTA + f"✍ Author |• {AUTHOR}")
    print(Fore.YELLOW + "Type 'exit' to quit\n")

    while True:
        user = input(Fore.GREEN + "You: ").strip()
        if user.lower() == "exit":
            print(Fore.RED + "👋 Goodbye.")
            break

        try:
            r = subprocess.run(
                ["ollama", "run", MODEL_NAME, user],
                capture_output=True,
                text=True,
                timeout=60
            )
            print(Fore.CYAN + "XyperiaAI:", r.stdout.strip())
        except subprocess.TimeoutExpired:
            print(Fore.RED + "⚠ Took too long. Try a shorter prompt.")

# ---------- MAIN ----------

if __name__ == "__main__":
    # Phone-safe limits
    os.environ["OLLAMA_NUM_THREADS"] = "4"
    os.environ["OLLAMA_MAX_LOADED_MODELS"] = "1"
    os.environ["OLLAMA_KEEP_ALIVE"] = "0"

    start_ollama()
    setup_model()
    chat()