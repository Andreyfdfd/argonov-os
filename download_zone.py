#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download Zone v3 — загрузчик с Tab-автодополнением"""

import os, sys, re, subprocess, time, shutil, json
from urllib.parse import urlparse
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

console = Console()

DOWNLOADS_DIR = os.path.expanduser("~/storage/shared/Download")
HISTORY_FILE  = os.path.expanduser("~/.download_history.json")
MAX_HISTORY   = 50

ARIA_FLAGS = [
    "aria2c", "-x", "16", "-s", "16", "-k", "1M",
    "--continue=true", "--file-allocation=none",
    "--auto-file-renaming=false", "--max-tries=5", "--retry-wait=3",
    "--summary-interval=1", "--console-log-level=warn",
    "--download-result=hide", "--check-certificate=false",
    "--user-agent=Mozilla/5.0 (Linux; Android 10) Termux",
]

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

def has_aria(): return shutil.which("aria2c") is not None
def is_magnet(u): return u.startswith("magnet:")
def is_direct(u): return u.startswith(("http://","https://","ftp://","ftps://"))

def human_size(b):
    try: b = float(b)
    except: return "?"
    for u in ["B","KB","MB","GB","TB"]:
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} PB"

def guess_filename(url):
    try:
        return (os.path.basename(urlparse(url).path) or "download")[:60]
    except Exception:
        return "download"

# ─── История ───
def load_history():
    if not os.path.exists(HISTORY_FILE): return []
    try:
        with open(HISTORY_FILE, encoding="utf-8") as f: return json.load(f)
    except Exception: return []

def save_history(items):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(items[-MAX_HISTORY:], f, ensure_ascii=False, indent=1)
    except Exception: pass

def push_history(url, ok):
    items = load_history()
    items.append({"url": url[:120], "ok": bool(ok),
                  "time": datetime.now().strftime("%d.%m.%Y %H:%M")})
    save_history(items)

# ─── Рисование ───
def clear(): console.clear()

def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("═" * 60, style=GREEN_DIM))
    return Group(*lines)

def menu_panel():
    t = Table(box=box.DOUBLE_EDGE, border_style="green",
              show_header=False, padding=(0, 2))
    t.add_column("Команда", style="bold yellow", width=18, justify="center")
    t.add_column("Действие", style="white")
    t.add_row("[cyan]URL / magnet[/]", "📥 Начать загрузку")
    t.add_row("[cyan]history[/]",      "📜 История загрузок")
    t.add_row("[cyan]list[/]",         "📂 Что уже скачано")
    t.add_row("[cyan]open[/]",         "📁 Открыть папку Download")
    t.add_row("[cyan]clear[/]",        "🧹 Очистить экран")
    t.add_row("[cyan]q[/]",            "🚪 Выход")
    console.print(Panel(t, title="[bold green]🌐  DOWNLOAD ZONE  (Tab — автодополнение)[/]",
                        border_style="green"))
    console.print()

