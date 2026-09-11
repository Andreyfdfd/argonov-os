# ARGONOV OS — Полный дамп всех скриптов

Дата: Fri Sep 11 15:55:11  2026
Устройство: RMX5090 / Android 16

---

## 📄 argonov

*12238 байт · 285 строк*

```bash
#!/data/data/com.termux/files/usr/bin/bash
# ═══════════════════════════════════════════════════════
#  ARGONOV OS v1.3 — art с поиском и welcome
# ═══════════════════════════════════════════════════════

ARGONOV_VERSION="1.3.0"
REPO_DIR="$HOME/argonov-os"
BACKUP_DIR="$HOME/argonov_backups"

G="\033[92m"; DG="\033[32m"; C="\033[96m"; B="\033[94m"
M="\033[95m"; Y="\033[93m"; R="\033[91m"; W="\033[97m"
DIM="\033[2m"; BLD="\033[1m"; RST="\033[0m"

header() {
    echo ""
    echo -e "${C}┌─────────────────────────────────────────────────┐${RST}"
    echo -e "${C}│${RST}          ${BLD}${W}⚡  A R G O N O V   O S  ⚡${RST}          ${C}│${RST}"
    echo -e "${C}│${RST}       ${DIM}Кастомная оболочка для Termux${RST}          ${C}│${RST}"
    echo -e "${C}│${RST}                ${DIM}v${ARGONOV_VERSION}${RST}                       ${C}│${RST}"
    echo -e "${C}└─────────────────────────────────────────────────┘${RST}"
    echo ""
}

show_help() {
    header
    echo -e "${M}[ КОМАНДЫ ]:${RST}"
    echo -e "${G}═══════════════════════════════════════════════════════${RST}"
    echo ""
    echo -e "  ${Y}🧠 ${C}ai${RST}      · ${Y}📈 ${C}crypto${RST}    · ${Y}🎵 ${C}music${RST}"
    echo -e "  ${Y}📌 ${C}todo${RST}    · ${Y}📝 ${C}notes${RST}     · ${Y}🔒 ${C}pm${RST}"
    echo -e "  ${Y}🎮 ${C}hack${RST}    · ${Y}🕹  ${C}rpg${RST}       · ${Y}📥 ${C}d${RST}"
    echo -e "  ${Y}🌧  ${C}m${RST}       · ${Y}🔐 ${C}p${RST}         · ${Y}⚡ ${C}s${RST}"
    echo -e "  ${Y}📦 ${C}util${RST}    · ${Y}🎨 ${C}art${RST}"
    echo ""
    echo -e "${M}[ ART ]:${RST}"
    echo -e "${G}═══════════════════════════════════════════════════════${RST}"
    echo ""
    echo -e "  ${C}argonov art${RST}               — показать welcome"
    echo -e "  ${C}argonov art <имя>${RST}         — найти и показать"
    echo -e "  ${C}argonov art <имя> set${RST}     — установить как welcome"
    echo -e "  ${C}argonov art reset${RST}         — сбросить welcome"
    echo -e "  ${C}argonov art list${RST}          — список картинок"
    echo ""
    echo -e "${M}[ GIT / БЭКАПЫ ]:${RST}"
    echo -e "${G}═══════════════════════════════════════════════════════${RST}"
    echo ""
    echo -e "  ${C}push · pull · status · backup · restore · doctor${RST}"
    echo ""
}

show_menu() {
    while true; do
        header
        echo -e "  ${C}1${RST})  🧠  ai          ${C}2${RST})  📈  crypto"
        echo -e "  ${C}3${RST})  🎵  music       ${C}4${RST})  📌  todo"
        echo -e "  ${C}5${RST})  📝  notes       ${C}6${RST})  🔒  pm"
        echo -e "  ${C}7${RST})  🎮  hack        ${C}8${RST})  🕹   rpg"
        echo -e "  ${C}9${RST})  📥  d           ${C}10${RST}) 🌧   m"
        echo -e "  ${C}11${RST}) 🔐  p           ${C}12${RST}) ⚡  s"
        echo -e "  ${C}13${RST}) 📦  util        ${C}14${RST}) 🎨  art"
        echo ""
        echo -e "  ${C}p${RST})   🚀  push    ${C}l${RST})   ⬇️   pull"
        echo -e "  ${C}st${RST})  📊  status  ${C}b${RST})   💾  backup"
        echo ""
        echo -e "  ${C}h${RST})   ❓  Справка  ${C}q${RST})   🚪  Выход"
        echo ""
        echo -ne "${BLD}${M}╰─❯ ${RST}"
        read -r c
        case "$c" in
            1) run_ai ;;
            2) run_crypto ;;
            3) run_music ;;
            4) run_todo ;;
            5) run_notes ;;
            6) run_pm ;;
            7) run_hack ;;
            8) run_rpg ;;
            9) run_d ;;
            10) run_m ;;
            11) run_p ;;
            12) run_s ;;
            13) run_util ;;
            14) run_art ;;
            p|push) do_push; echo -ne "${DIM}Enter...${RST}"; read -r ;;
            l|pull) do_pull; echo -ne "${DIM}Enter...${RST}"; read -r ;;
            st|status) do_status; echo -ne "${DIM}Enter...${RST}"; read -r ;;
            b|backup) do_backup ;;
            h|help) show_help; echo -ne "${DIM}Enter...${RST}"; read -r ;;
            q|exit|quit) echo -e "${DIM}До связи! 🖖${RST}"; exit 0 ;;
            *) echo -e "${R}❌ Неизвестно${RST}"; sleep 1 ;;
        esac
    done
}

check_py() {
    if [ ! -f "$1" ]; then
        echo -e "${R}❌ Не найден: $1${RST}"; sleep 2; return 1
    fi
    return 0
}

run_ai()      { check_py ~/ai.py && python ~/ai.py ; }
run_crypto()  { check_py ~/crypto_informer.py && python ~/crypto_informer.py ; }
run_music()   { check_py ~/randomaudio.py && python ~/randomaudio.py ; }
run_todo()    { check_py ~/todo.py && python ~/todo.py ; }
run_notes()   { check_py ~/notes.py && python ~/notes.py ; }
run_pm()      { check_py ~/passmanager.py && python ~/passmanager.py ; }
run_hack()    { check_py ~/hacktool.py && python ~/hacktool.py ; }
run_rpg()     { check_py ~/hacker_rpg.py && python ~/hacker_rpg.py ; }
run_d()       { check_py ~/download_zone.py && python ~/download_zone.py ; }
run_m()       { check_py ~/matrix.py && python ~/matrix.py ; }
run_p()       { check_py ~/passgen.py && python ~/passgen.py ; }
run_s()       { check_py ~/sysinfo.py && python ~/sysinfo.py ; }
run_util()    { check_py ~/utils.py && python ~/utils.py ; }
run_art()     { check_py ~/art.py && python ~/art.py ; }

do_push() {
    if [ ! -d "$REPO_DIR/.git" ]; then
        echo -e "${R}❌ $REPO_DIR не git-репозиторий${RST}"; return 1
    fi
    echo -e "${Y}⚙ Копирую актуальные файлы...${RST}"
    cp ~/argonov "$REPO_DIR/" 2>/dev/null
    for f in ai.py crypto_informer.py download_zone.py hacktool.py matrix.py \
             music_meta.py notes.py passmanager.py passgen.py randomaudio.py \
             sysinfo.py todo.py utils.py hacker_rpg.py art.py; do
        cp ~/"$f" "$REPO_DIR/" 2>/dev/null
    done
    [ -f ~/.config/fish/config.fish ] && cp ~/.config/fish/config.fish "$REPO_DIR/fish-config/config.fish" 2>/dev/null

    cd "$REPO_DIR" || return 1
    git add .
    if git diff --cached --quiet; then
        echo -e "${DIM}Нет изменений${RST}"; return 0
    fi
    ts=$(date +"%Y-%m-%d %H:%M")
    git commit -m "Update $ts" >/dev/null
    echo -e "${Y}⚙ Отправляю на GitHub...${RST}"
    git push origin main 2>&1 | tail -3
    echo -e "${G}✔ Готово${RST}"
}

do_pull() {
    if [ ! -d "$REPO_DIR/.git" ]; then
        echo -e "${R}❌ $REPO_DIR не git${RST}"; return 1
    fi
    cd "$REPO_DIR" || return 1
    git pull origin main 2>&1 | tail -5
    cp *.py argonov "$HOME/" 2>/dev/null
    chmod +x "$HOME/argonov"
    echo -e "${G}✔ Готово${RST}"
}

do_status() {
    if [ ! -d "$REPO_DIR/.git" ]; then
        echo -e "${R}❌ Нет репо${RST}"; return 1
    fi
    cd "$REPO_DIR" || return 1
    echo -e "${C}═══ GIT STATUS ═══${RST}"
    git status -s
    echo ""
    echo -e "${C}═══ КОММИТЫ ═══${RST}"
    git log --oneline -5
    echo ""
    echo -e "${C}═══ REMOTE ═══${RST}"
    git remote -v
}

do_backup() {
    mkdir -p "$BACKUP_DIR"
    ts=$(date +%Y%m%d_%H%M%S)
    file="$BACKUP_DIR/argonov_backup_${ts}.tar.gz"
    echo -e "${Y}⚙ Бэкап...${RST}"
    cd "$HOME" || exit 1
    tar -czf "$file" \
        --exclude='argonov_backups' --exclude='.cache' --exclude='.cargo' \
        --exclude='storage' \
        ai.py crypto_informer.py randomaudio.py todo.py notes.py \
        passmanager.py hacktool.py hacker_rpg.py download_zone.py matrix.py \
        passgen.py sysinfo.py utils.py music_meta.py art.py argonov \
        .ai_config.json .ai_context.json .crypto_watchlist.json \
        .todo.json .notes.json .pm.vault .music_favorites.json \
        .hacker_rpg_save.json .argonov_welcome_image \
        .config/fish .termux \
        music_cache ai_chats 2>/dev/null
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        echo -e "${G}✔ $file ${DIM}($size)${RST}"
    fi
    sleep 2
}

do_restore() {
    mkdir -p "$BACKUP_DIR"
    if [ -z "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]; then
        echo -e "${R}❌ Нет бэкапов${RST}"; sleep 2; return
    fi
    echo -e "${Y}Доступные бэкапы:${RST}"
    ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | awk '{print "  " $NF " (" $5 ")"}'
    echo ""
    echo -ne "${M}Путь к бэкапу> ${RST}"; read -r bf
    if [ -f "$bf" ]; then
        cd "$HOME" && tar -xzf "$bf"
        echo -e "${G}✔ Восстановлено${RST}"
    else
        echo -e "${R}❌ Не найден${RST}"
    fi
    sleep 2
}

do_doctor() {
    header
    echo -e "${M}[ ПРОВЕРКА ]:${RST}"
    echo -e "${G}═══════════════════════════════════════════════════════${RST}"
    echo ""
    cf() {
        [ -f "$1" ] && echo -e "  ${G}✔${RST} $1" || echo -e "  ${R}✘${RST} $1"
    }
    cc() {
        command -v "$1" &>/dev/null && echo -e "  ${G}✔${RST} $1" || echo -e "  ${R}✘${RST} $1"
    }
    echo -e "${C}📂 Скрипты:${RST}"
    for f in ai.py crypto_informer.py randomaudio.py todo.py notes.py \
             passmanager.py hacktool.py hacker_rpg.py download_zone.py matrix.py \
             passgen.py sysinfo.py utils.py music_meta.py art.py argonov; do
        cf "$HOME/$f"
    done
    echo ""
    echo -e "${C}⚙ Утилиты:${RST}"
    for c in python pip git fish llama-server viu chafa gh; do cc "$c"; done
    echo ""
    echo -e "${C}🧠 Модели:${RST}"
    for f in ~/*.gguf; do
        [ -f "$f" ] && echo -e "  ${G}✔${RST} $(basename "$f") ${DIM}($(du -h "$f"|cut -f1))${RST}"
    done
    echo ""
    echo -e "${C}🎨 Welcome-картинка:${RST}"
    if [ -f "$HOME/.argonov_welcome_image" ]; then
        wfile=$(cat "$HOME/.argonov_welcome_image")
        if [ -f "$wfile" ]; then
            echo -e "  ${G}✔${RST} $(basename "$wfile")"
        else
            echo -e "  ${Y}⚠${RST} Файл не найден: $wfile"
        fi
    else
        echo -e "  ${DIM}не установлена (по умолчанию ~/fantasy.png)${RST}"
    fi
    echo ""
    echo -e "${C}🌐 Git:${RST}"
    [ -d "$REPO_DIR/.git" ] && echo -e "  ${G}✔${RST} $REPO_DIR" || echo -e "  ${R}✘${RST} Нет репо"
    echo ""
    echo -ne "${DIM}Enter...${RST}"; read -r
}

case "$1" in
    "")              show_menu ;;
    ai)              run_ai ;;
    crypto)          run_crypto ;;
    music)           run_music ;;
    todo)            shift; python ~/todo.py "$@" ;;
    notes)           run_notes ;;
    pm)              run_pm ;;
    hack)            run_hack ;;
    rpg|game)        run_rpg ;;
    d|download)      run_d ;;
    m|matrix)        run_m ;;
    p|pass)          run_p ;;
    s|sysinfo)       run_s ;;
    util)            run_util ;;
    art)             shift; python ~/art.py "$@" ;;
    plate)           python ~/sysinfo.py; echo "" ;;
    push)            do_push ;;
    pull)            do_pull ;;
    status)          do_status ;;
    backup)          do_backup ;;
    restore)         do_restore ;;
    doctor)          do_doctor ;;
    help|-h|--help)  show_help ;;
    version|-v)      echo -e "${G}Argonov OS v${ARGONOV_VERSION}${RST}" ;;
    *)
        echo -e "${R}❌ Неизвестно: $1${RST}"
        echo -e "${DIM}Используй: ${C}argonov help${RST}"
        exit 1
        ;;
esac
```

---

## 📄 argonov-dump

*7223 байт · 188 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Argonov Dump — сборка ARGONOV_FULL_DUMP.md + push в GitHub"""

import os, sys, subprocess, time
from datetime import datetime

HOME = os.path.expanduser("~")
DUMP_FILE = os.path.join(HOME, "ARGONOV_FULL_DUMP.md")
REPO_DIR  = os.path.join(HOME, "argonov-os")

# ─── Файлы для дампа ───
SCRIPTS = [
    ("argonov",           "bash"),
    ("argonov-dump",      "python"),
    ("net_helper.py",     "python"),
    ("ai.py",             "python"),
    ("hacktool.py",       "python"),
    ("randomaudio.py",    "python"),
    ("music_meta.py",     "python"),
    ("todo.py",           "python"),
    ("notes.py",          "python"),
    ("passmanager.py",    "python"),
    ("crypto_informer.py","python"),
    ("hacker_rpg.py",     "python"),
    ("download_zone.py",  "python"),
    ("matrix.py",         "python"),
    ("passgen.py",        "python"),
    ("sysinfo.py",        "python"),
    ("utils.py",          "python"),
    ("art.py",            "python"),
]

G = "\033[92m"; C = "\033[96m"; Y = "\033[93m"; R = "\033[91m"
DIM = "\033[2m"; BLD = "\033[1m"; RST = "\033[0m"

def run(cmd, timeout=60):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True,
                              text=True, timeout=timeout)
    except Exception:
        return None

def getprop(p):
    r = run(f"getprop {p}")
    return r.stdout.strip() if r and r.stdout else "?"

def build_dump():
    print(f"{C}📦 Сборка дампа...{RST}")
    print()

    lines = []
    lines.append("# ARGONOV OS — Полный дамп всех скриптов")
    lines.append("")
    lines.append(f"Дата: {datetime.now().strftime('%a %b %d %H:%M:%S %Z %Y')}")
    lines.append(f"Устройство: {getprop('ro.product.model')} / Android {getprop('ro.build.version.release')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    included = 0
    skipped = []

    for fname, lang in SCRIPTS:
        path = os.path.join(HOME, fname)
        if not os.path.isfile(path):
            skipped.append(fname)
            print(f"  {Y}⚠{RST}  {fname} {DIM}[нет файла]{RST}")
            continue
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            skipped.append(fname)
            print(f"  {R}✘{RST}  {fname} {DIM}[{e}]{RST}")
            continue

        size = os.path.getsize(path)
        lines.append(f"## 📄 {fname}")
        lines.append("")
        lines.append(f"*{size} байт · {content.count(chr(10))+1} строк*")
        lines.append("")
        lines.append(f"```{lang}")
        lines.append(content.rstrip())
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
        included += 1
        print(f"  {G}✔{RST}  {fname} {DIM}[{size} б · {content.count(chr(10))+1} строк]{RST}")

    with open(DUMP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    total_size = os.path.getsize(DUMP_FILE)
    total_lines = sum(1 for _ in open(DUMP_FILE, encoding="utf-8"))

    print()
    print(f"{G}✅ Дамп собран:{RST}  {BLD}{DUMP_FILE}{RST}")
    print(f"   {C}{included}{RST} скриптов  ·  {total_lines} строк  ·  {total_size//1024} КБ")
    if skipped:
        print(f"   {Y}пропущено: {len(skipped)} ({', '.join(skipped)}){RST}")
    print()
    return included

def do_push():
    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
        print(f"{R}❌ {REPO_DIR} — не git-репозиторий{RST}")
        print(f"{DIM}   Сначала: argonov push (создаст и запушит){RST}")
        return False

    print(f"{C}⚙ Копирую свежие скрипты в репо...{RST}")
    # Копируем всё из SCRIPTS + конфиги
    for fname, _ in SCRIPTS:
        src = os.path.join(HOME, fname)
        if os.path.isfile(src):
            subprocess.run(f'cp "{src}" "{REPO_DIR}/"', shell=True)

    # Дамп тоже кладём в репо
    subprocess.run(f'cp "{DUMP_FILE}" "{REPO_DIR}/"', shell=True)

    # fish config
    fish_src = os.path.join(HOME, ".config/fish/config.fish")
    fish_dst = os.path.join(REPO_DIR, "fish-config/config.fish")
    if os.path.isfile(fish_src):
        os.makedirs(os.path.dirname(fish_dst), exist_ok=True)
        subprocess.run(f'cp "{fish_src}" "{fish_dst}"', shell=True)

    os.chdir(REPO_DIR)
    subprocess.run("git add .", shell=True)

    r = run("git diff --cached --quiet", timeout=10)
    if r and r.returncode == 0:
        print(f"{DIM}Нет изменений для коммита{RST}")
        return True

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    subprocess.run(f'git commit -m "Update {ts}"', shell=True, capture_output=True)

    print(f"{C}⚙ Отправляю на GitHub...{RST}")
    r = run("git push origin main 2>&1", timeout=120)
    if r:
        tail = (r.stdout or r.stderr or "").strip().split("\n")
        for ln in tail[-5:]:
            print(f"   {DIM}{ln}{RST}")

    if r and r.returncode == 0:
        print(f"{G}✔ Push выполнен{RST}")
        return True
    else:
        print(f"{R}✘ Push вернул код {r.returncode if r else '?'}{RST}")
        return False

def main():
    print()
    print(f"{C}┌─────────────────────────────────────────────────┐{RST}")
    print(f"{C}│{RST}      {BLD}ARGONOV DUMP + PUSH{RST}                       {C}│{RST}")
    print(f"{C}└─────────────────────────────────────────────────┘{RST}")
    print()

    n = build_dump()
    if n == 0:
        print(f"{R}❌ Нечего собирать{RST}")
        sys.exit(1)

    print(f"{C}📤 Push в GitHub...{RST}")
    print()
    ok = do_push()
    print()

    if ok:
        print(f"{G}═══════════════════════════════════════════════════{RST}")
        print(f"{G}  ✅ ГОТОВО  ·  дамп + push{RST}")
        print(f"{G}═══════════════════════════════════════════════════{RST}")
    else:
        print(f"{Y}═══════════════════════════════════════════════════{RST}")
        print(f"{Y}  ⚠ Дамп собран, но push не прошёл{RST}")
        print(f"{Y}═══════════════════════════════════════════════════{RST}")
        print(f"{DIM}Проверь: cd ~/argonov-os && git status{RST}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{DIM}Прервано.{RST}")
        sys.exit(1)
```

---

## 📄 net_helper.py

*24789 байт · 617 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Net Helper v2.2 — fallback + кэш + force-refresh"""

import json, time, os, sys, hashlib
import urllib.request, urllib.error, urllib.parse

DEFAULT_UA = "Mozilla/5.0 (Linux; Android 10; Termux) AppleWebKit/537.36"

CACHE_DIR         = os.path.expanduser("~/.cache/argonov")
CACHE_DEFAULT_TTL = 300
CACHE_MAX_AGE     = 86400
CACHE_DISABLED    = os.environ.get("ARGONOV_NO_CACHE") == "1"

_set_counter = 0

def _cache_path(key):
    safe  = hashlib.md5(key.encode("utf-8")).hexdigest()[:16]
    clean = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)[:32]
    return os.path.join(CACHE_DIR, f"{clean}_{safe}.json")

def cache_get_meta(key, ttl=CACHE_DEFAULT_TTL, allow_stale=False):
    if CACHE_DISABLED: return None, None
    p = _cache_path(key)
    if not os.path.exists(p): return None, None
    try:
        with open(p, encoding="utf-8") as f:
            obj = json.load(f)
    except Exception:
        return None, None
    ts = obj.get("ts", 0)
    age = time.time() - ts
    if age <= ttl:
        return obj.get("data"), {"ts": ts, "age": age, "fresh": True, "stale": False}
    if allow_stale and age <= CACHE_MAX_AGE:
        return obj.get("data"), {"ts": ts, "age": age, "fresh": False, "stale": True}
    return None, None

def cache_get(key, ttl=CACHE_DEFAULT_TTL):
    data, _ = cache_get_meta(key, ttl)
    return data

def cache_set(key, data):
    global _set_counter
    if CACHE_DISABLED: return
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        p   = _cache_path(key)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "data": data}, f, ensure_ascii=False)
        os.replace(tmp, p)
        _set_counter += 1
        if _set_counter % 50 == 0: cache_cleanup()
    except Exception:
        pass

def cache_clear():
    if not os.path.isdir(CACHE_DIR): return 0
    n = 0
    for f in os.listdir(CACHE_DIR):
        try: os.remove(os.path.join(CACHE_DIR, f)); n += 1
        except Exception: pass
    return n

def cache_cleanup(max_age=CACHE_MAX_AGE):
    if not os.path.isdir(CACHE_DIR): return 0
    now = time.time(); n = 0
    for f in os.listdir(CACHE_DIR):
        p = os.path.join(CACHE_DIR, f)
        try:
            if now - os.path.getmtime(p) > max_age:
                os.remove(p); n += 1
        except Exception: pass
    return n

def cache_info():
    if not os.path.isdir(CACHE_DIR):
        return {"files": 0, "size": 0, "dir": CACHE_DIR}
    files = [os.path.join(CACHE_DIR, f) for f in os.listdir(CACHE_DIR)]
    size  = sum(os.path.getsize(f) for f in files if os.path.isfile(f))
    return {"files": len(files), "size": size, "dir": CACHE_DIR}

# ═══════════════════════════════════════════════════════
def fetch(url, timeout=10, headers=None, parse="json"):
    h = {"User-Agent": DEFAULT_UA, "Accept": "*/*"}
    if headers: h.update(headers)
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read().decode("utf-8", errors="ignore")
        if parse == "json":
            try: return json.loads(data)
            except Exception: return None
        return data
    except Exception:
        return None

def get_json_cached(url, ttl=CACHE_DEFAULT_TTL, cache_key=None, timeout=10, headers=None):
    key = cache_key or f"json:{url}"
    cached = cache_get(key, ttl)
    if cached is not None: return cached
    data = fetch(url, timeout=timeout, headers=headers, parse="json")
    if data is not None: cache_set(key, data)
    return data

def get_text_cached(url, ttl=CACHE_DEFAULT_TTL, cache_key=None, timeout=10, headers=None):
    key = cache_key or f"text:{url}"
    cached = cache_get(key, ttl)
    if cached is not None: return cached
    data = fetch(url, timeout=timeout, headers=headers, parse="text")
    if data is not None: cache_set(key, data)
    return data

def try_sources(sources, timeout=8):
    for name, fn in sources:
        try:
            data = fn(timeout)
            if data: return data, name
        except Exception:
            continue
    return None, None

# ═══ КРИПТА ═══
def crypto_coingecko(timeout=8):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin,cardano&vs_currencies=usd,rub&include_24hr_change=true"
    data = fetch(url, timeout=timeout)
    if not data: return None
    out = {}
    for cid, d in data.items():
        out[cid] = {
            "symbol": {"bitcoin":"BTC","ethereum":"ETH","solana":"SOL",
                       "binancecoin":"BNB","cardano":"ADA"}.get(cid, cid.upper()[:4]),
            "name": {"bitcoin":"Bitcoin","ethereum":"Ethereum","solana":"Solana",
                     "binancecoin":"BNB","cardano":"Cardano"}.get(cid, cid.title()),
            "usd": d.get("usd", 0), "rub": d.get("rub", 0),
            "change_24h": d.get("usd_24h_change", 0),
        }
    return out if out else None

def crypto_coincap(timeout=8):
    url = "https://api.coincap.io/v2/assets?ids=bitcoin,ethereum,solana,binance-coin,cardano"
    data = fetch(url, timeout=timeout)
    if not data or "data" not in data: return None
    out = {}
    for a in data["data"]:
        cid = a["id"]
        cid_key = "binancecoin" if cid == "binance-coin" else cid
        out[cid_key] = {
            "symbol": a["symbol"], "name": a["name"],
            "usd": float(a["priceUsd"] or 0), "rub": 0,
            "change_24h": float(a.get("changePercent24Hr") or 0),
        }
    return out if out else None

def crypto_paprika(timeout=8):
    url = "https://api.coinpaprika.com/v1/tickers?quotes=USD,RUB"
    data = fetch(url, timeout=timeout)
    if not data: return None
    targets = {"btc-bitcoin":"bitcoin","eth-ethereum":"ethereum",
               "sol-solana":"solana","bnb-binance-coin":"binancecoin",
               "ada-cardano":"cardano"}
    out = {}
    for a in data:
        if a["id"] in targets:
            key = targets[a["id"]]
            q = a.get("quotes", {})
            out[key] = {
                "symbol": a["symbol"], "name": a["name"],
                "usd": q.get("USD", {}).get("price", 0),
                "rub": q.get("RUB", {}).get("price", 0),
                "change_24h": q.get("USD", {}).get("percent_change_24h", 0),
            }
    return out if out else None

def crypto_binance(timeout=8):
    symbols = {"BTCUSDT":"bitcoin","ETHUSDT":"ethereum","SOLUSDT":"solana",
               "BNBUSDT":"binancecoin","ADAUSDT":"cardano"}
    out = {}
    for sym, key in symbols.items():
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={sym}"
        d = fetch(url, timeout=timeout)
        if d and "lastPrice" in d:
            out[key] = {
                "symbol": key.upper()[:4], "name": key.title(),
                "usd": float(d["lastPrice"]), "rub": 0,
                "change_24h": float(d.get("priceChangePercent", 0)),
            }
    return out if out else None

def get_crypto_prices(ttl=CACHE_DEFAULT_TTL, with_meta=False, force=False):
    """
    force=True → игнорирует свежий кэш, делает live fetch.
    При падении сети всё равно берёт stale кэш.
    """
    key = "prices:crypto"
    if not force:
        cached, meta = cache_get_meta(key, ttl, allow_stale=True)
        if cached:
            src = cached.get("source", "кэш")
            label = f"{src} (STALE)" if meta["stale"] else f"{src} (кэш)"
            if with_meta: return cached.get("data"), label, meta
            return cached.get("data"), label

    sources = [
        ("CoinGecko",   crypto_coingecko),
        ("CoinPaprika", crypto_paprika),
        ("CoinCap",     crypto_coincap),
        ("Binance",     crypto_binance),
    ]
    data, source = try_sources(sources)
    if data:
        cache_set(key, {"data": data, "source": source})
        live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
        if with_meta: return data, source, live_meta
        return data, source

    stale = cache_get(key, ttl=CACHE_MAX_AGE)
    if stale:
        label = f"{stale.get('source','?')} (STALE)"
        stale_meta = {"fresh": False, "stale": True, "age": CACHE_MAX_AGE, "ts": 0}
        if with_meta: return stale.get("data"), label, stale_meta
        return stale.get("data"), label

    if with_meta: return None, None, None
    return None, None

# ═══ КУРС ВАЛЮТ ═══
def fx_cbr_xml(timeout=8):
    data = fetch("https://www.cbr-xml-daily.ru/daily_json.js", timeout=timeout)
    if not data or "Valute" not in data: return None
    v = data["Valute"]
    usd_rub = v.get("USD", {}).get("Value")
    eur_rub = v.get("EUR", {}).get("Value")
    if not usd_rub: return None
    return {
        "USD_RUB": usd_rub, "EUR_RUB": eur_rub,
        "USD_EUR": (usd_rub / eur_rub) if eur_rub else None,
        "updated": data.get("Date", "")[:10], "source": "ЦБ РФ",
    }

def fx_erapi(timeout=8):
    data = fetch("https://open.er-api.com/v6/latest/USD", timeout=timeout)
    if not data or data.get("result") != "success": return None
    rates = data.get("rates", {})
    usd_rub = rates.get("RUB"); usd_eur = rates.get("EUR")
    if not usd_rub: return None
    return {
        "USD_RUB": usd_rub,
        "EUR_RUB": (usd_rub / usd_eur) if usd_eur else None,
        "USD_EUR": usd_eur,
        "updated": data.get("time_last_update_utc", "")[:16],
        "source": "open.er-api.com",
    }

def fx_frankfurter(timeout=8):
    data = fetch("https://api.frankfurter.app/latest?from=USD&to=RUB,EUR", timeout=timeout)
    if not data or "rates" not in data: return None
    rates = data["rates"]
    usd_rub = rates.get("RUB"); usd_eur = rates.get("EUR")
    if not usd_rub: return None
    return {
        "USD_RUB": usd_rub,
        "EUR_RUB": (usd_rub / usd_eur) if usd_eur else None,
        "USD_EUR": usd_eur,
        "updated": data.get("date", ""), "source": "ECB (Frankfurter)",
    }

def fx_exhost(timeout=8):
    data = fetch("https://api.exchangerate.host/latest?base=USD&symbols=RUB,EUR", timeout=timeout)
    if not data or "rates" not in data: return None
    rates = data["rates"]
    usd_rub = rates.get("RUB"); usd_eur = rates.get("EUR")
    if not usd_rub: return None
    return {
        "USD_RUB": usd_rub,
        "EUR_RUB": (usd_rub / usd_eur) if usd_eur else None,
        "USD_EUR": usd_eur,
        "updated": data.get("date", ""), "source": "exchangerate.host",
    }

