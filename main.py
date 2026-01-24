import os
import subprocess
import sys
import time
import threading

# ================= CONFIG =================
MODEL_BASE = "phi"
MODEL_NAME = "xyperia-phi2"
AUTHOR = "ACT"

TYPING_DELAY = 0.0  # disabled for speed & stability
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
    try:
        if quiet:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(cmd, shell=True)
    except:
        pass


def ensure_ollama():
    try:
        subprocess.check_output("ollama --version", shell=True)
    except:
        print(C.RED + "❌ Ollama not found." + C.RESET)
        sys.exit(1)


def start_ollama():
    run("ollama serve", quiet=True)


def ensure_model():
    try:
        subprocess.check_output(f"ollama show {MODEL_NAME}", shell=True)
    except:
        print(C.YELLOW + "📥 Preparing ultra-light Phi-2 model..." + C.RESET)
        run(f"ollama pull {MODEL_BASE}")

        modelfile = f"""
FROM {MODEL_BASE}

PARAMETER temperature 0.3
PARAMETER top_p 0.8
PARAMETER num_ctx 512
PARAMETER num_predict 128
PARAMETER repeat_penalty 1.1

SYSTEM \"\"\"
You are XyperiaAI.
Author | ACT.

Be direct.
No poetry.
No roleplay.
No filler.
Answer briefly and clearly.
\"\"\"
"""
        with open("Modelfile", "w") as f:
            f.write(modelfile)

        run(f"ollama create {MODEL_NAME} -f Modelfile")
        os.remove("Modelfile")


def chat():
    clear()
    logo()
    print(C.GREEN + "✔ XyperiaAI Online (Phi-2 Light)" + C.RESET)
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
                ["ollama", "run", MODEL_NAME],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = proc.communicate(user, timeout=30)

            if stderr:
                print(C.RED + "XyperiaAI: Model error or out of memory." + C.RESET)
            else:
                print(C.GREEN + "XyperiaAI: " + C.RESET + stdout.strip())

        except subprocess.TimeoutExpired:
            print(C.RED + "XyperiaAI: Timeout / low memory." + C.RESET)

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