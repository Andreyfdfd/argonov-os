#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════
#  ARGONOV OS · Core Registry
#  Менеджер реестра скриптов
#  Версия: 1.0  ·  Обновлён: 2026-09-11
# ═══════════════════════════════════════════════════════
"""
Управляет реестром всех скриптов ARGONOV OS.

Использование:
    argonov-core list              # все скрипты
    argonov-core info <name>       # инфо о скрипте
    argonov-core edit <name>       # открыть в nano для правки
    argonov-core run <name>        # запустить
    argonov-core check             # проверить целостность
    argonov-core add <name> <file> <short> [group]
    argonov-core rm <name>         # убрать из реестра
    argonov-core init              # создать реестр из текущих скриптов
    argonov-core show              # показать сырой JSON

Зависимости:
    - rich
"""

import os
import sys
import json
import time
import shutil
import subprocess
from datetime import datetime

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import SIMPLE_HEAD

# ═══ КОНСТАНТЫ ═══
console = Console()
HOME = os.path.expanduser("~")
REGISTRY_FILE = os.path.join(HOME, ".argonov_registry.json")

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

GROUP_ORDER = ["core", "ai", "media", "data", "security",
               "games", "network", "tools", "other"]

# Дефолтный реестр — создаётся при `init`
DEFAULT_SCRIPTS = {
    "argonov":      {"file": "argonov",           "short": "argonov",  "type": "bash",   "version": "2.0", "desc": "⚡ Меню системы",                "group": "core",     "interactive": True,  "deps": []},
    "argonov-core": {"file": "argonov-core.py",   "short": "core",     "type": "python", "version": "1.0", "desc": "🗂  Реестр скриптов",              "group": "core",     "interactive": False, "deps": ["rich"]},
    "argonov-dump": {"file": "argonov-dump",      "short": "dump",     "type": "python", "version": "2.0", "desc": "📦 Дамп + push",                   "group": "core",     "interactive": False, "deps": []},
    "doctor":       {"file": "doctor.py",         "short": "doctor",   "type": "python", "version": "2.0", "desc": "🩺 Диагностика",                    "group": "core",     "interactive": False, "deps": ["rich"]},
    "net_helper":   {"file": "net_helper.py",     "short": "net",      "type": "python", "version": "3.0", "desc": "🌐 Fallback API + кэш",             "group": "core",     "interactive": False, "deps": []},
    "ai":           {"file": "ai.py",             "short": "ai",       "type": "python", "version": "16",  "desc": "🧠 AI-ассистент",                  "group": "ai",       "interactive": True,  "deps": ["rich", "prompt_toolkit", "llama-server"]},
    "music":        {"file": "randomaudio.py",    "short": "music",    "type": "python", "version": "3.0", "desc": "🎵 Музыкальный плеер",              "group": "media",    "interactive": True,  "deps": ["rich", "prompt_toolkit", "chafa"]},
    "music-meta":   {"file": "music_meta.py",     "short": "meta",     "type": "python", "version": "3.0", "desc": "🎼 Метаданные треков",              "group": "media",    "interactive": False, "deps": ["rich", "requests", "mutagen"]},
    "art":          {"file": "art.py",            "short": "art",      "type": "python", "version": "3.0", "desc": "🎨 Картинки",                        "group": "media",    "interactive": False, "deps": ["rich", "viu"]},
    "todo":         {"file": "todo.py",           "short": "todo",     "type": "python", "version": "3.0", "desc": "📌 Задачи",                          "group": "data",     "interactive": True,  "deps": ["rich", "prompt_toolkit"]},
    "notes":        {"file": "notes.py",          "short": "notes",    "type": "python", "version": "3.0", "desc": "📝 Заметки",                         "group": "data",     "interactive": True,  "deps": ["rich", "prompt_toolkit"]},
    "pm":           {"file": "passmanager.py",    "short": "pm",       "type": "python", "version": "3.0", "desc": "🔒 Пароли (AES-256)",                "group": "security", "interactive": True,  "deps": ["rich", "prompt_toolkit", "cryptography"]},
    "passgen":      {"file": "passgen.py",        "short": "passgen",  "type": "python", "version": "2.0", "desc": "🔐 Генератор паролей",               "group": "security", "interactive": False, "deps": []},
    "hack":         {"file": "hacktool.py",       "short": "hack",     "type": "python", "version": "3.0", "desc": "🎮 OSINT мультитул",                 "group": "security", "interactive": True,  "deps": ["rich", "prompt_toolkit"]},
    "crypto":       {"file": "crypto_informer.py","short": "crypto",   "type": "python", "version": "3.0", "desc": "📈 Курсы крипты и валют",           "group": "data",     "interactive": True,  "deps": ["rich", "net_helper"]},
    "sysinfo":      {"file": "sysinfo.py",        "short": "s",        "type": "python", "version": "5.0", "desc": "⚡ Центр управления",                "group": "tools",    "interactive": False, "deps": ["net_helper"]},
    "utils":        {"file": "utils.py",          "short": "util",     "type": "python", "version": "3.0", "desc": "📦 Сканер пакетов",                  "group": "tools",    "interactive": True,  "deps": ["rich", "prompt_toolkit"]},
    "rpg":          {"file": "hacker_rpg.py",     "short": "rpg",      "type": "python", "version": "3.0", "desc": "🕹  Симулятор хакера",                "group": "games",    "interactive": True,  "deps": ["rich"]},
    "matrix":       {"file": "matrix.py",         "short": "m",        "type": "python", "version": "2.0", "desc": "🌧  Цифровой дождь",                 "group": "games",    "interactive": True,  "deps": ["curses"]},
    "download":     {"file": "download_zone.py",  "short": "d",        "type": "python", "version": "3.0", "desc": "📥 Загрузчик (aria2c)",              "group": "network",  "interactive": True,  "deps": ["rich", "prompt_toolkit", "aria2c"]},
}

