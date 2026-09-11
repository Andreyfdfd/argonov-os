#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════
#  ARGONOV OS · Doctor v3
#  Расширенная диагностика — по реестру скриптов
#  Версия: 3.0  ·  Обновлён: 2026-09-11
# ═══════════════════════════════════════════════════════
"""
Диагностика ARGONOV OS: система, скрипты (по реестру),
инструменты, AI, Termux:API, storage, сеть, кэш, конфиги, git.

Использование:
    doctor                 # быстрая проверка (без сети)
    doctor --full          # + проверка доступности API
    doctor -f              # короткий алиас
    argonov doctor         # через меню
    argonov doctor --full

Зависимости:
    - rich
    - ~/.argonov_registry.json (создать: argonov-core init)
"""

import os
import re
import sys
import json
import shutil
import platform
import subprocess
from datetime import datetime

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.box import SIMPLE_HEAD

# ═══ КОНСТАНТЫ ═══
console = Console()
HOME = os.path.expanduser("~")
REPO_DIR = os.path.join(HOME, "argonov-os")
REGISTRY_FILE = os.path.join(HOME, ".argonov_registry.json")
PREFIX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

SOC_NAMES = {
    "SM8750": "Snapdragon 8 Elite", "SM8650": "Snapdragon 8 Gen 3",
    "SM8550": "Snapdragon 8 Gen 2", "SM8450": "Snapdragon 8 Gen 1",
    "SM8350": "Snapdragon 888", "SM8250": "Snapdragon 870/865",
    "SM8150": "Snapdragon 855", "SM7325": "Snapdragon 778G",
    "SM6375": "Snapdragon 695", "SM6225": "Snapdragon 680",
    "SM4350": "Snapdragon 480", "MT6989": "Dimensity 9300",
    "MT6985": "Dimensity 9200", "MT6983": "Dimensity 9000",
    "MT6895": "Dimensity 8100", "MT6877": "Dimensity 900",
    "MT6833": "Dimensity 700", "MT6769": "Helio G85/G80",
}

TOOLS = [
    ("python",        "python",        "--version", "python",       True),
    ("pip",           "pip",           "--version", "python",       True),
    ("git",           "git",           "--version", "git",          True),
    ("fish",          "fish",          "--version", "fish",         False),
    ("starship",      "starship",      "--version", "starship",     False),
    ("eza",           "eza",           "--version", "eza",          False),
    ("bat",           "bat",           "--version", "bat",          False),
    ("fd",            "fd",            "--version", "fd",           False),
    ("fzf",           "fzf",           "--version", "fzf",          False),
    ("rg",            "rg",            "--version", "ripgrep",      False),
    ("zoxide",        "zoxide",        "--version", "zoxide",       False),
    ("jq",            "jq",            "--version", "jq",           False),
    ("curl",          "curl",          "--version", "curl",         True),
    ("wget",          "wget",          "--version", "wget",         False),
    ("aria2c",        "aria2c",        "--version", "aria2",        True),
    ("chafa",         "chafa",         "--version", "chafa",        False),
    ("viu",           "viu",           "--version", "viu",          False),
    ("ffmpeg",        "ffmpeg",        "-version",  "ffmpeg",       False),
    ("nmap",          "nmap",          "--version", "nmap",         False),
    ("llama-server",  "llama-server",  "-h",        "llama-cpp",    True),
    ("tmux",          "tmux",          "-V",        "tmux",         False),
    ("tree",          "tree",          "--version", "tree",         False),
    ("ncdu",          "ncdu",          "--version", "ncdu",         False),
    ("gh",            "gh",            "--version", "gh",           False),
]

TERMUX_API = [
    ("termux-battery-status", "🔋 Батарея"),
    ("termux-notification",   "🔔 Уведомления"),
    ("termux-media-player",   "🎵 Плеер"),
    ("termux-open",           "📂 Открыть файл"),
    ("termux-toast",          "💬 Toast"),
    ("termux-clipboard-get",  "📋 Буфер (get)"),
    ("termux-clipboard-set",  "📋 Буфер (set)"),
]

