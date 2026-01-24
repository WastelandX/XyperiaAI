import subprocess
import os

MODEL = "phi:2"
AI_NAME = "XyperiaAI"
AUTHOR = "ACT"

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

def run_phi(prompt):
    try:
        p = subprocess.Popen(
            ["ollama", "run", MODEL],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # VERY SMALL PROMPT → prevents crash
        clean_prompt = (
            "Answer briefly and directly.\n"
            "No poetry. No roleplay.\n"
            f"User: {prompt}\n"
            f"{AI_NAME}:"
        )

        out, err = p.communicate(clean_prompt, timeout=30)

        if err.strip():
            return RED + "Model error or out of memory." + RESET

        return out.strip()

    except subprocess.TimeoutExpired:
        p.kill()
        return RED + "Model timed out." + RESET

    except Exception as e:
        return RED + "Crash occurred." + RESET

def main():
    banner()
    while True:
        try:
            user = input(CYAN + "You: " + RESET).strip()
            if user.lower() in ["exit", "quit"]:
                print(GREEN + "Bye 👋" + RESET)
                break

            reply = run_phi(user)
            print(GREEN + f"{AI_NAME}: " + RESET + reply + "\n")

        except KeyboardInterrupt:
            print("\n" + GREEN + "Exited." + RESET)
            break

if __name__ == "__main__":
    main()