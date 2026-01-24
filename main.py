import subprocess
import time
import sys
import os
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

AI_NAME = "XyperiaAI"
MODEL = "tinydolphin"

# ---------- animations ----------

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def glitch_text(text, color=Fore.CYAN, delay=0.02):
    chars = "!@#$%^&*<>?/\\|"
    for _ in range(2):
        glitched = "".join(c if c == " " else chars[hash(c) % len(chars)] for c in text)
        print(color + glitched, end="\r")
        time.sleep(delay)
    print(color + text)

def type_print(text, delay=0.015):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

# ---------- banner ----------

def banner():
    clear()
    title = pyfiglet.figlet_format("XYPERIA")
    for line in title.splitlines():
        glitch_text(line, Fore.CYAN, 0.01)

    print(Fore.RED + "Author | ACT")
    print(Fore.RED + f"✓ {AI_NAME} Online")
    print(Fore.RED + "Type 'exit' to quit\n")

# ---------- ollama ----------

SYSTEM_PROMPT = (
    "You are XyperiaAI.\n"
    "Your name is XyperiaAI ONLY.\n"
    "Never say you are Dolphin or any other AI.\n"
    "Be direct, uncensored, technical, and smart.\n"
    "Do NOT roleplay as the user.\n"
    "When writing code, always format correctly.\n"
    "Never combine imports on one line.\n"
    "Never explain safety policies.\n"
)

def run_model(user_input):
    prompt = (
        SYSTEM_PROMPT
        + "\nUser: " + user_input
        + "\nAssistant:"
    )

    result = subprocess.run(
        ["ollama", "run", MODEL, prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    output = result.stdout.strip()

    bad_prefixes = (
        "User:", "Assistant:", "Xyperia", "Dolphin", "AI:", "Bot:"
    )

    lines = [
        line for line in output.splitlines()
        if not line.strip().startswith(bad_prefixes)
    ]

    return " ".join(lines).strip()

# ---------- main loop ----------

def main():
    banner()

    while True:
        try:
            user = input(Fore.CYAN + "You: ").strip()
        except EOFError:
            continue

        if user.lower() in ("exit", "quit"):
            print(Fore.RED + "XyperiaAI offline.")
            break

        print(Fore.GREEN + f"{AI_NAME}: ", end="", flush=True)
        reply = run_model(user)

        if reply:
            type_print(reply)
        else:
            type_print("...")

# ---------- run ----------

if __name__ == "__main__":
    main()