# ═══ РЕЕСТР ═══
def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return None
    try:
        with open(REGISTRY_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]❌ Ошибка чтения реестра: {e}[/]")
        return None


def save_registry(reg):
    reg["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmp = REGISTRY_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(reg, f, ensure_ascii=False, indent=1)
        os.replace(tmp, REGISTRY_FILE)
        return True
    except Exception as e:
        console.print(f"[red]❌ Ошибка записи: {e}[/]")
        return False


def get_scripts(reg):
    return reg.get("scripts", {}) if reg else {}

# ═══ РИСОВКА ═══
def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒░ ", style=f"bold {GREEN_BRIGHT}")]
    if sub:
        lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("─" * 55, style=GREEN_DIM))
    return Group(*lines)

# ═══ КОМАНДЫ ═══
def cmd_init():
    """Создаёт реестр из текущих скриптов."""
    if os.path.exists(REGISTRY_FILE):
        console.print(f"[yellow]⚠ Реестр уже существует: {REGISTRY_FILE}[/]")
        try:
            a = console.input("[bold magenta]Перезаписать? (y/N)> [/]").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return
        if a != "y":
            console.print("[dim]Отменено[/]")
            return

    reg = {"version": 1, "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "scripts": dict(DEFAULT_SCRIPTS)}

    # Проверяем что файлы на месте
    missing = []
    for name, info in reg["scripts"].items():
        fp = os.path.join(HOME, info["file"])
        if not os.path.isfile(fp):
            missing.append((name, info["file"]))

    if save_registry(reg):
        console.print(f"[green]✔ Реестр создан: {REGISTRY_FILE}[/]")
        console.print(f"   Записей: [cyan]{len(reg['scripts'])}[/]")
        if missing:
            console.print(f"   [yellow]⚠ Файлы не найдены:[/]")
            for name, fp in missing:
                console.print(f"     [dim]• {name} → {fp}[/]")


def cmd_list():
    reg = load_registry()
    if not reg:
        console.print("[red]❌ Реестр не найден. Запусти: argonov-core init[/]")
        return
    scripts = get_scripts(reg)

    # Группируем
    grouped = {}
    for name, info in scripts.items():
        g = info.get("group", "other")
        grouped.setdefault(g, []).append((name, info))

    console.print()
    console.print(title_block("ARGONOV REGISTRY",
                              f"{len(scripts)} скриптов  ·  обновлён {reg.get('updated','?')}"))
    console.print()

    for g in GROUP_ORDER:
        if g not in grouped:
            continue
        items = sorted(grouped[g], key=lambda x: x[0])
        t = Table(box=SIMPLE_HEAD, border_style="black",
                  header_style=f"bold {GREEN_BRIGHT}", padding=(0,1), expand=True)
        t.add_column("short", style=f"bold {YELLOW}", width=12)
        t.add_column("Файл", style=CYAN, width=22)
        t.add_column("Версия", style=GREEN_DIM, width=8)
        t.add_column("Описание", style=WHITE)
        t.add_column("Есть?", width=6, justify="center")

        for name, info in items:
            fp = os.path.join(HOME, info["file"])
            mark = "[green]✔[/]" if os.path.isfile(fp) else "[red]✘[/]"
            t.add_row(info.get("short", name), info["file"],
                      str(info.get("version", "?")), info.get("desc", ""), mark)

        console.print(f"[bold {MAGENTA}]{g.upper()}[/]")
        console.print(t)
        console.print()


def cmd_info(name):
    reg = load_registry()
    if not reg:
        console.print("[red]❌ Реестр не найден[/]")
        return
    scripts = get_scripts(reg)

    # Ищем по имени или short
    found = None
    for n, info in scripts.items():
        if n == name or info.get("short") == name:
            found = (n, info)
            break
    if not found:
        console.print(f"[red]❌ Не найдено: {name}[/]")
        return

    n, info = found
    fp = os.path.join(HOME, info["file"])
    exists = os.path.isfile(fp)
    size = os.path.getsize(fp) if exists else 0

    console.print()
    console.print(title_block(f"🔍 {n}"))
    console.print()

    t = Table(box=SIMPLE_HEAD, border_style="black",
              show_header=False, padding=(0, 2))
    t.add_column("", style=f"bold {YELLOW}", width=16)
    t.add_column("", style=WHITE)
    t.add_row("Имя", n)
    t.add_row("Файл", info["file"])
    t.add_row("Short", info.get("short", "—"))
    t.add_row("Тип", info.get("type", "—"))
    t.add_row("Версия", str(info.get("version", "—")))
    t.add_row("Группа", info.get("group", "—"))
    t.add_row("Описание", info.get("desc", "—"))
    t.add_row("Интерактивный", "да" if info.get("interactive") else "нет")
    t.add_row("Зависимости", ", ".join(info.get("deps", [])) or "—")
    t.add_row("Файл на месте", f"[green]✔[/] ({size} б)" if exists else "[red]✘ нет[/]")
    t.add_row("Путь", fp)
    console.print(t)
    console.print()


def cmd_edit(name):
    reg = load_registry()
    if not reg:
        console.print("[red]❌ Реестр не найден[/]")
        return
    scripts = get_scripts(reg)

    found = None
    for n, info in scripts.items():
        if n == name or info.get("short") == name:
            found = (n, info)
            break
    if not found:
        console.print(f"[red]❌ Не найдено: {name}[/]")
        return

    n, info = found
    fp = os.path.join(HOME, info["file"])
    if not os.path.isfile(fp):
        console.print(f"[red]❌ Файл не найден: {fp}[/]")
        return

    console.print(f"[yellow]⚙ Открываю в nano: {info['file']}[/]")
    console.print(f"[dim]   Не забудь Ctrl+O → Enter → Ctrl+X для сохранения[/]")
    time.sleep(0.7)
    try:
        subprocess.run(["nano", fp])
    except KeyboardInterrupt:
        pass
    except FileNotFoundError:
        console.print("[red]❌ nano не найден, используй: nano ~/" + info["file"] + "[/]")


def cmd_run(name):
    reg = load_registry()
    if not reg:
        console.print("[red]❌ Реестр не найден[/]")
        return
    scripts = get_scripts(reg)

    found = None
    for n, info in scripts.items():
        if n == name or info.get("short") == name:
            found = (n, info)
            break
    if not found:
        console.print(f"[red]❌ Не найдено: {name}[/]")
        return

    n, info = found
    fp = os.path.join(HOME, info["file"])
    if not os.path.isfile(fp):
        console.print(f"[red]❌ Файл не найден: {fp}[/]")
        return

    typ = info.get("type", "python")
    if typ == "python":
        subprocess.run(["python", fp])
    elif typ == "bash":
        subprocess.run(["bash", fp])
    else:
        subprocess.run([fp])


def cmd_check():
    reg = load_registry()
    if not reg:
        console.print("[red]❌ Реестр не найден[/]")
        return
    scripts = get_scripts(reg)

    console.print()
    console.print(title_block("ПРОВЕРКА РЕЕСТРА"))
    console.print()

    ok_count = 0
    missing = []
    syntax_errors = []

    for name, info in scripts.items():
        fp = os.path.join(HOME, info["file"])
        typ = info.get("type", "python")

        if not os.path.isfile(fp):
            missing.append((name, info["file"]))
            console.print(f"  [red]✘[/] {name:20} {info['file']:25} [dim]не найден[/]")
            continue

        if typ == "python":
            r = subprocess.run(["python", "-m", "py_compile", fp],
                               capture_output=True, timeout=10)
            if r.returncode != 0:
                syntax_errors.append((name, info["file"]))
                console.print(f"  [red]✘[/] {name:20} {info['file']:25} [red]syntax error[/]")
                continue

        size = os.path.getsize(fp)
        console.print(f"  [green]✔[/] {name:20} {info['file']:25} {size:>6} б")
        ok_count += 1

    console.print()
    console.print(f"  Всего: [bold]{len(scripts)}[/]  ·  "
                  f"OK: [green]{ok_count}[/]  ·  "
                  f"Нет файла: [red]{len(missing)}[/]  ·  "
                  f"Синтаксис: [red]{len(syntax_errors)}[/]")
    console.print()


def cmd_add(name, fname, short, group="other"):
    if not name or not fname or not short:
        console.print("[red]❌ argonov-core add <name> <file> <short> [group][/]")
        return
    reg = load_registry()
    if not reg:
        reg = {"version": 1, "scripts": {}}
    scripts = reg.setdefault("scripts", {})

    if name in scripts:
        console.print(f"[yellow]⚠ {name} уже в реестре. Перезапишется.[/]")

    scripts[name] = {
        "file": fname,
        "short": short,
        "type": "python" if fname.endswith(".py") else "bash",
        "version": "1.0",
        "desc": f"➕ {name}",
        "group": group,
        "interactive": False,
        "deps": [],
    }
    if save_registry(reg):
        console.print(f"[green]✔ Добавлено: {name} → {fname}[/]")


def cmd_rm(name):
    reg = load_registry()
    if not reg:
        console.print("[red]❌ Реестр не найден[/]")
        return
    scripts = reg.get("scripts", {})
    if name not in scripts:
        # может это short?
        found = None
        for n, info in scripts.items():
            if info.get("short") == name:
                found = n
                break
        if found:
            name = found
        else:
            console.print(f"[red]❌ Не найдено: {name}[/]")
            return

    del scripts[name]
    if save_registry(reg):
        console.print(f"[green]✔ Удалено из реестра: {name}[/]")
        console.print(f"[dim]   (сам файл не тронут)[/]")


def cmd_show():
    if not os.path.exists(REGISTRY_FILE):
        console.print("[red]❌ Реестр не найден[/]")
        return
    try:
        with open(REGISTRY_FILE, encoding="utf-8") as f:
            data = json.load(f)
        console.print_json(data=data)
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

# ═══ СПРАВКА ═══
def show_help():
    console.print()
    console.print(title_block("ARGONOV CORE", "менеджер реестра скриптов"))
    console.print()

    t = Table(box=SIMPLE_HEAD, border_style="black",
              header_style=f"bold {GREEN_BRIGHT}", padding=(0, 2))
    t.add_column("Команда", style=f"bold {YELLOW}", width=36)
    t.add_column("Действие", style=WHITE)
    t.add_row("list",                          "📋 Показать все скрипты")
    t.add_row("info <name>",                   "🔍 Инфо о скрипте (имя или short)")
    t.add_row("edit <name>",                   "✏ Открыть в nano для правки")
    t.add_row("run <name>",                    "🚀 Запустить скрипт")
    t.add_row("check",                         "✅ Проверить все файлы + синтаксис")
    t.add_row("add <name> <file> <short> [gr]", "➕ Добавить в реестр")
    t.add_row("rm <name>",                     "🗑 Убрать из реестра (файл не трогается)")
    t.add_row("init",                          "⚙ Создать реестр с базовыми скриптами")
    t.add_row("show",                          "📄 Сырой JSON реестра")
    console.print(t)
    console.print()
    console.print(f"  [dim]Реестр: {REGISTRY_FILE}[/]")
    console.print()

# ═══ MAIN ═══
def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help", "?"):
        show_help()
        return

    cmd = args[0].lower()
    rest = args[1:]

    if cmd == "list":
        cmd_list()
    elif cmd == "info":
        if not rest:
            console.print("[red]❌ info <name>[/]")
            return
        cmd_info(rest[0])
    elif cmd == "edit":
        if not rest:
            console.print("[red]❌ edit <name>[/]")
            return
        cmd_edit(rest[0])
    elif cmd == "run":
        if not rest:
            console.print("[red]❌ run <name>[/]")
            return
        cmd_run(rest[0])
    elif cmd == "check":
        cmd_check()
    elif cmd == "add":
        if len(rest) < 3:
            console.print("[red]❌ add <name> <file> <short> [group][/]")
            return
        group = rest[3] if len(rest) > 3 else "other"
        cmd_add(rest[0], rest[1], rest[2], group)
    elif cmd == "rm":
        if not rest:
            console.print("[red]❌ rm <name>[/]")
            return
        cmd_rm(rest[0])
    elif cmd == "init":
        cmd_init()
    elif cmd == "show":
        cmd_show()
    else:
        console.print(f"[red]❌ Неизвестная команда: {cmd}[/]")
        console.print("[dim]Используй: argonov-core help[/]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано.[/]")
