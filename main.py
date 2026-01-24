import os, sys, time, requests
from llama_cpp import Llama
from colorama import Fore, Style, init

init(autoreset=True)

AI_NAME = "XyperiaAI"

MODEL_NAME = "gemma-3-1b-it-heretic-extreme-uncensored-abliterated.Q4_K_S.gguf"
MODEL_URL = (
    "https://huggingface.co/TheBloke/"
    "gemma-3-1b-it-Heretic-Extreme-GGUF/resolve/main/"
    + MODEL_NAME
)

# --------- typing animation ----------
def type_print(text, delay=0.012):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# --------- download ----------
def download_model():
    print(Fore.YELLOW + "🔒 This model requires a Hugging Face token.")
    token = input(Fore.CYAN + "Enter HF token: ").strip()

    headers = {"Authorization": f"Bearer {token}"}
    with requests.get(MODEL_URL, headers=headers, stream=True) as r:
        if r.status_code == 401:
            print(Fore.RED + "❌ Invalid token or no access to this model.")
            sys.exit(1)
        r.raise_for_status()
        with open(MODEL_NAME, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(Fore.GREEN + "✅ Model downloaded successfully.\n")

# --------- check ----------
if not os.path.exists(MODEL_NAME):
    print(Fore.YELLOW + "⚠ Model not found.")
    download_model()

# --------- banner ----------
print(Fore.CYAN + Style.BRIGHT + r"""
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗
╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
 ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
 ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
""")
print(Fore.GREEN + "✔ XyperiaAI Online")
print(Fore.YELLOW + "Type 'exit' to quit\n")

# --------- load model (LOW RAM, NOT DUMB) ----------
llm = Llama(
    model_path=MODEL_NAME,
    n_ctx=1024,          # keep memory low
    n_threads=4,
    n_batch=64,
    use_mmap=True,       # huge RAM saver
    use_mlock=False,     # android-safe
    f16_kv=True          # better memory efficiency
)

SYSTEM_PROMPT = (
    "You are XyperiaAI. Be direct, concise, and intelligent. "
    "Do not roleplay as a human. Do not invent names. "
    "Avoid unnecessary filler, rhyming, or self-talk. "
    "Answer clearly and honestly."
)

# --------- chat ----------
while True:
    user = input(Fore.CYAN + "You: " + Style.RESET_ALL).strip()
    if user.lower() in ("exit", "quit"):
        break
    if not user:
        continue

    prompt = f"{SYSTEM_PROMPT}\nUser: {user}\nAssistant:"

    try:
        out = llm(
            prompt,
            max_tokens=256,
            temperature=0.9,
            top_p=0.95,
            stop=["User:", "Assistant:"]
        )
        reply = out["choices"][0]["text"].strip()
        print(Fore.GREEN + f"{AI_NAME}: ", end="")
        type_print(reply)

    except Exception as e:
        print(Fore.RED + "⚠ Generation failed (RAM limit hit).")