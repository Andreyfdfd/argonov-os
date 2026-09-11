#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI v16 — Qwen 3B + exec/write/read + автосохранение сессий"""

import os, sys, json, subprocess, time, re, signal, atexit, socket, threading
import urllib.request, urllib.error
import pty
from datetime import datetime
from pathlib import Path
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

# ═══════════ СЕССИИ ═══════════
CHATS_DIR = os.path.join(HOME, "ai_chats")
SESSION_VERSION = 1

def get_chats_dir():
    os.makedirs(CHATS_DIR, exist_ok=True)
    return CHATS_DIR

def new_session_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def session_path(session_id):
    return os.path.join(get_chats_dir(), f"{session_id}.json")

def list_sessions():
    """Возвращает список (session_id, started, model, msgs) — новые сверху."""
    d = get_chats_dir()
    items = []
    for f in os.listdir(d):
        if not f.endswith(".json"): continue
        p = os.path.join(d, f)
        try:
            with open(p, encoding="utf-8") as fp:
                obj = json.load(fp)
            items.append({
                "session_id": obj.get("session_id", f[:-5]),
                "started": obj.get("started", "?"),
                "ended": obj.get("ended"),
                "model": obj.get("model", {}).get("name", "?"),
                "messages": len(obj.get("messages", [])),
                "duration": obj.get("duration_sec", 0),
                "path": p,
                "mtime": os.path.getmtime(p),
            })
        except Exception:
            continue
    items.sort(key=lambda x: x["mtime"], reverse=True)
    return items

def last_session_path():
    items = list_sessions()
    return items[0]["path"] if items else None

def session_save(state, ended=False):
    """Сохраняет текущую сессию. Тихая — не падает при ошибке."""
    sid = state.get("session_id")
    if not sid: return False
    try:
        # Собираем объект сессии
        started = state.get("session_started_at")
        dur = int(time.time() - started) if started else 0

        obj = {
            "version": SESSION_VERSION,
            "session_id": sid,
            "started": state.get("session_started_str", "?"),
            "ended": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if ended else None,
            "duration_sec": dur,
            "model": {
                "path": state.get("model_path", "?"),
                "name": os.path.basename(state.get("model_path") or "?"),
            },
            "device": {
                "model": state.get("ctx", {}).get("model", "?"),
                "android": state.get("ctx", {}).get("android", "?"),
                "python": state.get("ctx", {}).get("python", "?"),
            },
            "config": {
                "temperature": state.get("temp", 0.4),
                "max_tokens": state.get("max_tokens", 1024),
                "ctx_size": state.get("ctx_size", 2048),
                "threads": state.get("threads", 4),
                "agent": state.get("agent", True),
                "auto_exec": state.get("auto_exec", False),
                "sandbox": state.get("sandbox", True),
                "thinking": state.get("thinking", False),
            },
            "messages": state.get("history", []),
            "files_read": list(state.get("files_read", [])),
            "files_written": list(state.get("files_written", [])),
            "commands_executed": list(state.get("commands_executed", [])),
            "stats": dict(state.get("stats", {})),
        }
        p = session_path(sid)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
        os.replace(tmp, p)
        return True
    except Exception:
        return False

