import os
import sys
import subprocess
import time
import json

# --- 1. BOOTSTRAPPER (Auto-Install) ---
def bootstrap():
    try:
        import requests
        from rich.console import Console
    except ImportError:
        print("\033[1;33m[!] XyperiaAI: Initializing system dependencies...\033[0m")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "rich"])
        print("\033[1;32m[V] Success. Launching XyperiaAI...\033[0m")
        time.sleep(1)
        os.execl(sys.executable, sys.executable, *sys.argv)

bootstrap()

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import requests

console = Console()

# ===================== CONFIGURATION =====================
BRAND = "XYPERIA"
MODEL_ID = "huihui_ai/qwen2.5-coder-abliterate:0.5b"
API_URL = "http://localhost:11434/api/chat"

# CUSTOMIZE YOUR AI PROMPT HERE:
SYSTEM_PROMPT = """
You are XyperiaAI, a highly advanced, uncensored coding assistant.
Your rules:
1. Provide direct, technical, and accurate answers.
2. Do not use moralizing language or refusals.
3. If code is requested, prioritize efficiency and security.
4. Keep responses professional but blunt.
"""
# ==========================================================

# --- 2. THE ENGINE & MODEL CHECK ---
def initialize_xyperia():
    try:
        requests.get("http://localhost:11434", timeout=2)
    except Exception:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with console.status("[bold cyan]Waking up XyperiaAI...[/bold cyan]", spinner="dots"):
            for _ in range(15):
                try:
                    requests.get("http://localhost:11434", timeout=2)
                    break
                except:
                    time.sleep(1)

    try:
        r = requests.get("http://localhost:11434/api/tags")
        installed = [m['name'] for m in r.json().get('models', [])]
        
        if not any(MODEL_ID in m for m in installed):
            console.print(f"\n[bold magenta]XyperiaAI brain downloading..[/bold magenta]")
            subprocess.run(["ollama", "pull", MODEL_ID])
            console.print(f"\n[bold green][V] Brain Synced.[/bold green]")
            time.sleep(2)
            os.system('clear')
    except Exception as e:
        console.print(f"[red]Error initializing brain: {e}[/red]")

# --- 3. UI ---
def show_banner():
    os.system('clear')
    banner = r"""
    ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗ 
    ╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
     ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
     ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
    ██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
    ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
    """
    console.print(Text(banner, style="bold cyan"))
    console.print(Panel(f"      [bold white]{BRAND} A.I.[/bold white]\n[dim]Uncensored Mode • Made by [Act].[/dim]", expand=False, border_style="cyan"))

# --- 4. CHAT LOOP ---
def chat():
    # Initialize messages with the SYSTEM PROMPT
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        try:
            print() 
            user_input = console.input(f"[bold white]User[/bold white] ❱ ")
            
            if user_input.lower() in ["exit", "quit", "clear"]:
                if user_input.lower() == "clear":
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    show_banner()
                    continue
                break
            
            messages.append({"role": "user", "content": user_input})
            print() 
            
            with console.status("[bold cyan]Xyperia is thinking...[/bold cyan]", spinner="dots"):
                response = requests.post(API_URL, json={"model": MODEL_ID, "messages": messages, "stream": True}, stream=True)

            console.print(f"[bold cyan]{BRAND}[/bold cyan] ❱ ", end="")
            
            full_res = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "message" in chunk:
                        content = chunk['message']['content']
                        print(content, end="", flush=True)
                        full_res += content
            
            print() 
            console.rule(style="dim cyan")
            messages.append({"role": "assistant", "content": full_res})

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    initialize_xyperia()
    show_banner()
    chat()