def get_fx_rates(ttl=1800, with_meta=False, force=False):
    key = "prices:fx"
    if not force:
        cached, meta = cache_get_meta(key, ttl, allow_stale=True)
        if cached:
            src = cached.get("source", "кэш")
            label = f"{src} (STALE)" if meta["stale"] else f"{src} (кэш)"
            if with_meta: return cached.get("data"), label, meta
            return cached.get("data"), label

    sources = [
        ("ЦБ РФ",            fx_cbr_xml),
        ("open.er-api",      fx_erapi),
        ("Frankfurter",      fx_frankfurter),
        ("exchangerate.host",fx_exhost),
    ]
    data, source = try_sources(sources)
    if data:
        cache_set(key, {"data": data, "source": source})
        live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
        if with_meta: return data, source, live_meta
        return data, source

    stale = cache_get(key, ttl=CACHE_MAX_AGE)
    if stale:
        label = f"{stale.get('source','?')} (STALE)"
        stale_meta = {"fresh": False, "stale": True, "age": CACHE_MAX_AGE, "ts": 0}
        if with_meta: return stale.get("data"), label, stale_meta
        return stale.get("data"), label

    if with_meta: return None, None, None
    return None, None

# ═══ ГЕО IP ═══
def ip_ipinfo(timeout=8):
    d = fetch("https://ipinfo.io/json", timeout=timeout)
    if not d or "ip" not in d: return None
    return {"ip": d.get("ip"), "city": d.get("city"), "region": d.get("region"),
            "country": d.get("country"), "org": d.get("org"),
            "timezone": d.get("timezone"), "loc": d.get("loc"),
            "source": "ipinfo.io"}

def ip_ipapi(timeout=8):
    d = fetch("http://ip-api.com/json/?fields=status,country,regionName,city,isp,query,timezone", timeout=timeout)
    if not d or d.get("status") != "success": return None
    return {"ip": d.get("query"), "city": d.get("city"), "region": d.get("regionName"),
            "country": d.get("country"), "org": d.get("isp"),
            "timezone": d.get("timezone"), "loc": "", "source": "ip-api.com"}

def ip_ipwhois(timeout=8):
    d = fetch("https://ipwhois.app/json/", timeout=timeout)
    if not d or not d.get("ip"): return None
    return {"ip": d.get("ip"), "city": d.get("city"), "region": d.get("region"),
            "country": d.get("country"), "org": d.get("org"),
            "timezone": d.get("timezone"),
            "loc": f"{d.get('latitude','')},{d.get('longitude','')}",
            "source": "ipwhois.app"}

def get_ip_info(ttl=3600, with_meta=False, force=False):
    key = "ip:info"
    if not force:
        cached, meta = cache_get_meta(key, ttl, allow_stale=True)
        if cached:
            src = cached.get("source", "кэш")
            label = f"{src} (STALE)" if meta["stale"] else f"{src} (кэш)"
            if with_meta: return cached.get("data"), label, meta
            return cached.get("data"), label

    sources = [("ipinfo.io", ip_ipinfo), ("ip-api.com", ip_ipapi), ("ipwhois.app", ip_ipwhois)]
    data, source = try_sources(sources)
    if data:
        cache_set(key, {"data": data, "source": source})
        live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
        if with_meta: return data, source, live_meta
        return data, source
    if with_meta: return None, None, None
    return None, None

# ═══ НОВОСТИ ═══
NEWS_FEEDS_RU = [
    ("Хабр",         "https://habr.com/ru/rss/all/all/"),
    ("N+1 Наука",    "https://nplus1.ru/rss"),
    ("3DNews",       "https://3dnews.ru/news/rss/"),
    ("IXBT",         "https://www.ixbt.com/export/news.rss"),
    ("Ferra",        "https://www.ferra.ru/rss/"),
    ("Код Дурова",   "https://kod.ru/rss"),
]
NEWS_FEEDS_GLOBAL = [
    ("TechCrunch",   "https://techcrunch.com/feed/"),
    ("MIT Tech",     "https://www.technologyreview.com/feed/"),
]

def get_news_feeds(include_global=False):
    feeds = list(NEWS_FEEDS_RU)
    if include_global: feeds += NEWS_FEEDS_GLOBAL
    return feeds

# ═══ ОБЛОЖКИ ═══
def cover_itunes(artist, title, timeout=8):
    q = urllib.parse.quote(f"{artist} {title}")
    url = f"https://itunes.apple.com/search?term={q}&entity=song&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("results"): return None
    art = d["results"][0].get("artworkUrl100", "")
    if art: return art.replace("100x100", "600x600")
    return None

def cover_deezer(artist, title, timeout=8):
    q = urllib.parse.quote(f"{artist} {title}")
    url = f"https://api.deezer.com/search?q={q}&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("data"): return None
    first = d["data"][0]
    return first.get("album", {}).get("cover_xl") or first.get("album", {}).get("cover_big")

def cover_lastfm(artist, title, timeout=8, api_key=None):
    if not api_key: return None
    q = urllib.parse.quote(artist)
    url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={q}&api_key={api_key}&format=json"
    d = fetch(url, timeout=timeout)
    if not d: return None
    imgs = d.get("artist", {}).get("image", [])
    for img in reversed(imgs):
        if img.get("#text"): return img["#text"]
    return None

def get_cover(artist, title, ttl=604800, with_meta=False, force=False):
    key = f"cover:{artist.lower()}|{title.lower()}"
    if not force:
        cached, meta = cache_get_meta(key, ttl)
        if cached:
            label = f"{cached.get('source','кэш')} (кэш)"
            if with_meta: return cached.get("url"), label, meta
            return cached.get("url"), label
    sources = [
        ("iTunes", lambda t: cover_itunes(artist, title, timeout=t)),
        ("Deezer", lambda t: cover_deezer(artist, title, timeout=t)),
    ]
    for name, fn in sources:
        try:
            url = fn(8)
            if url:
                cache_set(key, {"url": url, "source": name})
                live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
                if with_meta: return url, name, live_meta
                return url, name
        except Exception:
            continue
    if with_meta: return None, None, None
    return None, None

# ═══ МЕТАДАННЫЕ ═══
def meta_itunes(title, artist, timeout=8):
    q = urllib.parse.quote(f"{artist} {title}" if artist else title)
    url = f"https://itunes.apple.com/search?term={q}&entity=song&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("results"): return None
    r = d["results"][0]
    return {"title":  r.get("trackName","").strip(),
            "artist": r.get("artistName","").strip(),
            "album":  r.get("collectionName","").strip(),
            "genre":  r.get("primaryGenreName","").strip(),
            "year":   (r.get("releaseDate") or "")[:4],
            "source": "iTunes"}

def meta_deezer(title, artist, timeout=8):
    q = urllib.parse.quote(f"{artist} {title}" if artist else title)
    url = f"https://api.deezer.com/search?q={q}&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("data"): return None
    r = d["data"][0]
    return {"title":  r.get("title","").strip(),
            "artist": r.get("artist",{}).get("name","").strip(),
            "album":  r.get("album",{}).get("title","").strip(),
            "genre":  "", "year": "", "source": "Deezer"}

def meta_musicbrainz(title, artist, timeout=10):
    q = urllib.parse.quote(f"{artist} {title}" if artist else title)
    url = f"https://musicbrainz.org/ws/2/recording?query={q}&fmt=json&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("recordings"): return None
    rec = d["recordings"][0]
    credits = rec.get("artist-credit", [])
    artist_name = "".join((c.get("name","") + (c.get("joinphrase","") or "")) for c in credits).strip()
    releases = rec.get("releases", [])
    album = releases[0].get("title","").strip() if releases else ""
    year = ""
    if releases and releases[0].get("date"): year = releases[0]["date"][:4]
    genre = ""
    if rec.get("tags"): genre = rec["tags"][0].get("name","").capitalize()
    return {"title":  rec.get("title","").strip(),
            "artist": artist_name, "album": album,
            "genre":  genre, "year": year, "source": "MusicBrainz"}

def get_track_meta(title, artist="", ttl=604800, with_meta=False, force=False):
    key = f"meta:{artist.lower()}|{title.lower()}"
    if not force:
        cached, meta = cache_get_meta(key, ttl)
        if cached:
            label = f"{cached.get('source','кэш')} (кэш)"
            if with_meta: return cached.get("meta"), label, meta
            return cached.get("meta"), label
    sources = [
        ("iTunes",      lambda t: meta_itunes(title, artist, t)),
        ("Deezer",      lambda t: meta_deezer(title, artist, t)),
        ("MusicBrainz", lambda t: meta_musicbrainz(title, artist, t)),
    ]
    for name, fn in sources:
        try:
            meta_data = fn(10)
            if meta_data and meta_data.get("title"):
                cache_set(key, {"meta": meta_data, "source": name})
                live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
                if with_meta: return meta_data, name, live_meta
                return meta_data, name
        except Exception:
            continue
    if with_meta: return None, None, None
    return None, None

# ═══ БЕЙДЖ СВЕЖЕСТИ ═══
def freshness_badge(meta):
    if not meta:
        return "[dim]· нет данных[/]"
    if meta.get("fresh"):
        return "[bright_green]● LIVE[/]"
    if meta.get("stale"):
        age = meta.get("age", 0)
        if age < 3600:
            return f"[bright_red]⚠ STALE {int(age/60)}мин[/]"
        return f"[bright_red]⚠ STALE {age/3600:.1f}ч[/]"
    age = meta.get("age", 0)
    if age < 60:
        return "[bright_yellow]○ КЭШ <1мин[/]"
    if age < 3600:
        return f"[bright_yellow]○ КЭШ {int(age/60)}мин[/]"
    return f"[bright_yellow]○ КЭШ {age/3600:.1f}ч[/]"

def freshness_badge_plain(meta):
    if not meta: return "· нет"
    if meta.get("fresh"): return "● LIVE"
    if meta.get("stale"):
        age = meta.get("age", 0)
        return f"⚠ STALE {int(age/60)}мин" if age < 3600 else f"⚠ STALE {age/3600:.1f}ч"
    age = meta.get("age", 0)
    if age < 60: return "○ КЭШ <1мин"
    if age < 3600: return f"○ КЭШ {int(age/60)}мин"
    return f"○ КЭШ {age/3600:.1f}ч"

# ═══ SELFTEST + CLI ═══
def selftest():
    print("=" * 55)
    print("  net_helper v2.2 — self-test")
    print("=" * 55)
    print()
    info = cache_info()
    print(f"📁 Cache: {info['dir']}")
    print(f"   Файлов: {info['files']}  ·  Размер: {info['size']} байт")
    print(f"   Отключён: {CACHE_DISABLED}")
    print()

    print("🔍 1. fetch() — сеть...")
    t0 = time.time()
    d = fetch("https://api.ipify.org?format=json", timeout=8)
    print(f"   {'✔' if d else '✘'} [{time.time()-t0:.2f}с] {d}")
    print()

    print("🔍 2. get_fx_rates() — live...")
    t0 = time.time()
    fx, src, meta = get_fx_rates(with_meta=True, force=True)
    print(f"   {'✔' if fx else '✘'} [{time.time()-t0:.2f}с] {src}")
    print(f"     Бейдж: {freshness_badge_plain(meta)}")
    if fx: print(f"     USD_RUB = {fx.get('USD_RUB')}")
    print()

    print("🔍 3. get_fx_rates() — из кэша...")
    t0 = time.time()
    fx2, src2, meta2 = get_fx_rates(with_meta=True)
    dt = time.time() - t0
    print(f"   ✔ [{dt:.2f}с] {src2}")
    print(f"     Бейдж: {freshness_badge_plain(meta2)}")
    print(f"     {'✅ КЭШ РАБОТАЕТ' if dt < 0.5 else '⚠ Медленно'}")
    print()

    print("🔍 4. get_crypto_prices() — live (force)...")
    t0 = time.time()
    cr, src, meta = get_crypto_prices(with_meta=True, force=True)
    print(f"   {'✔' if cr else '✘'} [{time.time()-t0:.2f}с] {src}")
    print(f"     Бейдж: {freshness_badge_plain(meta)}")
    if cr:
        for cid, c in list(cr.items())[:3]:
            print(f"     {c['symbol']:5} = ${c['usd']:,.2f}")
    print()

    print("🔍 5. get_crypto_prices() — из кэша...")
    t0 = time.time()
    cr2, src2, meta2 = get_crypto_prices(with_meta=True)
    dt = time.time() - t0
    print(f"   ✔ [{dt:.2f}с] {src2}")
    print(f"     Бейдж: {freshness_badge_plain(meta2)}")
    print(f"     {'✅ КЭШ РАБОТАЕТ' if dt < 0.5 else '⚠ Медленно'}")
    print()

    print("🔍 6. get_crypto_prices(force=True) — обход кэша...")
    t0 = time.time()
    cr3, src3, meta3 = get_crypto_prices(with_meta=True, force=True)
    dt = time.time() - t0
    print(f"   ✔ [{dt:.2f}с] {src3}")
    print(f"     Бейдж: {freshness_badge_plain(meta3)}")
    print(f"     {'✅ FORCE РАБОТАЕТ (пошёл в сеть)' if dt > 0.2 else '⚠ Не пошёл в сеть'}")
    print()

    info = cache_info()
    print(f"📁 Итог: {info['files']} файлов · {info['size']} байт")
    print()
    print("=" * 55)

if __name__ == "__main__":
    if "--selftest" in sys.argv:        selftest()
    elif "--cache-info" in sys.argv:
        i = cache_info()
        print(f"Dir:   {i['dir']}\nFiles: {i['files']}\nSize:  {i['size']} байт")
    elif "--cache-clear" in sys.argv:
        print(f"✔ Удалено: {cache_clear()}")
    elif "--cache-cleanup" in sys.argv:
        print(f"✔ Удалено старого: {cache_cleanup()}")
    else:
        print("net_helper v2.2 — fallback + кэш + force")
        print()
        print("  python net_helper.py --selftest       — тест")
        print("  python net_helper.py --cache-info     — инфо")
        print("  python net_helper.py --cache-clear    — очистить")
        print("  python net_helper.py --cache-cleanup  — удалить старое")
        print()
        print("  ARGONOV_NO_CACHE=1                    — отключить кэш")
```

---

## 📄 ai.py

*26248 байт · 622 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI v15.5 — короткий промпт с примерами + pty.spawn"""

import os, sys, json, subprocess, time, re, signal, atexit, socket, threading
import urllib.request, urllib.error
import pty
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich.live import Live
from rich.box import SIMPLE_HEAD
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

console = Console()
HOME = os.path.expanduser("~")
CONFIG_FILE = os.path.join(HOME, ".ai_config.json")
HOST, PORT = "127.0.0.1", 8080
URL = f"http://{HOST}:{PORT}"

INTERACTIVE_KEYWORDS = [
    "randomaudio", "hacker_rpg", "matrix.py", "todo.py", "notes.py",
    "passmanager", "hacktool", "crypto_informer", "utils.py",
    "art.py", "music_meta", "ai.py",
    " vi ", "nano ", "vim ", "nvim ", "less ", "more ",
    "top", "htop", "btop",
]

def is_interactive(cmd):
    cl = " " + cmd.lower() + " "
    for kw in INTERACTIVE_KEYWORDS:
        if kw in cl: return True
    return False

STATE = {
    "model_path": None, "thinking": False, "auto": True,
    "agent": True, "auto_exec": False, "sandbox": True,
    "temp": 0.4, "max_tokens": 1024, "ctx_size": 2048, "threads": 4,
    "sys_prompt": "", "history": [], "proc": None, "ctx": {},
    "session_files": [],
}

def run(cmd, timeout=30):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except: return None

def hsize(b):
    for u in ["Б","КБ","МБ","ГБ"]:
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} ТБ"

def load_cfg():
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f: return json.load(f)
    except: return {}

def save_cfg(c):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(c, f, ensure_ascii=False, indent=1)
    except: pass

def collect():
    ctx = {"python":"?","android":"?","model":"?","scripts":[],"models":[]}
    r = run("python --version")
    if r and r.stdout: ctx["python"] = r.stdout.strip().replace("Python ","")
    r = run("getprop ro.product.model")
    if r and r.stdout: ctx["model"] = r.stdout.strip()
    r = run("getprop ro.build.version.release")
    if r and r.stdout: ctx["android"] = r.stdout.strip()
    try:
        ctx["scripts"] = [f for f in sorted(os.listdir(HOME))
                          if os.path.isfile(os.path.join(HOME, f))
                          and f.endswith((".py",".sh",".fish"))]
    except: pass
    for d in [HOME, os.path.join(HOME, "models")]:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".gguf"):
                    try: sz = os.path.getsize(os.path.join(d, f))
                    except: sz = 0
                    if sz > 100_000_000: ctx["models"].append(f"{f} ({hsize(sz)})")
    return ctx

def is_safe_path(path):
    if not STATE["sandbox"]: return True
    try: ap = os.path.abspath(os.path.expanduser(path))
    except: return False
    allowed = [os.path.abspath(HOME), os.path.abspath(os.path.join(HOME, "storage")), "/sdcard/Download"]
    for a in allowed:
        if ap.startswith(a): return True
    return False

def build_system_prompt(ctx):
    """~250 токенов с примерами — TTFT 5-10 сек"""
    return (
        "Ты AI в Termux (Android). Русский, кратко.\n\n"
        "ФОРМАТЫ:\n"
        "Запуск: ```exec\\npython ~/file.py\\n```\n"
        "Write: ```write\\n~/file.py\\nсодержимое\\n```\n"
        "Read: ```read\\n~/file.py\\n```\n\n"
        "ПРИМЕРЫ (используй ровно python ~/):\n"
        "'запусти матрицу' → ```exec\\npython ~/matrix.py\\n```\n"
        "'открой музыку' → ```exec\\npython ~/randomaudio.py\\n```\n"
        "'покажи задачи' → ```exec\\npython ~/todo.py\\n```\n"
        "'заметки' → ```exec\\npython ~/notes.py\\n```\n"
        "'пароли' → ```exec\\npython ~/passmanager.py\\n```\n"
        "'крипта' → ```exec\\npython ~/crypto_informer.py\\n```\n"
        "'хакерский тул' → ```exec\\npython ~/hacktool.py\\n```\n"
        "'RPG' → ```exec\\npython ~/hacker_rpg.py\\n```\n"
        "'загрузчик' → ```exec\\npython ~/download_zone.py\\n```\n"
        "'sysinfo' → ```exec\\npython ~/sysinfo.py\\n```\n"
        "'утилиты' → ```exec\\npython ~/utils.py\\n```\n"
        "'картинка' → ```exec\\npython ~/art.py\\n```\n"
        "'модели' → ```exec\\nls -lh ~/*.gguf\\n```\n\n"
        "ВАЖНО: ВСЕГДА пиши 'python ~/file.py'. НЕ просто 'matrix' или 'todo'.\n"
        "НЕ выдумывай termux-*, qrencode, apt и т.п."
    )

def check_port():
    s = socket.socket(); s.settimeout(0.5)
    try: s.connect((HOST, PORT)); s.close(); return True
    except: return False

def free_ram():
    try:
        with open("/proc/meminfo") as f:
            for ln in f:
                if ln.startswith("MemAvailable"):
                    return int(ln.split()[1]) // 1024
    except: pass
    return 0

def find_models():
    out = []
    for d in [HOME, os.path.join(HOME, "models")]:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".gguf"):
                    fp = os.path.join(d, f)
                    try: sz = os.path.getsize(fp)
                    except: sz = 0
                    if sz > 100_000_000: out.append((fp, sz))
    return out

def ask_model(cfg):
    models = find_models()
    if not models:
        console.print("[red]❌ Нет моделей[/]"); return None
    last = cfg.get("last_model")
    if last:
        for fp, sz in models:
            if fp == last:
                console.print(f"[green]✔ Модель: {os.path.basename(fp)}[/]")
                time.sleep(0.3); return fp
    for fp, sz in models:
        if "qwen" in os.path.basename(fp).lower():
            console.print(f"[green]✔ Модель: {os.path.basename(fp)}[/]")
            return fp
    return models[0][0]

def start_server(mp):
    if check_port(): return True
    console.print(f"[yellow]⚠ ОЗУ: {free_ram()} МБ[/]")
    cmd = ["llama-server", "-m", mp, "--host", HOST, "--port", str(PORT),
           "-c", str(STATE["ctx_size"]), "-t", str(STATE["threads"]), "--no-warmup"]
    try:
        with open(os.devnull,"w") as dn:
            STATE["proc"] = subprocess.Popen(cmd, stdout=dn, stderr=dn, stdin=dn, preexec_fn=os.setsid)
    except FileNotFoundError:
        console.print("[red]❌ llama-server не найден[/]"); return False
    return True

def warmup():
    st = time.time()
    while time.time() - st < 300:
        try:
            req = urllib.request.Request(f"{URL}/health")
            with urllib.request.urlopen(req, timeout=5) as r:
                if "ok" in r.read().decode("utf-8","ignore").lower():
                    return time.time() - st
        except: pass
        time.sleep(1)
    return None

def stop_server():
    p = STATE.get("proc")
    if p and p.poll() is None:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM); time.sleep(0.5)
            if p.poll() is None: os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except: pass
atexit.register(stop_server)

def stream(user_msg):
    msgs = [{"role":"system","content":STATE["sys_prompt"]}]
    msgs.extend(STATE["history"][-4:])
    msgs.append({"role":"user","content":user_msg})
    payload = {"messages":msgs,"stream":True,"temperature":STATE["temp"],
               "max_tokens":STATE["max_tokens"],"cache_prompt":True}
    req = urllib.request.Request(f"{URL}/v1/chat/completions",
        data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=600)
        for raw in resp:
            ln = raw.decode("utf-8","ignore").strip()
            if not ln or not ln.startswith("data: "): continue
            ch = ln[6:]
            if ch == "[DONE]": break
            try:
                obj = json.loads(ch)
                d = obj.get("choices",[{}])[0].get("delta",{})
                p = d.get("content","")
                if p: yield p
            except: continue
    except urllib.error.HTTPError as e: yield f"__ERROR__: HTTP {e.code}"
    except Exception as e: yield f"__ERROR__: {e}"

DANGER = re.compile(
    r"rm\s+-rf\s+/(?!data/data/com\.termux/files/home|sdcard|storage)|"
    r"mkfs|dd\s+if=|dd\s+of=/dev|shutdown|reboot|halt|poweroff|"
    r"fdisk|parted|>\s*/dev/sd|:\(\)\s*\{|chmod\s+-R\s+000|"
    r"sudo\s+rm|rm\s+-rf\s+/system|rm\s+-rf\s+/vendor",
    re.I)

EXEC = re.compile(r"```exec\s*\n(.*?)\n```", re.DOTALL)
WRITE = re.compile(r"```write\s*\n(.*?)\n(.*?)\n```", re.DOTALL)
READ = re.compile(r"```read\s*\n(.*?)\n```", re.DOTALL)

def process(gen):
    tb, ab = "", ""; it = False; st = time.time(); ft = {"t":None}
    def render_think():
        el = int(time.time() - st)
        status = f"⏱ {el}с · ⏳..." if ft["t"] is None else f"⏱ {el}с · TTFT {ft['t']-st:.1f}с"
        lines = [Text(status, style="bold yellow")]
        if tb:
            tail = tb[-400:] if len(tb) > 400 else tb
            lines.append(Text(tail, style="dim italic yellow"))
        return Group(*lines)
    with Live(render_think(), console=console, refresh_per_second=10, transient=True) as live:
        live.update(render_think())
        for p in gen:
            if ft["t"] is None: ft["t"] = time.time()
            if "<think>" in p and not it:
                sp = p.split("<think>",1); ab += sp[0]; tb += sp[1]; it = True
            elif "</think>" in p and it:
                sp = p.split("</think>",1); tb += sp[0]; ab += sp[1]; it = False
            else:
                if it: tb += p
                else: ab += p
            live.update(render_think())
    tb = tb.replace("<think>","").replace("</think>","").strip()
    ab = ab.replace("<think>","").replace("</think>","").strip()
    if not ab and tb: ab = tb; tb = ""
    return tb, ab

def reset_terminal():
    try: subprocess.run("stty sane 2>/dev/null", shell=True, timeout=3)
    except: pass
    try:
        sys.stdout.write("\033[0m\033[2J\033[H")
        sys.stdout.flush()
    except: pass

def run_interactive_tty(cmd):
    reset_terminal()
    console.print()
    console.print(f"[bold yellow]🎮 Запуск в TTY:[/] [cyan]{cmd}[/]")
    console.print("[dim]Выход: q / Ctrl+C / Esc[/]\n")
    time.sleep(0.5)
    try:
        sys.stdout.flush()
        sys.stdin.flush() if hasattr(sys.stdin, 'flush') else None
    except: pass
    try:
        rc = pty.spawn(["/data/data/com.termux/files/usr/bin/sh", "-c", cmd])
        return rc
    except Exception as e:
        console.print(f"[red]❌ pty.spawn: {e}[/]")
        return None
    finally:
        reset_terminal()

def execute(cmd, auto=False):
    console.print()
    if DANGER.search(cmd):
        console.print(f"[bold red]🛑 Заблокировано:[/] {cmd}")
        return None

    if is_interactive(cmd):
        console.print(f"[bold yellow]⚡ Интерактивная:[/] [cyan]{cmd}[/]")
        if not auto:
            try:
                a = input("\033[95mЗапустить в TTY? (y/N)> \033[0m").strip().lower()
            except: return None
            if a != "y":
                console.print("[dim]Отменено[/]\n"); return None
        rc = run_interactive_tty(cmd)
        console.print()
        if rc == 0:
            console.print(f"[green]✔ Код 0[/]\n")
        elif rc is not None:
            console.print(f"[red]✘ Код {rc}[/]\n")
        return f"TTY-команда завершена, код {rc}"

    console.print(f"[bold yellow]⚡ Команда:[/] [cyan]{cmd}[/]")
    if not auto:
        try:
            a = input("\033[95mВыполнить? (y/N)> \033[0m").strip().lower()
        except: return None
        if a != "y":
            console.print("[dim]Отменено[/]\n"); return None
    console.print(f"[dim]$ {cmd}[/]\n")
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True, bufsize=1)
        out = []
        for line in p.stdout:
            console.print(line.rstrip())
            out.append(line.rstrip())
        p.wait(timeout=600)
        result = "\n".join(out[-50:])
        if p.returncode == 0:
            console.print(f"[green]✔ Код 0[/]\n")
        else:
            console.print(f"[red]✘ Код {p.returncode}[/]\n")
        return result
    except subprocess.TimeoutExpired:
        console.print("[red]✘ Таймаут[/]\n")
        try: p.kill()
        except: pass
        return None
    except Exception as e:
        console.print(f"[red]✘ {e}[/]\n"); return None

def do_write(path, content, auto=False):
    path = os.path.expanduser(path.strip())
    console.print()
    if DANGER.search(content):
        console.print(f"[bold red]🛑 Заблокировано[/]"); return False
    if not is_safe_path(path):
        console.print(f"[bold red]🛑 Вне sandbox:[/] {path}"); return False
    console.print(f"[bold yellow]📝 Запись:[/] [cyan]{path}[/]")
    console.print(f"[dim]{len(content)} символов[/]")
    for line in content.split("\n")[:15]:
        console.print(f"[dim]│[/] {line}")
    if len(content.split("\n")) > 15:
        console.print(f"[dim]│ ... ({len(content.split(chr(10)))-15} строк)[/]")
    console.print()
    if not auto:
        try:
            a = input("\033[95mЗаписать? (y/N)> \033[0m").strip().lower()
        except: return False
        if a != "y":
            console.print("[dim]Отменено[/]\n"); return False
    try:
        d = os.path.dirname(path)
        if d: os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[green]✔ Записано[/]\n"); return True
    except Exception as e:
        console.print(f"[red]✘ {e}[/]\n"); return False

def do_read(path):
    path = os.path.expanduser(path.strip())
    console.print()
    if not is_safe_path(path):
        console.print(f"[bold red]🛑 Вне sandbox:[/] {path}"); return None
    if not os.path.exists(path):
        console.print(f"[red]❌ Не найден: {path}[/]\n"); return None
    if os.path.isdir(path):
        try:
            files = os.listdir(path)
            console.print(f"[yellow]📁 {path}:[/]")
            for f in files[:30]: console.print(f"  [cyan]•[/] {f}")
            console.print()
            return "\n".join(files)
        except: return None
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if len(content) > 8000:
            console.print(f"[yellow]📄 {path} (первые 8000 из {len(content)})[/]\n")
            content = content[:8000] + f"\n[... обрезано]"
        else:
            console.print(f"[yellow]📄 {path} ({len(content)} симв)[/]\n")
        STATE["session_files"].append(path)
        return content
    except Exception as e:
        console.print(f"[red]✘ {e}[/]\n"); return None

def handle_response(answer):
    did_something = False
    read_results = []
    for path in READ.findall(answer):
        content = do_read(path)
        if content is not None:
            read_results.append((path, content)); did_something = True
    write_results = []
    for path, content in WRITE.findall(answer):
        if do_write(path, content, auto=STATE["auto_exec"]):
            write_results.append(path); did_something = True
    exec_results = []
    for cmd in EXEC.findall(answer):
        cmd = cmd.strip()
        if not cmd: continue
        out = execute(cmd, auto=STATE["auto_exec"])
        if out is not None:
            exec_results.append((cmd, out)); did_something = True
    if read_results or write_results or exec_results:
        follow = "\n=== РЕЗУЛЬТАТЫ ===\n"
        for path, content in read_results:
            follow += f"\n[READ {path}]:\n{content[:3000]}\n"
        for path in write_results:
            follow += f"\n[WRITE OK]: {path}\n"
        for cmd, out in exec_results:
            follow += f"\n[EXEC '{cmd}']:\n{out[:2000]}\n"
        return follow
    return None

COMMANDS = [
    "думать","think","быстро","fast","авто","auto",
    "команды","agent","агент","sudo","sandbox",
    "env","модель","model",
    "очистить","clear","статистика","stats",
    "помощь","help","выход","q"
]

class Comp(Completer):
    def get_completions(self, doc, ev):
        t = doc.text_before_cursor
        if " " in t: return
        for c in sorted(COMMANDS):
            if c.startswith(t.lower()): yield Completion(c, start_position=-len(t))

