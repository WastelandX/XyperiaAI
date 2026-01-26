import os
import sys
import subprocess
import time
import json

# --- 1. AUTO-INSTALLER ---
def install_requirements():
    try:
        import requests
        from rich.console import Console
    except ImportError:
        print("\033[1;33m[!] Xyperia: Installing dependencies...\033[0m")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "rich"])
        print("\033[1;32m[V] Done. Restarting...\033[0m")
        time.sleep(1)
        os.execl(sys.executable, sys.executable, *sys.argv)

install_requirements()

# --- IMPORTS ---
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# --- CONFIGURATION ---
MODEL_ID = "huihui_ai/qwen2.5-coder-abliterate:0.5b"
API_URL = "http://localhost:11434/api/chat"
BRAND = "XYPERIA"
console = Console()

# --- 2. ENGINE SETUP ---
def setup_ollama():
    try:
        requests.get("http://localhost:11434")
    except requests.exceptions.ConnectionError:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with console.status("[bold cyan]Booting Neural Engine...[/bold cyan]", spinner="dots"):
            for _ in range(20):
                try:
                    requests.get("http://localhost:11434")
                    break
                except:
                    time.sleep(1)

# --- 3. UI DISPLAY ---
def show_banner():
    os.system('clear')
    banner = f"""
    ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗ 
    ╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
     ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
     ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
    ██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
    ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
    """
    console.print(Text(banner, style="bold cyan"))
    console.print(Panel(f"      [bold white]{BRAND} A.I.[/bold white]\n[dim]Made by [Act]. System Online • Uncensored[/dim]", expand=False, border_style="blue"))

# --- 4. CHAT LOOP WITH SPACING ---
def start_chat():
    messages = []
    
    while True:
        try:
            # Add space before the 'You' prompt
            print() 
            user_input = console.input(f"[bold white]You[/bold white] ❱ ")
            
            if user_input.lower() in ["exit", "quit"]:
                console.print("[dim]Session Terminated.[/dim]")
                break
            
            messages.append({"role": "user", "content": user_input})
            
            # Space between your input and the AI response
            print() 
            
            with console.status("[bold cyan]Processing...[/bold cyan]", spinner="dots"):
                payload = {"model": MODEL_ID, "messages": messages, "stream": True}
                response = requests.post(API_URL, json=payload, stream=True)

            console.print(f"[bold cyan]{BRAND}[/bold cyan] ❱ ", end="")
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    body = json.loads(line)
                    if "message" in body:
                        content = body["message"]["content"]
                        print(content, end="", flush=True)
                        full_response += content
            
            # Newline after the response and a divider for the next turn
            print()
            console.rule(style="dim cyan") 
            messages.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")

if __name__ == "__main__":
    setup_ollama()
    show_banner()
    start_chat()