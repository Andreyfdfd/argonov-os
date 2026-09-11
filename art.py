#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Art — поиск картинки по телефону и показ через viu"""

import os, sys, subprocess, time
from rich.console import Console
from rich.prompt import Prompt

console = Console()

HOME = os.path.expanduser("~")
WELCOME_FILE = os.path.join(HOME, ".argonov_welcome_image")
STORAGE = os.path.join(HOME, "storage")
SEARCH_DIRS = [
    os.path.join(STORAGE, "shared"),
    os.path.join(HOME, "storage"),
    HOME,
    "/sdcard",
    "/storage/emulated/0",
]

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"}

def has_cmd(c): 
    return subprocess.run(f"which {c}", shell=True, capture_output=True).returncode == 0

def find_image(name):
    """
    Ищет файл по имени в SEARCH_DIRS.
    name может быть:
      - полный путь
      - имя с расширением (fantasy.png)
      - имя без (fantasy)
    """
    # 1. Если полный путь
    if os.path.isfile(name): return name

    # 2. Если с расширением
    if os.path.splitext(name)[1].lower() in IMAGE_EXTS:
        target = name.lower()
    else:
        target_exts = IMAGE_EXTS
        target = name.lower()

    results = []
    for base in SEARCH_DIRS:
        if not os.path.isdir(base): continue
        for root, dirs, files in os.walk(base):
            # Пропускаем системные
            dirs[:] = [d for d in dirs if d not in
                       ("Android/data", "Android/obb", ".thumbnails", ".cache", "Termux")]
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext not in IMAGE_EXTS: continue
                f_lower = f.lower()
                if name.lower() in f_lower:
                    results.append(os.path.join(root, f))
            if len(results) > 50: break
        if len(results) > 50: break

    if not results: return None
    if len(results) == 1: return results[0]

    # Несколько результатов — показать выбор
    console.print()
    console.print(f"[bold yellow]🔍 Найдено {len(results)} файлов:[/]")
    console.print()
    for i, r in enumerate(results[:20], 1):
        sz = os.path.getsize(r)
        short = r.replace(STORAGE + "/", "").replace(HOME, "~")
        console.print(f"  [cyan]{i:2}.[/] {short}  [dim]({sz//1024} КБ)[/]")
    console.print()
    try:
        ch = console.input("[bold magenta]Номер (Enter = 1)> [/]").strip()
        n = int(ch) if ch.isdigit() else 1
        if 1 <= n <= len(results):
            return results[n-1]
    except: pass
    return results[0]

def show_art(path):
    if not path or not os.path.isfile(path):
        console.print(f"[red]❌ Файл не найден: {path}[/]")
        return False
    if not has_cmd("viu"):
        console.print("[red]❌ viu не установлен[/]")
        return False

    os.system("clear")
    cols = int(subprocess.run("tput cols", shell=True, capture_output=True, text=True).stdout.strip() or 50)
    rows = int(subprocess.run("tput lines", shell=True, capture_output=True, text=True).stdout.strip() or 40)
    w = cols - 2
    h = rows - 4

    console.print()
    console.print(f"[dim]🎨 {os.path.basename(path)}[/]")
    console.print()
    try:
        subprocess.run(["viu", "-w", str(w), "-h", str(h), "-b", "-t", path])
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")
        return False
    console.print()
    return True

def set_welcome(path):
    if not path or not os.path.isfile(path):
        console.print(f"[red]❌ Файл не найден: {path}[/]")
        return False
    with open(WELCOME_FILE, "w") as f:
        f.write(os.path.abspath(path))
    console.print(f"[green]✔ Welcome-картинка установлена:[/] [cyan]{os.path.basename(path)}[/]")
    console.print(f"[dim]   {os.path.abspath(path)}[/]")
    console.print()
    console.print(f"[dim]При следующем запуске Termux будет показана эта картинка.[/]")
    return True

def get_welcome():
    if not os.path.exists(WELCOME_FILE): return None
    try:
        with open(WELCOME_FILE) as f:
            p = f.read().strip()
        return p if os.path.isfile(p) else None
    except: return None

def reset_welcome():
    if os.path.exists(WELCOME_FILE):
        os.remove(WELCOME_FILE)
        console.print("[green]✔ Welcome-картинка сброшена[/]")
    else:
        console.print("[yellow]⚠ Welcome не был установлен[/]")

def show_help():
    console.print()
    console.print("[bold bright_green]🎨 ART — показ картинок[/]")
    console.print()
    console.print("  [cyan]art[/]                     — показать welcome-картинку")
    console.print("  [cyan]art <имя>[/]                — найти и показать файл")
    console.print("  [cyan]art <имя> set[/]            — установить как welcome")
    console.print("  [cyan]art set <имя>[/]            — то же самое")
    console.print("  [cyan]art reset[/]                — сбросить welcome")
    console.print("  [cyan]art list[/]                 — список найденных картинок")
    console.print("  [cyan]art help[/]                 — эта справка")
    console.print()

def list_images():
    console.print()
    console.print("[bold yellow]🔍 Поиск изображений в памяти телефона...[/]")
    console.print()
    found = []
    for base in SEARCH_DIRS[:2]:  # только shared/storage чтобы не долго
        if not os.path.isdir(base): continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in
                       ("Android/data", "Android/obb", ".thumbnails", ".cache", "Termux")]
            for f in files:
                if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
                    fp = os.path.join(root, f)
                    try: sz = os.path.getsize(fp)
                    except: sz = 0
                    found.append((fp, sz))
            if len(found) > 200: break
        if len(found) > 200: break

    found.sort(key=lambda x: -x[1])
    for i, (fp, sz) in enumerate(found[:30], 1):
        short = fp.replace(STORAGE + "/", "").replace(HOME, "~")
        console.print(f"  [cyan]{i:2}.[/] {short[:60]}  [dim]({sz//1024} КБ)[/]")
    console.print()
    console.print(f"[dim]Всего найдено: {len(found)} (показаны 30 крупнейших)[/]")
    console.print()

def main():
    args = sys.argv[1:]

    if not args:
        # Просто art — показать welcome
        w = get_welcome()
        if not w:
            console.print("[yellow]⚠ Welcome-картинка не установлена. Используй: art <имя> set[/]")
            console.print()
            show_help()
            return
        show_art(w)
        return

    # art help
    if args[0].lower() in ("help", "-h", "--help"):
        show_help()
        return

    # art list
    if args[0].lower() == "list":
        list_images()
        return

    # art reset
    if args[0].lower() == "reset":
        reset_welcome()
        return

    # art set <имя>
    if args[0].lower() == "set" and len(args) >= 2:
        name = " ".join(args[1:])
        console.print(f"[yellow]🔍 Ищу '{name}'...[/]")
        path = find_image(name)
        if path: set_welcome(path)
        else: console.print(f"[red]❌ Не найдено: {name}[/]")
        return

    # art <имя> set
    if len(args) >= 2 and args[-1].lower() == "set":
        name = " ".join(args[:-1])
        console.print(f"[yellow]🔍 Ищу '{name}'...[/]")
        path = find_image(name)
        if path: set_welcome(path)
        else: console.print(f"[red]❌ Не найдено: {name}[/]")
        return

    # art <имя> — просто показать
    name = " ".join(args)
    console.print(f"[yellow]🔍 Ищу '{name}'...[/]")
    path = find_image(name)
    if not path:
        console.print(f"[red]❌ Не найдено: {name}[/]")
        return
    console.print(f"[green]✔ {path}[/]")
    time.sleep(0.5)
    show_art(path)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано.[/]")
