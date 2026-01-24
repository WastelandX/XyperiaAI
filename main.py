import subprocess
import sys
import time
import os
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

AI_NAME = "XyperiaAI"
MODEL = "tinydolphin"

SYSTEM_PROMPT = """You are XyperiaAI.

Rules:
- Respond ONLY to the user's request.
- NEVER simulate the user.
- NEVER continue the conversation by yourself.
- NEVER ask follow-up questions unless explicitly asked.
- NO roleplay, NO marketing, NO filler.
- Be concise and technical.
- If code is requested, output clean working code.
- STOP immediately after completing the answer.
- Do NOT include labels like User:, Assistant:, or XyperiaAI:.
"""

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    clear()
    print(Fore.RED + pyfiglet.figlet_format("XYPERIA"))
    print(Fore.RED + "STATUS: ONLINE")
    print(Fore.RED + f"AI: {AI_NAME}")
    print(Fore.RED + "Type 'exit' to quit\n")

def thinking_animation(stop_flag):
    anim = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    i = 0
    while not stop_flag[0]:
        print(Fore.RED + f"\r{AI_NAME} thinking {anim[i % len(anim)]}", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print("\r" + " " * 40 + "\r", end="")

def run_model(user_input):
    prompt = f"""{SYSTEM_PROMPT}

Request:
{user_input}
"""

    proc = subprocess.Popen(
        ["ollama", "run", MODEL],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1
    )

    proc.stdin.write(prompt)
    proc.stdin.close()

    stop_flag = [False]
    import threading
    t = threading.Thread(target=thinking_animation, args=(stop_flag,))
    t.start()

    print(Fore.RED + f"{AI_NAME} ▶ ", end="", flush=True)

    for line in proc.stdout:
        line = line.rstrip()

        # hard stop self-reply / role hallucination
        if line.startswith(("User:", "You >", "Assistant:", "XyperiaAI >")):
            break

        if line:
            stop_flag[0] = True
            print(line, flush=True)

    stop_flag[0] = True
    t.join()
    print()

def main():
    banner()

    while True:
        try:
            user = input(Fore.RED + "You ▶ ").strip()
        except EOFError:
            continue

        if user.lower() in ("exit", "quit"):
            print(Fore.RED + "\nXyperiaAI offline.")
            break

        if not user:
            continue

        run_model(user)

if __name__ == "__main__":
    main()