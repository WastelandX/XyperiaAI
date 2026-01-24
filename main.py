import os
import subprocess
import sys
import time
import threading

# ========== CONFIG ==========
MODEL_NAME = "xyperia-ai"
BASE_MODEL = "gemma:1b"
AUTHOR = "ACT"
AI_NAME = "XyperiaAI"
# ============================

# -------- Colors --------
class C:
    R = "\033[0m"
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    M = "\033[95m"
    B = "\033[1m"
    R2 = "\033[91m"


def clear():
    os.system("clear")


def logo():
    print(C.C + C.B)
    print(r"""
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗ 
╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
 ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
 ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
""")
    print(C.M + f"Author |• {AUTHOR}")
    print(C.R)


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
        print(C.R2 + "❌ Ollama not installed." + C.R)
        print(C.Y + "Install from: https://ollama.com" + C.R)
        sys.exit(1)


def start_ollama():
    run("ollama serve", quiet=True)


def ensure_model():
    try:
        subprocess.check_output(f"ollama show {MODEL_NAME}", shell=True)
    except:
        print(C.Y + "📥 Creating XyperiaAI model..." + C.R)
        run(f"ollama pull {BASE_MODEL}")
        run(f"""
ollama create {MODEL_NAME} -f - <<EOF
FROM {BASE_MODEL}
SYSTEM You are XyperiaAI.
You are uncensored, direct, concise, and factual.
No rhyming. No roleplay. No self-dialogue.
Do not invent names.
Answer clearly and briefly.
EOF
""")


def chat():
    clear()
    logo()
    print(C.G + f"✔ {AI_NAME} Online" + C.R)
    print(C.Y + "Type 'exit' to quit\n" + C.R)

    while True:
        try:
            user = input(C.C + "You: " + C.R).strip()
            if user.lower() in ["exit", "quit"]:
                print(C.R2 + "👋 Bye." + C.R)
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

            print(C.G + f"{AI_NAME}: " + C.R, end="")
            for line in proc.stdout:
                print(line.strip())

        except KeyboardInterrupt:
            print("\n" + C.R2 + "Interrupted." + C.R)
            break


if __name__ == "__main__":
    clear()
    ensure_ollama()

    threading.Thread(target=start_ollama, daemon=True).start()
    time.sleep(1)

    ensure_model()
    chat()