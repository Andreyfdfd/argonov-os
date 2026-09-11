#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utils Scanner — все установленные пакеты с размерами"""

import os, sys, re, subprocess
from collections import defaultdict
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import SIMPLE_HEAD
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

console = Console()

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

CATEGORIES = {
    "🐍 Python / модули": ["python", "pip", "pipx", "uv", "poetry", "virtualenv"],
    "📦 Node.js / JS":    ["nodejs", "node", "npm", "yarn", "pnpm"],
    "🦀 Rust":            ["rustc", "cargo", "rust-analyzer"],
    "🧠 ИИ / ассистенты": ["aichat", "ollama", "llama", "openai", "llama-cpp"],
    "🔀 Git / VCS":       ["git", "lazygit", "gh", "tig"],
    "✏️  Редакторы":       ["nano", "vim", "neovim", "nvim", "emacs", "micro", "helix"],
    "💻  Терминал / оболочки": ["tmux", "screen", "zsh", "fish", "starship"],
    "🔧  Улучшение CLI":   ["eza", "exa", "bat", "ripgrep", "fd", "fzf", "zoxide",
                             "delta", "dust", "procs", "bottom", "btop", "htop",
                             "tree", "ncdu", "glow", "tldr", "duf"],
    "🌐  Сеть / интернет": ["curl", "wget", "openssh", "ssh", "rsync", "nmap",
                             "netcat", "socat", "inetutils", "dnsutils", "whois",
                             "iputils", "traceroute", "aria2", "httpie", "yt-dlp"],
    "🎬  Медиа / графика": ["ffmpeg", "imagemagick", "graphicsmagick", "sox", "mpv",
                             "scrcpy", "timg", "chafa", "libjpeg", "libpng", "libwebp"],
    "🗃  Базы данных":      ["sqlite", "postgresql", "mysql", "mariadb", "redis", "mongodb"],
    "🤖  Android-интеграция": ["termux-api", "termux-am", "termux-tools", "termux-x11",
                                "termux-services", "termux-exec", "termux-keyring"],
    "🖼  GUI / X11":       ["x11-repo", "xorg", "gtk", "qt5", "tk", "tcl"],
    "🔐  Криптография":     ["openssl", "gnupg", "gpg", "hashcat", "john",
                             "wireguard", "openvpn", "libgcrypt"],
    "📚  Документация":     ["man", "mandoc", "texinfo", "man-pages"],
    "📊  Мониторинг":      ["neofetch", "fastfetch", "screenfetch", "iotop"],
    "📝  Данные":          ["jq", "yq", "pandoc", "dos2unix", "iconv", "miller"],
    "📚  Библиотеки":      ["libssl", "libffi", "libxml2", "libxslt", "zlib",
                             "readline", "ncurses", "libsqlite", "libcrypt", "libandroid"],
    "🔨  Компиляция":      ["clang", "gcc", "make", "cmake", "ninja", "pkg-config",
                             "binutils", "libtool", "autoconf", "automake", "meson", "llvm"],
    "🗂  Базовые утилиты": ["coreutils", "findutils", "grep", "sed", "gawk", "tar",
                             "gzip", "bzip2", "xz-utils", "zip", "unzip", "which",
                             "bash", "dash", "util-linux", "procps", "psmisc", "less",
                             "diffutils", "patch", "bc", "ed"],
}
CATCH_ALL = "🎁  Прочие"

def run(cmd, timeout=30):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except: return None

def human_size(b):
    try: b = int(b)
    except: return "—"
    if b == 0: return "—"
    for u in ["Б","КБ","МБ","ГБ"]:
        if b < 1024: return f"{b:.1f} {u}" if b < 100 else f"{b:.0f} {u}"
        b /= 1024
    return f"{b:.1f} ТБ"

def fmt_kb(kb):
    """Форматирует размер в килобайтах"""
    if not kb: return "—"
    if kb < 1024: return f"{kb} КБ"
    mb = kb / 1024
    if mb < 1024: return f"{mb:.1f} МБ"
    return f"{mb/1024:.2f} ГБ"

def get_pkg_packages():
    """Возвращает {name: version} из dpkg-query"""
    r = run("dpkg-query -W -f='${Package}\\t${Version}\\n' 2>/dev/null")
    out = {}
    if r and r.stdout:
        for line in r.stdout.strip().split("\n"):
            parts = line.split("\t")
            if len(parts) == 2:
                out[parts[0].lower()] = parts[1]
    return out

def get_pkg_sizes():
    """Возвращает {name: size_kb} из dpkg-query"""
    r = run("dpkg-query -W -f='${Package}\\t${Installed-Size}\\n' 2>/dev/null")
    out = {}
    if r and r.stdout:
        for line in r.stdout.strip().split("\n"):
            parts = line.split("\t")
            if len(parts) == 2:
                try: out[parts[0].lower()] = int(parts[1])
                except: pass
    return out