def title_block():
    mode = "🤖 АВТО" if STATE["auto"] else ("💭 ВСЕГДА" if STATE["thinking"] else "⚡ БЫСТРО")
    agent = "🔥 АГЕНТ" if STATE["agent"] else "— выкл"
    auto_exec = "⚡ БЕЗ ПОДТВ." if STATE["auto_exec"] else "✋ ПОДТВ."
    sandbox = "🔒 SB" if STATE["sandbox"] else "⚠ БЕЗ SB"
    mn = os.path.basename(STATE['model_path'] or '?').replace('.gguf','')
    t = Text()
    t.append("▓▒░ ", style="bold bright_green")
    t.append(mn.upper(), style="bold bright_green")
    t.append(" ░▒▓ AI v15.5", style="bold green")
    t.append(f"\n  ", style="dim"); t.append(mode, style="bold bright_cyan")
    t.append(f"  ·  ", style="dim"); t.append(agent, style="bright_green" if STATE["agent"] else "dim")
    t.append(f"  ·  ", style="dim"); t.append(auto_exec, style="bright_red" if STATE["auto_exec"] else "bright_yellow")
    t.append(f"  ·  ", style="dim"); t.append(sandbox, style="bright_cyan")
    t.append(f"\n  📝 {len(STATE['history'])}  ·  📂 {len(STATE['session_files'])}  ·  ОЗУ {free_ram()} МБ", style="dim")
    return Panel(t, border_style="black", padding=(0,1))

def switch_model(cfg):
    models = find_models()
    if not models: return False
    console.print()
    t = Table(box=SIMPLE_HEAD, border_style="black", padding=(0,2))
    t.add_column("#", style="bold yellow", width=4, justify="right")
    t.add_column("Модель"); t.add_column("Размер", style="cyan", justify="right", width=10)
    for i, (fp, sz) in enumerate(models, 1):
        m = "✔" if fp == STATE["model_path"] else ""
        t.add_row(str(i), os.path.basename(fp), hsize(sz), m)
    console.print(t); console.print()
    try:
        ch = input("\033[95mКакую? (Enter — отмена)> \033[0m").strip()
        if not ch.isdigit(): return False
        n = int(ch)
        if not (1 <= n <= len(models)): return False
        np = models[n-1][0]
        if np == STATE["model_path"]: console.print("[yellow]Уже[/]\n"); return False
        stop_server(); time.sleep(1)
        STATE["model_path"] = np; cfg["last_model"] = np; save_cfg(cfg)
        if not start_server(np): return False
        w = warmup()
        if w is None: console.print("[red]❌[/]\n"); return False
        console.print(f"[green]✔ {w:.1f}с[/]\n"); return True
    except: return False

def main():
    os.system("clear")
    cfg = load_cfg()
    STATE["model_path"] = ask_model(cfg)
    if not STATE["model_path"]: return
    cfg["last_model"] = STATE["model_path"]; save_cfg(cfg)
    STATE["agent"] = cfg.get("agent", True)
    STATE["auto_exec"] = cfg.get("auto_exec", False)
    STATE["sandbox"] = cfg.get("sandbox", True)

    console.print("[yellow]⚙ Контекст...[/]")
    STATE["ctx"] = collect()
    STATE["sys_prompt"] = build_system_prompt(STATE["ctx"])
    console.print(f"[green]✔ Скриптов: {len(STATE['ctx']['scripts'])}[/]")

    if not start_server(STATE["model_path"]): return
    console.print("[yellow]⏳ Загрузка модели...[/]")
    t0 = time.time()
    def rw():
        el = int(time.time() - t0)
        return Text(f"⏱ {el} сек...", style="bold yellow")
    with Live(rw(), console=console, refresh_per_second=2, transient=True) as live:
        res = {"w": None}
        def w(): res["w"] = warmup()
        th = threading.Thread(target=w, daemon=True); th.start()
        while th.is_alive(): live.update(rw()); time.sleep(0.5)
        th.join()
    if res["w"] is None: console.print("[red]❌[/]"); return
    console.print(f"[green]✔ Загружена за {res['w']:.1f}с[/]")
    time.sleep(0.3)

    os.system("clear"); console.print()
    console.print(title_block()); console.print()
    console.print("[bold green]Готов.[/] Попробуй: 'запусти матрицу', 'открой музыку'\n")

    st = Style.from_dict({"prompt":"bold ansibrightmagenta",
        "completion-menu.completion":"bg:#000000 #00ff88",
        "completion-menu.completion.current":"bg:#aa00aa #ffffff bold"})
    session = PromptSession(completer=Comp(), style=st, complete_while_typing=True)

    while True:
        try:
            ui = session.prompt(FormattedText([("bold ansibrightmagenta","╰─🧠❯ ")])).strip()
        except: console.print("\n[dim]Выход[/]"); break
        if not ui: continue
        lo = ui.lower()

        if lo in ("выход","q","quit","exit"): break
        if lo in ("думать","think"):
            STATE["thinking"]=True; STATE["auto"]=False
            console.print("[magenta]💭[/]\n"); continue
        if lo in ("быстро","fast"):
            STATE["thinking"]=False; STATE["auto"]=False
            console.print("[yellow]⚡[/]\n"); continue
        if lo in ("авто","auto"):
            STATE["auto"]=True; STATE["thinking"]=False
            console.print("[cyan]🤖[/]\n"); continue
        if lo in ("команды","agent"):
            STATE["agent"] = not STATE["agent"]
            cfg["agent"] = STATE["agent"]; save_cfg(cfg)
            console.print(f"[green]🔥 Exec: {'ВКЛ' if STATE['agent'] else 'выкл'}[/]\n"); continue
        if lo in ("sudo","агент"):
            STATE["auto_exec"] = not STATE["auto_exec"]
            cfg["auto_exec"] = STATE["auto_exec"]; save_cfg(cfg)
            console.print(f"[{'red' if STATE['auto_exec'] else 'yellow'}]{'⚡ БЕЗ ПОДТВ' if STATE['auto_exec'] else '✋ ПОДТВ'}[/]\n"); continue
        if lo == "sandbox":
            STATE["sandbox"] = not STATE["sandbox"]
            cfg["sandbox"] = STATE["sandbox"]; save_cfg(cfg)
            console.print(f"[cyan]🔒 SB: {'ВКЛ' if STATE['sandbox'] else 'ВЫКЛ'}[/]\n"); continue
        if lo == "env":
            c = STATE["ctx"]; console.print()
            console.print(f"[cyan]Python:[/] {c['python']}  ·  Android {c['android']}")
            console.print(f"[cyan]Скриптов:[/] {len(c['scripts'])}")
            console.print(f"[cyan]Модели:[/] " + ", ".join(c["models"]))
            console.print(); continue
        if lo in ("модель","model"):
            if switch_model(cfg):
                os.system("clear"); console.print(); console.print(title_block()); console.print()
            continue
        if lo in ("очистить","clear"):
            STATE["history"]=[]; STATE["session_files"]=[]
            os.system("clear"); console.print(); console.print(title_block()); console.print()
            console.print("[green]✔[/]\n"); continue
        if lo in ("статистика","stats"):
            console.print(Panel.fit(
                f"Модель: {os.path.basename(STATE['model_path'])}\n"
                f"Сообщений: {len(STATE['history'])}\nОЗУ: {free_ram()} МБ",
                border_style="black")); console.print(); continue
        if lo in ("помощь","help","?"):
            console.print()
            console.print("[bold]Команды:[/] авто · быстро · думать · команды · sudo · sandbox · env · модель · очистить · выход")
            console.print("[bold]Возможности:[/] exec · write · read")
            console.print(); continue

        STATE["history"].append({"role":"user","content":ui})
        console.print()
        t0 = time.time()
        try: tb, ab = process(stream(ui))
        except KeyboardInterrupt:
            console.print("\n[yellow]⏹[/]\n"); STATE["history"].pop(); continue
        el = time.time() - t0
        if ab.startswith("__ERROR__"):
            console.print(f"[red]❌ {ab[10:]}[/]\n"); STATE["history"].pop(); continue
        STATE["history"].append({"role":"assistant","content":ab})

        console.print()
        if tb: console.print(f"[dim italic yellow]💭 {tb[:400]}[/]\n")
        try: console.print(Markdown(ab))
        except: console.print(ab)
        console.print(f"\n[dim]⏱ {el:.1f}с[/]\n")

        if STATE["agent"]:
            follow = handle_response(ab)
            if follow:
                STATE["history"].append({"role":"user","content":follow})
                console.print("[dim]🔄 AI получает результаты...[/]\n")
                t1 = time.time()
                try: tb2, ab2 = process(stream(follow[:4000]))
                except KeyboardInterrupt: ab2 = None
                if ab2 and not ab2.startswith("__ERROR__"):
                    STATE["history"].append({"role":"assistant","content":ab2})
                    console.print()
                    if tb2: console.print(f"[dim italic yellow]💭 {tb2[:300]}[/]\n")
                    try: console.print(Markdown(ab2))
                    except: console.print(ab2)
                    console.print(f"\n[dim]⏱ {time.time()-t1:.1f}с[/]\n")

    reset_terminal()
    stop_server()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано[/]")
        reset_terminal()
        stop_server()
```

---

## 📄 hacktool.py

*34574 байт · 733 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HackTool v2 — расширенный OSINT-мультитул с 28 командами"""

import os, sys, time, random, subprocess, socket, secrets, string, json, re
import urllib.request, urllib.error, urllib.parse
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.markdown import Markdown
from rich.box import SIMPLE_HEAD, DOUBLE_EDGE
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

console = Console()

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

# ═══════════ БАННЕР ═══════════
def banner():
    os.system("clear")
    art = r"""
    ██╗  ██╗ █████╗  ██████╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗
    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝╚══██╔══╝██╔═══██╗██╔═══██╗██║
    ███████║███████║██║     █████╔╝    ██║   ██║   ██║██║   ██║██║
    ██╔══██║██╔══██║██║     ██╔═██╗    ██║   ██║   ██║██║   ██║██║
    ██║  ██║██║  ██║╚██████╗██║  ██╗   ██║   ╚██████╔╝╚██████╔╝███████╗
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    console.print(Align.center(f"[bold green]{art}[/]"))
    console.print(Align.center("[bold cyan]⚡ OSINT Мультитул v2 ⚡[/]"))
    console.print(Align.center(f"[dim]{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}[/]"))
    console.print()

def menu():
    t = Table(box=None, border_style="black", show_header=False, padding=(0, 1))
    t.add_column("Команда", style="bold yellow", width=24, justify="center")
    t.add_column("Описание", style="white")

    # Секция 1: Разведка
    t.add_row("[bold magenta]── РАЗВЕДКА ──[/]", "")
    t.add_row("[cyan]scan <domain>[/]",      "🌐 WHOIS + DNS + IP")
    t.add_row("[cyan]crt <domain>[/]",       "🕵️  Certificate Transparency")
    t.add_row("[cyan]subdomain <domain>[/]", "🔎 Поиск поддоменов (расширенный)")
    t.add_row("[cyan]dns-enum <domain>[/]",  "📡 Полный DNS (A/AAAA/MX/NS/TXT/SOA/CAA)")
    t.add_row("[cyan]robots <url>[/]",       "🤖 robots.txt сайта")
    t.add_row("[cyan]headers <url>[/]",      "📋 HTTP-заголовки + аудит")

    # Секция 2: Сеть
    t.add_row("", "")
    t.add_row("[bold magenta]── СЕТЬ ──[/]", "")
    t.add_row("[cyan]nmap <host>[/]",        "🔍 Профессиональный скан портов")
    t.add_row("[cyan]ports <host>[/]",       "⚙️  Быстрый скан популярных портов")
    t.add_row("[cyan]ping <host>[/]",        "🏓 Ping + проверка")
    t.add_row("[cyan]trace <host>[/]",       "🛰 Traceroute")
    t.add_row("[cyan]ip[/]",                 "📍 Внешний IP + геолокация")
    t.add_row("[cyan]speed[/]",              "⚡ Тест скорости")

    # Секция 3: Крипто/утилиты
    t.add_row("", "")
    t.add_row("[bold magenta]── КРИПТО ──[/]", "")
    t.add_row("[cyan]hash <text>[/]",        "🧮 MD5/SHA1/SHA256/SHA512")
    t.add_row("[cyan]hashid <hash>[/]",      "🔐 Определить тип хэша")
    t.add_row("[cyan]b64 enc|dec <text>[/]", "🔡 Base64")
    t.add_row("[cyan]pass <length>[/]",      "🎲 Криптостойкий пароль")
    t.add_row("[cyan]pass-audit <pass>[/]",  "🔍 Анализ пароля")

    # Секция 4: Данные
    t.add_row("", "")
    t.add_row("[bold magenta]── ДАННЫЕ ──[/]", "")
    t.add_row("[cyan]crypto[/]",             "💰 Курс BTC/ETH/SOL")
    t.add_row("[cyan]news[/]",               "📰 IT-новости (RU)")
    t.add_row("[cyan]qr <text>[/]",          "📱 QR-код")

    # Секция 5: Обучение
    t.add_row("", "")
    t.add_row("[bold magenta]── ОБУЧЕНИЕ ──[/]", "")
    t.add_row("[cyan]pentest-guide[/]",      "📚 Роадмап обучения пентесту")
    t.add_row("[cyan]ctf-links[/]",          "🏆 Площадки CTF")

    # Секция 6: Утилиты
    t.add_row("", "")
    t.add_row("[cyan]matrix[/]",             "🌧 5 сек матрицы")
    t.add_row("[cyan]sysinfo[/]",            "💻 Центр управления")
    t.add_row("[cyan]clear[/]",              "🧹 Очистить")
    t.add_row("[cyan]exit[/]",               "🚪 Выход")

    console.print(Panel(t, title="[bold green]🎮 Команды (Tab — автодополнение)[/]",
                        border_style="black"))
    console.print()

# ═══════════ УТИЛИТЫ ═══════════
def run(cmd, timeout=60):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except Exception:
        return None

def has_cmd(c): return subprocess.run(f"which {c}", shell=True, capture_output=True).returncode == 0

def http_get(url, timeout=15, headers=None):
    try:
        req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception:
        return None

# ═══════════ РАЗВЕДКА ═══════════
def cmd_scan(domain):
    if not domain: console.print("[red]❌ scan <домен>[/]"); return
    domain = domain.replace("http://","").replace("https://","").split("/")[0]
    console.print(f"\n[bold yellow]🔍 Сканирую:[/] [cyan]{domain}[/]\n")

    # IP
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"  [green]✔[/] IP: [cyan]{ip}[/]")
    except Exception:
        console.print(f"  [red]✘[/] IP не разрешён")

    # DNS
    try:
        import dns.resolver
        for rt in ["A","MX","NS","TXT","AAAA","CNAME"]:
            try:
                ans = dns.resolver.resolve(domain, rt, lifetime=5)
                vals = [str(a) for a in ans][:3]
                console.print(f"  [green]✔[/] DNS {rt}: [cyan]{', '.join(vals)}[/]")
            except Exception: pass
    except ImportError: pass

    # WHOIS
    try:
        import whois
        w = whois.whois(domain)
        for k, label in [("registrar","Регистратор"),("creation_date","Создан"),
                          ("expiration_date","Истекает"),("org","Организация")]:
            v = w.get(k)
            if isinstance(v, list): v = v[0] if v else None
            if v: console.print(f"  [green]✔[/] {label}: [cyan]{v}[/]")
    except Exception: pass
    console.print()

def cmd_crt(domain):
    if not domain: console.print("[red]❌ crt <домен>[/]"); return
    domain = domain.replace("http://","").replace("https://","").split("/")[0]
    console.print(f"\n[bold yellow]🕵️  crt.sh:[/] [cyan]{domain}[/]")
    console.print("[dim]Источник: публичные логи SSL-сертификатов[/]\n")
    try:
        data = http_get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=25)
        if not data: console.print("[red]❌ Ошибка запроса[/]"); return
        items = json.loads(data)
        names = set()
        for it in items:
            for n in it.get("name_value","").split("\n"):
                n = n.strip().lstrip("*.").lower()
                if n.endswith(domain): names.add(n)
        if not names: console.print("[yellow]⚠ Ничего не найдено[/]"); return
        console.print(f"[bold green]✔ Найдено поддоменов: {len(names)}[/]\n")
        for i, n in enumerate(sorted(names)[:50], 1):
            console.print(f"  [cyan]{i:3}.[/] {n}")
        if len(names) > 50: console.print(f"  [dim]... и ещё {len(names)-50}[/]")
        console.print()
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

def cmd_subdomain(domain):
    if not domain: console.print("[red]❌ subdomain <домен>[/]"); return
    domain = domain.replace("http://","").replace("https://","").split("/")[0]
    console.print(f"\n[bold yellow]🔎 Поиск поддоменов:[/] [cyan]{domain}[/]\n")

    found = set()

    # 1. crt.sh
    console.print("[dim]Источник 1: crt.sh[/]")
    try:
        data = http_get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=25)
        if data:
            for it in json.loads(data):
                for n in it.get("name_value","").split("\n"):
                    n = n.strip().lstrip("*.").lower()
                    if n.endswith(domain) and n != domain:
                        found.add(n)
    except Exception: pass
    console.print(f"  [green]✔[/] Всего из crt.sh: [cyan]{len(found)}[/]\n")

    # 2. Wordlist brute (базовый список)
    console.print("[dim]Источник 2: wordlist (30 частых поддоменов)[/]")
    wordlist = ["www","mail","ftp","webmail","smtp","pop","ns1","ns2","webdisk",
                "ns","cpanel","whm","autodiscover","autoconfig","m","imap","test",
                "ns3","blog","pop3","dev","www2","admin","forum","news","vpn",
                "ns4","mail2","new","mysql"]
    for sub in wordlist:
        try:
            socket.gethostbyname(f"{sub}.{domain}")
            found.add(f"{sub}.{domain}")
        except Exception: pass
    console.print(f"  [green]✔[/] Всего поддоменов: [cyan]{len(found)}[/]\n")

    if found:
        for i, n in enumerate(sorted(found), 1):
            console.print(f"  [cyan]{i:3}.[/] {n}")
    else:
        console.print("[yellow]⚠ Ничего не найдено[/]")
    console.print()

def cmd_dns_enum(domain):
    if not domain: console.print("[red]❌ dns-enum <домен>[/]"); return
    domain = domain.replace("http://","").replace("https://","").split("/")[0]
    console.print(f"\n[bold yellow]📡 DNS-анализ:[/] [cyan]{domain}[/]\n")

    try:
        import dns.resolver
    except ImportError:
        console.print("[red]❌ Установи: pip install dnspython[/]"); return

    record_types = ["A","AAAA","MX","NS","TXT","SOA","CNAME","CAA","PTR","SRV"]
    for rt in record_types:
        try:
            ans = dns.resolver.resolve(domain, rt, lifetime=5)
            vals = [str(a)[:100] for a in ans][:5]
            if vals:
                console.print(f"  [green]{rt:6}[/] → [cyan]{', '.join(vals)}[/]")
        except Exception: pass

    # Специальный анализ TXT
    console.print("\n[bold magenta]Анализ безопасности:[/]")
    try:
        txts = " ".join(str(a) for a in dns.resolver.resolve(domain, "TXT", lifetime=5))
        if "v=spf1" in txts: console.print("  [green]✔[/] SPF найден")
        else: console.print("  [red]✘[/] SPF отсутствует")
        if "DMARC" in txts or "_dmarc" in txts: console.print("  [green]✔[/] DMARC найден")
    except Exception: pass
    try:
        dmarc = dns.resolver.resolve(f"_dmarc.{domain}", "TXT", lifetime=5)
        console.print(f"  [green]✔[/] DMARC: [cyan]{str(dmarc[0])[:100]}[/]")
    except Exception:
        console.print("  [yellow]⚠[/] DMARC не настроен")
    console.print()

def cmd_robots(url):
    if not url: console.print("[red]❌ robots <url>[/]"); return
    if not url.startswith("http"): url = "https://" + url
    console.print(f"\n[bold yellow]🤖 robots.txt:[/] [cyan]{url}[/]\n")
    txt = http_get(url.rstrip("/") + "/robots.txt", timeout=10)
    if txt:
        console.print(txt[:3000])
    else:
        console.print("[red]❌ Не удалось получить robots.txt[/]")
    console.print()

def cmd_headers(url):
    if not url: console.print("[red]❌ headers <url>[/]"); return
    if not url.startswith("http"): url = "https://" + url
    console.print(f"\n[bold yellow]📋 HTTP-заголовки:[/] [cyan]{url}[/]\n")
    try:
        import requests
        r = requests.head(url, timeout=10, allow_redirects=True)
        t = Table(box=None, border_style="black", header_style="bold cyan", padding=(0,1))
        t.add_column("Заголовок", style="bold yellow")
        t.add_column("Значение", style="cyan")
        for k, v in r.headers.items():
            t.add_row(k, str(v)[:80])
        console.print(t)

        console.print("\n[bold magenta]🔒 Аудит безопасности:[/]")
        sec = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy": "CSP",
            "X-Frame-Options": "Anti-Clickjacking",
            "X-Content-Type-Options": "Anti-MIME-sniffing",
            "Referrer-Policy": "Referrer-Policy",
            "Permissions-Policy": "Permissions-Policy",
        }
        for h, label in sec.items():
            if h in r.headers:
                console.print(f"  [green]✔[/] {label}")
            else:
                console.print(f"  [red]✘[/] {label}")
        console.print()
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

# ═══════════ СЕТЬ ═══════════
def cmd_nmap(host):
    if not host: console.print("[red]❌ nmap <host>[/]"); return
    if not has_cmd("nmap"):
        console.print("[red]❌ nmap не установлен. Установи: pkg install nmap[/]")
        return
    console.print(f"\n[bold yellow]🔍 Nmap-скан:[/] [cyan]{host}[/]")
    console.print("[dim]⚠️  Только свои серверы или с разрешения владельца![/]\n")
    r = run(f"nmap -sT -T4 --top-ports 100 {host}", timeout=180)
    if r and r.stdout:
        console.print(r.stdout)
    else:
        console.print("[red]❌ Ошибка сканирования[/]")

def cmd_ports(host):
    if not host: console.print("[red]❌ ports <host>[/]"); return
    console.print(f"\n[bold yellow]⚙️  Быстрый скан портов:[/] [cyan]{host}[/]")
    console.print("[dim]⚠️  Только свои серверы![/]\n")
    ports = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",
             110:"POP3",143:"IMAP",443:"HTTPS",445:"SMB",3306:"MySQL",
             3389:"RDP",5432:"PostgreSQL",6379:"Redis",8080:"HTTP-Alt",
             8443:"HTTPS-Alt",27017:"MongoDB"}
    try:
        ip = socket.gethostbyname(host)
        cnt = 0
        for port, name in ports.items():
            s = socket.socket(); s.settimeout(0.5)
            try:
                if s.connect_ex((ip, port)) == 0:
                    console.print(f"  [green]✔[/] {port:5} [cyan]{name}[/]")
                    cnt += 1
            except Exception: pass
            finally: s.close()
        console.print(f"\n[bold]Открыто: {cnt}[/]\n")
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

def cmd_ping(host):
    if not host: console.print("[red]❌ ping <host>[/]"); return
    console.print(f"\n[bold yellow]🏓 {host}[/]\n")
    r = run(f"ping -c 4 {host}", timeout=20)
    console.print(r.stdout if r and r.stdout else "[red]❌ Нет ответа[/]")

def cmd_trace(host):
    if not host: console.print("[red]❌ trace <host>[/]"); return
    console.print(f"\n[bold yellow]🛰 Traceroute:[/] [cyan]{host}[/]\n")
    r = run(f"traceroute -m 15 {host}", timeout=60)
    if r and r.stdout: console.print(r.stdout)
    else:
        r2 = run(f"ping -c 1 -R {host}", timeout=20)
        console.print(r2.stdout if r2 and r2.stdout else "[red]❌[/]")

def cmd_ip():
    console.print("\n[bold yellow]📍 Определяю IP...[/]\n")
    try:
        import requests
        d = requests.get("https://ipinfo.io/json", timeout=10).json()
        t = Table(box=None, show_header=False, border_style="black", padding=(0,2))
        t.add_column("", style="bold yellow", width=16)
        t.add_column("", style="cyan")
        for k, label in [("ip","🌐 IP"),("city","🏙 Город"),("region","🌍 Регион"),
                          ("country","🏳 Страна"),("org","📡 Провайдер"),
                          ("timezone","⏰ TZ"),("loc","📍 Координаты")]:
            t.add_row(label, d.get(k,"?"))
        console.print(t)
        console.print()
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

def cmd_speed():
    console.print("\n[bold yellow]⚡ Тест скорости...[/]\n")
    try:
        import requests, time
        url = "https://speed.cloudflare.com/__down?bytes=5000000"
        st = time.time()
        r = requests.get(url, timeout=30, stream=True)
        sz = sum(len(c) for c in r.iter_content(8192))
        el = time.time() - st
        mbps = (sz * 8) / (el * 1_000_000)
        ps = time.time(); requests.get("https://1.1.1.1", timeout=5)
        pm = (time.time() - ps) * 1000
        t = Table(box=None, show_header=False, border_style="black", padding=(0,2))
        t.add_column("", style="bold yellow", width=16)
        t.add_column("", style="green")
        t.add_row("📥 Скорость", f"{mbps:.2f} Мбит/с")
        t.add_row("📡 Ping", f"{pm:.0f} мс")
        t.add_row("📦 Скачано", f"{sz/1024/1024:.2f} МБ")
        console.print(t); console.print()
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

# ═══════════ КРИПТО ═══════════
def cmd_hash(text):
    if not text: console.print("[red]❌ hash <текст>[/]"); return
    import hashlib
    console.print()
    t = Table(title=f"🧮 Хэши: {text[:40]}", box=None, border_style="black",
              header_style="bold cyan")
    t.add_column("Алгоритм", style="bold yellow", width=10)
    t.add_column("Хэш", style="cyan")
    for algo in ["md5","sha1","sha256","sha512"]:
        t.add_row(algo.upper(), hashlib.new(algo, text.encode()).hexdigest()[:80])
    console.print(t); console.print()

def cmd_hashid(h):
    if not h: console.print("[red]❌ hashid <хэш>[/]"); return
    h = h.strip()
    console.print(f"\n[bold yellow]🔐 Анализ хэша:[/] [cyan]{h[:60]}...[/]\n")
    length = len(h)
    is_hex = bool(re.match(r"^[0-9a-fA-F]+$", h))
    is_b64 = bool(re.match(r"^[A-Za-z0-9+/=]+$", h))

    types = []
    if is_hex:
        if length == 32: types.append(("MD5, MD4, NTLM, LM", "🔓"))
        elif length == 40: types.append(("SHA-1, MySQL5, RIPEMD-160", "🔓"))
        elif length == 56: types.append(("SHA-224", "🔓"))
        elif length == 64: types.append(("SHA-256, Keccak-256, Blake2s", "🔓"))
        elif length == 96: types.append(("SHA-384", "🔓"))
        elif length == 128: types.append(("SHA-512, Whirlpool", "🔓"))
        else: types.append((f"Неизвестный hex ({length} симв)", "❓"))
    if is_b64 and not is_hex:
        if length == 24: types.append(("bcrypt (Base64)", "🔒"))
        elif length == 60: types.append(("bcrypt", "🔒"))
        elif length == 20: types.append(("DES (crypt)", "🔓"))
        else: types.append((f"Возможно Base64 ({length})", "❓"))
    if not types:
        types.append(("Не определён", "❓"))

    t = Table(box=None, border_style="black", header_style="bold cyan")
    t.add_column("Символ", width=8)
    t.add_column("Тип хэша", style="cyan")
    for name, sym in types:
        t.add_row(sym, name)
    console.print(t)
    console.print(f"\n[dim]Длина: {length} символов  ·  Hex: {'да' if is_hex else 'нет'}  ·  Base64: {'да' if is_b64 else 'нет'}[/]\n")

def cmd_b64(args):
    p = args.split(maxsplit=1)
    if len(p) < 2: console.print("[red]❌ b64 enc|dec <текст>[/]"); return
    import base64
    mode, text = p[0].lower(), p[1]
    try:
        if mode in ("enc","e"): res = base64.b64encode(text.encode()).decode()
        elif mode in ("dec","d"): res = base64.b64decode(text.encode()).decode()
        else: console.print("[red]❌ enc|dec[/]"); return
        console.print(); console.print(Panel(f"[bold cyan]{res}[/]", border_style="black")); console.print()
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

def cmd_pass(length_str):
    try:
        length = int(length_str) if length_str else 20
        if not 4 <= length <= 128: raise ValueError
    except ValueError:
        console.print("[red]❌ Длина 4-128[/]"); return
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"
    pwd = "".join(secrets.choice(alphabet) for _ in range(length))
    console.print()
    console.print(Panel(f"[bold green]{pwd}[/]", title=f"🔐 {length} символов", border_style="black"))
    try:
        import pyperclip; pyperclip.copy(pwd)
        console.print("[dim]✔ Скопировано в буфер[/]")
    except Exception: pass
    console.print()

def cmd_pass_audit(pwd):
    if not pwd: console.print("[red]❌ pass-audit <пароль>[/]"); return
    import math
    lo = any(c.islower() for c in pwd); up = any(c.isupper() for c in pwd)
    di = any(c.isdigit() for c in pwd); sy = any(c in string.punctuation for c in pwd)
    common = {"123456","password","qwerty","admin","пароль","12345678"}
    is_c = pwd.lower() in common
    pool = (26 if lo else 0)+(26 if up else 0)+(10 if di else 0)+(32 if sy else 0)
    ent = math.log2(pool)*len(pwd) if pool else 0
    if is_c: lbl, col = "КАТАСТРОФА", "red"
    elif ent < 30: lbl, col = "Слабый", "red"
    elif ent < 50: lbl, col = "Средний", "yellow"
    elif ent < 70: lbl, col = "Хороший", "green"
    else: lbl, col = "Отличный", "bold green"
    t = Table(box=None, show_header=False, border_style=col, padding=(0,2))
    t.add_column("", style="bold yellow", width=18); t.add_column("", style="white")
    t.add_row("Длина", str(len(pwd)))
    t.add_row("Строчные", "✔" if lo else "✘"); t.add_row("Прописные", "✔" if up else "✘")
    t.add_row("Цифры", "✔" if di else "✘"); t.add_row("Символы", "✔" if sy else "✘")
    t.add_row("Энтропия", f"{ent:.1f} бит")
    t.add_row("В словаре", "[red]ДА[/]" if is_c else "[green]нет[/]")
    t.add_row("Оценка", f"[{col}]{lbl}[/]")
    console.print(); console.print(Panel(t, title="🔍 Аудит", border_style=col)); console.print()

# ═══════════ ДАННЫЕ ═══════════
def cmd_crypto():
    console.print("\n[bold yellow]💰 Крипта...[/]\n")
    try:
        import requests
        r = requests.get("https://api.coingecko.com/api/v3/simple/price",
            params={"ids":"bitcoin,ethereum,solana","vs_currencies":"usd,rub",
                    "include_24hr_change":"true"}, timeout=10)
        d = r.json()
        t = Table(box=None, border_style="black", header_style="bold yellow")
        t.add_column("Монета", style="bold cyan")
        t.add_column("USD", style="green", justify="right")
        t.add_column("RUB", style="green", justify="right")
        t.add_column("24ч", justify="right")
        for cid, label in [("bitcoin","BTC ₿"),("ethereum","ETH Ξ"),("solana","SOL ◎")]:
            if cid in d:
                x = d[cid]; ch = x.get("usd_24h_change",0)
                col = "green" if ch >= 0 else "red"
                t.add_row(label, f"${x['usd']:,.0f}", f"{x['rub']:,.0f}₽", f"[{col}]{ch:+.2f}%[/]")
        console.print(t); console.print()
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

def cmd_news():
    console.print("\n[bold yellow]📰 IT-новости...[/]\n")
    feeds = [
        ("Хабр", "https://habr.com/ru/rss/all/all/"),
        ("N+1", "https://nplus1.ru/rss"),
        ("3DNews", "https://3dnews.ru/news/rss/"),
        ("IXBT", "https://www.ixbt.com/export/news.rss"),
    ]
    try:
        import feedparser
        for name, url in feeds:
            feed = feedparser.parse(url)
            if not feed.entries: continue
            console.print(f"[bold magenta]━━━ {name} ━━━[/]")
            for e in feed.entries[:3]:
                console.print(f"  [cyan]•[/] {e.title[:90]}")
                console.print(f"    [dim]{e.get('published','')[:16]}[/]")
            console.print()
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

def cmd_qr(text):
    if not text: console.print("[red]❌ qr <текст>[/]"); return
    try:
        import qrcode
        q = qrcode.QRCode(border=1); q.add_data(text); q.make(fit=True)
        q.print_ascii(invert=True)
        console.print()
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

# ═══════════ ОБУЧЕНИЕ ═══════════
def cmd_pentest_guide():
    os.system("clear")
    console.print()
    console.print(Align.center(Panel.fit(
        "[bold green]📚  РОАДМАП ПЕНТЕСТЕРА  📚[/]\n"
        "[dim]Полный путь от новичка до профессионала[/]",
        border_style="black")))
    console.print()

    stages = [
        ("🟢 ЭТАП 1: Основы (1-2 месяца)", [
            "Linux — командная строка, файловая система",
            "Сети — TCP/IP, DNS, HTTP/HTTPS, OSI",
            "Python — базовый синтаксис, requests, sockets",
            "Ресурс: TryHackMe (Pre Security, Intro to Cyber)",
        ]),
        ("🟡 ЭТАП 2: Базовый пентест (3-4 месяца)", [
            "Recon — nmap, whois, dig, subfinder, amass",
            "Web — Burp Suite, OWASP Top 10",
            "Linux PrivEsc — linpeas, sudo, SUID",
            "Платформа: HackTheBox (Easy boxes)",
        ]),
        ("🟠 ЭТАП 3: Специализация (6-12 месяцев)", [
            "Web Pentest — SQLi, XSS, RCE, LFI",
            "Network Pentest — AD, Kerberos, BloodHound",
            "Reverse Engineering — Ghidra, IDA",
            "Платформа: HackTheBox (Medium), TryHackMe (Offensive)",
        ]),
        ("🔴 ЭТАП 4: Профессионал (1-2 года)", [
            "OSCP — главный сертификат пентестера",
            "Bug Bounty — HackerOne, Bugcrowd",
            "Red Team — C2, обход EDR, Cobalt Strike",
            "Специализация: облако, мобилки, IoT",
        ]),
    ]

    for title, items in stages:
        console.print(f"[bold]{title}[/]")
        for it in items:
            console.print(f"  [cyan]•[/] {it}")
        console.print()

    console.print("[bold magenta]═══ РЕСУРСЫ ═══[/]")
    console.print("  [cyan]📺 YouTube:[/] IppSec, John Hammond, LiveOverflow")
    console.print("  [cyan]📖 Книги:[/] «Web App Hacking», «Hacking: 2.0»")
    console.print("  [cyan]🛠 Инструменты:[/] Kali Linux, ParrotOS, Nmap, Metasploit")
    console.print("  [cyan]💬 Сообщества:[/] r/netsec, r/AskNetsec, Discord HTB")
    console.print()

def cmd_ctf_links():
    os.system("clear")
    console.print()
    console.print(Align.center(Panel.fit(
        "[bold green]🏆  ПЛОЩАДКИ CTF  🏆[/]\n"
        "[dim]Где учиться и соревноваться[/]",
        border_style="black")))
    console.print()

    t = Table(box=None, border_style="black", header_style="bold cyan")
    t.add_column("Площадка", style="bold cyan")
    t.add_column("Уровень", style="yellow")
    t.add_column("Ссылка", style="green")
    t.add_row("HackTheBox", "Средний/Сложный", "hackthebox.com")
    t.add_row("TryHackMe", "Новичок", "tryhackme.com")
    t.add_row("PicoCTF", "Новичок", "picoctf.org")
    t.add_row("OverTheWire", "Новичок/Средний", "overthewire.org")
    t.add_row("VulnHub", "Все уровни", "vulnhub.com")
    t.add_row("PentesterLab", "Средний", "pentesterlab.com")
    t.add_row("Root-Me", "Все уровни", "root-me.org")
    t.add_row("RingZer0", "Все уровни", "ringzer0team.com")
    t.add_row("HTB Academy", "Курсы", "academy.hackthebox.com")
    t.add_row("SANS Holiday Hack", "Новичок", "holidayhackchallenge.com")
    console.print(t)

    console.print("\n[bold magenta]💰 BUG BOUNTY (платят за баги):[/]")
    console.print("  [cyan]•[/] HackerOne — hackerone.com")
    console.print("  [cyan]•[/] Bugcrowd — bugcrowd.com")
    console.print("  [cyan]•[/] YesWeHack — yeswehack.com")
    console.print("  [cyan]•[/] Intigriti — intigriti.com")
    console.print()

# ═══════════ МАТРИЦА ═══════════
def cmd_matrix():
    import curses
    def _run(stdscr):
        curses.curs_set(0); stdscr.nodelay(True); stdscr.timeout(0)
        curses.start_color()
        try: curses.use_default_colors()
        except: pass
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        CH = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"
        my, mx = stdscr.getmaxyx()
        drops = [{"y": random.randint(-20,0), "s": random.choice([0.5,1,1.5])} for _ in range(mx)]
        end = time.time() + 5
        while time.time() < end:
            try:
                if stdscr.getch() in (ord('q'), 27): break
            except: pass
            my, mx = stdscr.getmaxyx()
            for x in range(min(mx, len(drops))):
                d = drops[x]; d["y"] += d["s"]; y = int(d["y"])
                if 0 <= y < my:
                    try: stdscr.addstr(y, x, random.choice(CH), curses.color_pair(1)|curses.A_BOLD)
                    except: pass
                e = y - 8
                if 0 <= e < my:
                    try: stdscr.addstr(e, x, " ", curses.color_pair(2))
                    except: pass
                if y - 8 >= my:
                    d["y"] = random.randint(-10,-1); d["s"] = random.choice([0.5,1,1.5])
            stdscr.refresh(); time.sleep(0.05)
    try: curses.wrapper(_run)
    except KeyboardInterrupt: pass

def cmd_sysinfo():
    console.print("\n[dim]sysinfo.py...[/]\n")
    time.sleep(0.2)
    subprocess.run(["python", os.path.expanduser("~/sysinfo.py")])

# ═══════════ TAB-COMPLETER ═══════════
COMMANDS = [
    "scan","crt","subdomain","dns-enum","robots","headers",
    "nmap","ports","ping","trace","ip","speed",
    "hash","hashid","b64","pass","pass-audit",
    "crypto","news","qr",
    "pentest-guide","ctf-links",
    "matrix","sysinfo","clear","exit","help"
]

class HackCompleter(Completer):
    def get_completions(self, doc, ev):
        t = doc.text_before_cursor
        if " " in t: return
        for c in sorted(COMMANDS):
            if c.startswith(t.lower()):
                yield Completion(c, start_position=-len(t))

# ═══════════ MAIN ═══════════
def main():
    banner(); menu()

    style = Style.from_dict({
        "prompt": "bold ansibrightmagenta",
        "completion-menu.completion": "bg:#000000 #00ff88",
        "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
    })
    session = PromptSession(completer=HackCompleter(), style=style, complete_while_typing=True)

    while True:
        try:
            line = session.prompt(FormattedText([("bold ansibrightmagenta","hacktool> ")])).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Выход.[/]"); break
        if not line: continue

        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ("exit","quit","q","выход"):
            console.print("[dim]До связи. 🖖[/]"); break
        elif cmd in ("clear","cls"): banner(); menu()
        elif cmd == "scan":          cmd_scan(arg)
        elif cmd == "crt":           cmd_crt(arg)
        elif cmd == "subdomain":     cmd_subdomain(arg)
        elif cmd == "dns-enum":      cmd_dns_enum(arg)
        elif cmd == "robots":        cmd_robots(arg)
        elif cmd == "headers":       cmd_headers(arg)
        elif cmd == "nmap":          cmd_nmap(arg)
        elif cmd == "ports":         cmd_ports(arg)
        elif cmd == "ping":          cmd_ping(arg)
        elif cmd == "trace":         cmd_trace(arg)
        elif cmd == "ip":            cmd_ip()
        elif cmd == "speed":         cmd_speed()
        elif cmd == "hash":          cmd_hash(arg)
        elif cmd == "hashid":        cmd_hashid(arg)
        elif cmd == "b64":           cmd_b64(arg)
        elif cmd in ("pass","password"): cmd_pass(arg)
        elif cmd == "pass-audit":    cmd_pass_audit(arg)
        elif cmd == "crypto":        cmd_crypto()
        elif cmd == "news":          cmd_news()
        elif cmd == "qr":            cmd_qr(arg)
        elif cmd == "pentest-guide": cmd_pentest_guide()
        elif cmd == "ctf-links":     cmd_ctf_links()
        elif cmd == "matrix":        cmd_matrix()
        elif cmd == "sysinfo":       cmd_sysinfo()
        elif cmd in ("help","h","?"): menu()
        else:
            console.print(f"[red]❌ Неизвестно: {cmd}[/] Введи [cyan]help[/]")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано.[/]")
```