# ─── Скачивание ───
def run_aria_with_progress(cmd, label):
    state = {"pct":0, "speed":"0 B/s", "eta":"--",
             "size":"?", "done_size":"0 B", "status":"start"}

    def render():
        bw = 50; filled = int((state["pct"]/100)*bw)
        bar = "▓"*filled + "░"*(bw-filled)
        lines = [
            Text(""),
            Text(f"  📥 {label}", style=f"bold {GREEN_BRIGHT}"),
            Text(""),
            Text(f"  Прогресс: {state['pct']:>5.1f}%", style=f"bold {CYAN}"),
            Text(f"  {bar}", style=GREEN_BRIGHT),
            Text(f"  Скорость: {state['speed']:<14}   ETA: {state['eta']}", style=YELLOW),
            Text(f"  Скачано:  {state['done_size']:<14}   Всего: {state['size']}", style=GRAY),
            Text(f"  Статус:   {state['status']}", style=GREEN_DIM),
            Text(""),
        ]
        return Panel(Group(*lines), border_style=GREEN_DIM, padding=(0,1))

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, bufsize=1, universal_newlines=True)
    except FileNotFoundError:
        console.print("[red]❌ aria2c не найден[/]"); return False
    except Exception as e:
        console.print(f"[red]❌ {e}[/]"); return False

    re_pct   = re.compile(r"\((\d+)%\)")
    re_dl    = re.compile(r"DL:([\d\.]+[KMG]?i?B)")
    re_size  = re.compile(r"([\d\.]+[KMG]?i?B)/([\d\.]+[KMG]?i?B)")
    re_eta   = re.compile(r"ETA:([\d]+[smhd])")
    re_error = re.compile(r"^\s*\d+/\d+\s+\d+:\d+:\d+\s+\[ERROR\]", re.IGNORECASE)

    try:
        with Live(render(), console=console, refresh_per_second=4) as live:
            for line in proc.stdout:
                line = line.strip()
                if not line: continue
                m = re_pct.search(line);  state["pct"] = float(m.group(1)) if m else state["pct"]
                m = re_dl.search(line);   state["speed"] = m.group(1) if m else state["speed"]
                m = re_size.search(line)
                if m:
                    state["done_size"] = m.group(1); state["size"] = m.group(2)
                m = re_eta.search(line);  state["eta"] = m.group(1) if m else state["eta"]
                if re_error.search(line): state["status"] = "⚠ Ошибка"
                live.update(render())

        proc.wait(timeout=5)
        if proc.returncode == 0:
            state["pct"] = 100.0; state["status"] = "✅ Завершено"
            live.update(render()); time.sleep(0.4)
            return True
        else:
            state["status"] = f"❌ Код: {proc.returncode}"
            live.update(render()); time.sleep(0.5)
            return False
    except KeyboardInterrupt:
        console.print("\n  [yellow]⚠ Прервано[/]")
        try: proc.terminate()
        except Exception: pass
        return False
    except Exception as e:
        console.print(f"\n  [red]❌ {e}[/]")
        try: proc.terminate()
        except Exception: pass
        return False

def download_direct(url):
    name = guess_filename(url)
    console.print()
    console.print(Panel(f"[bold {WHITE}]{name}[/]\n[dim]{url[:90]}[/]",
        title=f"[bold {YELLOW}]📥 Загрузка[/]", border_style=GREEN_DIM))
    cmd = ARIA_FLAGS + ["--dir", DOWNLOADS_DIR, "--referer", url, url]
    return run_aria_with_progress(cmd, name)

def download_magnet(magnet):
    console.print()
    console.print(Panel(f"[bold {WHITE}]🧲 Magnet[/]\n[dim]{magnet[:90]}...[/]",
        title=f"[bold {YELLOW}]📥 Торрент[/]", border_style=GREEN_DIM))
    console.print("[dim]Получаю метаданные торрента...[/]")
    cmd = ARIA_FLAGS + ["--dir", DOWNLOADS_DIR,
        "--bt-enable-lpd=true", "--enable-dht=true",
        "--bt-max-peers=200", "--seed-time=0", magnet]
    return run_aria_with_progress(cmd, "torrent")

# ─── История / List / Open ───
def show_history():
    items = load_history()
    console.print(); console.print(title_block("📜 ИСТОРИЯ")); console.print()
    if not items:
        console.print(Text("  Пока пусто.", style=f"dim {GRAY}")); console.print(); return
    t = Table(box=box.SIMPLE_HEAD, border_style=MAGENTA,
              header_style=f"bold {MAGENTA}", padding=(0,2))
    t.add_column("#", style=f"bold {YELLOW}", width=4, justify="right")
    t.add_column("✓", width=3, justify="center")
    t.add_column("URL", style=WHITE)
    t.add_column("Время", style=GRAY, width=18)
    for i, it in enumerate(reversed(items), 1):
        mark = "[green]✔[/]" if it.get("ok") else "[red]✘[/]"
        t.add_row(str(i), mark, it.get("url","")[:60], it.get("time",""))
    console.print(t); console.print()