# ═══ СЧЁТЧИКИ ═══
problems = []      # 🔴 критично
warnings = []      # 🟡 предупреждения
fix_hints = []     # как чинить

# ═══ УТИЛИТЫ ═══
def run(cmd, timeout=10):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True,
                              text=True, timeout=timeout)
    except Exception:
        return None


def getprop(p):
    r = run(f"getprop {p}")
    return r.stdout.strip() if r and r.stdout else "?"


def has_cmd(c):
    return shutil.which(c) is not None


def cmd_version(cmd, flag="--version"):
    r = run(f"{cmd} {flag} 2>&1 | head -1", timeout=4)
    if not r or not r.stdout:
        return "?"
    m = re.search(r"(\d+\.\d+(?:\.\d+)?)", r.stdout)
    return m.group(1) if m else "?"


def human_size(b):
    try:
        b = float(b)
    except Exception:
        return "?"
    for u in ["Б", "КБ", "МБ", "ГБ", "ТБ"]:
        if b < 1024:
            return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} ПБ"


def humanize_soc(raw):
    if not raw or raw == "?":
        return "?"
    up = raw.upper().replace("QTI ", "").strip()
    for k, name in SOC_NAMES.items():
        if k.upper() in up:
            return name
    return up


def sep():
    console.print(f"[{GREEN_DIM}]{'═' * 51}[/]")


def section(title):
    console.print()
    console.print(f"[{MAGENTA}][ {title} ]:[/]")
    sep()


def ok(msg, extra=""):
    console.print(f"  [{GREEN_BRIGHT}]✔[/] {msg}" + (f" [{GRAY}]{extra}[/]" if extra else ""))


def fail(msg, fix=None, level="problem"):
    col = RED if level == "problem" else YELLOW
    mark = "✘" if level == "problem" else "⚠"
    console.print(f"  [{col}]{mark}[/] {msg}")
    if fix:
        console.print(f"     [{GRAY}]→ {fix}[/]")
        if level == "problem":
            problems.append(msg)
            fix_hints.append(fix)
        else:
            warnings.append(msg)


def info(msg):
    console.print(f"  [{CYAN}]•[/] {msg}")