def get_pip_packages():
    r = run("pip list --format=freeze 2>/dev/null", timeout=30)
    out = {}
    if r and r.stdout:
        for line in r.stdout.strip().split("\n"):
            if "==" in line:
                n, v = line.split("==", 1)
                out[re.sub(r"[-_.]+","-",n).lower()] = (n, v)
    return out

def get_pip_sizes():
    r = run("python -c 'import site; print(site.getsitepackages()[0])'", timeout=5)
    if not r or not r.stdout: return {}
    sp = r.stdout.strip()
    if not os.path.isdir(sp): return {}
    out = {}
    try:
        for entry in os.listdir(sp):
            if not entry.endswith(".dist-info"): continue
            record = os.path.join(sp, entry, "RECORD")
            if not os.path.exists(record): continue
            base = entry[:-len(".dist-info")]
            parts = base.rsplit("-", 1)
            key = re.sub(r"[-_.]+","-", (parts[0] if len(parts) == 2 else base)).lower()
            total = 0
            try:
                with open(record, encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        fp = line.strip().split(",")[0]
                        full = os.path.join(sp, fp)
                        if os.path.isfile(full):
                            try: total += os.path.getsize(full)
                            except: pass
                out[key] = total // 1024
            except: continue
    except: pass
    return out

def classify(name):
    n = name.lower()
    for cat, kws in CATEGORIES.items():
        for kw in kws:
            if kw in n: return cat
    return CATCH_ALL

def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("─"*60, style=GREEN_DIM))
    return Group(*lines)

def stats_panel(pkg, pip):
    total_pkg_kb = sum(pkg.values())
    total_pip_kb = sum(pip.values())
    total = total_pkg_kb + total_pip_kb
    t = Table(box=None, show_header=False, padding=(0,3))
    t.add_column("", style=f"bold {YELLOW}"); t.add_column("", style=f"bold {CYAN}")
    t.add_column("", style=f"bold {YELLOW}"); t.add_column("", style=f"bold {CYAN}")
    t.add_row("📦 pkg-пакетов", str(len(pkg)), "💾 Размер pkg", fmt_kb(total_pkg_kb))
    t.add_row("🐍 pip-пакетов", str(len(pip)), "💾 Размер pip", fmt_kb(total_pip_kb))
    t.add_row("[bold green]ВСЕГО[/]", f"[bold green]{len(pkg)+len(pip)}[/]",
              "[bold green]Общий размер[/]", f"[bold green]{fmt_kb(total)}[/]")
    return t

def commands_panel():
    c = Table(box=None, show_header=False, padding=(0,2))
    c.add_column("", style=f"bold {YELLOW}", width=16, justify="right")
    c.add_column("", style=f"{CYAN}")
    c.add_row("[cyan]/поиск[/]", "🔍 Найти пакет (или просто введи часть имени)")
    c.add_row("[cyan]/cat имя[/]", "📁 Показать одну категорию")
    c.add_row("[cyan]cat[/]", "📂 Список всех категорий")
    c.add_row("[cyan]sort[/]", "📊 Сортировка: имя ↔ размер")
    c.add_row("[cyan]reset[/]", "↩ Сбросить фильтры")
    c.add_row("[cyan]q[/cyan]", "🚪 Выход")
    return Panel(c, title=f"[bold {CYAN}]⌨  КОМАНДЫ[/]", border_style="black", padding=(0,1))

# ═══════════ TAB-COMPLETER ═══════════
COMMANDS = ["/", "cat", "sort", "reset", "q", "quit", "exit"]

class UtilsComp(Completer):
    def get_completions(self, doc, ev):
        t = doc.text_before_cursor
        if " " in t: return
        for c in COMMANDS:
            if c.startswith(t.lower()): yield Completion(c, start_position=-len(t))

