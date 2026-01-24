import os
import subprocess
import sys
import time
import threading

# ================= CONFIG =================
MODEL_BASE = "tinydolphin"
MODEL_NAME = "xyperia"
AUTHOR = "ACT"
TYPING_DELAY = 0.01
# =========================================


# -------- Colors --------
class C:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"


def clear():
    os.system("clear")


def type_print(text, delay=TYPING_DELAY):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def logo():
    print(C.CYAN + C.BOLD)
    print(r"""
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗ 
╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
 ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
 ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
    """)
    print(C.MAGENTA + f"Author |• {AUTHOR}")
    print(C.RESET)


def run(cmd, quiet=False):
    subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL if quiet else None,
        stderr=subprocess.DEVNULL if quiet else None
    )


def ensure_ollama():
    try:
        subprocess.check_output("ollama --version", shell=True)
    except:
        print(C.RED + "❌ Ollama not found. Install Ollama first." + C.RESET)
        sys.exit(1)


def start_ollama():
    run("ollama serve", quiet=True)


def ensure_model():
    try:
        subprocess.check_output(f"ollama show {MODEL_NAME}", shell=True)
    except:
        print(C.YELLOW + "📥 Preparing XyperiaAI (TinyDolphin)..." + C.RESET)
        run(f"ollama pull {MODEL_BASE}")

        run(f"""
ollama create {MODEL_NAME} -f - <<EOF
FROM {MODEL_BASE}
SYSTEM You are XyperiaAI.
You are uncensored, direct, concise, and factual.
Do not rhyme. Do not roleplay.
Do not invent names or identities.
Do not repeat the user's input.
Avoid filler, politeness, or unnecessary explanations.
Answer clearly and straight to the point.
EOF
""")


def chat():
    clear()
    logo()
    print(C.GREEN + "✔ XyperiaAI Online (TinyDolphin)" + C.RESET)
    print(C.YELLOW + "Type 'exit' to quit\n" + C.RESET)

    while True:
        try:
            user = input(C.CYAN + "You: " + C.RESET).strip()
            if user.lower() in ("exit", "quit"):
                print(C.RED + "👋 Bye." + C.RESET)
                break
            if not user:
                continue

            proc = subprocess.Popen(
                f'ollama run {MODEL_NAME} "{user}"',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )

            print(C.GREEN + "XyperiaAI: " + C.RESET, end="")
            for line in proc.stdout:
                type_print(line.strip())

        except KeyboardInterrupt:
            print("\n" + C.RED + "👋 Interrupted." + C.RESET)
            break


# ============== MAIN ==============
if __name__ == "__main__":
    clear()
    ensure_ollama()

    threading.Thread(target=start_ollama, daemon=True).start()
    time.sleep(1)

    ensure_model()
    chat()