# ═══ РЕЕСТР ═══
def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return None
    try:
        with open(REGISTRY_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# ═══ СЕКЦИИ ═══
def check_system():
    section("СИСТЕМА")
    model = getprop("ro.product.model")
    android = getprop("ro.build.version.release")
    info(f"{model}  ·  Android {android}")

    try:
        with open("/proc/meminfo") as f:
            mem = f.read()
        total = int(re.search(r"MemTotal:\s+(\d+)", mem).group(1)) // 1024
        avail = int(re.search(r"MemAvailable:\s+(\d+)", mem).group(1)) // 1024
        pct = int(avail / total * 100)
        col = GREEN_BRIGHT if avail > 1500 else (YELLOW if avail > 800 else RED)
        console.print(f"  [{CYAN}]💻[/] ОЗУ: [{col}]{avail} МБ[/] / {total} МБ ({pct}% свободно)")
        if avail < 1500:
            fail("Мало ОЗУ для AI (нужно ≥ 2 ГБ свободно)",
                 "закрой лишние приложения", level="warning")
    except Exception:
        fail("Не удалось прочитать /proc/meminfo")

    try:
        u = shutil.disk_usage(HOME)
        free_gb = u.free // (1024**3)
        total_gb = (u.free + u.used) // (1024**3)
        col = GREEN_BRIGHT if free_gb > 5 else (YELLOW if free_gb > 2 else RED)
        console.print(f"  [{CYAN}]💾[/] Диск: [{col}]{free_gb} ГБ свободно[/] / {total_gb} ГБ")
        if free_gb < 2:
            fail("Мало места на диске", "очисти ~/.cache и ~/argonov_backups")
    except Exception:
        pass

    r = run("termux-battery-status 2>/dev/null")
    if r and r.stdout:
        try:
            d = json.loads(r.stdout)
            pct = d.get("percentage", "?")
            st = d.get("status", "?")
            col = GREEN_BRIGHT if str(pct).isdigit() and int(pct) > 20 else YELLOW
            console.print(f"  [{CYAN}]🔋[/] Батарея: [{col}]{pct}%[/] ({st})")
        except Exception:
            pass


def check_scripts():
    section("СКРИПТЫ (по реестру)")

    reg = load_registry()
    if not reg:
        fail("Реестр не найден", "python ~/argonov-core.py init")
        return

    scripts = reg.get("scripts", {})
    ok_count = 0
    missing = []
    syntax_errors = []

    for name, info_data in sorted(scripts.items()):
        fname = info_data.get("file")
        if not fname:
            continue
        fp = os.path.join(HOME, fname)
        if not os.path.isfile(fp):
            missing.append(fname)
            fail(f"{fname} не найден", f"восстанови из дампа или git pull")
            continue

        size = os.path.getsize(fp)
        typ = info_data.get("type", "python")

        # Проверка синтаксиса Python
        if typ == "python":
            r = subprocess.run(["python", "-m", "py_compile", fp],
                               capture_output=True, timeout=10)
            if r.returncode != 0:
                syntax_errors.append(fname)
                fail(f"{fname} — syntax error", f"python -m py_compile {fp}")
                continue

        # +x для исполняемых
        if fname in ("argonov", "argonov-dump"):
            if os.access(fp, os.X_OK):
                ok(fname, f"{size} б · +x")
            else:
                fail(f"{fname} — нет +x", f"chmod +x ~/{fname}")
                ok_count += 1
        else:
            ok(fname, f"{size} б")
            ok_count += 1

    console.print()
    total = len([s for s in scripts.values() if s.get("file")])
    if not missing and not syntax_errors:
        console.print(f"  [{GREEN_BRIGHT}]✔ Все скрипты: {ok_count}/{total}[/]")
    else:
        console.print(f"  [{RED}]✘ Проблемы: {len(missing)} нет файла · {len(syntax_errors)} syntax[/]")


def check_symlinks():
    section("СИМЛИНКИ / PATH")
    bin_dir = os.path.join(PREFIX, "bin")
    if not os.path.isdir(bin_dir):
        fail(f"{bin_dir} не найден")
        return

    links = {
        "argonov":      os.path.join(HOME, "argonov"),
        "argonov-dump": os.path.join(HOME, "argonov-dump"),
        "argonov-core": os.path.join(HOME, "argonov-core.py"),
        "doctor":       os.path.join(HOME, "doctor.py"),
    }
    for name, target in links.items():
        link = os.path.join(bin_dir, name)
        if os.path.islink(link):
            real = os.path.realpath(link)
            if real == os.path.realpath(target):
                ok(f"{name} → {target.replace(HOME, '~')}")
            else:
                fail(f"{name} — битый симлинк", f"ln -sf {target} {link}")
        elif os.path.isfile(link):
            ok(f"{name} — файл (не симлинк)")
        else:
            fail(f"{name} — не в $PREFIX/bin", f"ln -sf {target} {link}")


def check_tools():
    section("ИНСТРУМЕНТЫ")
    ok_count = 0
    for label, cmd, flag, pkg, critical in TOOLS:
        if has_cmd(cmd):
            v = cmd_version(cmd, flag)
            ok(label, v)
            ok_count += 1
        else:
            if critical:
                fail(f"{label} не установлен", f"pkg install {pkg}")
            else:
                fail(f"{label} не установлен", f"pkg install {pkg}", level="warning")
    console.print()
    console.print(f"  [{GREEN_BRIGHT}]✔ Установлено: {ok_count}/{len(TOOLS)}[/]")


def check_ai():
    section("AI (модели + llama.cpp)")

    if has_cmd("llama-server"):
        v = cmd_version("llama-server", "--version")
        ok("llama-server", v)
    else:
        fail("llama-server не установлен", "pkg install llama-cpp")

    models = []
    for d in [HOME, os.path.join(HOME, "models")]:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".gguf"):
                    fp = os.path.join(d, f)
                    try:
                        sz = os.path.getsize(fp)
                    except Exception:
                        sz = 0
                    if sz > 50_000_000:
                        models.append((fp, sz))
    models.sort(key=lambda x: -x[1])

    if models:
        console.print()
        console.print(f"  [{CYAN}]📦 Модели GGUF:[/]")
        for fp, sz in models:
            name = os.path.basename(fp)
            col = GREEN_BRIGHT if "qwen" in name.lower() else CYAN
            console.print(f"    [{col}]•[/] {name}  [{GRAY}]({human_size(sz)})[/]")
        try:
            with open("/proc/meminfo") as f:
                mem = f.read()
            avail_mb = int(re.search(r"MemAvailable:\s+(\d+)", mem).group(1)) // 1024
            biggest_mb = models[0][1] // (1024*1024)
            if avail_mb < biggest_mb + 300:
                fail(f"ОЗУ ({avail_mb} МБ) < модель ({biggest_mb} МБ) + запас",
                     "перезагрузка телефона или закрытие приложений", level="warning")
            else:
                ok(f"ОЗУ хватает для {os.path.basename(models[0][0])}",
                   f"{avail_mb} МБ свободно, модель ~{biggest_mb} МБ")
        except Exception:
            pass
    else:
        fail("Модели GGUF не найдены",
             "скачай Qwen2.5-Coder-3B-Q4_K_M.gguf в ~/ (см. INSTALL.md)")


