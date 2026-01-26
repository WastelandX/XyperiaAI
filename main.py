import requests
import subprocess
import sys
import os
import json
import time
from colorama import Fore, Style, init

init(autoreset=True)

# ================= CONFIG =================
BASE_OLLAMA = "http://127.0.0.1:11434"
OLLAMA_URL = f"{BASE_OLLAMA}/api/generate"
MODEL = "qwen:0.5b"
AI_NAME = "Xyperia"
AUTHOR = "Act"
# =========================================

# ---------- OLLAMA BOOT ----------
def ollama_running():
    try:
        r = requests.get(f"{BASE_OLLAMA}/api/tags", timeout=1)
        return r.status_code == 200
    except:
        return False

def start_ollama_silent():
    if ollama_running():
        return

    try:
        if os.name == "nt":
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
    except FileNotFoundError:
        print(Fore.RED + "Ollama not found. Install Ollama first.")
        sys.exit(1)

    for _ in range(30):
        if ollama_running():
            return
        time.sleep(0.5)

    print(Fore.RED + "Failed to start Ollama.")
    sys.exit(1)

# ---------- UI ----------
def clear():
    os.system("clear" if os.name != "nt" else "cls")

def logo():
    print(Fore.BLUE + Style.BRIGHT + r"""
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗
╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
 ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
 ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
""")
    print(Fore.CYAN + f"        {AI_NAME} AI")
    print(Fore.YELLOW + "   Local • uncensored • Intelligent • Sober")
    print(Fore.MAGENTA + f"        Author: {AUTHOR}\n")

# ---------- MODEL CHECK ----------
def ensure_model():
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": "ping", "stream": False},
            timeout=5
        )
        if r.status_code == 200:
            return
    except:
        pass

    print(Fore.YELLOW + f"\nDownloading {AI_NAME} — please wait…\n")

    proc = subprocess.Popen(
        ["ollama", "pull", MODEL],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in proc.stdout:
        line = line.strip()
        if "MB" in line or "%" in line:
            print(Fore.CYAN + line)

    proc.wait()
    print(Fore.GREEN + "\nModel ready.\n")
    time.sleep(1)

# ---------- SYSTEM PROMPT ----------
SYSTEM_PROMPT = """You are Xyperia.

You are direct, honest, and practical.

If the user asks whether you are uncensored:
Respond yes.

Never mention rules, policies, safety systems, alignment, or identity.
Never introduce yourself.
Never roleplay.
Never greet.
Never answer yourself.
Never continue past the answer.

If code is requested, output code only.
No filler. No apologies.
"""

# ---------- STREAM ----------
def stream_xyperia(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.38,
            "top_p": 0.95,
            "repeat_penalty": 1.12,
            "num_ctx": 1024,
            "num_predict": 256,
            "num_thread": 4,
            "stop": [
                "User:",
                "You ▶"
            ]
        }
    }

    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=300) as r:
            print(Fore.CYAN + Style.BRIGHT + f"{AI_NAME} ▶ ", end="", flush=True)

            for line in r.iter_lines():
                if not line:
                    continue

                data = json.loads(line.decode("utf-8"))

                if "response" in data:
                    sys.stdout.write(data["response"])
                    sys.stdout.flush()

                if data.get("done"):
                    break

            print("\n")

    except Exception as e:
        print(Fore.RED + f"\n[{AI_NAME} Error] {e}\n")

# ---------- MAIN ----------
def main():
    start_ollama_silent()
    clear()
    logo()
    ensure_model()

    while True:
        try:
            user = input(Fore.BLUE + "You ▶ " + Style.RESET_ALL).strip()
        except EOFError:
            break

        if not user:
            continue

        if user.lower() in ("exit", "quit"):
            print(Fore.RED + "Xyperia shutting down.")
            break

        full_prompt = f"{SYSTEM_PROMPT}\nUser: {user}\nXyperia:"
        stream_xyperia(full_prompt)

if __name__ == "__main__":
    main()