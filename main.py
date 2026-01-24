import requests
import time
import sys
from colorama import Fore, Style, init

init(autoreset=True)

AI_NAME = "Xyperia"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def type_print(text, delay=0.015):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗
╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
 ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
 ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
""")
    print(Fore.MAGENTA + "Author |• ACT")
    print(Fore.GREEN + "✔ Xyperia Online\n")

def main():
    banner()
    api_key = input(Fore.YELLOW + "Enter OpenRouter API key: ").strip()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "You are XyperiaAI. Be direct, concise, intelligent, and honest. "
        "Avoid unnecessary filler, rhyming, roleplay, or self-talk. "
        "Answer clearly and efficiently."
    )

    print(Fore.YELLOW + "Type 'exit' to quit.\n")

    while True:
        user = input(Fore.CYAN + "You: " + Style.RESET_ALL).strip()
        if user.lower() in ("exit", "quit"):
            print(Fore.RED + "👋 Bye.")
            break
        if not user:
            continue

        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user}
            ],
            "temperature": 0.9,
            "top_p": 0.95,
            "max_tokens": 300
        }

        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            reply = r.json()["choices"][0]["message"]["content"]

            print(Fore.GREEN + f"{AI_NAME}: ", end="")
            type_print(reply.strip())

        except Exception as e:
            print(Fore.RED + f"⚠ Error: {e}")
            break

if __name__ == "__main__":
    main()