---

## 📄 randomaudio.py

*32659 байт · 716 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Music Player v9 — обложки (iTunes) + favorites + экспорт"""

import os, sys, json, random, subprocess, time, re, hashlib
import urllib.request, urllib.parse, urllib.error
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markup import escape
from rich.box import SIMPLE_HEAD
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

console = Console()
CACHE_FILE = os.path.expanduser("~/music_cache/library.json")
COVERS_DIR = os.path.expanduser("~/music_cache/covers")
FAV_FILE = os.path.expanduser("~/.music_favorites.json")
EXPORT_DIR = os.path.expanduser("~/music_cache/exports")
PAGE_SIZE = 15

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

GENRE_COLORS = {
    "rock":"bright_red","metal":"bright_red","punk":"bright_red",
    "pop":"bright_yellow","dance":"bright_yellow",
    "hip-hop":"dark_orange","rap":"dark_orange",
    "electronic":"bright_blue","edm":"bright_blue","techno":"bright_blue",
    "anime":"medium_purple1","soundtrack":"medium_purple1","ost":"medium_purple1",
    "classical":"bright_green","jazz":"bright_green",
    "instrumental":"cyan",
}
def genre_color(g):
    if not g: return GRAY
    gl = g.lower()
    for k, c in GENRE_COLORS.items():
        if k in gl: return c
    return CYAN

TYPE_LABELS = {
    "opening":"🎌 Опенинг","ending":"🎬 Эндинг","ost":"🎼 OST","theme":"🎵 Тема",
    "game":"🎮 Игра","anime":"🌸 Аниме","film":"🎞 Кино","classical":"🎻 Классика",
    "remix":"🎛 Ремикс","live":"🎤 Live","acoustic":"🎸 Акустика","cover":"🎙 Кавер",
    "instrumental":"🎹 Инстр.","song":"🎵 Песня",
}

def run(cmd, timeout=10):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except: return None

def has_cmd(cmd):
    r = run(f"which {cmd}")
    return r is not None and r.stdout.strip() != ""

def human_size(b):
    try: b = int(b)
    except: return "?"
    for u in ["B","KB","MB","GB"]:
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} TB"

def fmt_duration(s):
    if not s: return "--:--"
    try: s = int(s)
    except: return "--:--"
    m, sec = divmod(s, 60); h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"

def nkey(s): return " ".join(str(s).lower().split()).strip()

# ═══════════ ФИЛЬТР ГОЛОСОВЫХ ═══════════
NON_MUSIC_KEYWORDS = [
    "whatsapp audio", "voice", "recording", "запись", "record",
    "голосовое", "voice message", "dictaphone", "диктофон",
    "note_to_self", "audio_20", "rec_20", "запись_20", "голос_20",
]

def is_music_track(track):
    path = (track.get("path") or "").lower()
    title = (track.get("title") or "").lower()
    artist = (track.get("artist") or "").lower()
    album = (track.get("album") or "").lower()
    dur = track.get("duration") or 0
    genre = track.get("genre") or ""
    source = track.get("source") or "local"

    if 0 < dur < 30: return False
    hay = f"{path} {title}"
    for kw in NON_MUSIC_KEYWORDS:
        if kw in hay: return False
    if "whatsapp/media" in path.replace("\\", "/"): return False
    if (artist in ("неизвестен","unknown","") and
        album in ("без альбома","") and not genre and source == "local"):
        if any(x in path for x in ["/dcim/", "/recordings/", "/record/", "/voice/"]):
            return False
        if re.match(r"^\d+[\d_\-\.]+$", os.path.basename(path).rsplit(".",1)[0]):
            return False
    return True

# ═══════════ ОБЛОЖКИ (iTunes API) ═══════════
def cover_cache_path(artist, album, title):
    key = f"{artist}|{album}|{title}".lower()
    h = hashlib.md5(key.encode()).hexdigest()[:16]
    return os.path.join(COVERS_DIR, f"{h}.jpg")

def fetch_cover_url(artist, album, title):
    """Ищет обложку на iTunes. Возвращает URL или None."""
    try:
        q = f"{artist} {album}" if album and album != "Без альбома" else f"{artist} {title}"
        params = urllib.parse.urlencode({"term": q, "entity":"album", "limit":1})
        url = f"https://itunes.apple.com/search?{params}"
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
            results = data.get("results", [])
            if results:
                art = results[0].get("artworkUrl100", "")
                if art:
                    return art.replace("100x100", "600x600")
    except Exception:
        pass
    return None

def ensure_cover(artist, album, title):
    """Возвращает путь к обложке или None. Скачивает если надо."""
    if not artist or artist == "Неизвестен": return None
    os.makedirs(COVERS_DIR, exist_ok=True)
    cp = cover_cache_path(artist, album, title)
    if os.path.exists(cp) and os.path.getsize(cp) > 1000:
        return cp
    url = fetch_cover_url(artist, album, title)
    if not url: return None
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read()
        with open(cp, "wb") as f: f.write(data)
        return cp
    except Exception:
        return None

def show_cover(path, width=40, height=20):
    """Показывает обложку через chafa."""
    if not path or not os.path.exists(path): return
    if not has_cmd("chafa"): return
    try:
        subprocess.run(
            ["chafa", f"--size={width}x{height}", "--symbols=block",
             "--fg-only", "--dither=fs", "--colors=256", path])
    except Exception:
        pass

# ═══════════ FAVORITES ═══════════
def load_favs():
    if not os.path.exists(FAV_FILE): return set()
    try:
        with open(FAV_FILE, encoding="utf-8") as f:
            d = json.load(f)
            return set(d.get("paths", []))
    except: return set()

def save_favs(favs):
    try:
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump({"paths": sorted(favs)}, f, ensure_ascii=False, indent=1)
    except: pass

# ═══════════ ЭКСПОРТ ═══════════
def export_m3u(tracks, name="playlist"):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{name}.m3u")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for t in tracks:
                dur = int(t.get("duration") or -1)
                f.write(f"#EXTINF:{dur},{t.get('artist','')} - {t.get('title','')}\n")
                f.write(f"{t['path']}\n")
        return path
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")
        return None

def export_csv(tracks, name="library"):
    import csv
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{name}.csv")
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Artist","Title","Album","Genre","Year","Duration","Type","Path"])
            for t in tracks:
                w.writerow([
                    t.get("artist",""), t.get("title",""), t.get("album",""),
                    t.get("genre",""), t.get("year",""), t.get("duration",""),
                    t.get("type",""), t.get("path","")
                ])
        return path
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")
        return None

# ═══════════ БИБЛИОТЕКА ═══════════
def load_cache():
    if not os.path.exists(CACHE_FILE):
        console.print("[red]❌ Кэш не найден. Запусти music-meta[/]")
        return None
    try:
        with open(CACHE_FILE, encoding="utf-8") as f: return json.load(f)
    except Exception as e:
        console.print(f"[red]❌ {e}[/]"); return None

def build_library(cache):
    artists = {}; skipped = 0
    for path, m in cache["tracks"].items():
        if not os.path.exists(path): continue
        a = (m.get("artist") or "Неизвестен").strip()
        alb = (m.get("album") or "Без альбома").strip()
        try: size = os.path.getsize(path)
        except: size = 0
        track = {
            "title": m.get("title") or os.path.basename(path),
            "path": path, "duration": m.get("duration") or 0,
            "size": size, "genre": (m.get("genre") or "").strip(),
            "year": (m.get("year") or "").strip(),
            "type": m.get("type") or "song", "source": m.get("source") or "local",
            "album": alb, "artist": a,
        }
        if not is_music_track(track):
            skipped += 1; continue
        ak = nkey(a)
        if ak not in artists:
            artists[ak] = {"display": a, "albums": {}, "genres": set()}
        alk = nkey(alb)
        if alk not in artists[ak]["albums"]:
            artists[ak]["albums"][alk] = {"display": alb, "tracks": []}
        artists[ak]["albums"][alk]["tracks"].append(track)
        if track["genre"]: artists[ak]["genres"].add(track["genre"])
    for a in artists.values():
        for alb in a["albums"].values():
            alb["tracks"].sort(key=lambda x: x["title"].lower())
    return artists, skipped

def all_tracks(artists):
    o = []
    for a in artists.values():
        for alb in a["albums"].values(): o.extend(alb["tracks"])
    return o

def all_genres(artists):
    g = {}
    for a in artists.values():
        for alb in a["albums"].values():
            for t in alb["tracks"]:
                if t.get("genre"): g[t["genre"]] = g.get(t["genre"],0)+1
    return g

def all_types(artists):
    tp = {}
    for a in artists.values():
        for alb in a["albums"].values():
            for t in alb["tracks"]:
                k = t.get("type") or "song"; tp[k] = tp.get(k,0)+1
    return tp

# ═══════════ ПЛЕЕР ═══════════
PS = {"playing":False,"path":None,"title":None,"artist":None,"album":None,
      "genre":None,"year":None,"type":None,"duration":0,"started_at":0}

def play_track(path, track=None):
    run("termux-media-player stop"); time.sleep(0.2)
    r = run(f'termux-media-player play "{path}"', timeout=10)
    if r is not None and r.returncode == 0:
        PS.update({"playing":True,"path":path,"started_at":time.time()})
        if track:
            for k in ("title","artist","album","genre","year","type"):
                PS[k] = track.get(k)
            PS["duration"] = track.get("duration") or 0
        return True
    return False

def stop_playback():
    run("termux-media-player stop")
    PS.update({"playing":False,"path":None,"started_at":0})

def cur_pos():
    return max(0, int(time.time() - PS["started_at"])) if PS["playing"] else 0

def now_playing_panel(show_cover_img=False):
    if not PS["playing"]: return None
    pos = cur_pos(); dur = PS["duration"] or 0
    if dur > 0:
        bw = 40; filled = min(int((pos/dur)*bw), bw)
        bar = "▓"*filled + "░"*(bw-filled)
    else:
        bar = "▓"*8 + "░"*32
    gc = genre_color(PS["genre"])
    lines = [
        Text(f"  ▶  {PS['artist']} — {PS['title']}", style=f"bold {WHITE}"),
        Text(f"     💿 {PS['album'] or '—'}", style=f"dim {GRAY}"),
    ]
    if PS["genre"]:
        lines.append(Text(f"     🎼 {PS['genre']}", style=gc))
    lines.append(Text(f"     {bar}  {fmt_duration(pos)} / {fmt_duration(dur) if dur else '--:--'}", style=GREEN_BRIGHT))
    return Panel(Group(*lines), title=f"[bold {YELLOW}]┃ PLAYING ┃[/]",
                 border_style=GREEN_DIM, padding=(0,1))

def play_and_wait(track, pool=None):
    if not play_track(track["path"], track):
        console.print(f"[red]❌ Не удалось запустить[/]"); return

    console.clear()
    console.print()
    # ⬅️ Обложка слева, панель справа
    cover_path = ensure_cover(track.get("artist",""), track.get("album",""), track.get("title",""))
    if cover_path and has_cmd("chafa"):
        console.print(f"[dim]🎨 Обложка: {os.path.basename(cover_path)}[/]")
        console.print()
        show_cover(cover_path, width=40, height=18)
        console.print()
    console.print(now_playing_panel())
    console.print()
    console.print(f"  [dim]s = стоп  ·  n = след.  ·  f = ♥  ·  Enter = назад[/]\n")

    try:
        import termios, tty, select
        has_t = True
    except: has_t = False

    def read_key():
        if not has_t: return None
        fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            rl, _, _ = select.select([sys.stdin], [], [], 0.3)
            if rl: return sys.stdin.read(1)
        except: return None
        finally:
            try: termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except: pass
        return None

    max_dur = PS["duration"] if PS["duration"] > 0 else 300
    start = time.time()
    favs = load_favs()

    try:
        while PS["playing"]:
            elapsed = time.time() - start
            if PS["duration"] > 0 and cur_pos() >= PS["duration"]:
                stop_playback(); console.print(f"  [dim]✔ Завершён[/]")
                return "done"
            if PS["duration"] == 0 and elapsed > max_dur:
                stop_playback(); console.print(f"  [dim]✔ Таймаут[/]")
                return "done"

            k = read_key()
            if k:
                kl = k.lower()
                if kl in ("s","q"):
                    stop_playback(); console.print(f"  [yellow]⏹ Стоп[/]")
                    return "stop"
                elif kl == "n" and pool:
                    tr = random.choice(pool); stop_playback(); time.sleep(0.3)
                    return play_and_wait(tr, pool)
                elif kl == "f":
                    p = track["path"]
                    if p in favs:
                        favs.discard(p); console.print(f"  [dim]💔 Убран из favorites[/]")
                    else:
                        favs.add(p); console.print(f"  [magenta]♥ Добавлен в favorites[/]")
                    save_favs(favs); time.sleep(0.5)
                elif k in ("\r","\n","\x1b"):
                    return "back"
            time.sleep(0.2)
    except KeyboardInterrupt:
        stop_playback(); console.print(f"\n  [yellow]⏹[/]")
        return "stop"
    return "done"

# ═══════════ ТАБЛИЦЫ ═══════════
def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("─"*60, style=GREEN_DIM))
    return Group(*lines)

def stats_panel(artists, favs):
    tt = sum(len(alb["tracks"]) for a in artists.values() for alb in a["albums"].values())
    ts = sum(t["size"] for a in artists.values() for alb in a["albums"].values() for t in alb["tracks"])
    g = all_genres(artists)
    t = Table(box=None, show_header=False, padding=(0,3))
    t.add_column("", style=f"bold {YELLOW}"); t.add_column("", style=f"bold {CYAN}")
    t.add_column("", style=f"bold {YELLOW}"); t.add_column("", style=f"bold {CYAN}")
    t.add_row("🎤 Исполнителей", str(len(artists)), "🎵 Треков", str(tt))
    t.add_row("💾 Вес", human_size(ts), "🎼 Жанров", str(len(g)))
    t.add_row("♥ Favorites", str(len(favs)), "", "")
    return t

def commands_panel(extra=None):
    rows = [("<номер>","🎤 Выбрать")]
    if extra: rows.extend(extra)
    rows += [("random","🎲 Случайный"),("favorites","♥ Favorites"),
             ("export","💾 Экспорт"),("stop","⏹ Стоп"),("q","🚪 Выход")]
    c = Table(box=None, show_header=False, padding=(0,2))
    c.add_column("", style=f"bold {YELLOW}", width=16, justify="right")
    c.add_column("", style=f"{CYAN}")
    half = (len(rows)+1)//2
    for i in range(half):
        L = rows[i]; R = rows[i+half] if i+half < len(rows) else None
        c.add_row(escape(f"[{L[0]}]"), L[1], escape(f"[{R[0]}]") if R else "", R[1] if R else "")
    return Panel(c, title=f"[bold {CYAN}]⌨  КОМАНДЫ[/]", border_style=CYAN, padding=(0,1))

def artists_table(items, page, favs):
    tp = max(1, (len(items)+PAGE_SIZE-1)//PAGE_SIZE)
    page = max(1, min(page, tp)); s = (page-1)*PAGE_SIZE; e = s+PAGE_SIZE
    t = Table(box=SIMPLE_HEAD, border_style=GREEN_DIM,
              header_style=f"bold {GREEN_BRIGHT}", padding=(0,2), expand=True)
    t.add_column("#", justify="right", width=4, style=f"bold {YELLOW}")
    t.add_column("ИСПОЛНИТЕЛЬ", style=WHITE)
    t.add_column("ТРЕКОВ", justify="right", width=8, style=CYAN)
    t.add_column("ЖАНР", width=20)
    for i, (ak, a) in enumerate(items[s:e], s+1):
        cnt = sum(len(alb["tracks"]) for alb in a["albums"].values())
        gl = list(a["genres"]); mg = gl[0] if gl else "—"
        t.add_row(str(i), a["display"], str(cnt), Text(mg[:18], style=genre_color(mg)))
    return t, page, tp

def tracks_table(tracks, start_idx=1, favs=None):
    favs = favs or set()
    t = Table(box=SIMPLE_HEAD, border_style=MAGENTA,
              header_style=f"bold {MAGENTA}", padding=(0,1),
              expand=True, show_header=False)
    t.add_column("♥", width=3, justify="center")
    t.add_column("#", justify="right", width=4, style=f"bold {YELLOW}")
    t.add_column("НАЗВАНИЕ", style=WHITE)
    t.add_column("ЖАНР", width=16); t.add_column("ТИП", width=14)
    t.add_column("ВРЕМЯ", justify="right", width=8, style=GRAY)
    for i, tr in enumerate(tracks, start_idx):
        heart = "[magenta]♥[/]" if tr["path"] in favs else " "
        t.add_row(heart, str(i), tr["title"][:55],
                  Text((tr.get("genre") or "—")[:14], style=genre_color(tr.get("genre",""))),
                  Text(TYPE_LABELS.get(tr.get("type"),"—"), style=CYAN),
                  fmt_duration(tr["duration"]))
    return t

def filter_tracks(artists, st):
    o = []
    for t in all_tracks(artists):
        if st.get("fg") and t.get("genre","").lower() != st["fg"].lower(): continue
        if st.get("ft") and t.get("type") != st["ft"]: continue
        if st.get("s"):
            q = st["s"].lower()
            if q not in f"{t.get('title','')} {t.get('genre','')} {t.get('artist','')}".lower(): continue
        o.append(t)
    return o

COMMANDS = ["bygenre","bytype","random","favorites","export","stop","q","back","n","p","f","help"]

class MusicComp(Completer):
    def get_completions(self, doc, ev):
        t = doc.text_before_cursor
        if " " in t: return
        for c in sorted(COMMANDS):
            if c.startswith(t.lower()): yield Completion(c, start_position=-len(t))
        if t.isdigit() or t == "":
            for i in range(1,21):
                si = str(i)
                if si.startswith(t): yield Completion(si, start_position=-len(t))

def main():
    if not has_cmd("termux-media-player"):
        console.clear(); console.print("[red]❌ termux-media-player не найден[/]"); return
    cache = load_cache()
    if not cache: return
    console.clear()
    with console.status(f"[bold {GREEN_BRIGHT}]🎵 Загрузка...[/]", spinner="dots"):
        artists, skipped = build_library(cache)
    if not artists:
        console.print("[red]❌ Нет музыки (всё отфильтровано)[/]"); return
    favs = load_favs()
    console.print(f"[green]✔ Загружено[/]  ·  [dim]пропущено: {skipped}  ·  favorites: {len(favs)}[/]")
    time.sleep(0.8)

    state = {"mode":"main","artist_key":None,"page":1,"search":"","fg":None,"ft":None,
             "current_tracks":[],"current_filtered":[],"filter_page":1}

    session = PromptSession(
        completer=MusicComp(), complete_while_typing=True,
        style=Style.from_dict({
            "prompt": "bold ansibrightmagenta",
            "completion-menu.completion": "bg:#000000 #00ff88",
            "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
        }))

    while True:
        console.clear()
        if state["mode"]=="main":
            title = "М У З Ы К А Л Ь Н А Я   Б И Б Л И О Т Е К А"
            sub = "Terminal Argonov  •  Music Edition  •  с обложками"
        elif state["mode"]=="favorites":
            title = "♥  F A V O R I T E S"
            sub = f"{len(favs)} треков"
        else:
            d = artists[state["artist_key"]]
            title = f"🎤  {d['display']}"
            sub = ", ".join(sorted(d["genres"]))[:60] or ""

        console.print(); console.print(title_block(title, sub)); console.print()
        if PS["playing"]:
            np = now_playing_panel()
            if np: console.print(np); console.print()

        # ── FAVORITES ──
        if state["mode"]=="favorites":
            fav_tracks = [t for t in all_tracks(artists) if t["path"] in favs]
            if not fav_tracks:
                console.print(Text("💔 Favorites пусто. Нажми 'f' при воспроизведении.", style=GRAY))
            else:
                console.print(tracks_table(fav_tracks, favs=favs))
                state["current_filtered"] = fav_tracks
            console.print()
            console.print(commands_panel([("back","◀ К библиотеке"),("export","💾 Экспорт")]))
        # ── MAIN ──
        elif state["mode"]=="main":
            console.print(stats_panel(artists, favs)); console.print()
            hf = state["fg"] or state["ft"] or state["search"]
            if hf:
                fl = Text(); fl.append("🔎 ", style=YELLOW)
                if state["fg"]: fl.append(f"жанр: {state['fg']}  ", style=genre_color(state['fg']))
                if state["ft"]: fl.append(f"тип: {TYPE_LABELS.get(state['ft'],state['ft'])}  ", style=CYAN)
                if state["search"]: fl.append(f"поиск: {state['search']}", style=YELLOW)
                console.print(fl); console.print()
                tracks = filter_tracks(artists, {"fg":state["fg"],"ft":state["ft"],"s":state["search"]})
                if not tracks:
                    console.print(Text("❌ Ничего не найдено", style=RED)); console.print()
                else:
                    tp = max(1,(len(tracks)+PAGE_SIZE-1)//PAGE_SIZE)
                    state["filter_page"] = max(1,min(state["filter_page"],tp))
                    s = (state["filter_page"]-1)*PAGE_SIZE; e = s+PAGE_SIZE
                    state["current_filtered"] = tracks
                    console.print(tracks_table(tracks[s:e], start_idx=s+1, favs=favs)); console.print()
                    console.print(Text(f"   Стр. {state['filter_page']}/{tp}  ·  всего {len(tracks)}", style=f"dim {GRAY}")); console.print()
                console.print(commands_panel([("n/p","◀ ▶"),("f","Сброс"),
                                               ("/слово","Поиск"),("bygenre","Жанр"),("bytype","Тип")]))
            else:
                items = sorted(artists.items(), key=lambda x: x[1]["display"].lower())
                tbl, p, tp = artists_table(items, state["page"], favs); state["page"] = p
                console.print(tbl); console.print()
                console.print(Text(f"   Стр. {p}/{tp}  ·  всего {len(items)}", style=f"dim {GRAY}")); console.print()
                console.print(commands_panel([("n/p","◀ ▶"),("/слово","Поиск"),
                                               ("bygenre","Жанр"),("bytype","Тип")]))
        # ── ARTIST ──
        else:
            d = artists[state["artist_key"]]
            state["current_tracks"] = []; flat = []; idx = 1
            albums = sorted(d["albums"].items(),
                            key=lambda x: (x[1]["display"]=="Без альбома", x[1]["display"].lower()))
            for alk, alb in albums:
                console.print(Text(f"💿 {alb['display']}  ({len(alb['tracks'])})", style=f"bold {MAGENTA}"))
                console.print(tracks_table(alb["tracks"], start_idx=idx, favs=favs)); console.print()
                flat.extend(alb["tracks"]); idx += len(alb["tracks"])
            state["current_tracks"] = flat
            console.print(commands_panel([("back","◀ К списку")]))

        try:
            cmd = session.prompt(FormattedText([("bold ansibrightmagenta","╰─❯ ")])).strip()
        except: console.print(Text("\n До связи. 🖖", style=f"dim {GREEN_DIM}")); stop_playback(); break

        if not cmd: continue
        cl = cmd.lower()

        if cl in ("q","exit","quit","выход"): stop_playback(); break
        if cl=="stop": stop_playback(); console.print(Text("  ⏹ Стоп", style=YELLOW)); time.sleep(0.4); continue

        if cl=="random":
            pool = (state["current_filtered"] if state.get("current_filtered")
                    else state["current_tracks"] if state["mode"]=="artist"
                    else [t for t in all_tracks(artists) if t["path"] in favs] if state["mode"]=="favorites"
                    else all_tracks(artists))
            if pool:
                tr = random.choice(pool)
                play_and_wait(tr, pool)
            continue

        if cl=="favorites":
            state["mode"] = "favorites"
            state["current_filtered"] = []
            continue

        if cl=="back":
            if state["mode"] in ("favorites","artist"):
                state["mode"] = "main"
                state["artist_key"] = None
                state["page"] = 1
            continue

        if cl=="export":
            # Что экспортируем: filtered / favorites / всё
            pool = (state["current_filtered"] if state.get("current_filtered")
                    else state["current_tracks"] if state["mode"]=="artist"
                    else [t for t in all_tracks(artists) if t["path"] in favs] if state["mode"]=="favorites"
                    else all_tracks(artists))
            console.print()
            console.print("[yellow]💾 Экспорт:[/]")
            console.print(f"  [cyan]1[/])  M3U playlist")
            console.print(f"  [cyan]2[/])  CSV (Excel)")
            console.print(f"  [cyan]0[/])  Отмена")
            try:
                ch = console.input("[bold magenta]Выбери> [/]").strip()
            except: continue
            name = f"export_{int(time.time())}"
            if ch == "1":
                p = export_m3u(pool, name)
                if p: console.print(f"[green]✔ {p}[/] ({len(pool)} треков)")
            elif ch == "2":
                p = export_csv(pool, name)
                if p: console.print(f"[green]✔ {p}[/] ({len(pool)} треков)")
            console.print()
            console.input("[dim]Enter — назад[/] ")
            continue

        if cl=="bygenre":
            g = all_genres(artists)
            if not g: continue
            console.clear(); console.print(); console.print(title_block("ВЫБОР ЖАНРА")); console.print()
            t = Table(box=SIMPLE_HEAD, border_style=MAGENTA, header_style=f"bold {MAGENTA}", padding=(0,2))
            t.add_column("#", style=f"bold {YELLOW}", width=4, justify="right")
            t.add_column("ЖАНР", style=WHITE); t.add_column("ТРЕКОВ", style=CYAN, justify="right", width=10)
            gs = sorted(g.items(), key=lambda x: -x[1])
            for i, (gg, c) in enumerate(gs, 1): t.add_row(str(i), Text(gg, style=genre_color(gg)), str(c))
            console.print(t); console.print(Text("\n  0 — сброс  •  Enter — назад", style=f"dim {GRAY}")); console.print()
            try:
                ch = console.input(Text("╰─[жанр]❯ ", style=f"bold {GREEN_BRIGHT}")).strip()
                if ch=="0": state["fg"]=None
                elif ch.isdigit() and 1<=int(ch)<=len(gs): state["fg"]=gs[int(ch)-1][0]
                state["filter_page"]=1; state["current_filtered"]=[]
            except: pass
            continue

        if cl=="bytype":
            tp = all_types(artists)
            if not tp: continue
            console.clear(); console.print(); console.print(title_block("ВЫБОР ТИПА")); console.print()
            t = Table(box=SIMPLE_HEAD, border_style=CYAN, header_style=f"bold {CYAN}", padding=(0,2))
            t.add_column("#", style=f"bold {YELLOW}", width=4, justify="right")
            t.add_column("ТИП", style=WHITE); t.add_column("ТРЕКОВ", style=CYAN, justify="right", width=10)
            ts = sorted(tp.items(), key=lambda x: -x[1])
            for i, (tt, c) in enumerate(ts, 1): t.add_row(str(i), TYPE_LABELS.get(tt,tt), str(c))
            console.print(t); console.print(Text("\n  0 — сброс  •  Enter — назад", style=f"dim {GRAY}")); console.print()
            try:
                ch = console.input(Text("╰─[тип]❯ ", style=f"bold {GREEN_BRIGHT}")).strip()
                if ch=="0": state["ft"]=None
                elif ch.isdigit() and 1<=int(ch)<=len(ts): state["ft"]=ts[int(ch)-1][0]
                state["filter_page"]=1; state["current_filtered"]=[]
            except: pass
            continue

        if cl=="f":
            state["fg"]=None; state["ft"]=None; state["search"]=""
            state["filter_page"]=1; state["current_filtered"]=[]
            continue
        if cmd.startswith("/"):
            state["search"]=cmd[1:].strip(); state["filter_page"]=1; state["current_filtered"]=[]
            continue

        if state["mode"]=="main":
            hf = state["fg"] or state["ft"] or state["search"]
            if hf:
                if cl=="n": state["filter_page"]+=1; continue
                if cl=="p" and state["filter_page"]>1: state["filter_page"]-=1; continue
            else:
                if cl=="n": state["page"]+=1; continue
                if cl=="p" and state["page"]>1: state["page"]-=1; continue

        if cl.isdigit():
            num = int(cl)
            if state["mode"]=="main":
                hf = state["fg"] or state["ft"] or state["search"]
                if hf:
                    tracks = state["current_filtered"] or filter_tracks(artists,
                        {"fg":state["fg"],"ft":state["ft"],"s":state["search"]})
                    if 1<=num<=len(tracks):
                        tr = tracks[num-1]
                        play_and_wait(tr, tracks)
                    else: console.print(f"[red]❌ 1..{len(tracks)}[/]"); time.sleep(0.8)
                else:
                    items = sorted(artists.items(), key=lambda x: x[1]["display"].lower())
                    s = (state["page"]-1)*PAGE_SIZE; e = s+PAGE_SIZE
                    if s+1<=num<=min(e, len(items)):
                        state["artist_key"]=items[num-1][0]; state["mode"]="artist"
                    else: console.print("[red]❌ вне страницы[/]"); time.sleep(0.8)
            elif state["mode"]=="favorites":
                fav_tracks = [t for t in all_tracks(artists) if t["path"] in favs]
                if 1<=num<=len(fav_tracks):
                    play_and_wait(fav_tracks[num-1], fav_tracks)
                else: console.print(f"[red]❌ 1..{len(fav_tracks)}[/]"); time.sleep(0.8)
            else:
                if 1<=num<=len(state["current_tracks"]):
                    play_and_wait(state["current_tracks"][num-1], state["current_tracks"])
                else: console.print(f"[red]❌ 1..{len(state['current_tracks'])}[/]"); time.sleep(0.8)
            continue

        console.print(Text(f"  ❌ {cmd}", style=RED)); time.sleep(0.6)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        stop_playback(); console.print(Text("\n Прервано.", style=f"dim {GREEN_DIM}"))
```

---

## 📄 music_meta.py

*16841 байт · 420 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Music Metadata Fetcher v2 — iTunes + Deezer + MusicBrainz, потокобезопасный"""