def show_downloads():
    console.print(); console.print(title_block("📂 ФАЙЛЫ В DOWNLOAD")); console.print()
    if not os.path.isdir(DOWNLOADS_DIR):
        console.print(f"[red]❌ Нет папки: {DOWNLOADS_DIR}[/]"); return
    files = []
    try:
        for f in os.listdir(DOWNLOADS_DIR):
            fp = os.path.join(DOWNLOADS_DIR, f)
            if os.path.isfile(fp):
                try: files.append((f, os.path.getsize(fp)))
                except Exception: pass
    except Exception as e:
        console.print(f"[red]❌ {e}[/]"); return
    files.sort(key=lambda x: -x[1])
    if not files:
        console.print(Text("  Пусто.", style=f"dim {GRAY}")); console.print(); return
    t = Table(box=box.SIMPLE_HEAD, border_style=CYAN,
              header_style=f"bold {CYAN}", padding=(0,1))
    t.add_column("#", style=f"bold {YELLOW}", width=4, justify="right")
    t.add_column("Файл", style=WHITE)
    t.add_column("Размер", style=GREEN_BRIGHT, justify="right", width=12)
    for i, (n, sz) in enumerate(files[:40], 1):
        t.add_row(str(i), n[:60], human_size(sz))
    console.print(t); console.print()

def open_downloads():
    try:
        subprocess.Popen(["termux-open", DOWNLOADS_DIR])
        console.print(f"[green]✔ Открываю: {DOWNLOADS_DIR}[/]")
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")
    time.sleep(0.6)

# ─── MAIN ───
def main():
    if not has_aria():
        clear()
        console.print(Panel("[red]❌ aria2c не найден[/]\n[yellow]Установи:[/] [cyan]pkg install aria2[/]",
                            border_style="red"))
        return

    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    # ─── Tab-автодополнение ───
    commands = ["history", "list", "open", "clear", "q"]
    completer = WordCompleter(commands, ignore_case=True, sentence=False)
    style = Style.from_dict({
        "prompt": "bold ansibrightmagenta",
        "completion-menu.completion": "bg:#000000 #00ff88",
        "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
    })
    session = PromptSession(completer=completer, style=style, complete_while_typing=True)

    while True:
        clear()
        console.print()
        console.print(title_block("DOWNLOAD ZONE", "Terminal Argonov  •  Downloader"))
        console.print()
        console.print(f"[dim]📁 Папка: {DOWNLOADS_DIR}[/]")
        console.print()
        menu_panel()

        try:
            cmd = session.prompt(HTML("<prompt>╰─❯</prompt> ")).strip()
        except (EOFError, KeyboardInterrupt):
            console.print(Text("\n До связи. 🖖", style=f"dim {GREEN_DIM}"))
            break

        if not cmd: continue
        cl = cmd.lower()

        if cl in ("q","exit","quit","выход"):
            console.print(Text(" До связи. 🖖", style=f"dim {GREEN_DIM}")); break
        if cl == "clear": continue

        if cl == "history":
            clear(); show_history()
            try: console.input("[dim]Enter — назад[/] ")
            except (EOFError, KeyboardInterrupt): pass
            continue

        if cl == "list":
            clear(); show_downloads()
            try: console.input("[dim]Enter — назад[/] ")
            except (EOFError, KeyboardInterrupt): pass
            continue

        if cl == "open":
            open_downloads(); continue

        if is_magnet(cmd):
            ok = download_magnet(cmd); push_history(cmd, ok)
            try: console.input("\n[dim]Enter — назад[/] ")
            except (EOFError, KeyboardInterrupt): pass
        elif is_direct(cmd):
            ok = download_direct(cmd); push_history(cmd, ok)
            try: console.input("\n[dim]Enter — назад[/] ")
            except (EOFError, KeyboardInterrupt): pass
        else:
            console.print(Text("  ❌ Это не URL и не magnet", style=RED))
            time.sleep(1)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print(Text("\n Прервано.", style=f"dim {GREEN_DIM}"))
