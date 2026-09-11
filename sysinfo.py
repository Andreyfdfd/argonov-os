#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sysinfo v5 — центр управления + индикатор свежести курса"""

import subprocess, os, shutil, platform, re, sys
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~"))

G = "\033[92m"; DG = "\033[32m"; C = "\033[96m"; B = "\033[94m"
M = "\033[95m"; Y = "\033[93m"; R = "\033[91m"; W = "\033[97m"
DIM = "\033[2m"; BLD = "\033[1m"; RST = "\033[0m"

HOME = os.path.expanduser("~")

SOC_NAMES = {
    "SM8750": "Snapdragon 8 Elite",
    "SM8650": "Snapdragon 8 Gen 3",
    "SM8550": "Snapdragon 8 Gen 2",
    "SM8450": "Snapdragon 8 Gen 1",
    "SM8350": "Snapdragon 888",
    "SM8250": "Snapdragon 870/865",
    "SM8150": "Snapdragon 855",
    "SM7325": "Snapdragon 778G",
    "SM6375": "Snapdragon 695",
    "SM6225": "Snapdragon 680",
    "SM4350": "Snapdragon 480",
    "MT6989": "Dimensity 9300",
    "MT6985": "Dimensity 9200",
    "MT6983": "Dimensity 9000",
    "MT6895": "Dimensity 8100",
    "MT6877": "Dimensity 900",
    "MT6833": "Dimensity 700",
    "MT6769": "Helio G85/G80",
}

def humanize_soc(raw):
    if not raw or raw == "?": return "?"
    raw_upper = raw.upper().replace("QTI ", "").strip()
    for key, name in SOC_NAMES.items():
        if key.upper() in raw_upper: return name
    return raw_upper

def run(cmd, timeout=15):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except: return None

def getprop(p):
    r = run(f"getprop {p}")
    return r.stdout.strip() if r and r.stdout else "?"

def read_first(path, key):
    try:
        with open(path) as f:
            for line in f:
                if line.startswith(key): return line.split(":", 1)[1].strip()
    except: pass
    return "?"

def human_size(kb):
    try: kb = int(kb)
    except: return "?"
    for unit in ["КБ","МБ","ГБ","ТБ"]:
        if kb < 1024: return f"{kb:.1f} {unit}"
        kb /= 1024
    return f"{kb:.1f} ПБ"

def battery():
    r = run("termux-battery-status 2>/dev/null")
    if not r or not r.stdout: return None
    try:
        import json
        d = json.loads(r.stdout)
        return f"{d.get('percentage','?')}% ({d.get('status','?')})"
    except: return None

def has_cmd(c): return shutil.which(c) is not None

def cmd_version(cmd, flag="--version"):
    r = run(f"{cmd} {flag} 2>&1", timeout=5)
    if not r or not r.stdout: return "?"
    text = r.stdout.split("\n")[0]
    m = re.search(r"(\d+\.\d+(?:\.\d+)?)", text)
    if m: return m.group(1)
    r2 = run(f"{cmd} --help 2>&1 | head -3", timeout=5)
    if r2 and r2.stdout:
        m = re.search(r"(\d+\.\d+(?:\.\d+)?)", r2.stdout)
        if m: return m.group(1)
    return "?"

def get_pip_packages():
    r = run("pip list --format=freeze 2>/dev/null", timeout=30)
    out = {}
    if r and r.stdout:
        for line in r.stdout.strip().split("\n"):
            if "==" in line:
                n, v = line.split("==", 1)
                key = re.sub(r"[-_.]+", "-", n).lower()
                out[key] = v
    return out

