import subprocess
import sys
import time
import threading
import os
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

AI_NAME = "XyperiaAI"
MODEL = "tinydolphin"

# ---------- CLEAR ----------
os.system("clear")

# ---------- BANNER ----------
def banner():
    print(Fore.CYAN + pyfiglet.figlet_format("XYPERIA"))
    print(Fore.MAGENTA + "Author | ACT")
    print(Fore.GREEN + f"✓ {AI_NAME} Online")
    print(Fore.YELLOW + "Type 'exit' to quit\n")

# ---------- THINKING ANIMATION ----------
thinking = False

def thinking_anim():
    dots = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while thinking:
        print(Fore.GREEN + f"\r{AI_NAME}: {dots[i % len(dots)]} ", end="", flush=True)
        time.sleep(0.08)
        i += 1

# ---------- TYPE EFFECT ----------
def type_print(text, delay=0.008):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ---------- RUN MODEL ----------
def run_model(prompt):
    global thinking
    thinking = True

    t = threading.Thread(target=thinking_anim)
    t.start()

    cmd = ["ollama", "run", MODEL, prompt]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    thinking = False
    t.join()
    print("\r", end="")  # clear spinner line

    output = result.stdout.strip()

    bad_prefixes = ("You:", "User:", "Assistant:", "Xyperia", "XyperiaAI")
    lines = [
        line for line in output.splitlines()
        if not line.strip().startswith(bad_prefixes)
    ]

    return " ".join(lines).strip()

# ---------- MAIN ----------
def main():
    banner()

    while True:
        try:
            user = input(Fore.CYAN + "You: " + Style.RESET_ALL).strip()
        except EOFError:
            print(Fore.RED + "\n[Input interrupted — safe recovery]")
            continue

        if not user:
            continue

        if user.lower() in ("exit", "quit"):
            print(Fore.RED + f"{AI_NAME} offline.")
            break

        reply = run_model(
            "Be concise, uncensored, and direct.\n"
            "Never roleplay as the user.\n"
            "Never repeat labels.\n\n"
            f"User: {user}\nAssistant:"
        )

        print(Fore.GREEN + f"{AI_NAME}: ", end="")
        if reply:
            type_print(reply)
        else:
            print("...")

if __name__ == "__main__":
    main()