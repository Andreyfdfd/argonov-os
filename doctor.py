#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Doctor v2 — расширенная диагностика ARGONOV OS"""

import os, sys, shutil, subprocess, platform, re
from datetime import datetime
from pathlib import Path

HOME = os.path.expanduser("~")
REPO_DIR = os.path.join(HOME, "argonov-os")
PREFIX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")

# ─── Цвета ───
G  = "\033[92m"; DG = "\033[32m"; C  = "\033[96m"; B  = "\033[94m"
M  = "\033[95m"; Y  = "\033[93m"; R  = "\033[91m"; W  = "\033[97m"
DIM = "\033[2m"; BLD = "\033[1m"; RST = "\033[0m"

# ─── Счётчики ───
problems = []      # 🔴 критично
warnings = []      # 🟡 предупреждения
fixed_hints = []   # что делать

SCRIPTS = [
    "argonov", "argonov-dump", "doctor.py", "net_helper.py",
    "ai.py", "hacktool.py", "randomaudio.py", "music_meta.py",
    "todo.py", "notes.py", "passmanager.py", "crypto_informer.py",
    "hacker_rpg.py", "download_zone.py", "matrix.py", "passgen.py",
    "sysinfo.py", "utils.py", "art.py",
]

TOOLS = [
    ("python",         "python",     "--version", "python",       True),
    ("pip",            "pip",        "--version", "python",       True),
    ("git",            "git",        "--version", "git",          True),
    ("fish",           "fish",       "--version", "fish",         False),
    ("starship",       "starship",   "--version", "starship",     False),
    ("eza",            "eza",        "--version", "eza",          False),
    ("bat",            "bat",        "--version", "bat",          False),
    ("fd",             "fd",         "--version", "fd",           False),
    ("fzf",            "fzf",        "--version", "fzf",          False),
    ("rg",             "rg",         "--version", "ripgrep",      False),
    ("zoxide",         "zoxide",     "--version", "zoxide",       False),
    ("jq",             "jq",         "--version", "jq",           False),
    ("curl",           "curl",       "--version", "curl",         True),
    ("wget",           "wget",       "--version", "wget",         False),
    ("aria2c",         "aria2c",     "--version", "aria2",        True),
    ("chafa",          "chafa",      "--version", "chafa",        False),
    ("viu",            "viu",        "--version", "viu",          False),
    ("ffmpeg",         "ffmpeg",     "-version",   "ffmpeg",       False),
    ("nmap",           "nmap",       "--version", "nmap",         False),
    ("llama-server",   "llama-server", "-h",       "llama-cpp",    True),
    ("tmux",           "tmux",       "-V",         "tmux",         False),
    ("tree",           "tree",       "--version", "tree",         False),
    ("ncdu",           "ncdu",       "--version", "ncdu",         False),
    ("gh",             "gh",         "--version", "gh",           False),
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

PY_MODULES = [
    ("rich",            "UI"),
    ("prompt_toolkit",  "UI"),
    ("requests",        "сеть"),
    ("cryptography",    "пароли"),
    ("mutagen",         "музыка"),
    ("feedparser",      "новости"),
    ("dnspython",       "DNS"),
    ("qrcode",          "QR"),
    ("pyperclip",       "буфер"),
    ("PIL",             "картинки"),
]

# ─── Утилиты ───
def sep(): print(f"{G}═══════════════════════════════════════════════════{RST}")
def section(title):
    print()
    print(f"{M}[ {title} ]:{RST}")
    sep()

def run(cmd, timeout=10):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True,
                              text=True, timeout=timeout)
    except Exception:
        return None

def getprop(p):
    r = run(f"getprop {p}")
    return r.stdout.strip() if r and r.stdout else "?"

def has_cmd(c): return shutil.which(c) is not None

def cmd_version(cmd, flag="--version"):
    r = run(f"{cmd} {flag} 2>&1 | head -1", timeout=4)
    if not r or not r.stdout: return "?"
    m = re.search(r"(\d+\.\d+(?:\.\d+)?)", r.stdout)
    return m.group(1) if m else "?"

def human_size(b):
    try: b = float(b)
    except: return "?"
    for u in ["Б","КБ","МБ","ГБ","ТБ"]:
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} ПБ"

def ok(msg, extra=""):
    print(f"  {G}✔{RST} {msg}" + (f" {DIM}{extra}{RST}" if extra else ""))

def fail(msg, fix=None, level="problem"):
    col = R if level == "problem" else Y
    mark = "✘" if level == "problem" else "⚠"
    print(f"  {col}{mark}{RST} {msg}")
    if fix:
        print(f"     {DIM}→ {fix}{RST}")
        if level == "problem":
            problems.append(msg)
            fixed_hints.append(fix)
        else:
            warnings.append(msg)