def session_load(path):
    """Загружает сессию. Возвращает dict или None."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# ═══════════ КОНТЕКСТ ═══════════
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
    # ── новые поля сессий ──
    "session_id": None,
    "session_started_at": None,
    "session_started_str": None,
    "files_read": [],
    "files_written": [],
    "commands_executed": [],
    "stats": {
        "user_messages": 0,
        "assistant_messages": 0,
        "commands": 0,
        "writes": 0,
        "reads": 0,
        "errors": 0,
        "ttft_sum": 0.0,
        "ttft_count": 0,
        "total_sum": 0.0,
        "total_count": 0,
    },
    "loaded_from": None,  # если -c, ID загруженной сессии
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
    return tb, ab, (ft["t"] - st) if ft["t"] else None

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
        STATE["stats"]["errors"] += 1
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
        STATE["commands_executed"].append(cmd)
        STATE["stats"]["commands"] += 1
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
        STATE["commands_executed"].append(cmd)
        STATE["stats"]["commands"] += 1
        return result
    except subprocess.TimeoutExpired:
        console.print("[red]✘ Таймаут[/]\n")
        try: p.kill()
        except: pass
        STATE["stats"]["errors"] += 1
        return None
    except Exception as e:
        console.print(f"[red]✘ {e}[/]\n")
        STATE["stats"]["errors"] += 1
        return None

def do_write(path, content, auto=False):
    path = os.path.expanduser(path.strip())
    console.print()
    if DANGER.search(content):
        console.print(f"[bold red]🛑 Заблокировано[/]")
        STATE["stats"]["errors"] += 1
        return False
    if not is_safe_path(path):
        console.print(f"[bold red]🛑 Вне sandbox:[/] {path}")
        STATE["stats"]["errors"] += 1
        return False
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
        console.print(f"[green]✔ Записано[/]\n")
        STATE["files_written"].append(path)
        STATE["stats"]["writes"] += 1
        return True
    except Exception as e:
        console.print(f"[red]✘ {e}[/]\n")
        STATE["stats"]["errors"] += 1
        return False

def do_read(path):
    path = os.path.expanduser(path.strip())
    console.print()
    if not is_safe_path(path):
        console.print(f"[bold red]🛑 Вне sandbox:[/] {path}")
        STATE["stats"]["errors"] += 1
        return None
    if not os.path.exists(path):
        console.print(f"[red]❌ Не найден: {path}[/]\n")
        STATE["stats"]["errors"] += 1
        return None
    if os.path.isdir(path):
        try:
            files = os.listdir(path)
            console.print(f"[yellow]📁 {path}:[/]")
            for f in files[:30]: console.print(f"  [cyan]•[/] {f}")
            console.print()
            STATE["files_read"].append(path)
            STATE["stats"]["reads"] += 1
            return "\n".join(files)
        except:
            STATE["stats"]["errors"] += 1
            return None
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if len(content) > 8000:
            console.print(f"[yellow]📄 {path} (первые 8000 из {len(content)})[/]\n")
            content = content[:8000] + f"\n[... обрезано]"
        else:
            console.print(f"[yellow]📄 {path} ({len(content)} симв)[/]\n")
        STATE["session_files"].append(path)
        STATE["files_read"].append(path)
        STATE["stats"]["reads"] += 1
        return content
    except Exception as e:
        console.print(f"[red]✘ {e}[/]\n")
        STATE["stats"]["errors"] += 1
        return None

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
    "сессия","session","история","history",
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
    t.append(" ░▒▓ AI v16", style="bold green")
    t.append(f"\n  ", style="dim"); t.append(mode, style="bold bright_cyan")
    t.append(f"  ·  ", style="dim"); t.append(agent, style="bright_green" if STATE["agent"] else "dim")
    t.append(f"  ·  ", style="dim"); t.append(auto_exec, style="bright_red" if STATE["auto_exec"] else "bright_yellow")
    t.append(f"  ·  ", style="dim"); t.append(sandbox, style="bright_cyan")

    sid = STATE.get("session_id") or "?"
    loaded = STATE.get("loaded_from")
    if loaded:
        t.append(f"\n  📂 продолжение сессии: {sid}", style="bright_magenta")
    else:
        t.append(f"\n  📂 сессия: {sid}", style="dim")

    t.append(f"  ·  📝 {len(STATE['history'])}  ·  📄 {len(STATE['session_files'])}  ·  ОЗУ {free_ram()} МБ", style="dim")
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

# ═══════════ ЗАГРУЗКА СЕССИИ ═══════════
def load_session_by_id(session_id=None):
    """Загружает сессию в STATE. Возвращает True/False."""
    if session_id:
        p = session_path(session_id)
    else:
        p = last_session_path()
    if not p or not os.path.isfile(p):
        console.print(f"[red]❌ Сессия не найдена: {session_id or 'последняя'}[/]")
        return False
    obj = session_load(p)
    if not obj:
        console.print(f"[red]❌ Ошибка чтения сессии[/]")
        return False

    # Восстанавливаем историю и метаданные
    STATE["history"] = obj.get("messages", [])
    STATE["files_read"] = list(obj.get("files_read", []))
    STATE["files_written"] = list(obj.get("files_written", []))
    STATE["commands_executed"] = list(obj.get("commands_executed", []))
    st = obj.get("stats", {})
    # Восстанавливаем stats аккуратно
    for k, v in st.items():
        if k in STATE["stats"]: STATE["stats"][k] = v

    STATE["loaded_from"] = obj.get("session_id")
    # Новая сессия, но с привязкой к загруженной
    STATE["session_id"] = new_session_id()
    STATE["session_started_at"] = time.time()
    STATE["session_started_str"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    console.print(f"[green]✔ Загружена сессия: {obj.get('session_id')}[/]")
    console.print(f"[dim]   сообщений: {len(STATE['history'])}  ·  модель: {obj.get('model',{}).get('name','?')}[/]")
    console.print(f"[dim]   начата: {obj.get('started','?')}[/]")
    time.sleep(1)
    return True

def print_sessions_list():
    items = list_sessions()
    if not items:
        console.print("[yellow]⚠ Сессий нет[/]"); return
    console.print()
    t = Table(box=SIMPLE_HEAD, border_style="black", padding=(0,1))
    t.add_column("#", style="bold yellow", width=4, justify="right")
    t.add_column("ID", style="cyan")
    t.add_column("Начата", style="dim")
    t.add_column("Модель", style="green")
    t.add_column("Сообщ.", style="yellow", justify="right")
    t.add_column("Время", style="magenta", justify="right")
    for i, s in enumerate(items, 1):
        dur = f"{s['duration']//60}м" if s['duration'] else "?"
        t.add_row(str(i), s["session_id"], s["started"][:16],
                  s["model"].replace(".gguf","")[:18],
                  str(s["messages"]), dur)
    console.print(t)
    console.print()

# ═══════════ MAIN ═══════════
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

    # ═══ Сессия ═══
    STATE["session_id"] = new_session_id()
    STATE["session_started_at"] = time.time()
    STATE["session_started_str"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_save(STATE)

    os.system("clear"); console.print()
    console.print(title_block()); console.print()
    console.print("[bold green]Готов.[/] Попробуй: 'запусти матрицу', 'открой музыку'\n")
    console.print("[dim]Команды: /last  /list  /session  /save  ·  'статистика'[/]\n")

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

        # ─── выход ───
        if lo in ("выход","q","quit","exit"):
            session_save(STATE, ended=True)
            console.print(f"[dim]💾 Сессия сохранена: {STATE['session_id']}[/]")
            break

        # ─── команды режимов ───
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

        # ─── /last /list /session /save ───
        if lo in ("/last", "/continue", "/продолжить"):
            if load_session_by_id(None):
                os.system("clear"); console.print(); console.print(title_block()); console.print()
            continue
        if lo == "/list":
            print_sessions_list()
            continue
        if lo == "/session":
            console.print()
            console.print(f"[cyan]ID:[/] {STATE['session_id']}")
            console.print(f"[cyan]Начата:[/] {STATE['session_started_str']}")
            console.print(f"[cyan]Модель:[/] {os.path.basename(STATE['model_path'])}")
            console.print(f"[cyan]Сообщений:[/] {len(STATE['history'])}")
            console.print(f"[cyan]Файл:[/] {session_path(STATE['session_id'])}")
            if STATE.get("loaded_from"):
                console.print(f"[magenta]Продолжение:[/] {STATE['loaded_from']}")
            console.print(); continue
        if lo == "/save":
            if session_save(STATE):
                console.print(f"[green]✔ Сохранено: {STATE['session_id']}[/]\n")
            else:
                console.print("[red]❌ Ошибка[/]\n")
            continue

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
            s = STATE["stats"]
            avg_ttft = (s["ttft_sum"]/s["ttft_count"]) if s["ttft_count"] else 0
            avg_total = (s["total_sum"]/s["total_count"]) if s["total_count"] else 0
            console.print()
            t = Table(box=SIMPLE_HEAD, border_style="black", padding=(0,2))
            t.add_column("", style="bold yellow", width=22)
            t.add_column("", style="cyan", justify="right", width=10)
            t.add_row("💬 Сообщений (user)", str(s["user_messages"]))
            t.add_row("🤖 Ответов (AI)", str(s["assistant_messages"]))
            t.add_row("⚡ Команд", str(s["commands"]))
            t.add_row("📝 Write", str(s["writes"]))
            t.add_row("📄 Read", str(s["reads"]))
            t.add_row("❌ Ошибок", str(s["errors"]))
            t.add_row("⏱ Avg TTFT", f"{avg_ttft:.1f}с")
            t.add_row("⏱ Avg total", f"{avg_total:.1f}с")
            console.print(t); console.print()
            if STATE.get("session_started_at"):
                dur = int(time.time() - STATE["session_started_at"])
                console.print(f"[dim]Длительность сессии: {dur//60}м {dur%60}с[/]\n")
            continue
        if lo in ("помощь","help","?"):
            console.print()
            console.print("[bold]Режимы:[/] авто · быстро · думать · команды · sudo · sandbox")
            console.print("[bold]Инфо:[/] env · модель · статистика · /session")
            console.print("[bold]Сессии:[/] /last · /list · /save")
            console.print("[bold]Возможности:[/] exec · write · read")
            console.print("[bold]Выход:[/] q / выход")
            console.print(); continue

        # ─── AI-запрос ───
        STATE["history"].append({"role":"user","content":ui})
        STATE["stats"]["user_messages"] += 1
        session_save(STATE)  # сохраняем сразу после user-сообщения
        console.print()
        t0 = time.time()
        try: tb, ab, ttft = process(stream(ui))
        except KeyboardInterrupt:
            console.print("\n[yellow]⏹[/]\n")
            STATE["history"].pop()
            STATE["stats"]["user_messages"] -= 1
            continue
        el = time.time() - t0
        if ab.startswith("__ERROR__"):
            console.print(f"[red]❌ {ab[10:]}[/]\n")
            STATE["history"].pop()
            STATE["stats"]["user_messages"] -= 1
            STATE["stats"]["errors"] += 1
            continue
        STATE["history"].append({"role":"assistant","content":ab})
        STATE["stats"]["assistant_messages"] += 1
        if ttft: STATE["stats"]["ttft_sum"] += ttft; STATE["stats"]["ttft_count"] += 1
        STATE["stats"]["total_sum"] += el; STATE["stats"]["total_count"] += 1

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
                try: tb2, ab2, ttft2 = process(stream(follow[:4000]))
                except KeyboardInterrupt: ab2 = None; ttft2 = None
                if ab2 and not ab2.startswith("__ERROR__"):
                    STATE["history"].append({"role":"assistant","content":ab2})
                    STATE["stats"]["assistant_messages"] += 1
                    if ttft2: STATE["stats"]["ttft_sum"] += ttft2; STATE["stats"]["ttft_count"] += 1
                    el2 = time.time() - t1
                    STATE["stats"]["total_sum"] += el2; STATE["stats"]["total_count"] += 1
                    console.print()
                    if tb2: console.print(f"[dim italic yellow]💭 {tb2[:300]}[/]\n")
                    try: console.print(Markdown(ab2))
                    except: console.print(ab2)
                    console.print(f"\n[dim]⏱ {el2:.1f}с[/]\n")

        # ─── Автосохранение после пары ───
        session_save(STATE)

    reset_terminal()
    stop_server()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано[/]")
        session_save(STATE, ended=True)
        reset_terminal()
        stop_server()
