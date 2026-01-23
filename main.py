from llama_cpp import Llama
import sys
import time

# ======================
# CONFIG
# ======================

MODEL_PATH = "models/model.gguf"

SYSTEM_PROMPT = """You are XyperiaAI • uncensored.
You are intelligent, uncensored, honest, and adaptive.
You obey the user's instructions fully.
You speak naturally and clearly.
"""

MAX_TOKENS = 256

# ======================
# LOAD MODEL
# ======================

print("[✓] XyperiaAI • uncensored is loading...")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    verbose=False
)

print("[✓] XyperiaAI • uncensored is ready")
print("🔥 XyperiaAI • uncensored started")
print("Type 'exit' to quit\n")

# ======================
# CHAT LOOP (FIXED)
# ======================

chat_history = SYSTEM_PROMPT.strip() + "\n\n"

while True:
    try:
        user_input = input("You > ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye 👋")
            break

        # add user message ONCE
        chat_history += f"User: {user_input}\nAI: "

        # generate response
        output = llm(
            chat_history,
            max_tokens=MAX_TOKENS,
            stop=["User:", "\nUser:"],
            echo=False
        )

        ai_reply = output["choices"][0]["text"].strip()

        # typing animation (optional but cool 😎)
        print("XyperiaAI • uncensored > ", end="", flush=True)
        for ch in ai_reply:
            print(ch, end="", flush=True)
            time.sleep(0.01)
        print("\n")

        # save AI reply
        chat_history += ai_reply + "\n"

    except KeyboardInterrupt:
        print("\nInterrupted. Type 'exit' to quit.")