def check_termux_api():
    section("TERMUX:API")
    ok_count = 0
    for cmd, label in TERMUX_API:
        if has_cmd(cmd):
            ok(label, cmd)
            ok_count += 1
        else:
            fail(label, "pkg install termux-api + приложение Termux:API",
                 level="warning")
    console.print()
    if ok_count == 0:
        fail("Termux:API не установлен",
             "Установи приложение Termux:API из F-Droid + pkg install termux-api")


def check_storage():
    section("ПРАВА / STORAGE")
    storage = os.path.join(HOME, "storage")
    if not os.path.isdir(storage):
        fail("~/storage не смонтирован",
             "termux-setup-storage (дай разрешение на файлы)")
        return
    subs = ["shared", "music", "downloads", "dcim"]
    found = 0
    for sub in subs:
        p = os.path.join(storage, sub)
        if os.path.islink(p) or os.path.isdir(p):
            if os.access(p, os.R_OK):
                ok(f"storage/{sub}", "читается")
                found += 1
            else:
                fail(f"storage/{sub} — нет доступа", "termux-setup-storage")
        else:
            fail(f"storage/{sub} отсутствует", "termux-setup-storage", level="warning")
    console.print()
    if found == len(subs):
        console.print(f"  [{GREEN_BRIGHT}]✔ Все {found} папок доступны[/]")


def check_network():
    section("СЕТЬ / API")
    console.print(f"  [{GRAY}]Проверка доступности API...[/]")
    console.print()

    sources = [
        ("api.ipify.org",        "https://api.ipify.org?format=json"),
        ("www.cbr-xml-daily.ru", "https://www.cbr-xml-daily.ru/daily_json.js"),
        ("api.coingecko.com",    "https://api.coingecko.com/api/v3/ping"),
        ("itunes.apple.com",     "https://itunes.apple.com/search?term=test&limit=1"),
    ]

    alive = 0
    for name, url in sources:
        r = run(f'curl -s -o /dev/null -w "%{{http_code}}" --max-time 5 "{url}"', timeout=7)
        code = (r.stdout or "").strip() if r else ""
        if code and code != "000" and code[0] in "23":
            ok(name, f"HTTP {code}")
            alive += 1
        elif code == "000":
            fail(name, "curl вернул 000 (нет сети или таймаут)", level="warning")
        else:
            fail(name, f"HTTP {code}", level="warning")

    console.print()
    if alive == len(sources):
        console.print(f"  [{GREEN_BRIGHT}]✔ Все {alive} источников живы[/]")
    else:
        console.print(f"  [{YELLOW}]⚠ Живых: {alive}/{len(sources)}[/]")

    cache_dir = os.path.join(HOME, ".cache/argonov")
    if os.path.isdir(cache_dir):
        files = os.listdir(cache_dir)
        size = sum(os.path.getsize(os.path.join(cache_dir, f))
                   for f in files if os.path.isfile(os.path.join(cache_dir, f)))
        console.print()
        info(f"Кэш: {len(files)} файлов  ·  {human_size(size)}")
        if size > 5_000_000:
            fail("Кэш > 5 МБ", "python ~/net_helper.py --cache-clear", level="warning")