def get_pkg_sizes():
    r = run("dpkg-query -W -f='${Package}\\t${Installed-Size}\\n' 2>/dev/null", timeout=15)
    out = {}
    if r and r.stdout:
        for line in r.stdout.strip().split("\n"):
            parts = line.split("\t")
            if len(parts) == 2:
                try: out[parts[0].lower()] = int(parts[1])
                except ValueError: pass
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
            pkg_key = re.sub(r"[-_.]+", "-", (parts[0] if len(parts) == 2 else base)).lower()
            total = 0
            try:
                with open(record, encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        fp = line.strip().split(",")[0]
                        full = os.path.join(sp, fp)
                        if os.path.isfile(full):
                            try: total += os.path.getsize(full)
                            except OSError: pass
                out[pkg_key] = total // 1024
            except OSError: continue
    except OSError: pass
    return out

def sep(): print(f"{G}═══════════════════════════════════════════════════{RST}")

def section(title):
    print()
    print(f"{M}[ {title} ]:{RST}")
    sep()

def item(icon, label, value, color=C):
    print(f"  {icon} {label} → {color}[ {value} ]{RST}")

def fmt_size(kb):
    if kb is None: return ""
    try: kb = int(kb)
    except: return ""
    if kb < 1024: return f"{kb} КБ"
    mb = kb / 1024
    if mb < 1024: return f"{mb:.1f} МБ"
    return f"{mb/1024:.2f} ГБ"

def size_part(kb):
    s = fmt_size(kb)
    return f" {DIM}[ {s} ]{RST}" if s else ""

def tool_line(label, cmd, flag, pkg_name, pkg_sizes):
    if has_cmd(cmd):
        v = cmd_version(cmd, flag)
        sz = pkg_sizes.get(pkg_name.lower()) if pkg_name else None
        print(f"  {G}✔{RST} {label} → {B}[ {v} ]{RST}{size_part(sz)}")
    else:
        print(f"  {R}✘{RST} {label} {DIM}[ not installed ]{RST}")

def py_line(name, version, size_kb=None):
    print(f"    {G}✔{RST} {name} → {B}[ {version} ]{RST}{size_part(size_kb)}")

def py_missing(name):
    print(f"    {R}✘{RST} {name} {DIM}[ not installed ]{RST}")

def py_section(title): print(f"{Y}  ▬ {title}:{RST}")

def py_check(pip_pkgs, pip_sizes, names):
    total = 0; any_found = False
    for m in names:
        key = re.sub(r"[-_.]+", "-", m).lower()
        if key in pip_pkgs:
            sz = pip_sizes.get(key)
            py_line(m, pip_pkgs[key], sz)
            if sz: total += sz
            any_found = True
        else:
            py_missing(m)
    if any_found and total > 0:
        print(f"    {DIM}↳ Итого: {fmt_size(total)}{RST}")

TOOLS = [
    ("python", "python", "--version", "python"),
    ("git", "git", "--version", "git"),
    ("nano", "nano", "--version", "nano"),
    ("nvim", "nvim", "--version", "neovim"),
    ("tmux", "tmux", "-V", "tmux"),
    ("clang", "clang", "--version", "clang"),
    ("rustc", "rustc", "--version", "rust"),
    ("cargo", "cargo", "--version", "rust"),
    ("node", "node", "--version", "nodejs-lts"),
    ("npm", "npm", "--version", "nodejs-lts"),
    ("fish", "fish", "--version", "fish"),
    ("starship", "starship", "--version", "starship"),
    ("eza", "eza", "--version", "eza"),
    ("bat", "bat", "--version", "bat"),
    ("fd", "fd", "--version", "fd"),
    ("fzf", "fzf", "--version", "fzf"),
    ("rg", "rg", "--version", "ripgrep"),
    ("zoxide", "zoxide", "--version", "zoxide"),
    ("curl", "curl", "--version", "curl"),
    ("wget", "wget", "--version", "wget"),
    ("aria2c", "aria2c", "--version", "aria2"),
    ("chafa", "chafa", "--version", "chafa"),
    ("ffmpeg", "ffmpeg", "-version", "ffmpeg"),
    ("jq", "jq", "--version", "jq"),
    ("yq", "yq", "--version", "python-yq"),
    ("duf", "duf", "--version", "duf"),
    ("ncdu", "ncdu", "--version", "ncdu"),
    ("glow", "glow", "--version", "glow"),
    ("tree", "tree", "--version", "tree"),
    ("llama-server", "llama-server", "-h", "llama-cpp"),
]

DB_SERVERS = [
    ("SQLite3", "sqlite3", "--version", "sqlite"),
    ("PostgreSQL", "psql", "--version", "postgresql"),
    ("Redis Server", "redis-server", "--version", "redis"),
    ("MySQL", "mysql", "--version", "mysql"),
    ("MariaDB", "mariadb", "--version", "mariadb"),
    ("MongoDB", "mongod", "--version", "mongodb"),
]

DB_PIP = ["sqlalchemy","aiosqlite","asyncpg","psycopg2","psycopg2-binary",
          "redis","aioredis","pymongo","tinydb","alembic"]

def main():
    pip_pkgs = get_pip_packages()
    pip_sizes = get_pip_sizes()
    pkg_sizes = get_pkg_sizes()

    print(f"{C}┌─────────────────────────────────────────────────┐{RST}")
    print(f"{C}│{RST}      {BLD}{W}ЦЕНТР УПРАВЛЕНИЯ СРЕДОЙ TERMUX{RST}       {C}│{RST}")
    print(f"{C}└─────────────────────────────────────────────────┘{RST}")

    # ═══ ЖЕЛЕЗО ═══
    section("СПЕЦИФИКАЦИЯ ЖЕЛЕЗА И ПО")
    model = getprop("ro.product.model")
    market = getprop("ro.product.marketname") or getprop("ro.product.odm.marketname")
    soc_raw = getprop("ro.soc.model") or getprop("ro.board.platform")
    soc_manuf = getprop("ro.soc.manufacturer") or "Qualcomm"
    soc_human = humanize_soc(soc_raw)
    abi = getprop("ro.product.cpu.abi")

    if market and market != "?":
        item("📱", "Устройство:          ", f"{market} ({model})")
    else:
        item("📱", "Модель девайса:      ", f"{model}")
    item("⚡", "SoC:                 ", f"{soc_manuf} {soc_human}")
    item("💻", "Процессор:           ", f"ARM ({os.cpu_count() or '?'} ядер, {abi})")
    item("📱", "Android:             ", getprop("ro.build.version.release"))
    kern = platform.release()
    if kern:
        kern_ver = kern.split("-")[0] if "-" in kern else kern
        item("🧩", "Ядро Linux:          ", f"Linux {kern_ver}", color=DG)

    # ═══ РЕСУРСЫ ═══
    section("СИСТЕМНЫЕ РЕСУРСЫ")
    bat = battery()
    if bat: print(f"  🔋 Батарея: {G}{bat}{RST}")
    try:
        total = read_first("/proc/meminfo", "MemTotal")
        avail = read_first("/proc/meminfo", "MemAvailable")
        t_h = human_size(int(total.split()[0]))
        a_h = human_size(int(avail.split()[0]))
        pct = int(int(avail.split()[0]) / int(total.split()[0]) * 100)
        print(f"  💻 Память ОЗУ: {G}{a_h}{RST} / {t_h} ({pct}%)")
    except: pass
    try:
        u = shutil.disk_usage(HOME)
        free_gb = u.free // (1024**3)
        total_gb = (u.free + u.used) // (1024**3)
        pct_used = int(u.used / (u.free + u.used) * 100) if (u.free + u.used) > 0 else 0
        print(f"  💾 Накопитель: {G}{free_gb} ГБ свободно{RST} / {total_gb} ГБ ({pct_used}% занято)")
    except: pass
    try:
        code_bytes, py_files = 0, 0
        for f in os.listdir(HOME):
            fp = os.path.join(HOME, f)
            if os.path.isfile(fp) and f.endswith((".py", ".sh", ".fish")):
                code_bytes += os.path.getsize(fp)
                py_files += 1
        print(f"  📦 Объем кода: {G}{code_bytes/(1024*1024):.1f} МБ{RST} (Файлов Python: {G}{py_files}{RST})")
    except: pass

    # ═══ КУРС ВАЛЮТ (с индикатором) ═══
    section("КУРС ВАЛЮТ (онлайн)")
    try:
        from net_helper import get_fx_rates, freshness_badge_plain
        fx, fx_src, fx_meta = get_fx_rates(with_meta=True)
        if fx:
            badge = freshness_badge_plain(fx_meta)
            # Цвет бейджа
            if fx_meta and fx_meta.get("fresh"):
                bcol = G
            elif fx_meta and fx_meta.get("stale"):
                bcol = R
            else:
                bcol = Y
            print(f"  💵 1 USD  →  {G}{fx['USD_RUB']:.2f} ₽{RST}    {bcol}{badge}{RST}")
            if fx.get("EUR_RUB"):
                print(f"  💶 1 EUR  →  {G}{fx['EUR_RUB']:.2f} ₽{RST}")
            if fx.get("USD_EUR"):
                print(f"  💵 1 USD  →  {C}{fx['USD_EUR']:.4f} €{RST}")
            upd = fx.get("updated", "")
            if upd:
                print(f"  {DIM}🕐 {upd}  ·  📡 {fx_src}{RST}")
        else:
            print(f"  {R}✘{RST} {DIM}Все источники курса недоступны{RST}")
    except ImportError:
        print(f"  {R}✘{RST} {DIM}net_helper.py не найден{RST}")
    except Exception as e:
        print(f"  {R}✘{RST} {DIM}{e}{RST}")

    # ═══ ИНСТРУМЕНТЫ ═══
    section("СИСТЕМНЫЕ ИНСТРУМЕНТЫ")
    for label, cmd, flag, pkg in TOOLS:
        tool_line(label, cmd, flag, pkg, pkg_sizes)

    # ═══ PYTHON-МОДУЛИ ═══
    section("МОДУЛИ РАЗРАБОТКИ PYTHON")
    py_section("Интерфейс и логи")
    py_check(pip_pkgs, pip_sizes, ["rich", "customtkinter", "flet", "loguru"])
    py_section("Сеть и парсинг веб-страниц")
    py_check(pip_pkgs, pip_sizes, ["requests", "httpx", "aiohttp", "beautifulsoup4", "lxml"])
    py_section("Веб-серверы. Боты и ORM")
    py_check(pip_pkgs, pip_sizes, ["fastapi", "uvicorn", "pydantic", "aiogram", "sqlalchemy"])

    section("РАСШИРЕННЫЕ БИБЛИОТЕКИ")
    py_section("Система и мониторинг")
    py_check(pip_pkgs, pip_sizes, ["psutil", "colorama", "tqdm", "halo"])
    py_section("Визуал и утилиты")
    py_check(pip_pkgs, pip_sizes, ["pyfiglet", "qrcode", "pillow", "pyperclip", "prompt_toolkit"])
    py_section("Сеть и данные")
    py_check(pip_pkgs, pip_sizes, ["feedparser", "python-whois", "dnspython", "python-dotenv", "mutagen", "cryptography"])

    # ═══ БД ═══
    section("БАЗЫ ДАННЫХ")
    py_section("Серверы БД")
    found = False
    for label, cmd, flag, pkg in DB_SERVERS:
        if has_cmd(cmd):
            tool_line(label, cmd, flag, pkg, pkg_sizes); found = True
    if not found: print(f"    {R}✘{RST} {DIM}Не найдены{RST}")
    py_section("Python-клиенты и ORM")
    py_check(pip_pkgs, pip_sizes, DB_PIP)

    # ═══ ИТОГО ═══
    print()
    sep()
    print(f"{BLD}Всего пакетов Termux: {G}{len(pkg_sizes)}{RST}")
    print(f"{BLD}Всего pip-пакетов: {G}{len(pip_pkgs)}{RST}")
    print()

if __name__ == "__main__":
    main()