import os, re, json, time, sys
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn
from rich import box

console = Console()

CACHE_DIR = os.path.expanduser("~/music_cache")
CACHE_FILE = os.path.join(CACHE_DIR, "library.json")
CACHE_VERSION = 2

AUDIO_EXTS = {".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac",
              ".wav", ".wma", ".amr", ".3gp", ".3gpp", ".mp4a"}

SEARCH_DIRS = [
    os.path.expanduser("~/storage/music"),
    os.path.expanduser("~/storage/shared/Music"),
    os.path.expanduser("~/storage/shared/Download"),
    os.path.expanduser("~/storage/shared/Downloads"),
    os.path.expanduser("~/storage/shared/WhatsApp/Media/WhatsApp Audio"),
    os.path.expanduser("~/storage/shared/Telegram"),
    os.path.expanduser("~/storage/shared/DCIM"),
    os.path.expanduser("~/storage/shared/Ringtones"),
    os.path.expanduser("~/storage/shared/Notifications"),
    os.path.expanduser("~/storage/shared/Alarms"),
    os.path.expanduser("~/storage/shared/Podcasts"),
    os.path.expanduser("~/storage/shared"),
]

# ═══════════ ТИПЫ ТРЕКОВ ═══════════
TYPE_PATTERNS = [
    ("opening", [r"\bop\s?\d", r"\bopening\b", r"опенинг", r"\bop\d+\b", r"\bop\b"]),
    ("ending",  [r"\bed\s?\d", r"\bending\b", r"эндинг", r"\bed\d+\b", r"\bed\b"]),
    ("ost",     [r"\bost\b", r"soundtrack", r"саундтрек", r"original soundtrack"]),
    ("theme",   [r"\btheme\b", r"\bтема\b", r"main theme"]),
    ("game",    [r"\bgame\b", r"игров", r"game ost", r"игра\b"]),
    ("anime",   [r"\banime\b", r"аниме"]),
    ("film",    [r"\bfilm\b", r"\bmovie\b", r"кино\b", r"из фильма"]),
    ("classical", [r"classical", r"классика", r"симфони"]),
    ("remix",   [r"\bremix\b", r"ремикс", r"\bmix\b"]),
    ("live",    [r"\blive\b", r"концерт"]),
    ("acoustic", [r"acoustic", r"акустик"]),
    ("cover",   [r"\bcover\b", r"кавер"]),
    ("instrumental", [r"instrumental", r"инструментал"]),
]

def detect_type(title, path):
    parts = [p.lower() for p in path.split(os.sep)]
    for part in parts:
        for t, patterns in TYPE_PATTERNS:
            for p in patterns:
                if re.search(p, part, re.IGNORECASE):
                    return t
    text = (str(title) + " " + str(path)).lower()
    for t, patterns in TYPE_PATTERNS:
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                return t
    return "song"

# ═══════════ HTTP ═══════════
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "TermuxMusicMeta/2.0 ( https://termux.dev )",
    "Accept": "application/json",
})

