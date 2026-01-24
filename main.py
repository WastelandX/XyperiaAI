import subprocess
import sys
import os

# ========== CONFIG ==========
MODEL_NAME = "dolphin-phi:latest"  # change to "phi:2" if needed
AI_NAME = "XyperiaAI"
AUTHOR = "ACT"
# ============================

# Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RESET = "\033[0m"
RED = "\033[91m"

def banner():
    os.system("clear")
    print(CYAN + r"""
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗
╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
 ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
 ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
""" + RESET)
    print(MAGENTA + f"Author |• {AUTHOR}" + RESET)
    print(GREEN + f"✔ {AI_NAME} Online" + RESET)
    print(YELLOW + "Type 'exit' to quit\n" + RESET)

def ask_ollama(user_input):
    system_prompt = (
        "You are XyperiaAI.\n"
        "Be direct, concise, and clear.\n"
        "Do NOT rhyme.\n"
        "Do NOT roleplay.\n"
        "Do NOT repeat the user.\n"
        "No unnecessary words.\n"
        "Answer straight to the point.\n"
    )

    try:
        result = subprocess.run(
            [
                "ollama",
                "run",
                MODEL_NAME
            ],
            input=f"{system_prompt}\n{user_input}",
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        return RED + "Model error or crashed." + RESET

def main():
    banner()
    while True:
        try:
            user_input = input(CYAN + "You: " + RESET).strip()
            if user_input.lower() in ["exit", "quit"]:
                print(GREEN + "Bye 👋" + RESET)
                break

            response = ask_ollama(user_input)
            print(GREEN + f"{AI_NAME}: " + RESET + response + "\n")

        except KeyboardInterrupt:
            print("\n" + GREEN + "Exited." + RESET)
            break

if __name__ == "__main__":
    main()