def check_configs():
    section("КОНФИГИ")
    configs = [
        (os.path.join(HOME, ".termux/colors.properties"), "Termux цвета"),
        (os.path.join(HOME, ".termux/termux.properties"), "Termux свойства"),
        (os.path.join(HOME, ".config/fish/config.fish"),  "Fish конфиг"),
    ]
    for path, label in configs:
        if os.path.isfile(path):
            sz = os.path.getsize(path)
            ok(label, f"{sz} б")
        else:
            fail(f"{label} не найден",
                 f"см. репо: {'termux-config' if 'termux' in path else 'fish-config'}",
                 level="warning")


def check_git():
    section("GIT")
    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
        fail(f"{REPO_DIR} — не git-репозиторий",
             "git clone https://github.com/Andreyfdfd/argonov-os.git ~/argonov-os")
        return

    os.chdir(REPO_DIR)
    r = run("git remote get-url origin")
    if r and r.stdout:
        ok("Remote", r.stdout.strip())

    r = run("git log --oneline -1")
    if r and r.stdout:
        ok("Last commit", r.stdout.strip()[:60])

    r = run("git status --porcelain")
    if r and r.stdout.strip():
        cnt = len(r.stdout.strip().split("\n"))
        fail(f"{cnt} несохранённых изменений", "argonov push", level="warning")
    else:
        ok("Working tree", "clean")

# ═══ ИТОГО ═══
def print_summary():
    section("ИТОГО")
    if not problems and not warnings:
        console.print(f"  [{GREEN_BRIGHT}]🎉 ВСЁ ИДЕАЛЬНО![/]")
        console.print()
        console.print(f"  [{GRAY}]Проблем: 0  ·  Предупреждений: 0[/]")
        console.print()
        return

    if problems:
        console.print(f"  [{RED}]🔴 Критических проблем: {len(problems)}[/]")
        for i, p in enumerate(problems, 1):
            console.print(f"     {i}. {p}")
        console.print()
        console.print(f"  [{CYAN}]💡 Как починить:[/]")
        seen = set()
        for h in fix_hints:
            if h not in seen:
                console.print(f"     [{YELLOW}]→[/] {h}")
                seen.add(h)

    if warnings:
        console.print()
        console.print(f"  [{YELLOW}]🟡 Предупреждений: {len(warnings)}[/]")
        for i, w in enumerate(warnings, 1):
            console.print(f"     {i}. {w}")

    console.print()
    if not problems:
        console.print(f"  [{GREEN_BRIGHT}]✔ Критических проблем нет[/]")

# ═══ MAIN ═══
def main():
    full = "--full" in sys.argv or "-f" in sys.argv

    console.print()
    console.print(Panel(
        Align.center(Group(
            Text("🩺 DOCTOR v3 — ДИАГНОСТИКА", style=f"bold {WHITE}"),
            Text(f"Terminal Argonov  ·  {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                 style=f"dim {GRAY}"),
        )),
        border_style=CYAN, padding=(0, 2)))

    check_system()
    check_scripts()
    check_symlinks()
    check_tools()
    check_ai()
    check_termux_api()
    check_storage()
    if full:
        check_network()
    else:
        section("СЕТЬ / API")
        console.print(f"  [{GRAY}]Пропущено (запусти с --full чтобы проверить)[/]")
    check_configs()
    check_git()
    print_summary()

    console.print()
    console.print(f"  [{GRAY}]Флаги: --full — включает проверку сети[/]")
    console.print(f"  [{GRAY}]       -f     — короткий алиас[/]")
    console.print()

    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n[{GRAY}]Прервано.[/]")
        sys.exit(130)