def info(msg):
    print(f"  {C}•{RST} {msg}")

# ═══════════════════════════════════════════════════════
#  СЕКЦИИ
# ═══════════════════════════════════════════════════════
def check_system():
    section("СИСТЕМА")
    model = getprop("ro.product.model")
    android = getprop("ro.build.version.release")
    info(f"{model}  ·  Android {android}")

    # ОЗУ
    try:
        with open("/proc/meminfo") as f:
            mem = f.read()
        total = int(re.search(r"MemTotal:\s+(\d+)", mem).group(1)) // 1024
        avail = int(re.search(r"MemAvailable:\s+(\d+)", mem).group(1)) // 1024
        pct = int(avail / total * 100)
        col = G if avail > 1500 else (Y if avail > 800 else R)
        print(f"  {C}💻{RST} ОЗУ: {col}{avail} МБ{RST} / {total} МБ ({pct}% свободно)")
        if avail < 1500:
            fail("Мало ОЗУ для AI (нужно ≥ 2 ГБ свободно)", "закрой лишние приложения",
                 level="warning")
    except Exception:
        fail("Не удалось прочитать /proc/meminfo")

    # Диск
    try:
        u = shutil.disk_usage(HOME)
        free_gb = u.free // (1024**3)
        total_gb = (u.free + u.used) // (1024**3)
        col = G if free_gb > 5 else (Y if free_gb > 2 else R)
        print(f"  {C}💾{RST} Диск: {col}{free_gb} ГБ свободно{RST} / {total_gb} ГБ")
        if free_gb < 2:
            fail("Мало места на диске", "очисти ~/.cache и ~/argonov_backups")
    except Exception:
        pass

    # Батарея
    r = run("termux-battery-status 2>/dev/null")
    if r and r.stdout:
        try:
            import json
            d = json.loads(r.stdout)
            pct = d.get("percentage", "?")
            st = d.get("status", "?")
            col = G if str(pct).isdigit() and int(pct) > 20 else Y
            print(f"  {C}🔋{RST} Батарея: {col}{pct}%{RST} ({st})")
        except Exception:
            pass

def check_scripts():
    section("СКРИПТЫ")
    found = 0
    missing = []
    for f in SCRIPTS:
        path = os.path.join(HOME, f)
        if os.path.isfile(path):
            size = os.path.getsize(path)
            # Проверка на exec-бит (только для argonov и argonov-dump)
            if f in ("argonov", "argonov-dump"):
                if os.access(path, os.X_OK):
                    ok(f, f"{size} б  ·  +x")
                else:
                    fail(f"{f} — нет +x", f"chmod +x ~/{f}")
                    found += 1
            else:
                ok(f, f"{size} б")
                found += 1
        else:
            missing.append(f)
            fail(f"{f} не найден", "восстанови из дампа или git pull")

    print()
    if not missing:
        print(f"  {G}✔ Все скрипты на месте: {found}/{len(SCRIPTS)}{RST}")
    else:
        print(f"  {R}✘ Отсутствуют: {len(missing)}/{len(SCRIPTS)}{RST}")

def check_symlinks():
    section("СИМЛИНКИ / PATH")
    bin_dir = os.path.join(PREFIX, "bin")
    if not os.path.isdir(bin_dir):
        fail(f"{bin_dir} не найден")
        return

    links = {
        "argonov":     os.path.join(HOME, "argonov"),
        "argonov-dump":os.path.join(HOME, "argonov-dump"),
        "doctor":      os.path.join(HOME, "doctor.py"),
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
            fail(f"{name} — не в $PREFIX/bin",
                 f"ln -sf {target} {link}")

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
    print()
    print(f"  {G}✔ Установлено: {ok_count}/{len(TOOLS)}{RST}")

def check_ai():
    section("AI (модели + llama.cpp)")

    # llama-server
    if has_cmd("llama-server"):
        v = cmd_version("llama-server", "--version")
        ok("llama-server", v)
    else:
        fail("llama-server не установлен", "pkg install llama-cpp")

    # Модели
    models = []
    for d in [HOME, os.path.join(HOME, "models")]:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".gguf"):
                    fp = os.path.join(d, f)
                    try: sz = os.path.getsize(fp)
                    except: sz = 0
                    if sz > 50_000_000:
                        models.append((fp, sz))
    models.sort(key=lambda x: -x[1])

    if models:
        print()
        print(f"  {C}📦 Модели GGUF:[/]")
        for fp, sz in models:
            name = os.path.basename(fp)
            col = G if "qwen" in name.lower() else C
            print(f"    {col}•{RST} {name}  {DIM}({human_size(sz)}){RST}")
        # Проверка ОЗУ для самой большой модели
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
    print()
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
    # Проверяем ключевые подпапки
    subs = ["shared", "music", "downloads", "dcim"]
    found = 0
    for sub in subs:
        p = os.path.join(storage, sub)
        if os.path.islink(p) or os.path.isdir(p):
            if os.access(p, os.R_OK):
                ok(f"storage/{sub}", "читается")
                found += 1
            else:
                fail(f"storage/{sub} — нет доступа",
                     "termux-setup-storage")
        else:
            fail(f"storage/{sub} отсутствует", "termux-setup-storage", level="warning")
    print()
    if found == len(subs):
        print(f"  {G}✔ Все {found} папок доступны{RST}")