# ═══════════ MAIN ═══════════
def main():
    os.system("clear")
    console.print()
    console.print(Text("⚙ Сканирую пакеты и размеры...", style=f"bold {GREEN_BRIGHT}"))
    console.print()

    pkg_ver = get_pkg_packages()
    pkg_sizes = get_pkg_sizes()
    pip_data = get_pip_packages()
    pip_sizes = get_pip_sizes()

    # Объединяем: {name: (source, display_name, version, size_kb)}
    items = {}
    for name, ver in pkg_ver.items():
        items[name] = ("pkg", name, ver, pkg_sizes.get(name, 0))
    for key, (name, ver) in pip_data.items():
        # Если уже есть в pkg — pip приоритетнее
        items[key] = ("pip", name, ver, pip_sizes.get(key, 0))

    sort_by = {"mode": "name"}
    filt = {"cat": None, "search": None}

    session = PromptSession(
        completer=UtilsComp(), complete_while_typing=True,
        style=Style.from_dict({
            "prompt": "bold ansibrightmagenta",
            "completion-menu.completion": "bg:#000000 #00ff88",
            "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
        }))

    while True:
        os.system("clear")
        console.print()
        console.print(title_block("У Т И Л И Т Ы  ·  S C A N N E R",
            "Terminal Argonov  •  размеры пакетов"))
        console.print()

        # Группируем по категориям
        grouped = defaultdict(list)
        for key, (src, name, ver, size) in items.items():
            cat = classify(name)
            if filt["cat"] and cat != filt["cat"]: continue
            if filt["search"]:
                q = filt["search"].lower()
                if q not in name.lower(): continue
            grouped[cat].append((src, name, ver, size))

        # Считаем итого
        total = sum(len(v) for v in grouped.values())
        total_kb = sum(item[3] for v in grouped.values() for item in v)

        console.print(stats_panel(pkg_sizes, pip_sizes))
        console.print()

        # Активные фильтры
        active = []
        if filt["cat"]: active.append(f"cat: [magenta]{filt['cat']}[/]")
        if filt["search"]: active.append(f"поиск: [yellow]{filt['search']}[/]")
        active.append(f"сортировка: [cyan]{sort_by['mode']}[/]")
        console.print("[bold]🔎 Фильтры:[/] " + "  ·  ".join(active))
        console.print()

        if total == 0:
            console.print(Text("❌ Ничего не найдено", style=RED))
            console.print()
        else:
            # Порядок категорий
            ordered = list(CATEGORIES.keys())
            if CATCH_ALL in grouped: ordered.append(CATCH_ALL)

            for cat in ordered:
                lst = grouped.get(cat, [])
                if not lst: continue
                # Сортировка внутри категории
                if sort_by["mode"] == "size":
                    lst.sort(key=lambda x: -x[3])
                else:
                    lst.sort(key=lambda x: x[1].lower())

                cat_kb = sum(x[3] for x in lst)
                t = Table(box=SIMPLE_HEAD, border_style="black",
                          header_style=f"bold {GREEN_BRIGHT}", padding=(0,1), expand=True)
                t.add_column("#", style=f"bold {YELLOW}", width=4, justify="right")
                t.add_column("Пакет", style=WHITE)
                t.add_column("Версия", style=GREEN_DIM, width=16)
                t.add_column("Размер", style=f"bold {MAGENTA}", width=12, justify="right")
                t.add_column("Src", width=6, justify="center")

                for i, (src, name, ver, size) in enumerate(lst, 1):
                    src_s = f"[green]pkg[/]" if src == "pkg" else f"[blue]pip[/]"
                    t.add_row(str(i), name, ver[:16], fmt_kb(size), src_s)

                # Заголовок категории + общий размер
                console.print(Text(f"{cat}  [dim]· {len(lst)} шт · {fmt_kb(cat_kb)}[/]",
                                   style=f"bold {MAGENTA}"))
                console.print(t)
                console.print()

        console.print(f"[bold green]📊 Всего показано:[/] {total}  ·  [bold magenta]{fmt_kb(total_kb)}[/]")
        console.print()
        console.print(commands_panel())
        console.print()

        try:
            cmd = session.prompt(FormattedText([("bold ansibrightmagenta","╰─❯ ")])).strip()
        except: break

        if not cmd: continue
        cl = cmd.lower()

        if cl in ("q","exit","quit","выход"): break
        if cl == "sort":
            sort_by["mode"] = "size" if sort_by["mode"] == "name" else "name"
            continue
        if cl == "reset":
            filt["cat"] = None; filt["search"] = None
            continue
        if cl == "cat":
            console.print()
            console.print("[bold]Категории:[/]")
            for i, c in enumerate(CATEGORIES.keys(), 1):
                if c in grouped:
                    console.print(f"  [cyan]{i}.[/] {c}  [dim]({len(grouped[c])})[/]")
            console.print()
            try:
                ch = console.input("[bold magenta]Номер категории> [/]").strip()
            except: continue
            cats = list(CATEGORIES.keys())
            if ch.isdigit() and 1 <= int(ch) <= len(cats):
                filt["cat"] = cats[int(ch)-1]
            continue
        if cl.startswith("/cat "):
            c = cmd[5:].strip()
            for k in CATEGORIES.keys():
                if c.lower() in k.lower():
                    filt["cat"] = k; break
            continue
        if cmd.startswith("/"):
            filt["search"] = cmd[1:].strip()
            continue
        # Поиск по строке
        filt["search"] = cmd

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано.[/]")
