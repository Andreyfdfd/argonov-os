#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Termux Utils Scanner — все установленные утилиты по категориям"""

import subprocess, re
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console()

CATEGORIES = {
    "🐍  Python / модули": ["python", "pip", "pipx", "uv", "poetry", "virtualenv"],
    "📦  Node.js / JS":    ["nodejs", "node", "npm", "yarn", "pnpm"],
    "🦀  Rust":            ["rustc", "cargo", "rust-analyzer"],
    "🧠  ИИ / ассистенты": ["aichat", "ollama", "llama", "openai"],
    "🔀  Git / VCS":       ["git", "lazygit", "gh", "tig"],
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

def run(cmd, timeout=60):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except Exception:
        return None

def get_pkg_packages():
    r = run("pkg list-installed 2>/dev/null")
    out = {}
    if r and r.stdout:
        for line in r.stdout.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("Listing"): continue
            parts = line.split()
            if parts:
                out[parts[0].split("/")[0]] = parts[1] if len(parts) >= 2 else ""
    return out

def get_pip_packages():
    r = run("pip list 2>/dev/null")
    out = {}
    if r and r.stdout:
        for line in r.stdout.strip().split("\n"):
            if "---" in line or line.startswith("Package"): continue
            p = line.split()
            if len(p) >= 2: out[p[0]] = p[1]
    return out

def get_npm_packages():
    r = run("npm list -g --depth=0 2>/dev/null")
    out = {}
    if r and r.stdout:
        for line in r.stdout.split("\n"):
            m = re.search(r"[├└]──\s+(@?[\w\-./]+)@([\w\-.]+)", line)
            if m: out[m.group(1)] = m.group(2)
    return out

def get_cargo_packages():
    r = run("cargo install --list 2>/dev/null")
    out = {}
    if r and r.stdout:
        for line in r.stdout.split("\n"):
            m = re.match(r"^([\w\-]+)\s+v([\w\-.]+):", line)
            if m: out[m.group(1)] = m.group(2)
    return out

def classify(name):
    n = name.lower()
    for cat, kws in CATEGORIES.items():
        for kw in kws:
            if kw in n: return cat
    return CATCH_ALL

def main():
    with console.status("[bold green]Сканирую установленные утилиты...[/]", spinner="dots"):
        pkg = get_pkg_packages()
        pip = get_pip_packages()
        npm = get_npm_packages()
        car = get_cargo_packages()

    console.print()
    total = len(pkg) + len(pip) + len(npm) + len(car)

    # Сводка
    s = Table(box=box.ROUNDED, show_header=False, border_style="black", padding=(0, 1))
    s.add_column("", style="bold yellow", width=22)
    s.add_column("", style="white")
    s.add_row("📦 pkg (Termux)", str(len(pkg)))
    s.add_row("🐍 pip (Python)", str(len(pip)))
    s.add_row("📦 npm (Node.js)", str(len(npm)))
    s.add_row("🦀 cargo (Rust)", str(len(car)))
    s.add_row("[bold green]ВСЕГО[/]", f"[bold green]{total}[/]")
    console.print(Panel(s, title="[bold]📈 Сводка утилит[/]", border_style="black"))
    console.print()

    # Категории
    all_items = []
    for src, d in [("pkg", pkg), ("pip", pip), ("npm", npm), ("cargo", car)]:
        for n, v in d.items():
            all_items.append((src, n, v))

    grouped = defaultdict(list)
    for src, n, v in all_items:
        grouped[classify(n)].append((src, n, v))

    ordered = list(CATEGORIES.keys())
    if CATCH_ALL in grouped:
        ordered.append(CATCH_ALL)

    console.rule("[bold magenta]📂 Утилиты по категориям[/]", style="magenta")
    console.print()

    for cat in ordered:
        items = grouped.get(cat, [])
        if not items: continue
        items.sort(key=lambda x: x[1].lower())
        t = Table(title=f"[bold]{cat}[/] [dim]({len(items)})[/]",
                  box=box.SIMPLE_HEAVY, border_style="black", padding=(0, 1))
        t.add_column("#", style="dim", width=4, justify="right")
        t.add_column("Утилита", style="bold cyan")
        t.add_column("Версия", style="yellow", width=17)
        t.add_column("Источник", width=8)
        for i, (src, n, v) in enumerate(items, 1):
            s = {"pkg":"[green]pkg[/]","pip":"[blue]pip[/]",
                 "npm":"[red]npm[/]","cargo":"[yellow]cargo[/]"}.get(src, src)
            t.add_row(str(i), n, (v or "—")[:16], s)
        console.print(t)
        console.print()

if __name__ == "__main__":
    main()