def check_network(full=False):
    section("СЕТЬ / API")
    print(f"  {DIM}Проверка доступности API...{RST}")
    print()

    sources = [
        ("api.ipify.org",             "https://api.ipify.org?format=json"),
        ("www.cbr-xml-daily.ru",      "https://www.cbr-xml-daily.ru/daily_json.js"),
        ("api.coingecko.com",         "https://api.coingecko.com/api/v3/ping"),
        ("itunes.apple.com",          "https://itunes.apple.com/search?term=test&limit=1"),
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

    print()
    if alive == len(sources):
        print(f"  {G}✔ Все {alive} источников живы{RST}")
    else:
        print(f"  {Y}⚠ Живых: {alive}/{len(sources)}{RST}")

    # Кэш
    cache_dir = os.path.join(HOME, ".cache/argonov")
    if os.path.isdir(cache_dir):
        files = os.listdir(cache_dir)
        size = sum(os.path.getsize(os.path.join(cache_dir, f))
                   for f in files if os.path.isfile(os.path.join(cache_dir, f)))
        print()
        info(f"Кэш: {len(files)} файлов  ·  {human_size(size)}")
        if size > 5_000_000:
            fail("Кэш > 5 МБ", "python ~/net_helper.py --cache-clear", level="warning")

def check_configs():
    section("КОНФИГИ")
    configs = [
        (os.path.join(HOME, ".termux/colors.properties"),     "Termux цвета"),
        (os.path.join(HOME, ".termux/termux.properties"),     "Termux свойства"),
        (os.path.join(HOME, ".config/fish/config.fish"),      "Fish конфиг"),
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

def print_summary():
    section("ИТОГО")
    if not problems and not warnings:
        print(f"  {G}🎉 ВСЁ ИДЕАЛЬНО!{RST}")
        print()
        print(f"  {DIM}Проблем: 0  ·  Предупреждений: 0{RST}")
        print()
        return

    if problems:
        print(f"  {R}🔴 Критических проблем: {len(problems)}{RST}")
        for i, p in enumerate(problems, 1):
            print(f"     {i}. {p}")
        print()
        print(f"  {C}💡 Как починить:{RST}")
        seen = set()
        for h in fixed_hints:
            if h not in seen:
                print(f"     {Y}→{RST} {h}")
                seen.add(h)

    if warnings:
        print()
        print(f"  {Y}🟡 Предупреждений: {len(warnings)}{RST}")
        for i, w in enumerate(warnings, 1):
            print(f"     {i}. {w}")

    print()
    if not problems:
        print(f"  {G}✔ Критических проблем нет{RST}")

# ═══════════════════════════════════════════════════════
def main():
    full = "--full" in sys.argv or "-f" in sys.argv

    print()
    print(f"{C}┌─────────────────────────────────────────────────┐{RST}")
    print(f"{C}│{RST}      {BLD}{W}🩺 DOCTOR v2 — ДИАГНОСТИКА{RST}              {C}│{RST}")
    print(f"{C}│{RST}      {DIM}Terminal Argonov  ·  {datetime.now().strftime('%d.%m.%Y %H:%M')}{RST}       {C}│{RST}")
    print(f"{C}└─────────────────────────────────────────────────┘{RST}")

    check_system()
    check_scripts()
    check_symlinks()
    check_tools()
    check_ai()
    check_termux_api()
    check_storage()
    if full:
        check_network(full=True)
    else:
        section("СЕТЬ / API")
        print(f"  {DIM}Пропущено (запусти с --full чтобы проверить){RST}")
    check_configs()
    check_git()
    print_summary()

    print()
    print(f"  {DIM}Флаги: --full — включает проверку сети{RST}")
    print(f"  {DIM}       -f     — короткий алиас{RST}")
    print()

    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{DIM}Прервано.{RST}")
        sys.exit(130)