def clean_query(s):
    if not s: return ""
    s = str(s).strip()
    s = re.sub(r"^\d{1,3}[\s.\-_]+\s*", "", s)
    s = re.sub(r"[\(\[].*?[\)\]]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# ═══════════ iTUNES ═══════════
def search_itunes(query):
    if not query: return None
    for attempt in range(2):
        try:
            r = SESSION.get("https://itunes.apple.com/search",
                params={"term": query, "entity": "song", "limit": 1}, timeout=8)
            if r.status_code != 200: return None
            results = r.json().get("results", [])
            if not results: return None
            f = results[0]
            return {
                "artist": f.get("artistName", "").strip(),
                "title":  f.get("trackName", "").strip(),
                "album":  f.get("collectionName", "").strip(),
                "genre":  f.get("primaryGenreName", "").strip(),
                "year":   (f.get("releaseDate") or "")[:4],
                "source": "itunes",
            }
        except Exception:
            if attempt == 0: time.sleep(0.5)
    return None

# ═══════════ DEEZER ═══════════
def search_deezer(query):
    if not query: return None
    for attempt in range(2):
        try:
            r = SESSION.get("https://api.deezer.com/search",
                params={"q": query, "limit": 1}, timeout=8)
            if r.status_code != 200: return None
            items = r.json().get("data", [])
            if not items: return None
            f = items[0]
            return {
                "artist": f.get("artist", {}).get("name", "").strip(),
                "title":  f.get("title", "").strip(),
                "album":  f.get("album", {}).get("title", "").strip(),
                "genre":  "",
                "year":   "",
                "source": "deezer",
            }
        except Exception:
            if attempt == 0: time.sleep(0.5)
    return None

# ═══════════ MUSICBRAINZ ═══════════
def search_musicbrainz(query):
    if not query: return None
    for attempt in range(2):
        try:
            # MusicBrainz любит Lucene-синтаксис
            r = SESSION.get("https://musicbrainz.org/ws/2/recording",
                params={"query": query, "fmt": "json", "limit": 1}, timeout=10)
            if r.status_code != 200: return None
            recordings = r.json().get("recordings", [])
            if not recordings: return None
            rec = recordings[0]
            title = rec.get("title", "").strip()
            # Artist
            credits = rec.get("artist-credit", [])
            artist = ""
            if credits:
                artist = "".join(
                    (c.get("name") or "") + (c.get("joinphrase") or "")
                    for c in credits
                ).strip()
            # Album
            album = ""
            releases = rec.get("releases", [])
            if releases:
                album = (releases[0].get("title") or "").strip()
            # Year
            year = ""
            if releases:
                date = releases[0].get("date", "")
                if date: year = date[:4]
            # Genre — из tags
            genre = ""
            tags = rec.get("tags", [])
            if tags:
                genre = tags[0].get("name", "").capitalize()
            return {
                "artist": artist,
                "title":  title,
                "album":  album,
                "genre":  genre,
                "year":   year,
                "source": "musicbrainz",
            }
        except Exception:
            if attempt == 0: time.sleep(0.5)
    return None

def fetch_metadata(title, artist):
    """Каскад: iTunes → Deezer → MusicBrainz"""
    if not title and not artist:
        return None

    # Пробуем artist + title
    if artist and title:
        q = clean_query(f"{artist} {title}")
        for fn in (search_itunes, search_deezer, search_musicbrainz):
            res = fn(q)
            if res and res.get("title"):
                return res

    # Только title
    if title:
        q = clean_query(title)
        for fn in (search_itunes, search_deezer, search_musicbrainz):
            res = fn(q)
            if res and res.get("title"):
                return res

    return None

# ═══════════ ЛОКАЛЬНЫЕ ТЕГИ ═══════════
def read_local_metadata(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    artist = album = title = None
    duration = 0
    try:
        from mutagen import File as MutagenFile
        audio = MutagenFile(path, easy=True)
        if audio:
            if audio.get("artist"):  artist = audio["artist"][0].strip()
            if audio.get("album"):   album  = audio["album"][0].strip()
            if audio.get("title"):   title  = audio["title"][0].strip()
        audio2 = MutagenFile(path)
        if audio2 and hasattr(audio2, "info") and audio2.info:
            duration = int(audio2.info.length)
    except Exception:
        pass

    if not title or not artist:
        name = re.sub(r"^\d{1,3}[\s.\-_]+\s*", "", filename)
        if " - " in name:
            left, right = name.split(" - ", 1)
            if not artist: artist = left.strip()
            if not title:  title  = right.strip()
        else:
            if not title: title = name

    return artist or "", album or "", title or filename, duration

# ═══════════ КЭШ ═══════════
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {"version": CACHE_VERSION, "tracks": {}}
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            data = json.load(f)
            if data.get("version") != CACHE_VERSION:
                # Мигрируем: старые версии совместимы
                data["version"] = CACHE_VERSION
            data.setdefault("tracks", {})
            return data
    except Exception:
        return {"version": CACHE_VERSION, "tracks": {}}

def save_cache(cache):
    """Сохраняет кэш. Делает снимок dict чтобы избежать ошибок."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = CACHE_FILE + ".tmp"
    # Снимок — теперь точно никто не изменит во время записи
    snapshot = {"version": cache.get("version", CACHE_VERSION),
                "tracks": dict(cache["tracks"])}
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=1)
    os.replace(tmp, CACHE_FILE)

# ═══════════ ФАЙЛЫ ═══════════
def find_all_audio():
    found, seen = [], set()
    for base in SEARCH_DIRS:
        if not os.path.isdir(base): continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in
                       ("Android/data", "Android/obb", ".thumbnails", ".cache")]
            for f in files:
                if os.path.splitext(f)[1].lower() in AUDIO_EXTS:
                    full = os.path.join(root, f)
                    if full not in seen:
                        seen.add(full); found.append(full)
    return found

# ═══════════ ВОРКЕР (НЕ пишет в кэш!) ═══════════
def worker(path, force):
    """
    Читает метаданные и ищет в интернете.
    ВАЖНО: возвращает (path, entry) или None. НЕ трогает общий кэш.
    """
    local_artist, local_album, local_title, dur = read_local_metadata(path)
    track_type = detect_type(local_title, path)

    # Убираем "Неизвестен" из запроса, чтобы не мусорить
    q_artist = local_artist if local_artist and local_artist.lower() not in ("неизвестен", "unknown") else ""

    # Если в локальных тегах уже есть artist + title — попробуем сначала найти только жанр
    remote = fetch_metadata(local_title, q_artist)

    if remote:
        entry = {
            "title":  remote.get("title") or local_title,
            "artist": remote.get("artist") or local_artist or "Неизвестен",
            "album":  remote.get("album") or local_album or "",
            "genre":  remote.get("genre") or "",
            "year":   remote.get("year") or "",
            "type":   track_type,
            "source": remote.get("source"),
            "duration": dur,
        }
    else:
        entry = {
            "title":  local_title,
            "artist": local_artist or "Неизвестен",
            "album":  local_album or "",
            "genre":  "",
            "year":   "",
            "type":   track_type,
            "source": "local",
            "duration": dur,
        }
    return (path, entry)

# ═══════════ ГЛАВНОЕ ═══════════
def main():
    console.clear()
    force = "--force" in sys.argv

    console.print()
    console.print(Align.center(Panel.fit(
        "[bold green]🌐  MUSIC METADATA FETCHER v2  🌐[/]\n"
        "[dim]iTunes + Deezer + MusicBrainz → кэш в ~/music_cache/[/]",
        border_style="green")))
    console.print()

    console.print("[bold yellow]🔍 Сканирую память телефона...[/]")
    files = find_all_audio()
    console.print(f"   Найдено аудиофайлов: [green]{len(files)}[/]\n")

    cache = load_cache()
    cached_count = len(cache["tracks"])
    console.print(f"💾 В кэше уже: [green]{cached_count}[/] записей\n")

    # Отбираем треки для поиска
    to_process = []
    for f in files:
        existing = cache["tracks"].get(f)
        if force:
            to_process.append(f)
        else:
            # Ищем только те, у которых нет данных из интернета
            if not existing or existing.get("source") in (None, "local", "filename", "filename-only"):
                to_process.append(f)

    if not to_process:
        console.print("[green]✔ Всё уже найдено. Нечего искать.[/]")
        console.print("[dim]Запусти music-force для полного переискивания.[/]")
        return

    console.print(f"[bold cyan]📡 Ищу: {len(to_process)} треков (параллельно в 6 потоков)[/]")
    console.print("[dim]Можно прервать Ctrl+C — прогресс сохранится.[/]\n")

    done = 0
    found_remote = 0
    found_mb = 0
    not_found = 0
    save_every = 20

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            console=console,
        ) as prog:
            task = prog.add_task("Поиск...", total=len(to_process))

            # ВАЖНО: воркеры только возвращают результат, кэш мутирует ГЛАВНЫЙ поток
            with ThreadPoolExecutor(max_workers=6) as pool:
                futures = {pool.submit(worker, f, force): f for f in to_process}
                for fut in as_completed(futures):
                    try:
                        result = fut.result()
                        if result:
                            key, entry = result
                            # Мутация кэша — только в этом потоке
                            cache["tracks"][key] = entry
                            if entry.get("source") in ("itunes", "deezer", "musicbrainz"):
                                found_remote += 1
                                if entry.get("source") == "musicbrainz":
                                    found_mb += 1
                            else:
                                not_found += 1
                    except Exception:
                        pass

                    done += 1
                    prog.update(
                        task, advance=1,
                        description=f"[cyan]✔ {found_remote}  ✘ {not_found}  (MB: {found_mb})"
                    )

                    if done % save_every == 0:
                        try: save_cache(cache)
                        except Exception: pass
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Прервано. Сохраняю...[/]")

    try: save_cache(cache)
    except Exception as e:
        console.print(f"[red]❌ Ошибка сохранения: {e}[/]")

    console.print()
    t = Table(box=box.ROUNDED, show_header=False, border_style="green")
    t.add_column("", style="bold yellow", width=24)
    t.add_column("", style="white")
    t.add_row("✅ Найдено в интернете", f"[green]{found_remote}[/]")
    t.add_row("   из них MusicBrainz",  f"[cyan]{found_mb}[/]")
    t.add_row("⚠ Не найдено",          f"[yellow]{not_found}[/]")
    t.add_row("💾 Всего в кэше",         f"[cyan]{len(cache['tracks'])}[/]")
    t.add_row("📁 Файл",                 f"[dim]{CACHE_FILE}[/]")
    console.print(t)
    console.print()
    console.print("[green]✔ Готово. Запусти [cyan]music[/][/]")
    console.print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано.[/]")
```

---

## 📄 todo.py

*20040 байт · 448 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TODO — трекер задач с Tab-автодополнением и уведомлениями"""

import os, sys, json, re, subprocess, time
from datetime import datetime, timedelta
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

console = Console()
TODO_FILE = os.path.expanduser("~/.todo.json")

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"
ORANGE = "dark_orange"

PRIORITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🟢"}
PRIORITY_LABEL = {"high": "Высокий", "medium": "Средний", "low": "Низкий"}
PRIORITY_COLOR = {"high": RED, "medium": YELLOW, "low": GREEN_BRIGHT}

# ═══════════ ХРАНИЛИЩЕ ═══════════
def load_todo():
    if not os.path.exists(TODO_FILE):
        return {"next_id": 1, "tasks": []}
    try:
        with open(TODO_FILE, encoding="utf-8") as f:
            d = json.load(f)
            d.setdefault("next_id", 1)
            d.setdefault("tasks", [])
            return d
    except Exception:
        return {"next_id": 1, "tasks": []}

def save_todo(data):
    try:
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

# ═══════════ ПАРСИНГ ═══════════
def parse_date(s):
    """Поддержка: today, tomorrow, +3d, +2h, +1w, 15.09, 15.09.2026, 15.09 18:00"""
    s = s.lower().strip()
    now = datetime.now()
    if s in ("today", "сегодня"):     return now.strftime("%Y-%m-%d 23:59")
    if s in ("tomorrow", "завтра"):   return (now + timedelta(days=1)).strftime("%Y-%m-%d 23:59")
    m = re.match(r"\+(\d+)([dhmw])", s)
    if m:
        n = int(m.group(1)); u = m.group(2)
        delta = {"d": timedelta(days=n), "h": timedelta(hours=n),
                 "m": timedelta(minutes=n), "w": timedelta(weeks=n)}[u]
        return (now + delta).strftime("%Y-%m-%d %H:%M")
    m = re.match(r"(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?(?:\s+(\d{1,2}):(\d{2}))?$", s)
    if m:
        d = int(m.group(1)); mo = int(m.group(2))
        y  = int(m.group(3)) if m.group(3) else now.year
        h  = int(m.group(4)) if m.group(4) else 23
        mi = int(m.group(5)) if m.group(5) else 59
        try:
            return datetime(y, mo, d, h, mi).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return None
    return None

def parse_add(text):
    """add Купить молоко !high @tomorrow #покупки"""
    title_parts = []; priority = "medium"; deadline = None; tags = []
    for w in text.split():
        if w.startswith("!"):
            p = w[1:].lower()
            if p in ("h","high","1","в","высокий"): priority = "high"
            elif p in ("m","mid","medium","2","с","средний"): priority = "medium"
            elif p in ("l","low","3","н","низкий"): priority = "low"
        elif w.startswith("@") and not deadline:
            deadline = parse_date(w[1:])
        elif w.startswith("#") and len(w) > 1:
            tags.append(w[1:])
        else:
            title_parts.append(w)
    return {"title": " ".join(title_parts).strip(),
            "priority": priority, "deadline": deadline, "tags": tags}

# ═══════════ ДАТЫ / ПРИОРИТЕТЫ ═══════════
def is_overdue(task):
    if task.get("done") or not task.get("deadline"): return False
    try:
        return datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M") < datetime.now()
    except Exception:
        return False

def is_today(task):
    if task.get("done") or not task.get("deadline"): return False
    try:
        d = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
        return d.date() == datetime.now().date()
    except Exception:
        return False

def is_soon(task, hours=24):
    if task.get("done") or not task.get("deadline"): return False
    try:
        d = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
        delta = d - datetime.now()
        return timedelta(0) <= delta <= timedelta(hours=hours)
    except Exception:
        return False

def fmt_deadline(s):
    if not s: return "—"
    try:
        d = datetime.strptime(s, "%Y-%m-%d %H:%M")
        now = datetime.now()
        delta = d - now
        # Короткий формат
        date_s = d.strftime("%d.%m %H:%M")
        if d.date() == now.date():   date_s = f"сегодня {d.strftime('%H:%M')}"
        elif d.date() == (now + timedelta(days=1)).date(): date_s = f"завтра {d.strftime('%H:%M')}"
        if delta.total_seconds() < 0:
            return f"❗ {date_s}"
        if delta.total_seconds() < 3600:
            return f"⏰ {date_s} ({int(delta.total_seconds()//60)} мин)"
        if delta < timedelta(days=1):
            return f"⏰ {date_s}"
        return date_s
    except Exception:
        return s

# ═══════════ УВЕДОМЛЕНИЯ ═══════════
def notify(task):
    """Отправить уведомление через termux-notification"""
    title = f"📌 TODO #{task['id']}: {task['title']}"
    content = f"Приоритет: {PRIORITY_LABEL.get(task['priority'],'—')}"
    if task.get("deadline"): content += f"\nДедлайн: {fmt_deadline(task['deadline'])}"
    if task.get("tags"):     content += f"\nТеги: {', '.join(task['tags'])}"
    try:
        subprocess.run(["termux-notification",
            "--title", title, "--content", content,
            "--id", str(task["id"])], check=False)
        return True
    except Exception:
        return False

# ═══════════ РИСОВКА ═══════════
def clear(): os.system("clear")

def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("═"*60, style=GREEN_DIM))
    return Group(*lines)

def stats_panel(tasks):
    total = len(tasks)
    active = sum(1 for t in tasks if not t.get("done"))
    done = sum(1 for t in tasks if t.get("done"))
    overdue = sum(1 for t in tasks if is_overdue(t))
    today = sum(1 for t in tasks if is_today(t))
    t = Table(box=None, show_header=False, padding=(0, 3))
    for _ in range(4): t.add_column("")
    t.add_row(f"📋 Всего [bold]{total}[/]", f"⏳ Активных [bold]{active}[/]",
              f"✅ Выполнено [bold]{done}[/]", f"❗ Просрочено [bold]{overdue}[/]")
    t.add_row(f"📅 Сегодня [bold]{today}[/]", "", "", "")
    return t

def tasks_table(tasks, filter_mode="active"):
    """filter_mode: active, done, all, today, overdue"""
    now = datetime.now()
    if filter_mode == "active":
        shown = [t for t in tasks if not t.get("done")]
    elif filter_mode == "done":
        shown = [t for t in tasks if t.get("done")]
    elif filter_mode == "today":
        shown = [t for t in tasks if is_today(t)]
    elif filter_mode == "overdue":
        shown = [t for t in tasks if is_overdue(t)]
    else:
        shown = tasks

    # Сортировка: активные → по дедлайну → по приоритету
    def sort_key(t):
        pri = {"high": 0, "medium": 1, "low": 2}.get(t.get("priority"), 1)
        d = t.get("deadline") or "9999-99-99 99:99"
        return (t.get("done", False), d, pri)
    shown = sorted(shown, key=sort_key)

    if not shown:
        console.print(Text(f"  📭 Задач нет (фильтр: {filter_mode})", style=f"dim {GRAY}"))
        console.print()
        return

    t = Table(box=box.SIMPLE_HEAD, border_style=CYAN,
              header_style=f"bold {CYAN}", padding=(0, 1), expand=True)
    t.add_column("ID", style=f"bold {YELLOW}", width=4, justify="right")
    t.add_column("✓",  width=3, justify="center")
    t.add_column("!",  width=3, justify="center")
    t.add_column("Задача", style=WHITE)
    t.add_column("Дедлайн", width=22)
    t.add_column("Теги", style=MAGENTA, width=18)

    for task in shown:
        mark = "[green]✔[/]" if task.get("done") else "[ ]"
        pri_icon = PRIORITY_ICON.get(task.get("priority"), "⚪")
        title = task["title"]
        if task.get("done"):
            title = f"[dim strikethrough]{title}[/]"
        deadline_s = fmt_deadline(task.get("deadline"))
        if is_overdue(task):
            deadline_s = f"[bold {RED}]{deadline_s}[/]"
        elif is_soon(task):
            deadline_s = f"[{YELLOW}]{deadline_s}[/]"
        else:
            deadline_s = f"[{GRAY}]{deadline_s}[/]"
        tags_s = " ".join(f"#{x}" for x in task.get("tags", []))[:18] or "[dim]—[/]"
        t.add_row(str(task["id"]), mark, pri_icon, title, deadline_s, tags_s)
    console.print(t)
    console.print()

def commands_panel():
    t = Table(box=box.DOUBLE_EDGE, border_style="black",
              show_header=False, padding=(0, 2))
    t.add_column("Команда", style="bold yellow", width=26, justify="right")
    t.add_column("Действие", style="white")
    t.add_row("[cyan]add <текст> !high @tomorrow #tag[/]", "➕ Добавить задачу")
    t.add_row("[cyan]done <id>[/]",     "✅ Отметить выполненной")
    t.add_row("[cyan]undone <id>[/]",   "↩ Вернуть в работу")
    t.add_row("[cyan]del <id>[/]",      "🗑 Удалить задачу")
    t.add_row("[cyan]edit <id>[/]",     "✏ Изменить задачу")
    t.add_row("[cyan]notify <id>[/]",   "🔔 Отправить уведомление")
    t.add_row("[cyan]notify-all[/]",    "🔔 Уведомить о всех активных")
    t.add_row("[cyan]filter <mode>[/]", "🔎 filter: active/done/all/today/overdue")
    t.add_row("[cyan]clear-done[/]",    "🧹 Удалить все выполненные")
    t.add_row("[cyan]q[/]",             "🚪 Выход")
    console.print(Panel(t, title="[bold green]⌨  КОМАНДЫ  (Tab — автодополнение)[/]",
                        border_style="black"))
    console.print()

# ═══════════ TAB-COMPLETER ═══════════
class TodoCompleter(Completer):
    def __init__(self, get_tasks):
        self.get_tasks = get_tasks

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        # Первое слово — команда
        if not words or (len(words) == 1 and not text.endswith(" ")):
            partial = words[0] if words else ""
            commands = [
                "add","done","undone","del","edit","notify","notify-all",
                "filter","clear-done","clear","help","q",
            ]
            for c in commands:
                if c.startswith(partial.lower()):
                    yield Completion(c, start_position=-len(partial))
            return
        cmd = words[0].lower()
        partial = words[-1] if not text.endswith(" ") else ""

        if cmd in ("done","undone","del","edit","notify"):
            tasks = self.get_tasks()
            for t in tasks:
                sid = str(t["id"])
                if sid.startswith(partial):
                    label = f'{sid}  {t["title"][:50]}'
                    yield Completion(sid, start_position=-len(partial),
                                     display=label, display_meta=PRIORITY_LABEL.get(t.get("priority"),""))
            return

        if cmd == "filter":
            for m in ("active","done","all","today","overdue"):
                if m.startswith(partial.lower()):
                    yield Completion(m, start_position=-len(partial))

# ═══════════ MAIN ═══════════
def main():
    data = load_todo()
    current_filter = "active"

    style = Style.from_dict({
        "prompt": "bold ansibrightmagenta",
        "completion-menu.completion": "bg:#000000 #00ff88",
        "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
        "completion-menu.meta.completion": "bg:#000000 #557755",
        "completion-menu.meta.completion.current": "bg:#aa00aa #000000",
    })

    while True:
        data = load_todo()
        tasks = data["tasks"]

        clear()
        console.print()
        console.print(title_block("T O D O", "Terminal Argonov  •  Task Manager"))
        console.print()
        console.print(stats_panel(tasks))
        console.print()

        # Напоминание о близких
        soon = [t for t in tasks if (is_overdue(t) or is_today(t) or is_soon(t)) and not t.get("done")]
        if soon:
            console.print(f"[bold {YELLOW}]⏰ Требуют внимания ({len(soon)}):[/]")
            for t in soon[:3]:
                mark = "❗" if is_overdue(t) else "⏰"
                console.print(f"  {mark} [bold]#{t['id']}[/] {t['title'][:55]}  [dim]{fmt_deadline(t.get('deadline'))}[/]")
            console.print()

        console.print(f"[dim]Фильтр: [bold]{current_filter}[/][/]")
        console.print()
        tasks_table(tasks, filter_mode=current_filter)
        commands_panel()

        session = PromptSession(
            completer=TodoCompleter(lambda: load_todo()["tasks"]),
            style=style, complete_while_typing=True)
        try:
            cmd = session.prompt(HTML("<prompt>╰─❯</prompt> ")).strip()
        except (EOFError, KeyboardInterrupt):
            console.print(Text("\n До связи. 🖖", style=f"dim {GREEN_DIM}"))
            break

        if not cmd: continue
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if c in ("q","exit","quit","выход"):
            console.print(Text(" До связи. 🖖", style=f"dim {GREEN_DIM}")); break
        if c == "clear": continue

        if c == "add":
            if not arg:
                console.print(Text("  ❌ add <текст> [!high] [@tomorrow] [#tag]", style=RED))
                time.sleep(1); continue
            p = parse_add(arg)
            if not p["title"]:
                console.print(Text("  ❌ Пустой заголовок", style=RED)); time.sleep(1); continue
            task = {
                "id": data["next_id"],
                "title": p["title"],
                "priority": p["priority"],
                "deadline": p["deadline"],
                "tags": p["tags"],
                "done": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            data["next_id"] += 1
            data["tasks"].append(task)
            save_todo(data)
            console.print(Text(f"  ✔ Добавлено #{task['id']}: {task['title']}", style=GREEN_BRIGHT))
            if task["deadline"]:
                console.print(Text(f"     📅 {fmt_deadline(task['deadline'])}", style=YELLOW))
            time.sleep(0.8); continue

        if c in ("done","undone","del","edit","notify"):
            if not arg.isdigit():
                console.print(Text(f"  ❌ {c} <id>", style=RED)); time.sleep(1); continue
            tid = int(arg)
            task = next((t for t in data["tasks"] if t["id"] == tid), None)
            if not task:
                console.print(Text(f"  ❌ Задача #{tid} не найдена", style=RED)); time.sleep(1); continue

            if c == "done":
                task["done"] = True
                save_todo(data)
                console.print(Text(f"  ✅ #{tid} выполнено", style=GREEN_BRIGHT))
            elif c == "undone":
                task["done"] = False
                save_todo(data)
                console.print(Text(f"  ↩ #{tid} возвращено в работу", style=YELLOW))
            elif c == "del":
                data["tasks"] = [t for t in data["tasks"] if t["id"] != tid]
                save_todo(data)
                console.print(Text(f"  🗑 #{tid} удалено", style=RED))
            elif c == "edit":
                console.print(Text(f"  ✏ Текущий: {task['title']}", style=WHITE))
                try:
                    new_title = console.input("[bold magenta]Новый заголовок (Enter — оставить)> [/]").strip()
                    if new_title: task["title"] = new_title
                    new_pri = console.input("[bold magenta]Приоритет (h/m/l, Enter — оставить)> [/]").strip().lower()
                    if new_pri in ("h","high","1"): task["priority"] = "high"
                    elif new_pri in ("m","mid","2"): task["priority"] = "medium"
                    elif new_pri in ("l","low","3"): task["priority"] = "low"
                    new_dl = console.input("[bold magenta]Дедлайн (@tomorrow, @+3d, Enter — оставить)> [/]").strip()
                    if new_dl.startswith("@"):
                        pd = parse_date(new_dl[1:])
                        if pd: task["deadline"] = pd
                    save_todo(data)
                    console.print(Text(f"  ✔ #{tid} обновлено", style=GREEN_BRIGHT))
                except (EOFError, KeyboardInterrupt):
                    console.print(Text("  Отменено", style=YELLOW))
            elif c == "notify":
                if notify(task):
                    console.print(Text(f"  🔔 Уведомление отправлено: {task['title']}", style=GREEN_BRIGHT))
                else:
                    console.print(Text("  ⚠ termux-notification не сработал (установлен ли Termux:API?)", style=YELLOW))
            time.sleep(0.8); continue

        if c == "notify-all":
            active = [t for t in data["tasks"] if not t.get("done")]
            if not active:
                console.print(Text("  ⚠ Нет активных задач", style=YELLOW)); time.sleep(1); continue
            cnt = 0
            for t in active[:10]:
                if notify(t): cnt += 1
                time.sleep(0.3)
            console.print(Text(f"  🔔 Отправлено уведомлений: {cnt}", style=GREEN_BRIGHT))
            time.sleep(1); continue

        if c == "filter":
            if arg in ("active","done","all","today","overdue"):
                current_filter = arg
                console.print(Text(f"  🔎 Фильтр: {arg}", style=GREEN_BRIGHT))
                time.sleep(0.5)
            else:
                console.print(Text("  ❌ filter: active/done/all/today/overdue", style=RED))
                time.sleep(1)
            continue

        if c == "clear-done":
            before = len(data["tasks"])
            data["tasks"] = [t for t in data["tasks"] if not t.get("done")]
            save_todo(data)
            removed = before - len(data["tasks"])
            console.print(Text(f"  🧹 Удалено выполненных: {removed}", style=GREEN_BRIGHT))
            time.sleep(0.8); continue

        if c in ("help","h","?"):
            console.print(Text("  Tab — автодополнение. Пример: add Купить хлеб !high @tomorrow #покупки", style=CYAN))
            time.sleep(1.5); continue

        console.print(Text(f"  ❌ Неизвестно: {c}", style=RED))
        time.sleep(0.6)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print(Text("\n Прервано.", style=f"dim {GREEN_DIM}"))
```

---

## 📄 notes.py

*18700 байт · 427 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NOTES — заметки с тегами, поиском, экспортом + Tab-автодополнение"""

import os, sys, json, re, subprocess, time
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

console = Console()
NOTES_FILE  = os.path.expanduser("~/.notes.json")
EXPORT_DIR  = os.path.expanduser("~/notes_export")

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

# ═══════════ ХРАНИЛИЩЕ ═══════════
def load_notes():
    if not os.path.exists(NOTES_FILE):
        return {"next_id": 1, "notes": []}
    try:
        with open(NOTES_FILE, encoding="utf-8") as f:
            d = json.load(f)
            d.setdefault("next_id", 1)
            d.setdefault("notes", [])
            return d
    except Exception:
        return {"next_id": 1, "notes": []}

def save_notes(data):
    try:
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

# ═══════════ ПАРСИНГ ═══════════
def parse_new(text):
    """new Заголовок | Тело заметки #тег1 #тег2"""
    # Теги ищем в конце
    tags = re.findall(r"#(\S+)", text)
    text_no_tags = re.sub(r"#\S+", "", text).strip()
    if "|" in text_no_tags:
        title, body = text_no_tags.split("|", 1)
    else:
        title = text_no_tags
        body = ""
    return {"title": title.strip(), "body": body.strip(), "tags": tags}

def edit_note_interactive(note):
    """Интерактивное редактирование через мультистрочный ввод"""
    console.print(Text(f"  ✏ Текущий заголовок: {note['title']}", style=WHITE))
    try:
        new_title = console.input("[bold magenta]Новый заголовок (Enter — оставить)> [/]").strip()
        if new_title: note["title"] = new_title
    except (EOFError, KeyboardInterrupt):
        console.print(Text("  Отменено", style=YELLOW)); return False

    console.print(Text("  Текущее тело:", style=WHITE))
    console.print(Panel(note.get("body","") or "[dim](пусто)[/]", border_style=GRAY))
    console.print(Text("  Введи новый текст (Enter на пустой строке — конец):", style=CYAN))
    lines = []
    try:
        while True:
            line = console.input("[bold magenta]...[/] ")
            if not line: break
            lines.append(line)
    except (EOFError, KeyboardInterrupt):
        pass
    if lines:
        note["body"] = "\n".join(lines)

    try:
        new_tags = console.input(f"[bold magenta]Теги через пробел (текущие: {', '.join(note.get('tags',[])) or '—'})> [/]").strip()
        if new_tags:
            note["tags"] = [t.lstrip("#") for t in new_tags.split()]
    except (EOFError, KeyboardInterrupt):
        pass
    note["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return True

# ═══════════ ЭКСПОРТ ═══════════
def export_notes(fmt="md"):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    data = load_notes()
    notes = data["notes"]
    if not notes:
        console.print(Text("  ⚠ Нечего экспортировать", style=YELLOW)); return

    if fmt == "json":
        path = os.path.join(EXPORT_DIR, f"notes_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
    elif fmt == "md":
        path = os.path.join(EXPORT_DIR, f"notes_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Мои заметки\n\n_Экспорт: {datetime.now().strftime('%d.%m.%Y %H:%M')}_\n\n")
            for n in notes:
                f.write(f"## #{n['id']} — {n['title']}\n\n")
                if n.get("tags"):
                    f.write("**Теги:** " + " ".join(f"`#{t}`" for t in n["tags"]) + "\n\n")
                if n.get("body"):
                    f.write(n["body"] + "\n\n")
                f.write(f"_Создано: {n.get('created','—')}_\n\n---\n\n")
    elif fmt == "txt":
        path = os.path.join(EXPORT_DIR, f"notes_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
        with open(path, "w", encoding="utf-8") as f:
            for n in notes:
                f.write(f"=== #{n['id']} — {n['title']} ===\n")
                if n.get("tags"): f.write("Теги: " + ", ".join(n["tags"]) + "\n")
                if n.get("body"): f.write(n["body"] + "\n")
                f.write("\n")
    else:
        console.print(Text(f"  ❌ Неизвестный формат: {fmt}", style=RED)); return

    console.print(Text(f"  ✔ Экспортировано: {path}", style=GREEN_BRIGHT))

# ═══════════ РИСОВКА ═══════════
def clear(): os.system("clear")

def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("═" * 60, style=GREEN_DIM))
    return Group(*lines)

def stats_panel(notes):
    total = len(notes)
    tags_count = {}
    for n in notes:
        for t in n.get("tags", []):
            tags_count[t] = tags_count.get(t, 0) + 1
    top_tags = sorted(tags_count.items(), key=lambda x: -x[1])[:5]
    top_s = " ".join(f"#{t}({c})" for t, c in top_tags) or "[dim]нет[/]"

    t = Table(box=None, show_header=False, padding=(0, 3))
    t.add_column(""); t.add_column("")
    t.add_row(f"📝 Заметок: [bold]{total}[/]",
              f"🏷 Тегов: [bold]{len(tags_count)}[/]")
    t.add_row(f"🔝 Топ теги: {top_s}", "")
    return t

def notes_table(notes, filter_mode=None):
    """filter_mode: None (все), 'tag:xxx', search-строка"""
    shown = notes
    if filter_mode and filter_mode.startswith("tag:"):
        tag = filter_mode[4:].lower()
        shown = [n for n in notes if tag in [x.lower() for x in n.get("tags", [])]]
    elif filter_mode:
        q = filter_mode.lower()
        shown = [n for n in notes
                 if q in n["title"].lower() or q in n.get("body","").lower()
                 or any(q in t.lower() for t in n.get("tags", []))]

    shown = sorted(shown, key=lambda x: x.get("updated") or x.get("created",""), reverse=True)

    if not shown:
        console.print(Text(f"  📭 Заметок нет (фильтр: {filter_mode or 'нет'})", style=f"dim {GRAY}"))
        console.print()
        return

    t = Table(box=box.SIMPLE_HEAD, border_style=CYAN,
              header_style=f"bold {CYAN}", padding=(0, 1), expand=True)
    t.add_column("ID", style=f"bold {YELLOW}", width=4, justify="right")
    t.add_column("Заголовок", style=WHITE)
    t.add_column("Теги", style=MAGENTA, width=20)
    t.add_column("Обновлено", style=GRAY, width=17)

    for n in shown:
        title = n["title"][:55]
        tags_s = " ".join(f"#{x}" for x in n.get("tags", []))[:20] or "[dim]—[/]"
        upd = n.get("updated") or n.get("created", "—")
        t.add_row(str(n["id"]), title, tags_s, upd[:16])
    console.print(t)
    console.print()

def commands_panel():
    t = Table(box=box.DOUBLE_EDGE, border_style="black",
              show_header=False, padding=(0, 2))
    t.add_column("Команда", style="bold yellow", width=26, justify="right")
    t.add_column("Действие", style="white")
    t.add_row("[cyan]new <заголовок> | <тело> #tag[/]", "➕ Новая заметка")
    t.add_row("[cyan]show <id>[/]",     "👁 Показать заметку")
    t.add_row("[cyan]edit <id>[/]",     "✏ Редактировать")
    t.add_row("[cyan]del <id>[/]",      "🗑 Удалить")
    t.add_row("[cyan]tag <тег>[/]",     "🏷 Фильтр по тегу")
    t.add_row("[cyan]search <текст>[/]", "🔍 Поиск по всем полям")
    t.add_row("[cyan]tags[/]",          "📋 Список всех тегов")
    t.add_row("[cyan]reset[/]",         "↩ Сбросить фильтр")
    t.add_row("[cyan]export md|txt|json[/]", "💾 Экспорт в ~/notes_export/")
    t.add_row("[cyan]q[/]",             "🚪 Выход")
    console.print(Panel(t, title="[bold green]⌨  КОМАНДЫ  (Tab — автодополнение)[/]",
                        border_style="black"))
    console.print()

# ═══════════ TAB-COMPLETER ═══════════
class NotesCompleter(Completer):
    def __init__(self, get_data):
        self.get_data = get_data

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        if not words or (len(words) == 1 and not text.endswith(" ")):
            partial = words[0] if words else ""
            commands = ["new","show","edit","del","tag","search","tags",
                        "reset","export","clear","help","q"]
            for c in commands:
                if c.startswith(partial.lower()):
                    yield Completion(c, start_position=-len(partial))
            return

        cmd = words[0].lower()
        partial = words[-1] if not text.endswith(" ") else ""

        if cmd in ("show","edit","del"):
            data = self.get_data()
            for n in data["notes"]:
                sid = str(n["id"])
                if sid.startswith(partial):
                    label = f'{sid}  {n["title"][:55]}'
                    yield Completion(sid, start_position=-len(partial),
                                     display=label)
            return

        if cmd == "tag":
            data = self.get_data()
            tags = set()
            for n in data["notes"]:
                tags.update(n.get("tags", []))
            for t in sorted(tags):
                if t.lower().startswith(partial.lower()):
                    yield Completion(t, start_position=-len(partial))
            return

        if cmd == "export":
            for m in ("md","txt","json"):
                if m.startswith(partial.lower()):
                    yield Completion(m, start_position=-len(partial))

# ═══════════ MAIN ═══════════
def main():
    data = load_notes()
    current_filter = None

    style = Style.from_dict({
        "prompt": "bold ansibrightmagenta",
        "completion-menu.completion": "bg:#000000 #00ff88",
        "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
        "completion-menu.meta.completion": "bg:#000000 #557755",
        "completion-menu.meta.completion.current": "bg:#aa00aa #000000",
    })

    while True:
        data = load_notes()
        notes = data["notes"]

        clear()
        console.print()
        console.print(title_block("N O T E S", "Terminal Argonov  •  Notes"))
        console.print()
        console.print(stats_panel(notes))
        console.print()

        if current_filter:
            console.print(f"[dim]Фильтр: [bold]{current_filter}[/][/]")
            console.print()

        notes_table(notes, filter_mode=current_filter)
        commands_panel()

        session = PromptSession(
            completer=NotesCompleter(lambda: load_notes()),
            style=style, complete_while_typing=True)
        try:
            cmd = session.prompt(HTML("<prompt>╰─❯</prompt> ")).strip()
        except (EOFError, KeyboardInterrupt):
            console.print(Text("\n До связи. 🖖", style=f"dim {GREEN_DIM}"))
            break

        if not cmd: continue
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if c in ("q","exit","quit","выход"):
            console.print(Text(" До связи. 🖖", style=f"dim {GREEN_DIM}")); break
        if c == "clear": continue

        if c == "new":
            if not arg:
                console.print(Text("  ❌ new <заголовок> | <тело> #тег", style=RED))
                time.sleep(1); continue
            p = parse_new(arg)
            if not p["title"]:
                console.print(Text("  ❌ Пустой заголовок", style=RED)); time.sleep(1); continue
            note = {
                "id": data["next_id"],
                "title": p["title"],
                "body": p["body"],
                "tags": p["tags"],
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            data["next_id"] += 1
            data["notes"].append(note)
            save_notes(data)
            console.print(Text(f"  ✔ Заметка #{note['id']} создана", style=GREEN_BRIGHT))
            time.sleep(0.8); continue

        if c == "show":
            if not arg.isdigit():
                console.print(Text("  ❌ show <id>", style=RED)); time.sleep(1); continue
            tid = int(arg)
            note = next((n for n in data["notes"] if n["id"] == tid), None)
            if not note:
                console.print(Text(f"  ❌ #{tid} не найдена", style=RED)); time.sleep(1); continue
            clear()
            console.print()
            console.print(title_block(f"#{note['id']}  {note['title']}"))
            console.print()
            if note.get("tags"):
                console.print(Text("🏷 " + " ".join(f"#{t}" for t in note["tags"]), style=MAGENTA))
                console.print()
            body = note.get("body") or "[dim](пусто)[/]"
            try:
                console.print(Markdown(body))
            except Exception:
                console.print(body)
            console.print()
            console.print(Text(f"📅 Создано: {note.get('created','—')}", style=GRAY))
            console.print(Text(f"🕐 Обновлено: {note.get('updated','—')}", style=GRAY))
            console.print()
            try: console.input("[dim]Enter — назад[/] ")
            except (EOFError, KeyboardInterrupt): pass
            continue

        if c in ("edit","del"):
            if not arg.isdigit():
                console.print(Text(f"  ❌ {c} <id>", style=RED)); time.sleep(1); continue
            tid = int(arg)
            note = next((n for n in data["notes"] if n["id"] == tid), None)
            if not note:
                console.print(Text(f"  ❌ #{tid} не найдена", style=RED)); time.sleep(1); continue
            if c == "edit":
                if edit_note_interactive(note):
                    save_notes(data)
                    console.print(Text(f"  ✔ Заметка #{tid} обновлена", style=GREEN_BRIGHT))
                time.sleep(1); continue
            if c == "del":
                try:
                    ans = console.input(f"[bold red]Удалить #{tid} «{note['title'][:40]}»? (y/N)> [/]").strip().lower()
                    if ans == "y":
                        data["notes"] = [n for n in data["notes"] if n["id"] != tid]
                        save_notes(data)
                        console.print(Text(f"  🗑 #{tid} удалена", style=RED))
                    else:
                        console.print(Text("  Отменено", style=YELLOW))
                except (EOFError, KeyboardInterrupt):
                    console.print(Text("  Отменено", style=YELLOW))
                time.sleep(0.8); continue

        if c == "tag":
            if not arg:
                console.print(Text("  ❌ tag <тег>", style=RED)); time.sleep(1); continue
            current_filter = f"tag:{arg.lstrip('#')}"
            console.print(Text(f"  🏷 Фильтр по тегу: {arg}", style=GREEN_BRIGHT))
            time.sleep(0.5); continue

        if c == "search":
            if not arg:
                console.print(Text("  ❌ search <текст>", style=RED)); time.sleep(1); continue
            current_filter = arg
            console.print(Text(f"  🔍 Поиск: {arg}", style=GREEN_BRIGHT))
            time.sleep(0.5); continue

        if c == "tags":
            tags_count = {}
            for n in data["notes"]:
                for t in n.get("tags", []):
                    tags_count[t] = tags_count.get(t, 0) + 1
            if not tags_count:
                console.print(Text("  ⚠ Тегов нет", style=YELLOW)); time.sleep(1); continue
            clear()
            console.print(); console.print(title_block("🏷 ВСЕ ТЕГИ")); console.print()
            t = Table(box=box.SIMPLE_HEAD, border_style=MAGENTA,
                      header_style=f"bold {MAGENTA}", padding=(0, 2))
            t.add_column("Тег", style=MAGENTA)
            t.add_column("Заметок", style=CYAN, justify="right", width=10)
            for tg, cnt in sorted(tags_count.items(), key=lambda x: -x[1]):
                t.add_row(f"#{tg}", str(cnt))
            console.print(t); console.print()
            try: console.input("[dim]Enter — назад[/] ")
            except (EOFError, KeyboardInterrupt): pass
            continue

        if c == "reset":
            current_filter = None
            console.print(Text("  ↩ Фильтр сброшен", style=GREEN_BRIGHT))
            time.sleep(0.5); continue

        if c == "export":
            fmt = (arg or "md").lower()
            export_notes(fmt)
            time.sleep(1.2); continue

        if c in ("help","h","?"):
            console.print(Text("  Tab — автодополнение. Пример: new Рецепт блинов | 2 яйца, мука, молоко #кухня", style=CYAN))
            time.sleep(2); continue

        console.print(Text(f"  ❌ Неизвестно: {c}", style=RED))
        time.sleep(0.6)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print(Text("\n Прервано.", style=f"dim {GREEN_DIM}"))
```

---

## 📄 passmanager.py

*23101 байт · 507 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PassManager — зашифрованное хранилище паролей (AES-256 + PBKDF2)"""

import os, sys, json, time, base64, getpass, secrets, string, hashlib
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

# ─── Криптография ───
try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.exceptions import InvalidTag
except ImportError:
    print("❌ Установи: pip install cryptography")
    sys.exit(1)

console = Console()
VAULT_FILE = os.path.expanduser("~/.pm.vault")
BACKUP_DIR = os.path.expanduser("~/pm_backups")

# ANSI/rich цвета
GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

# ═══════════ КРИПТО ═══════════
PBKDF2_ITERS = 480_000
SALT_SIZE    = 16
NONCE_SIZE   = 12

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERS,
    )
    return kdf.derive(password.encode())

def encrypt_vault(data: dict, password: str) -> bytes:
    """Возвращает salt + nonce + ciphertext"""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    plaintext = json.dumps(data, ensure_ascii=False).encode()
    ct = AESGCM(key).encrypt(nonce, plaintext, None)
    return salt + nonce + ct

def decrypt_vault(blob: bytes, password: str) -> dict:
    """Расшифровывает. Бросает InvalidTag при неверном пароле."""
    if len(blob) < SALT_SIZE + NONCE_SIZE + 16:
        raise ValueError("Повреждённый файл хранилища")
    salt = blob[:SALT_SIZE]
    nonce = blob[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ct = blob[SALT_SIZE + NONCE_SIZE:]
    key = derive_key(password, salt)
    pt = AESGCM(key).decrypt(nonce, ct, None)
    return json.loads(pt.decode())

# ═══════════ ГЕНЕРАЦИЯ ═══════════
def gen_password(length=20, symbols=True, digits=True, upper=True, lower=True) -> str:
    pool = ""
    if lower:  pool += string.ascii_lowercase
    if upper:  pool += string.ascii_uppercase
    if digits: pool += string.digits
    if symbols: pool += "!@#$%^&*()-_=+[]{};:,.<>?"
    if not pool: pool = string.ascii_letters
    return "".join(secrets.choice(pool) for _ in range(length))

# ═══════════ РИСОВКА ═══════════
def clear(): os.system("clear")

def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("═" * 60, style=GREEN_DIM))
    return Group(*lines)

def stats_panel(entries):
    total = len(entries)
    categories = {}
    for e in entries.values():
        c = e.get("category", "без категории")
        categories[c] = categories.get(c, 0) + 1
    cats = " ".join(f"{c}({n})" for c, n in sorted(categories.items(), key=lambda x: -x[1])[:5]) or "[dim]—[/]"
    t = Table(box=None, show_header=False, padding=(0, 3))
    t.add_column(""); t.add_column("")
    t.add_row(f"🔑 Записей: [bold]{total}[/]", f"📁 Категории: {cats}")
    return t

def entries_table(entries, filter_cat=None, filter_search=None):
    shown = []
    for name, e in entries.items():
        if filter_cat and e.get("category","").lower() != filter_cat.lower():
            continue
        if filter_search:
            q = filter_search.lower()
            if q not in name.lower() and q not in e.get("url","").lower() and q not in e.get("notes","").lower():
                continue
        shown.append((name, e))
    shown.sort(key=lambda x: x[0].lower())

    if not shown:
        console.print(Text(f"  📭 Записей нет", style=f"dim {GRAY}"))
        console.print()
        return

    t = Table(box=box.SIMPLE_HEAD, border_style=CYAN,
              header_style=f"bold {CYAN}", padding=(0, 1), expand=True)
    t.add_column("№", style=f"bold {YELLOW}", width=4, justify="right")
    t.add_column("Название", style=WHITE)
    t.add_column("Категория", style=MAGENTA, width=16)
    t.add_column("Логин", style=GRAY, width=24)
    t.add_column("URL", style=CYAN, width=30)

    for i, (name, e) in enumerate(shown, 1):
        t.add_row(str(i), name[:40],
                  (e.get("category","—") or "—")[:14],
                  (e.get("login","—") or "—")[:22],
                  (e.get("url","—") or "—")[:28])
    console.print(t)
    console.print()
    return shown

def commands_panel():
    t = Table(box=box.DOUBLE_EDGE, border_style="black",
              show_header=False, padding=(0, 2))
    t.add_column("Команда", style="bold yellow", width=30, justify="right")
    t.add_column("Действие", style="white")
    t.add_row("[cyan]add[/]",                 "➕ Добавить запись")
    t.add_row("[cyan]get <№>[/]",             "👁 Показать пароль")
    t.add_row("[cyan]copy <№>[/]",            "📋 Скопировать пароль в буфер")
    t.add_row("[cyan]gen [длина][/]",         "🎲 Сгенерировать пароль")
    t.add_row("[cyan]edit <№>[/]",            "✏ Редактировать")
    t.add_row("[cyan]del <№>[/]",             "🗑 Удалить")
    t.add_row("[cyan]cat <категория>[/]",     "📁 Фильтр по категории")
    t.add_row("[cyan]search <текст>[/]",      "🔍 Поиск")
    t.add_row("[cyan]reset[/]",               "↩ Сбросить фильтр")
    t.add_row("[cyan]backup[/]",              "💾 Резервная копия")
    t.add_row("[cyan]passwd[/]",              "🔑 Сменить мастер-пароль")
    t.add_row("[cyan]lock[/]",                "🔒 Заблокировать (выйти)")
    console.print(Panel(t, title="[bold green]⌨  КОМАНДЫ  (Tab — автодополнение)[/]",
                        border_style="black"))
    console.print()

# ═══════════ TAB-COMPLETER ═══════════
class PMCompleter(Completer):
    def __init__(self, get_entries, get_shown):
        self.get_entries = get_entries
        self.get_shown = get_shown

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        if not words or (len(words) == 1 and not text.endswith(" ")):
            partial = words[0] if words else ""
            commands = ["add","get","copy","gen","edit","del","cat","search",
                        "reset","backup","passwd","lock","q"]
            for c in commands:
                if c.startswith(partial.lower()):
                    yield Completion(c, start_position=-len(partial))
            return

        cmd = words[0].lower()
        partial = words[-1] if not text.endswith(" ") else ""

        if cmd in ("get","copy","edit","del"):
            shown = self.get_shown() or []
            for i, (name, _) in enumerate(shown, 1):
                si = str(i)
                if si.startswith(partial):
                    yield Completion(si, start_position=-len(partial),
                                     display=f"{si}  {name[:50]}")
            return

        if cmd == "cat":
            entries = self.get_entries()
            cats = set()
            for e in entries.values():
                if e.get("category"): cats.add(e["category"])
            for c in sorted(cats):
                if c.lower().startswith(partial.lower()):
                    yield Completion(c, start_position=-len(partial))
            return

# ═══════════ МАСТЕР-ПАРОЛЬ ═══════════
def unlock_vault():
    """Возвращает (vault_data, master_password) или (None, None)"""
    if not os.path.exists(VAULT_FILE):
        # Первый запуск — создаём
        clear()
        console.print()
        console.print(Align.center(Panel.fit(
            "[bold green]🔐  P A S S M A N A G E R  🔐[/]\n"
            "[dim]Первый запуск — создание мастер-пароля[/]",
            border_style="black")))
        console.print()
        console.print("[yellow]⚠  Мастер-пароль НЕЛЬЗЯ восстановить![/]")
        console.print("[yellow]   Запомни его или запиши в надёжном месте.[/]")
        console.print()
        try:
            p1 = getpass.getpass("🔑 Новый мастер-пароль: ")
            if len(p1) < 6:
                console.print("[red]❌ Минимум 6 символов[/]"); return None, None
            p2 = getpass.getpass("🔑 Повтори: ")
            if p1 != p2:
                console.print("[red]❌ Пароли не совпадают[/]"); return None, None
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Отменено[/]"); return None, None

        vault = {"entries": {}, "created": datetime.now().strftime("%Y-%m-%d %H:%M")}
        blob = encrypt_vault(vault, p1)
        with open(VAULT_FILE, "wb") as f: f.write(blob)
        try: os.chmod(VAULT_FILE, 0o600)
        except Exception: pass
        console.print("[green]✔ Хранилище создано[/]")
        time.sleep(1)
        return vault, p1

    # Разблокировка
    clear()
    console.print()
    console.print(Align.center(Panel.fit(
        "[bold green]🔐  P A S S M A N A G E R  🔐[/]\n"
        "[dim]Введи мастер-пароль[/]",
        border_style="black")))
    console.print()
    for attempt in range(3):
        try:
            pwd = getpass.getpass("🔑 Мастер-пароль: ")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Отменено[/]"); return None, None
        try:
            with open(VAULT_FILE, "rb") as f: blob = f.read()
            vault = decrypt_vault(blob, pwd)
            console.print("[green]✔ Разблокировано[/]")
            time.sleep(0.5)
            return vault, pwd
        except (InvalidTag, ValueError):
            console.print(f"[red]❌ Неверный пароль ({attempt+1}/3)[/]")
        except Exception as e:
            console.print(f"[red]❌ {e}[/]"); return None, None
    return None, None

def save_vault(vault, password):
    blob = encrypt_vault(vault, password)
    tmp = VAULT_FILE + ".tmp"
    with open(tmp, "wb") as f: f.write(blob)
    try: os.chmod(tmp, 0o600)
    except Exception: pass
    os.replace(tmp, VAULT_FILE)

# ═══════════ MAIN ═══════════
def main():
    vault, master_pwd = unlock_vault()
    if vault is None:
        return
    entries = vault.setdefault("entries", {})
    current_filter_cat = None
    current_search = None
    last_shown = []

    style = Style.from_dict({
        "prompt": "bold ansibrightmagenta",
        "completion-menu.completion": "bg:#000000 #00ff88",
        "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
    })

    while True:
        clear()
        console.print()
        console.print(title_block("P A S S M A N A G E R", "Terminal Argonov  •  AES-256"))
        console.print()
        console.print(stats_panel(entries))
        console.print()

        filters = []
        if current_filter_cat: filters.append(f"категория: [magenta]{current_filter_cat}[/]")
        if current_search:     filters.append(f"поиск: [yellow]{current_search}[/]")
        if filters:
            console.print("[bold]🔎 Фильтр:[/] " + "  •  ".join(filters))
            console.print()

        last_shown = entries_table(entries, current_filter_cat, current_search) or []
        commands_panel()

        session = PromptSession(
            completer=PMCompleter(lambda: entries, lambda: last_shown),
            style=style, complete_while_typing=True)
        try:
            cmd = session.prompt(HTML("<prompt>╰─❯</prompt> ")).strip()
        except (EOFError, KeyboardInterrupt):
            console.print(Text("\n 🔒 Хранилище заблокировано. 🖖", style=f"dim {GREEN_DIM}"))
            break

        if not cmd: continue
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if c in ("lock","q","exit","quit","выход"):
            console.print(Text(" 🔒 Заблокировано. 🖖", style=f"dim {GREEN_DIM}"))
            break
        if c == "clear": continue

        if c == "add":
            console.print()
            try:
                name = console.input("[bold cyan]📝 Название (Google, VK, банк)> [/]").strip()
                if not name: raise KeyboardInterrupt
                if name in entries:
                    console.print(f"[yellow]⚠ Уже есть «{name}». Будет перезаписано.[/]")
                url   = console.input("[bold cyan]🌐 URL (Enter — нет)> [/]").strip()
                login = console.input("[bold cyan]👤 Логин (Enter — нет)> [/]").strip()
                cat   = console.input("[bold cyan]📁 Категория (Enter — «личное»)> [/]").strip() or "личное"
                notes = console.input("[bold cyan]📄 Заметки (Enter — нет)> [/]").strip()

                console.print("[bold cyan]🔐 Пароль: (Enter — сгенерировать)[/]")
                pwd = getpass.getpass("   Пароль: ").strip()
                if not pwd:
                    pwd = gen_password(20)
                    console.print(f"[green]🎲 Сгенерирован:[/] [bold]{pwd}[/]")

                entries[name] = {
                    "login": login,
                    "password": pwd,
                    "url": url,
                    "category": cat,
                    "notes": notes,
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                save_vault(vault, master_pwd)
                console.print(f"[green]✔ Добавлено: {name}[/]")
            except (KeyboardInterrupt, EOFError):
                console.print("[yellow]Отменено[/]")
            time.sleep(1)
            continue

        if c in ("get","copy","edit","del"):
            if not arg.isdigit():
                console.print(f"[red]❌ {c} <№>[/]"); time.sleep(1); continue
            idx = int(arg)
            if not (1 <= idx <= len(last_shown)):
                console.print(f"[red]❌ № от 1 до {len(last_shown)}[/]"); time.sleep(1); continue
            name, e = last_shown[idx - 1]

            if c == "get":
                clear()
                console.print()
                console.print(title_block(f"🔑 {name}"))
                console.print()
                t = Table(box=box.ROUNDED, show_header=False, border_style=CYAN, padding=(0, 2))
                t.add_column("", style=f"bold {YELLOW}", width=16)
                t.add_column("", style=WHITE)
                t.add_row("📝 Название", name)
                t.add_row("🌐 URL", e.get("url") or "—")
                t.add_row("👤 Логин", e.get("login") or "—")
                t.add_row("🔐 Пароль", f"[bold {GREEN_BRIGHT}]{e.get('password','—')}[/]")
                t.add_row("📁 Категория", e.get("category") or "—")
                t.add_row("📄 Заметки", e.get("notes") or "—")
                t.add_row("📅 Создано", e.get("created","—"))
                t.add_row("🕐 Обновлено", e.get("updated","—"))
                console.print(t); console.print()
                try: console.input("[dim]Enter — назад[/] ")
                except (KeyboardInterrupt, EOFError): pass
                continue

            if c == "copy":
                try:
                    import pyperclip
                    pyperclip.copy(e.get("password",""))
                    console.print(f"[green]✔ Пароль скопирован в буфер[/]")
                except Exception:
                    console.print(f"[yellow]⚠ pyperclip не сработал. Пароль: {e.get('password')}[/]")
                time.sleep(1); continue

            if c == "del":
                try:
                    ans = console.input(f"[bold red]Удалить «{name}»? (y/N)> [/]").strip().lower()
                    if ans == "y":
                        del entries[name]
                        save_vault(vault, master_pwd)
                        console.print(f"[red]🗑 Удалено: {name}[/]")
                    else:
                        console.print("[yellow]Отменено[/]")
                except (KeyboardInterrupt, EOFError):
                    console.print("[yellow]Отменено[/]")
                time.sleep(0.8); continue

            if c == "edit":
                console.print()
                console.print(f"[bold]Редактирование «{name}»[/] [dim](Enter — оставить)[/]")
                try:
                    url = console.input(f"[cyan]URL ({e.get('url','')})> [/]").strip()
                    if url: e["url"] = url
                    login = console.input(f"[cyan]Логин ({e.get('login','')})> [/]").strip()
                    if login: e["login"] = login
                    cat = console.input(f"[cyan]Категория ({e.get('category','')})> [/]").strip()
                    if cat: e["category"] = cat
                    notes = console.input(f"[cyan]Заметки ({e.get('notes','')})> [/]").strip()
                    if notes: e["notes"] = notes
                    console.print("[cyan]Новый пароль (Enter — оставить, !gen — сгенерировать)[/]")
                    pwd = getpass.getpass("   > ").strip()
                    if pwd == "!gen":
                        pwd = gen_password(20)
                        console.print(f"[green]🎲 Новый:[/] [bold]{pwd}[/]")
                        e["password"] = pwd
                    elif pwd:
                        e["password"] = pwd
                    e["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    save_vault(vault, master_pwd)
                    console.print(f"[green]✔ Обновлено[/]")
                except (KeyboardInterrupt, EOFError):
                    console.print("[yellow]Отменено[/]")
                time.sleep(1); continue

        if c == "gen":
            try: length = int(arg) if arg else 20
            except ValueError: length = 20
            if not 4 <= length <= 128: length = 20
            pwd = gen_password(length)
            console.print()
            console.print(Panel(f"[bold {GREEN_BRIGHT}]{pwd}[/]",
                                title=f"🎲 {length} символов", border_style=GREEN_DIM))
            try:
                import pyperclip; pyperclip.copy(pwd)
                console.print("[dim]✔ Скопировано в буфер[/]")
            except Exception: pass
            console.print()
            try: console.input("[dim]Enter — назад[/] ")
            except (KeyboardInterrupt, EOFError): pass
            continue

        if c == "cat":
            if not arg:
                current_filter_cat = None
                console.print("[yellow]↩ Фильтр категории сброшен[/]")
            else:
                current_filter_cat = arg
                console.print(f"[green]📁 Фильтр: {arg}[/]")
            time.sleep(0.5); continue

        if c == "search":
            current_search = arg or None
            console.print(f"[green]🔍 Поиск: {arg or 'сброшен'}[/]")
            time.sleep(0.5); continue

        if c == "reset":
            current_filter_cat = None
            current_search = None
            console.print("[green]↩ Фильтры сброшены[/]")
            time.sleep(0.5); continue

        if c == "backup":
            os.makedirs(BACKUP_DIR, exist_ok=True)
            path = os.path.join(BACKUP_DIR,
                f"pm_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.vault")
            try:
                with open(VAULT_FILE, "rb") as f: data = f.read()
                with open(path, "wb") as f: f.write(data)
                console.print(f"[green]💾 Резервная копия: {path}[/]")
            except Exception as e:
                console.print(f"[red]❌ {e}[/]")
            time.sleep(1.2); continue

        if c == "passwd":
            console.print()
            console.print("[yellow]⚠ Смена мастер-пароля. Все данные останутся.[/]")
            try:
                old = getpass.getpass("🔑 Текущий мастер-пароль: ")
                try:
                    with open(VAULT_FILE,"rb") as f: decrypt_vault(f.read(), old)
                except Exception:
                    console.print("[red]❌ Неверный пароль[/]"); time.sleep(1); continue
                new1 = getpass.getpass("🔑 Новый мастер-пароль: ")
                if len(new1) < 6:
                    console.print("[red]❌ Минимум 6 символов[/]"); time.sleep(1); continue
                new2 = getpass.getpass("🔑 Повтори: ")
                if new1 != new2:
                    console.print("[red]❌ Не совпадают[/]"); time.sleep(1); continue
                save_vault(vault, new1)
                master_pwd = new1
                console.print("[green]✔ Мастер-пароль изменён[/]")
            except (KeyboardInterrupt, EOFError):
                console.print("[yellow]Отменено[/]")
            time.sleep(1); continue

        console.print(Text(f"  ❌ Неизвестно: {c}", style=RED))
        time.sleep(0.6)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print(Text("\n 🔒 Заблокировано.", style=f"dim {GREEN_DIM}"))
```

---

## 📄 crypto_informer.py

*7474 байт · 208 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crypto Informer v6 — простой вывод + опциональный watch"""

import os, sys, time, subprocess
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import SIMPLE_HEAD

sys.path.insert(0, os.path.expanduser("~"))
from net_helper import get_crypto_prices, get_fx_rates, freshness_badge

console = Console()

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

COIN_ICONS = {
    "bitcoin": "₿", "ethereum": "Ξ", "solana": "◎", "binancecoin": "🅑",
    "cardano": "₳", "ripple": "✕", "dogecoin": "Ð", "polkadot": "●",
    "tron": "◈", "litecoin": "Ł", "chainlink": "⬡", "matic-network": "⬢",
    "avalanche-2": "▲", "uniswap": "🦄", "shiba-inu": "🐕",
    "toncoin": "💎", "near": "Ⓝ", "cosmos": "⚛", "stellar": "✦",
}

DEFAULT_INTERVAL = 60

def clear():
    subprocess.run("clear", shell=True)

def fmt_price(p):
    if p is None: return "—"
    if p < 0.01: return f"${p:.8f}"
    if p < 1:    return f"${p:.4f}"
    if p < 1000: return f"${p:,.2f}"
    return f"${p:,.0f}"

def fmt_change(pct):
    if pct is None: return "—"
    color = GREEN_BRIGHT if pct >= 0 else RED
    arrow = "▲" if pct >= 0 else "▼"
    return f"[{color}]{arrow}{abs(pct):.2f}%[/]"

def print_header(watch=False):
    line = Text()
    line.append("▓▒░ ", style=f"bold {GREEN_BRIGHT}")
    line.append("CRYPTO INFORMER", style=f"bold {GREEN_BRIGHT}")
    line.append(" ░▒▓", style=f"bold {GREEN_BRIGHT}")
    if watch:
        line.append("  ", style="")
        line.append("[LIVE]", style=f"bold {MAGENTA}")
    console.print(line)
    console.print(Text("─" * 50, style=GREEN_DIM))
    console.print()

def print_freshness(crypto_meta, fx_meta):
    line = Text()
    line.append("  ", style="")
    line.append_text(Text.from_markup(freshness_badge(crypto_meta)))
    line.append(" крипта   ·   ", style=f"dim {GRAY}")
    line.append_text(Text.from_markup(freshness_badge(fx_meta)))
    line.append(" курс   ·   ", style=f"dim {GRAY}")
    line.append(f"🕐 {datetime.now().strftime('%H:%M:%S')}", style=f"dim {GRAY}")
    console.print(line)
    console.print()

def print_fx(fx):
    if not fx:
        console.print(Text("  ⚠ Курс валют недоступен", style=YELLOW))
        console.print()
        return
    console.print(f"  [dim]💵 1 USD ≈ [/][bold {YELLOW}]{fx['USD_RUB']:.2f}₽[/]")
    if fx.get("EUR_RUB"):
        console.print(f"  [dim]💶 1 EUR ≈ [/][bold {YELLOW}]{fx['EUR_RUB']:.2f}₽[/]")
    if fx.get("USD_EUR"):
        console.print(f"  [dim]💵 1 USD ≈ [/][bold {CYAN}]{fx['USD_EUR']:.4f}€[/]")
    console.print()

def print_prices(prices, fx, source):
    if not prices:
        console.print("  [red]❌ Нет данных[/]")
        console.print()
        return
    t = Table(box=SIMPLE_HEAD, border_style="black",
              header_style=f"bold {CYAN}", padding=(0,1), expand=False)
    t.add_column("Монета", style=WHITE, min_width=18)
    t.add_column("USD", style=GREEN_BRIGHT, justify="right", min_width=12)
    t.add_column("RUB", style=YELLOW, justify="right", min_width=12)
    t.add_column("24ч", justify="right", min_width=8)
    usd_rub = fx.get("USD_RUB", 0) if fx else 0
    for cid, c in prices.items():
        icon = COIN_ICONS.get(cid, "●")
        name = f"{icon} {c['symbol']:<4} {c['name'][:10]}"
        usd = c.get("usd", 0)
        rub = c.get("rub") or (usd * usd_rub if usd_rub else 0)
        t.add_row(name, fmt_price(usd),
                  f"{rub:,.0f} ₽" if rub else "—",
                  fmt_change(c.get("change_24h", 0)))
    console.print(t)
    console.print()
    console.print(f"  [dim]📊 {source}[/]")
    console.print()

def fetch_all(force=False):
    """Возвращает (prices, source, crypto_meta, fx, fx_src, fx_meta)."""
    p, s, m  = get_crypto_prices(with_meta=True, force=force)
    f, fs, fm = get_fx_rates(with_meta=True, force=force)
    return p, s, m, f, fs, fm

def show_once(force=False):
    """Один показ."""
    with console.status(f"[bold {GREEN_BRIGHT}]📡 Загружаю...[/]", spinner="dots"):
        prices, source, crypto_meta, fx, fx_src, fx_meta = fetch_all(force=force)

    print_header(watch=False)
    print_freshness(crypto_meta, fx_meta)
    print_fx(fx)
    print_prices(prices, fx, source)

def show_watch_footer(interval):
    console.print(f"  [dim]⏱ обновление каждые {interval}с  ·  [/][bold {YELLOW}]Ctrl+C[/][dim] — выход[/]")
    console.print()

def watch_loop(interval):
    """Простой цикл: clear → показать → sleep."""
    try:
        while True:
            clear()
            prices, source, crypto_meta, fx, fx_src, fx_meta = fetch_all(force=True)

            print_header(watch=True)
            print_freshness(crypto_meta, fx_meta)
            print_fx(fx)
            print_prices(prices, fx, source)
            show_watch_footer(interval)

            time.sleep(interval)
    except KeyboardInterrupt:
        console.print()
        console.print("[dim]⏹ Watch остановлен.[/]")
        console.print()

def one_shot():
    """Обычный режим: показать один раз + подсказки."""
    clear()
    show_once(force=False)

    # Подсказки
    hint = Table(box=None, show_header=False, padding=(0, 2))
    hint.add_column("", style=f"bold {YELLOW}", width=14, justify="right")
    hint.add_column("", style=f"{CYAN}")
    hint.add_row("[crypto -w 30]", "🚀 watch — автообновление каждые 30с")
    hint.add_row("[crypto -w 60]", "🚀 watch — автообновление каждые 60с")
    hint.add_row("[crypto -w 10]", "🚀 watch — автообновление каждые 10с")
    hint.add_row("[crypto]", "🔄 просто показать (сейчас)")
    hint.add_row("[q]", "🚪 выход")
    console.print(Panel(hint, title=f"[bold {GREEN_BRIGHT}]⌨  ЧТО ДАЛЬШЕ[/]",
                        border_style=GREEN_DIM, padding=(0, 1)))
    console.print()

    try:
        cmd = console.input(f"[bold {MAGENTA}]╰─❯ [/]").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return

    if cmd in ("q", "exit", "quit", "выход"):
        return
    elif cmd.startswith("w"):
        parts = cmd.split()
        iv = DEFAULT_INTERVAL
        if len(parts) > 1 and parts[1].isdigit():
            iv = int(parts[1])
        watch_loop(iv)
    elif cmd == "":
        one_shot()

def main():
    args = sys.argv[1:]
    watch = False
    interval = DEFAULT_INTERVAL
    for i, a in enumerate(args):
        if a in ("--watch", "-w"):
            watch = True
            if i + 1 < len(args) and args[i+1].isdigit():
                interval = int(args[i+1])
            break

    if watch:
        watch_loop(interval)
        return

    try:
        one_shot()
    except KeyboardInterrupt:
        console.print()
        console.print("[dim]Выход.[/]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print()
        console.print("[dim]Выход.[/]")
```

---

## 📄 hacker_rpg.py

*36556 байт · 729 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HACKER SIMULATOR RPG — текстовый квест в стиле Terminal Argonov"""

import os, sys, json, time, random, hashlib
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.markdown import Markdown
from rich.progress import Progress, BarColumn
from rich.box import SIMPLE_HEAD
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

console = Console()
HOME = os.path.expanduser("~")
SAVE_FILE = os.path.join(HOME, ".hacker_rpg_save.json")

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"; ORANGE = "dark_orange"

# ═══════════ ИГРОВЫЕ ДАННЫЕ ═══════════
SKILLS = {
    "cracking":    {"name": "🔐 Cracking",    "desc": "Взлом паролей и защит"},
    "stealth":     {"name": "🕵️  Stealth",     "desc": "Снижает риск обнаружения"},
    "trading":     {"name": "💰 Trading",     "desc": "Больше денег с миссий"},
    "programming": {"name": "🛠 Programming", "desc": "Открывает сложные цели"},
    "network":     {"name": "🌐 Network",     "desc": "Доступ к сетевым миссиям"},
    "social":      {"name": "💬 Social",      "desc": "Фишинг, манипуляции"},
}

FACTIONS = {
    "crimson":   {"name": "🔴 Crimson",   "desc": "Русские хакеры. Сильные, дорогие",  "bonus": "+25% денег, +10% риск"},
    "ghost":     {"name": "🔵 Ghost",     "desc": "Анонимные. Скрытные, дешёвые",       "bonus": "-25% риск, -10% денег"},
    "whitehat":  {"name": "🟢 White Hat", "desc": "Пентестеры. Легальные, стабильные", "bonus": "-50% геймовер-риск"},
    "syndicate": {"name": "🟡 Syndicate", "desc": "Корпорация. Максимум денег",          "bonus": "+50% денег, +25% риск"},
}

# ═══════════ МИССИИ (по уровням) ═══════════
MISSIONS = {
    0: [  # Newbie
        {"id":"m01","name":"Ломаем дверь","story":"Древний форум на PHP. Админка на /admin, пароль 12345?","target":"forum.local","reward":15,"xp":10,"diff":1,"req":{},"skills":["cracking"]},
        {"id":"m02","name":"Старый WordPress","story":"Блог соседа. Плагин не обновлялся 3 года.","target":"blog.local","reward":25,"xp":15,"diff":2,"req":{},"skills":["cracking","programming"]},
        {"id":"m03","name":"Wi-Fi кафе","story":"Открытая сеть кафе. Перехватить трафик и войти в роутер.","target":"cafe-wifi","reward":30,"xp":20,"diff":2,"req":{},"skills":["network"]},
        {"id":"m04","name":"Фишинговый сайт","story":"Поддельная страница банка. Найти и обрушить.","target":"fake-bank.xyz","reward":40,"xp":25,"diff":3,"req":{},"skills":["social","cracking"]},
        {"id":"m05","name":"Разведка портов","story":"Просканировать открытые порты сервера конкурента.","target":"rival-server","reward":50,"xp":30,"diff":3,"req":{},"skills":["network"]},
    ],
    1: [  # Script Kiddie
        {"id":"m06","name":"SQL-инъекция","story":"Интернет-магазин с дырявой формой поиска.","target":"shop-online.ru","reward":120,"xp":60,"diff":4,"req":{"cracking":3},"skills":["cracking","programming"]},
        {"id":"m07","name":"Социальная инженерия","story":"Убедить сотрудника выдать пароль.","target":"office.corp","reward":200,"xp":80,"diff":5,"req":{"social":3},"skills":["social"]},
        {"id":"m08","name":"DDoS-заказ","story":"Положить игровой сервер на 2 часа.","target":"game-server.io","reward":300,"xp":100,"diff":5,"req":{"network":3},"skills":["network"]},
        {"id":"m09","name":"Кража API-ключей","story":"Из чужого репозитория на GitHub.","target":"github.com/user/repo","reward":400,"xp":120,"diff":6,"req":{"programming":3},"skills":["programming","cracking"]},
        {"id":"m10","name":"Брутфорс-атака","story":"Подобрать пароль к корп-почте.","target":"mail.corp.ru","reward":500,"xp":150,"diff":6,"req":{"cracking":5},"skills":["cracking"]},
    ],
    2: [  # Hacker
        {"id":"m11","name":"Пентест банка","story":"Внутренний аудит безопасности.","target":"bank.internal","reward":1500,"xp":300,"diff":8,"req":{"cracking":7,"programming":5},"skills":["cracking","programming","stealth"]},
        {"id":"m12","name":"Кража базы данных","story":"3 миллиона пользователей.","target":"social-media.db","reward":2500,"xp":400,"diff":9,"req":{"programming":7,"network":5},"skills":["programming","network","stealth"]},
        {"id":"m13","name":"Взлом смарт-контракта","story":"Крипто-биржа с багом в контракте.","target":"crypto-exchange.eth","reward":5000,"xp":600,"diff":10,"req":{"programming":9},"skills":["programming","cracking"]},
        {"id":"m14","name":"APT-атака на корпорацию","story":"Многоступенчатая атака. 3 недели подготовки.","target":"megacorp.com","reward":8000,"xp":900,"diff":11,"req":{"cracking":10,"network":8,"stealth":8},"skills":["cracking","network","stealth","social"]},
        {"id":"m15","name":"Заряженный ransomware","story":"Развернуть вирус-вымогатель на 500 машинах.","target":"hospital.network","reward":12000,"xp":1200,"diff":12,"req":{"programming":11,"network":9},"skills":["programming","network"]},
    ],
    3: [  # Elite
        {"id":"m16","name":"Госструктура","story":"Взлом системы министерства.","target":"gov.system","reward":30000,"xp":2500,"diff":14,"req":{"cracking":13,"stealth":12},"skills":["cracking","stealth","programming"]},
        {"id":"m17","name":"Атака на SWIFT","story":"Межбанковские переводы. Только для настоящих мастеров.","target":"swift.network","reward":100000,"xp":5000,"diff":16,"req":{"cracking":15,"network":14,"programming":13},"skills":["cracking","network","programming","stealth"]},
        {"id":"m18","name":"Кража прототипа ИИ","story":"Секретная модель из лаборатории.","target":"research-lab.ai","reward":150000,"xp":7000,"diff":17,"req":{"programming":16,"social":12},"skills":["programming","social","stealth"]},
    ],
    4: [  # Legend
        {"id":"m19","name":"Anonymous-операция","story":"Атака на международную сеть. 1000 хакеров вместе.","target":"worldwide.anonymous","reward":500000,"xp":20000,"diff":20,"req":{"cracking":20,"stealth":20,"programming":20,"network":20,"social":15},"skills":["cracking","network","programming","stealth","social"]},
        {"id":"m20","name":"Взлом спутника","story":"Управление спутником связи. Финальный босс.","target":"satellite.sky","reward":1000000,"xp":50000,"diff":25,"req":{"cracking":25,"network":22,"programming":22,"stealth":20},"skills":["cracking","network","programming","stealth"]},
    ],
}

# ═══════════ МАГАЗИН ═══════════
SHOP_SOFT = [
    {"id":"s1","name":"🔧 Nmap Pro","price":500,"desc":"+1 к Cracking, открывает сетевые миссии","effect":{"cracking":1}},
    {"id":"s2","name":"🔍 SQLMap","price":800,"desc":"+2 к Cracking","effect":{"cracking":2}},
    {"id":"s3","name":"🎭 Proxy Chain","price":1200,"desc":"+2 к Stealth","effect":{"stealth":2}},
    {"id":"s4","name":"🔐 Hashcat","price":2000,"desc":"+3 к Cracking","effect":{"cracking":3}},
    {"id":"s5","name":"🕶  Tor Browser+","price":3000,"desc":"+3 к Stealth","effect":{"stealth":3}},
    {"id":"s6","name":"💬 SocialBot","price":4000,"desc":"+3 к Social","effect":{"social":3}},
    {"id":"s7","name":"🛠 CodeInjector","price":6000,"desc":"+3 к Programming","effect":{"programming":3}},
    {"id":"s8","name":"🌐 VPN-Ultra","price":8000,"desc":"+3 к Network","effect":{"network":3}},
    {"id":"s9","name":"💰 Trader-X","price":10000,"desc":"+3 к Trading","effect":{"trading":3}},
    {"id":"s10","name":"🚀 Quantum-Crack","price":25000,"desc":"+5 к Cracking","effect":{"cracking":5}},
]

# ═══════════ СОСТОЯНИЕ ═══════════
STATE = {
    "hp": 100,
    "money": 50,
    "xp": 0,
    "level": 0,
    "skills": {k: 0 for k in SKILLS.keys()},
    "faction": None,
    "completed": [],
    "owned_software": [],
    "equipment": [],
    "started_at": None,
    "total_missions": 0,
    "deaths": 0,
    "wins": 0,
}

LEVEL_NAMES = ["🟢 NEWBIE", "🟡 SCRIPT KIDDIE", "🟠 HACKER", "🔴 ELITE", "🏆 LEGEND"]
LEVEL_XP = [0, 200, 2000, 20000, 100000]

# ═══════════ УТИЛИТЫ ═══════════
def clear():
    os.system("clear")

def hp_bar(hp, width=30):
    filled = int((hp/100)*width)
    if hp > 70: color = "bright_green"
    elif hp > 40: color = "bright_yellow"
    elif hp > 15: color = "dark_orange"
    else: color = "bright_red"
    return Text("▓"*filled + "░"*(width-filled), style=color)

def save_game(silent=False):
    STATE["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(STATE, f, ensure_ascii=False, indent=1)
        if not silent:
            console.print(f"[green]💾 Прогресс сохранён[/]")
        return True
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")
        return False

def load_game():
    global STATE
    if not os.path.exists(SAVE_FILE): return False
    try:
        with open(SAVE_FILE, encoding="utf-8") as f:
            data = json.load(f)
        for k in STATE.keys():
            if k in data: STATE[k] = data[k]
        return True
    except: return False

def check_level_up():
    """Возвращает True если уровень повысился"""
    old_level = STATE["level"]
    new_level = 0
    for i, thresh in enumerate(LEVEL_XP):
        if STATE["xp"] >= thresh: new_level = i
    if new_level > old_level:
        STATE["level"] = new_level
        console.print()
        console.print(Panel(Align.center(Text(f"🎉 УРОВЕНЬ ПОВЫШЕН: {LEVEL_NAMES[new_level]}", style="bold bright_green")),
                            border_style="bright_green"))
        console.print()
        save_game(silent=True)
        return True
    return False

def get_available_missions():
    """Возвращает список доступных миссий с их сложностью (относительно скиллов)"""
    available = []
    for level, missions in MISSIONS.items():
        for m in missions:
            if m["id"] in STATE["completed"]: continue
            # Проверяем требования
            req_ok = True
            for skill, val in m["req"].items():
                if STATE["skills"].get(skill, 0) < val:
                    req_ok = False; break
            if req_ok:
                available.append((level, m))
    return available

# ═══════════ МИНИ-ИГРЫ ═══════════
def minigame_crack(diff):
    """Mastermind: угадать 4-значный код (0-9). 10 попыток."""
    code = [random.randint(0,9) for _ in range(4)]
    tries = max(3, 11 - diff)  # сложнее → меньше попыток

    console.print()
    console.print(Panel.fit(
        f"[bold cyan]🔐 ВЗЛОМ ПАРОЛЯ[/]\n"
        f"[dim]Код из 4 цифр (0-9). Угадай за {tries} попыток.[/]\n"
        f"[dim]● = правильная цифра на месте · ○ = правильная не на месте[/]",
        border_style="cyan"))
    console.print()

    for attempt in range(1, tries+1):
        try:
            guess_str = console.input(f"[bold magenta]Попытка {attempt}/{tries} > [/]").strip()
        except: return False
        if not guess_str.isdigit() or len(guess_str) != 4:
            console.print("[red]❌ Нужно ровно 4 цифры[/]")
            continue
        guess = [int(c) for c in guess_str]
        if guess == code:
            console.print(f"[bold green]✅ ВЗЛОМАНО за {attempt} попыток![/]\n")
            return True
        # Подсказки
        bulls = sum(1 for i in range(4) if guess[i] == code[i])
        code_c = code.copy(); guess_c = guess.copy()
        for i in range(4):
            if guess_c[i] == code_c[i]: code_c[i] = None; guess_c[i] = None
        cows = sum(1 for g in guess_c if g is not None and g in code_c)
        console.print(f"  [green]{'●'*bulls}[/][yellow]{'○'*cows}[/][dim]{'·'*(4-bulls-cows)}[/]")

    console.print(f"[red]❌ Не удалось взломать за {tries} попыток. Код был: {''.join(map(str,code))}[/]\n")
    return False

def minigame_infiltrate(diff):
    """Simon: запомнить последовательность символов"""
    seq_len = min(4 + diff, 12)
    chars = "ABCDEFGH"
    sequence = [random.choice(chars) for _ in range(seq_len)]

    console.print()
    console.print(Panel.fit(
        f"[bold cyan]🕵️  ПРОНИКНОВЕНИЕ[/]\n"
        f"[dim]Запомни последовательность {seq_len} символов.[/]",
        border_style="cyan"))
    console.print()
    console.print(f"[bold yellow]{' '.join(sequence)}[/]")
    time.sleep(2 + seq_len * 0.3)
    clear()
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]🕵️  ПРОНИКНОВЕНИЕ[/]\n"
        f"[dim]Введи последовательность через пробел.[/]",
        border_style="cyan"))
    console.print()
    try:
        answer = console.input("[bold magenta]> [/]").strip().upper().split()
    except: return False
    if answer == sequence:
        console.print("[bold green]✅ ПРОНИКНОВЕНИЕ УСПЕШНО![/]\n")
        return True
    console.print(f"[red]❌ Неверно. Было: {' '.join(sequence)}[/]\n")
    return False

def minigame_social(diff):
    """Выбрать правильную реплику из 3"""
    scenarios = [
        {"q":"Сотрудник банка: 'Кто вы такой?'",
         "options":[
             ("Я из IT-отдела, проверяю систему", True),
             ("Привет! Я хакер, дай пароль", False),
             ("Ты что, не узнал меня?", False),
         ]},
        {"q":"Админ: 'Назовите ваш отдел.'",
         "options":[
             ("Не помню точно, но начальник сказал...", False),
             ("Финансовый. У нас аудит на следующей неделе.", True),
             ("А какая разница?", False),
         ]},
        {"q":"Секретарь: 'Могу я увидеть ваш пропуск?'",
         "options":[
             ("Забыл в машине, сейчас вернусь", False),
             ("Конечно, вот он. Слушайте, у меня к вам личное дело...", True),
             ("Не ваше дело", False),
         ]},
        {"q":"Охранник: 'Стойте! Куда собрались?'",
         "options":[
             ("Домой, я устал", False),
             ("К начальнику, он сам меня вызвал", True),
             ("Тебе что, зарплату мало платят?", False),
         ]},
    ]
    rounds = min(2 + diff // 3, 5)
    console.print()
    console.print(Panel.fit(f"[bold cyan]💬 СОЦИАЛЬНАЯ ИНЖЕНЕРИЯ[/]\n[dim]Выбери правильный ответ. Раундов: {rounds}[/]",
                            border_style="cyan"))
    console.print()

    correct = 0
    for r in range(rounds):
        sc = random.choice(scenarios)
        console.print(f"[bold yellow]Раунд {r+1}/{rounds}[/]")
        console.print(f"  {sc['q']}\n")
        opts = sc["options"][:]
        random.shuffle(opts)
        for i, (o, _) in enumerate(opts, 1):
            console.print(f"  [cyan]{i}.[/] {o}")
        try:
            ch = console.input("\n[bold magenta]Выбор> [/]").strip()
        except: return False
        if ch.isdigit() and 1 <= int(ch) <= len(opts):
            if opts[int(ch)-1][1]:
                console.print("  [green]✔ Хорошо[/]\n"); correct += 1
            else:
                console.print("  [red]✘ Провал реплики[/]\n")

    needed = (rounds * 2) // 3
    if correct >= needed:
        console.print(f"[bold green]✅ ПРОШЛО: {correct}/{rounds}[/]\n")
        return True
    console.print(f"[red]❌ Провал: {correct}/{rounds} (нужно {needed})[/]\n")
    return False

def get_minigame(skill_type, diff):
    if skill_type == "cracking": return minigame_crack(diff)
    if skill_type in ("network", "stealth"): return minigame_infiltrate(diff)
    if skill_type == "social": return minigame_social(diff)
    if skill_type == "programming": return minigame_crack(diff)  # тоже код
    if skill_type == "trading": return minigame_social(diff)    # переговоры
    return minigame_crack(diff)

# ═══════════ МИССИИ — ИСПОЛНЕНИЕ ═══════════
def do_mission(level, mission):
    """Возвращает True если миссия пройдена"""
    clear()
    console.print()
    console.print(Panel(
        Group(
            Text(f"📋 МИССИЯ: {mission['name']}", style="bold bright_cyan"),
            Text(""),
            Text(f"🎯 Цель: {mission['target']}", style="yellow"),
            Text(f"💀 Сложность: {mission['diff']}/25", style="red"),
            Text(""),
            Text(mission['story'], style="white"),
            Text(""),
            Text(f"💰 Награда: ${mission['reward']}", style="green"),
            Text(f"⭐ Опыт: {mission['xp']}", style="cyan"),
        ),
        border_style="cyan", padding=(1,2)))
    console.print()

    try:
        ans = console.input("[bold magenta]Начать взлом? (y/n)> [/]").strip().lower()
    except: return False
    if ans != "y":
        console.print("[dim]Отмена[/]"); return False

    # Определяем какой скилл использовать
    main_skill = mission["skills"][0] if mission["skills"] else "cracking"

    # Мини-игра
    won = get_minigame(main_skill, mission["diff"])

    if not won:
        # Провал миссии → урон
        dmg = random.randint(10, 30)
        STATE["hp"] = max(0, STATE["hp"] - dmg)
        console.print(f"[red]💥 Провал! Потеряно {dmg} HP (осталось {STATE['hp']})[/]\n")

        # Проверка геймовера
        if STATE["hp"] <= 0:
            gameover()
            return False

        # Провал с шансом обнаружения (зависит от stealth)
        stealth = STATE["skills"].get("stealth", 0)
        detect_chance = max(5, 60 - stealth * 3 - mission["diff"] * 2)
        if random.randint(1, 100) <= detect_chance:
            console.print("[red bold]🚨 ТЕБЯ ОБНАРУЖИЛИ![/]\n")
            time.sleep(1.5)
            gameover()
            return False

        console.print("[yellow]⚠ Тебе удалось скрыться, но миссия провалена[/]\n")
        save_game(silent=True)
        return False

    # Успех!
    money = mission["reward"]
    xp = mission["xp"]

    # Множители от фракции
    if STATE["faction"] == "crimson": money = int(money * 1.25)
    elif STATE["faction"] == "ghost": money = int(money * 0.9)
    elif STATE["faction"] == "syndicate": money = int(money * 1.5)

    # Множители от скиллов
    trading = STATE["skills"].get("trading", 0)
    money = int(money * (1 + trading * 0.05))

    STATE["money"] += money
    STATE["xp"] += xp
    STATE["completed"].append(mission["id"])
    STATE["total_missions"] += 1
    STATE["wins"] += 1

    console.print()
    console.print(Panel(
        Group(
            Text("✅ МИССИЯ ВЫПОЛНЕНА", style="bold bright_green"),
            Text(""),
            Text(f"💰 Получено: ${money}", style="green"),
            Text(f"⭐ Опыт: +{xp}", style="cyan"),
            Text(f"💼 Всего денег: ${STATE['money']}", style="yellow"),
        ),
        border_style="green", padding=(1,2)))
    console.print()

    # Автосохранение при успехе
    save_game(silent=True)
    console.print("[dim]💾 Автосохранение[/]\n")

    check_level_up()
    time.sleep(2)
    return True

def gameover():
    clear()
    console.print()
    console.print(Align.center(Panel.fit(
        "[bold red]💀 GAME OVER 💀[/]\n\n"
        "[white]Ты попался. Суд, приговор, всё кончено.[/]\n\n"
        f"[yellow]Всего миссий: {STATE['total_missions']}[/]\n"
        f"[green]Успешных: {STATE['wins']}[/]\n"
        f"[cyan]Заработано: ${STATE['money']}[/]\n"
        f"[magenta]Уровень: {LEVEL_NAMES[STATE['level']]}[/]\n\n"
        "[dim]Прогресс удалён.[/]",
        border_style="red", padding=(2,4))))
    console.print()
    STATE["deaths"] += 1
    # Удаляем сейв
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    console.print("[dim]Нажми Enter чтобы начать заново...[/]")
    try: console.input()
    except: pass
    reset_game()
    main_menu()

def reset_game():
    global STATE
    STATE.update({
        "hp": 100, "money": 50, "xp": 0, "level": 0,
        "skills": {k: 0 for k in SKILLS.keys()},
        "faction": None, "completed": [], "owned_software": [],
        "equipment": [], "started_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_missions": 0, "deaths": STATE.get("deaths", 0), "wins": 0,
    })

# ═══════════ ЭКРАНЫ ═══════════
def banner():
    clear()
    console.print()
    art = r"""
    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗
    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
    ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                 S I M U L A T O R
    """
    console.print(Align.center(f"[bold bright_green]{art}[/]"))
    console.print(Align.center("[dim]Текстовая RPG хакера в Termux[/]"))
    console.print()

def status_panel():
    lvl_name = LEVEL_NAMES[STATE["level"]]
    faction = FACTIONS.get(STATE["faction"], {}).get("name", "— не в фракции")
    t = Table(box=None, show_header=False, padding=(0,2))
    t.add_column("", style="bold yellow", width=20)
    t.add_column("", width=30)
    t.add_column("", style="bold yellow", width=18)
    t.add_column("", width=20)

    t.add_row("👤 Уровень", lvl_name, "💰 Деньги", f"[green]${STATE['money']}[/]")
    t.add_row("⭐ Опыт", f"[cyan]{STATE['xp']}[/]", "🎯 Миссий", str(STATE['total_missions']))
    t.add_row("🩸 HP", hp_bar(STATE["hp"]), "🏴 Фракция", faction)
    t.add_row("💀 Смертей", str(STATE['deaths']), "🏆 Побед", str(STATE['wins']))
    return Panel(t, title="[bold yellow]┃ ПРОФИЛЬ ┃[/]", border_style="yellow", padding=(0,1))

def skills_panel():
    t = Table(box=SIMPLE_HEAD, border_style="cyan", header_style="bold cyan", padding=(0,2))
    t.add_column("Навык", style="bold cyan", width=20)
    t.add_column("Уровень", justify="right", width=10)
    t.add_column("Описание", style="dim")
    for k, v in STATE["skills"].items():
        s = SKILLS[k]
        t.add_row(s["name"], f"[bright_green]{v}[/]", s["desc"])
    return t

def missions_screen():
    available = get_available_missions()
    if not available:
        console.print("[yellow]⚠ Нет доступных миссий. Прокачай скиллы в магазине.[/]\n")
        return []

    # Сортируем по сложности
    available.sort(key=lambda x: x[1]["diff"])

    t = Table(box=SIMPLE_HEAD, border_style="magenta", header_style="bold magenta", padding=(0,1))
    t.add_column("#", style="bold yellow", width=4, justify="right")
    t.add_column("Миссия", style="white", width=28)
    t.add_column("Цель", style="cyan", width=24)
    t.add_column("Сложность", justify="center", width=10)
    t.add_column("💰", style="green", justify="right", width=10)
    t.add_column("⭐", style="cyan", justify="right", width=8)

    for i, (level, m) in enumerate(available, 1):
        lvl_mark = "🟢" if level == 0 else "🟡" if level == 1 else "🟠" if level == 2 else "🔴"
        diff_str = f"{lvl_mark} {m['diff']}"
        t.add_row(str(i), m["name"], m["target"], diff_str, f"${m['reward']}", str(m['xp']))
    console.print(t)
    console.print()
    return available

def shop_screen():
    t = Table(box=SIMPLE_HEAD, border_style="green", header_style="bold green", padding=(0,1))
    t.add_column("#", style="bold yellow", width=4, justify="right")
    t.add_column("Софт", style="white", width=24)
    t.add_column("Цена", style="green", justify="right", width=10)
    t.add_column("Описание", style="dim")
    t.add_column("Куплен", justify="center", width=8)

    for i, s in enumerate(SHOP_SOFT, 1):
        owned = "✔" if s["id"] in STATE["owned_software"] else ""
        t.add_row(str(i), s["name"], f"${s['price']}", s["desc"], owned)
    console.print(t)
    console.print()

def factions_screen():
    t = Table(box=SIMPLE_HEAD, border_style="magenta", header_style="bold magenta", padding=(0,1))
    t.add_column("#", style="bold yellow", width=4, justify="right")
    t.add_column("Фракция", style="white", width=18)
    t.add_column("Описание", width=44)
    t.add_column("Бонус", style="green", width=24)
    for i, (fid, f) in enumerate(FACTIONS.items(), 1):
        current = "✔" if STATE["faction"] == fid else ""
        t.add_row(str(i), f["name"] + " " + current, f["desc"], f["bonus"])
    console.print(t)
    console.print()

# ═══════════ TAB-COMPLETER ═══════════
COMMANDS = [
    "missions","m","shop","s","status","st","skills","sk",
    "factions","f","join","attack","a","save","load",
    "reset","help","h","q","quit","exit"
]

class RPGComp(Completer):
    def get_completions(self, doc, ev):
        t = doc.text_before_cursor
        if " " in t: return
        for c in sorted(COMMANDS):
            if c.startswith(t.lower()):
                yield Completion(c, start_position=-len(t))

# ═══════════ ГЛАВНОЕ МЕНЮ ═══════════
def main_menu():
    global STATE
    while True:
        banner()
        console.print(status_panel())
        console.print()

        # Подсказки
        c = Table(box=None, show_header=False, padding=(0,2))
        c.add_column("", style="bold yellow", width=20)
        c.add_column("", style="cyan", width=30)
        c.add_column("", style="bold yellow", width=20)
        c.add_column("", style="cyan", width=30)
        c.add_row("[m]issions","📋 Список миссий", "[sh]op","🛒 Магазин")
        c.add_row("[st]atus","👤 Профиль", "[sk]ills","🎯 Скиллы")
        c.add_row("[f]actions","🏴 Фракции", "[s]ave","💾 Сохранить")
        c.add_row("[h]elp","❓ Помощь", "[q]uit","🚪 Выход")
        console.print(Panel(c, title="[bold cyan]⌨  КОМАНДЫ[/]", border_style="cyan", padding=(0,1)))
        console.print()

        prompt_txt = "╰─🎮> "
        try:
            cmd = console.input(f"[bold magenta]{prompt_txt}[/]").strip().lower()
        except (EOFError, KeyboardInterrupt):
            save_game(silent=True)
            console.print("\n[dim]💾 Автосохранение при выходе. До связи! 🖖[/]")
            break

        if not cmd: continue

        if cmd in ("q","quit","exit"):
            save_game(silent=True)
            console.print("[dim]💾 Автосохранение. До связи! 🖖[/]")
            break

        elif cmd in ("missions","m"):
            avail = missions_screen()
            if avail:
                try:
                    ch = console.input("[bold magenta]Номер миссии (Enter — назад)> [/]").strip()
                except: continue
                if ch.isdigit() and 1 <= int(ch) <= len(avail):
                    level, m = avail[int(ch)-1]
                    do_mission(level, m)

        elif cmd in ("shop","sh","s"):
            shop_screen()
            try:
                ch = console.input("[bold magenta]Номер для покупки (Enter — назад)> [/]").strip()
            except: continue
            if ch.isdigit() and 1 <= int(ch) <= len(SHOP_SOFT):
                item = SHOP_SOFT[int(ch)-1]
                if item["id"] in STATE["owned_software"]:
                    console.print("[yellow]Уже куплено[/]\n"); time.sleep(1); continue
                if STATE["money"] < item["price"]:
                    console.print(f"[red]❌ Не хватает ${item['price'] - STATE['money']}[/]\n"); time.sleep(1.5); continue
                STATE["money"] -= item["price"]
                STATE["owned_software"].append(item["id"])
                for skill, val in item["effect"].items():
                    STATE["skills"][skill] = STATE["skills"].get(skill, 0) + val
                console.print(f"[green]✔ Куплено: {item['name']}[/]\n")
                save_game(silent=True)
                time.sleep(1.5)

        elif cmd in ("status","st"):
            clear()
            console.print()
            console.print(status_panel())
            console.print()
            console.print(skills_panel())
            console.print()
            console.input("[dim]Enter — назад[/] ")

        elif cmd in ("skills","sk"):
            clear()
            console.print()
            console.print(Panel.fit("[bold cyan]🎯 СКИЛЛЫ[/]", border_style="cyan"))
            console.print()
            console.print(skills_panel())
            console.print()
            console.input("[dim]Enter — назад[/] ")

        elif cmd in ("factions","f"):
            clear()
            console.print()
            console.print(Panel.fit("[bold magenta]🏴 ФРАКЦИИ[/]", border_style="magenta"))
            console.print()
            factions_screen()
            try:
                ch = console.input("[bold magenta]Номер для вступления (Enter — назад)> [/]").strip()
            except: continue
            if ch.isdigit() and 1 <= int(ch) <= len(FACTIONS):
                fid = list(FACTIONS.keys())[int(ch)-1]
                if STATE["faction"] == fid:
                    console.print("[yellow]Уже в этой фракции[/]\n"); time.sleep(1); continue
                STATE["faction"] = fid
                console.print(f"[green]✔ Вступил в {FACTIONS[fid]['name']}[/]\n")
                save_game(silent=True)
                time.sleep(1.5)

        elif cmd in ("save","sv"):
            save_game()

        elif cmd in ("load","l"):
            if load_game():
                console.print("[green]✔ Загрузка успешна[/]\n"); time.sleep(1)
            else:
                console.print("[red]❌ Сейв не найден[/]\n"); time.sleep(1)

        elif cmd in ("reset","r"):
            try:
                a = console.input("[red bold]Точно сбросить весь прогресс? (yes/n)> [/]").strip()
            except: continue
            if a == "yes":
                reset_game()
                if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
                console.print("[green]✔ Сброшено[/]\n"); time.sleep(1)

        elif cmd in ("help","h"):
            clear()
            console.print()
            console.print(Panel(
                Group(
                    Text("🎮 HACKER RPG — помощь", style="bold bright_green"),
                    Text(""),
                    Text("🎯 Цель: пройти все миссии, заработать $, стать LEGEND.", style="white"),
                    Text(""),
                    Text("📋 missions — список контрактов", style="cyan"),
                    Text("🛒 shop — купить софт (+ скиллы)", style="cyan"),
                    Text("🏴 factions — вступить во фракцию (+ бонусы)", style="cyan"),
                    Text("💾 save — сохранить прогресс", style="cyan"),
                    Text("💀 Если HP = 0 или тебя поймают — GAME OVER, прогресс стирается.", style="red"),
                    Text(""),
                    Text("⚙ Автосохранение после каждой успешной миссии.", style="dim"),
                ),
                border_style="bright_green", padding=(1,2)))
            console.print()
            console.input("[dim]Enter — назад[/] ")

        else:
            console.print(f"[red]❌ Неизвестно: {cmd}. Набери 'h' для помощи[/]\n")
            time.sleep(1)

# ═══════════ ЗАПУСК ═══════════
def main():
    global STATE
    clear()

    # Загрузка или новая игра
    if os.path.exists(SAVE_FILE):
        banner()
        console.print(Panel.fit(
            f"[bold green]💾 Найден сохранённый прогресс[/]\n\n"
            f"Уровень: {LEVEL_NAMES[STATE.get('level',0)]}\n"
            f"Деньги: ${STATE.get('money',0)}\n"
            f"Миссий пройдено: {STATE.get('total_missions',0)}",
            border_style="green"))
        console.print()
        console.print("  [cyan]1[/])  Продолжить")
        console.print("  [cyan]2[/])  Новая игра")
        console.print()
        try:
            ch = console.input("[bold magenta]Выбор> [/]").strip()
        except: ch = "1"
        if ch == "2":
            reset_game()
        else:
            load_game()
    else:
        reset_game()
        STATE["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    main_menu()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано.[/]")
        save_game(silent=True)
```

---

## 📄 download_zone.py

*12624 байт · 309 строк*

```python
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
```

---

## 📄 matrix.py

*7170 байт · 182 строк*

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matrix Rain MAX — гипер-масштабный цифровой дождь с мерцанием, вспышками и свечением"""

import curses
import random
import time

# ═══════════ СИМВОЛЫ ═══════════
KATAKANA = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ"
HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわん"
LATIN    = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
DIGITS   = "0123456789"
SYMBOLS  = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
GREEK    = "αβγδεζηθικλμνξοπρστυφχψω"
CYRILLIC = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

# Основной набор — катаканы больше всего (как в фильме)
ALL_CHARS = (KATAKANA * 6 + HIRAGANA * 2 + LATIN + DIGITS * 3 +
             SYMBOLS * 2 + GREEK + CYRILLIC)

# ═══════════ ЦВЕТА ═══════════
C_HEAD   = 1  # белый — голова капли
C_FLASH  = 2  # ярко-белый — вспышка
C_BRIGHT = 3  # ярко-зелёный
C_MID    = 4  # зелёный
C_DARK   = 5  # тёмно-зелёный
C_FAINT  = 6  # очень тёмный
C_FAINT2 = 7  # почти чёрный (глубокий хвост)

TAIL_LEN = 22  # Длинный хвост — эффект глубокого затухания


def init_colors():
    curses.start_color()
    try:
        curses.use_default_colors()
    except Exception:
        pass
    curses.init_pair(C_HEAD,   curses.COLOR_WHITE,   -1)
    curses.init_pair(C_FLASH,  curses.COLOR_WHITE,   -1)
    curses.init_pair(C_BRIGHT, curses.COLOR_GREEN,   -1)
    curses.init_pair(C_MID,    curses.COLOR_GREEN,   -1)
    curses.init_pair(C_DARK,   curses.COLOR_GREEN,   -1)
    curses.init_pair(C_FAINT,  curses.COLOR_GREEN,   -1)
    curses.init_pair(C_FAINT2, curses.COLOR_GREEN,   -1)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)
    init_colors()

    max_y, max_x = stdscr.getmaxyx()

    # Инициализация капель для каждой колонки
    def new_drop(x, spread=False):
        return {
            "x": x,
            "y": random.randint(-max_y * 3, -1) if spread else random.randint(-25, -3),
            "speed": random.choice([0.2, 0.35, 0.5, 0.7, 0.9, 1.1, 1.4, 1.8, 2.2]),
            "counter": 0.0,
            "tail_len": random.randint(TAIL_LEN - 8, TAIL_LEN + 6),
            "flash_chance": random.random() * 0.08,   # шанс вспышки на шаге
        }

    drops = [new_drop(x, spread=True) for x in range(max_x)]

    # Плотность: на очень широких экранах добавляем вторые капли
    if max_x > 60:
        drops += [new_drop(random.randint(0, max_x - 1), spread=True) for _ in range(max_x // 4)]

    frame = 0

    while True:
        # Выход
        try:
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q'), 27):
                break
        except Exception:
            pass

        max_y, max_x = stdscr.getmaxyx()
        frame += 1

        for drop in drops:
            drop["counter"] += drop["speed"]

            if drop["counter"] >= 1.0:
                drop["counter"] = 0.0
                drop["y"] += 1

                x = drop["x"]
                y = drop["y"]

                if x >= max_x:
                    continue

                # Случайное мерцание в хвосте (эффект «глюка»)
                flicker = random.random() < 0.15

                # ГОЛОВА (капля)
                if 0 <= y < max_y:
                    ch_head = random.choice(ALL_CHARS)
                    # Вспышка — иногда голова становится ярче
                    if random.random() < drop["flash_chance"]:
                        attr = curses.color_pair(C_FLASH) | curses.A_BOLD | curses.A_REVERSE
                    else:
                        attr = curses.color_pair(C_HEAD) | curses.A_BOLD
                    try:
                        stdscr.addstr(y, x, ch_head, attr)
                    except curses.error:
                        pass

                # ХВОСТ с плавным затуханием
                tail = drop["tail_len"]
                for i in range(1, tail + 1):
                    ty = y - i
                    if not (0 <= ty < max_y):
                        continue

                    tchar = random.choice(ALL_CHARS)

                    # Мерцание — иногда символ «перерождается» в середине хвоста
                    if flicker and i % 3 == 0:
                        attr = curses.color_pair(C_BRIGHT) | curses.A_BOLD
                    elif i == 1:
                        attr = curses.color_pair(C_BRIGHT) | curses.A_BOLD
                    elif i <= 3:
                        attr = curses.color_pair(C_BRIGHT)
                    elif i <= 6:
                        attr = curses.color_pair(C_MID)
                    elif i <= 10:
                        attr = curses.color_pair(C_DARK)
                    elif i <= 15:
                        attr = curses.color_pair(C_FAINT)
                    else:
                        attr = curses.color_pair(C_FAINT2) | curses.A_DIM

                    try:
                        stdscr.addstr(ty, x, tchar, attr)
                    except curses.error:
                        pass

                # Стираем «хвостик» позади капли
                erase_y = y - tail
                if 0 <= erase_y < max_y:
                    try:
                        stdscr.addstr(erase_y, x, " ")
                    except curses.error:
                        pass

                # Если капля ушла — перезапуск
                if y - tail >= max_y:
                    drop["y"] = random.randint(-30, -5)
                    drop["speed"] = random.choice([0.2, 0.35, 0.5, 0.7, 0.9, 1.1, 1.4, 1.8, 2.2])
                    drop["tail_len"] = random.randint(TAIL_LEN - 8, TAIL_LEN + 6)
                    drop["counter"] = 0.0
                    drop["flash_chance"] = random.random() * 0.08

        # Общая случайная вспышка по экрану (эффект «молнии»)
        if random.random() < 0.015:
            fx = random.randint(0, max_x - 1)
            fy = random.randint(0, max_y - 1)
            try:
                stdscr.addstr(fy, fx, random.choice(ALL_CHARS),
                              curses.color_pair(C_FLASH) | curses.A_BOLD | curses.A_REVERSE)
            except curses.error:
                pass

        stdscr.refresh()
        time.sleep(0.025)  # ~40 FPS


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
```

---

## 📄 passgen.py

*1729 байт · 45 строк*

```python
import string
import secrets
import sys

# Настройка цветов в терминале
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"

def generate_password(length=16, use_digits=True, use_special=True):
    # Базовый набор символов (строчные и прописные английские буквы)
    letters = string.ascii_letters
    digits = string.digits if use_digits else ""
    special = "!@#$%^&*()-_=+[{]};:,.<>?" if use_special else ""
    
    all_chars = letters + digits + special
    
    if not all_chars:
        return "Ошибка: нет символов для генерации!"
    
    # Секретная генерация (secrets надежнее, чем модуль random)
    password = "".join(secrets.choice(all_chars) for _ in range(length))
    return password

print(f"{CYAN}=== ГЕНЕРАТОР НАДЁЖНЫХ ПАРОЛЕЙ ==={RESET}\n")

try:
    # Запрашиваем длину пароля
    length_input = input(f"{YELLOW}Введите длину пароля (по умолчанию 16): {RESET}")
    length = int(length_input) if length_input.strip().isdigit() else 16
    
    # Генерируем пароль
    password = generate_password(length)
    
    # Выводим результат
    print(f"\n{GREEN}[+] Сгенерированный пароль:{RESET}")
    print(f"{GREEN}-----------------------------------{RESET}")
    print(password)
    print(f"{GREEN}-----------------------------------{RESET}")
    print(f"{CYAN}Скопируйте его и сохраните в надёжном месте.{RESET}")

except KeyboardInterrupt:
    print(f"\n{RESET}Выход...")
```

---

## 📄 sysinfo.py

*14361 байт · 369 строк*

```python
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
```

---

## 📄 utils.py

*14925 байт · 337 строк*

```python
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
```

---

## 📄 art.py

*8497 байт · 235 строк*

```python
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
```

---
