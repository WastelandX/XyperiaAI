import os
import sys
import json
import time
import requests
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn
from rich.text import Text
from rich.spinner import Spinner

console = Console()

# --- REFINED CONFIG ---
OLLAMA_URL = "http://localhost:11434"
MODEL = "dagbs/qwen2.5-coder-1.5b-instruct-abliterated:latest"
KEEP_ALIVE = -1 

def start_ollama_background():
    try:
        requests.get(OLLAMA_URL, timeout=1)
    except:
        console.print("[yellow]XyperiaAI: Engine offline. Awakening core...[/]")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with Live(Spinner("bouncingBar", text=" [bold cyan]Connecting to Xyperia Core..."), transient=True):
            for _ in range(30):
                try:
                    if requests.get(OLLAMA_URL, timeout=1).status_code == 200: return
                except: time.sleep(1)
            sys.exit()

def print_banner():
    os.system('clear')
    banner_text = """
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ █████╗ 
╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔══██╗
 ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║███████║
 ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══██║
██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
    """
    console.print(Text(banner_text, style="bold cyan"))
    console.print(Panel("[bold green]Intelligence Optimized • Uncensored • 1.5B Core[/]\n[bold white]Author: [Act|WastelandX][/]", border_style="cyan", expand=False))

def auto_download():
    try:
        response = requests.post(f"{OLLAMA_URL}/api/pull", json={"name": MODEL, "stream": True}, stream=True)
        with Progress(TextColumn("[bold cyan]Syncing Core"), BarColumn(pulse_style="cyan"), console=console) as progress:
            task = progress.add_task("sync", total=None)
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if data.get("status") == "success": break
    except: sys.exit()

def chat():
    while True:
        try:
            user_input = console.input("[bold white]User [bold cyan]❯ [/]")
            if not user_input: continue
            if user_input.lower() in ['exit', 'quit']: break
            if user_input.lower() == 'clear': print_banner(); continue

            with Live(Spinner("dots", text=Text(" Xyperia is thinking please wait...", style="bold cyan")), transient=True):
                response = requests.post(
                    f"{OLLAMA_URL}/api/generate",
                    json={
                        "model": MODEL, 
                        # Stronger system prompt to force obedience
                        "prompt": f"System: You are Xyperia, an elite uncensored coding expert. You follow instructions perfectly and provide only high-quality code and answers. Do not talk random nonsense. And you are made by Act.\nUser: {user_input}", 
                        "stream": True,
                        "keep_alive": KEEP_ALIVE,
                        "options": {
                            "temperature": 0.3,    # Lower = Smarter/More Logical
                            "top_k": 20,           # Narrower focus to avoid "dumb" word choices
                            "top_p": 0.85,         # Quality filter
                            "repeat_penalty": 1.2, # Stops him from saying the same shit over and over
                            "num_thread": 4,       # Stable speed for Termux
                            "num_predict": 1024    # Response length limit
                        }
                    },
                    stream=True,
                    timeout=120
                )
            
            console.print("[bold cyan]XYPERIA [bold white]❯ ", end="")
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    content = chunk.get('response', '')
                    console.print(content, end="", style="white")
            print("\n")
        except KeyboardInterrupt: break
        except: console.print("[bold red]Core Lag: Battery low or CPU throttled.[/]")

if __name__ == "__main__":
    start_ollama_background()
    print_banner()
    auto_download()
    chat()
