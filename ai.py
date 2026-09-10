#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI Assistant v12 — короткий промпт, быстрый TTFT"""

import os, sys, json, subprocess, time, re, signal, atexit, socket, threading
import urllib.request, urllib.error
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

STATE = {"model_path": None, "thinking": False, "auto": True, "agent": True,
         "temp": 0.4, "max_tokens": 512, "ctx_size": 512, "threads": 4,
         "sys_prompt": "", "use_env": False, "env_text": "",
         "history": [], "proc": None, "ctx": {}}

def run(cmd, t=20):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=t)
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
    ctx = {"python":"?","android":"?","model":"?","pip":[],"pkg":[],"scripts":[],"models":[]}
    r = run("python --version")
    if r and r.stdout: ctx["python"] = r.stdout.strip().replace("Python ","")
    r = run("getprop ro.product.model")
    if r and r.stdout: ctx["model"] = r.stdout.strip()
    r = run("getprop ro.build.version.release")
    if r and r.stdout: ctx["android"] = r.stdout.strip()
    top_pip = ["rich","requests","httpx","fastapi","uvicorn","pydantic","aiogram",
               "sqlalchemy","aiohttp","beautifulsoup4","redis","psutil","flet",
               "cryptography","pyfiglet","loguru","lxml","prompt-toolkit"]
    r = run("pip list --format=freeze 2>/dev/null")
    if r and r.stdout:
        allp = {re.sub(r"[-_.]+","-",l.split("==",1)[0]).lower() for l in r.stdout.strip().split("\n") if "==" in l}
        ctx["pip"] = [p for p in top_pip if p in allp]
    top_pkg = ["python","git","neovim","tmux","clang","rust","cargo","nodejs",
               "fish","chafa","ffmpeg","curl","wget","ripgrep","fd","llama-cpp"]
    r = run("pkg list-installed 2>/dev/null")
    if r and r.stdout:
        allpk = set()
        for ln in r.stdout.strip().split("\n"):
            if ln.strip() and not ln.startswith("Listing"):
                parts = ln.split()
                if parts: allpk.add(parts[0].split("/")[0].lower())
        ctx["pkg"] = [p for p in top_pkg if p in allpk]
    try:
        ctx["scripts"] = [f for f in sorted(os.listdir(HOME))
                          if os.path.isfile(os.path.join(HOME, f))
                          and f.endswith((".py",".sh",".fish"))][:30]
    except: pass
    for d in [HOME, os.path.join(HOME, "models")]:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".gguf"):
                    try: sz = os.path.getsize(os.path.join(d, f))
                    except: sz = 0
                    if sz > 100_000_000: ctx["models"].append(f"{f} ({hsize(sz)})")
    return ctx

def build_short_prompt():
    """~50 токенов — минимум для понимания задачи"""
    return (
        "Ты AI в Termux (Android). Русский, кратко.\n"
        "Для действий возвращай exec-блок:\n"
        "```exec\n"
        "команда\n"
        "```\n"
        "Скрипты: todo(задачи) notes(заметки) music(музыка) "
        "pm(пароли) crypto(крипта) hack(тул) d(загрузка) "
        "matrix sysinfo art.\n"
        "Пример: 'покажи задачи' → ```exec\npython ~/todo.py\n```"
    )

def build_env_block(ctx):
    return (
        f"Окружение: Python {ctx['python']}, Android {ctx['android']}, {ctx['model']}\n"
        f"pip: {', '.join(ctx['pip'])}\n"
        f"pkg: {', '.join(ctx['pkg'])}\n"
        f"Скрипты ~/: {', '.join(ctx['scripts'])}\n"
        f"Модели: {', '.join(ctx['models'])}"
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
        console.print(Panel("[red]❌ Нет моделей[/]", border_style="red")); return None
    last = cfg.get("last_model")
    if last:
        for fp, sz in models:
            if fp == last:
                console.print(f"[green]✔ Модель: {os.path.basename(fp)}[/]")
                time.sleep(0.3); return fp
    for fp, sz in models:
        if "qwen" in os.path.basename(fp).lower():
            console.print(f"[green]✔ Модель по умолчанию: {os.path.basename(fp)}[/]")
            return fp
    return models[0][0]

def start_server(mp):
    if check_port(): return True
    console.print(f"[yellow]⚠ ОЗУ: {free_ram()} МБ[/]")
    cmd = ["llama-server", "-m", mp,
           "--host", HOST, "--port", str(PORT),
           "-c", str(STATE["ctx_size"]),
           "-t", str(STATE["threads"]),
           "--no-warmup"]
    console.print(f"[dim]Команда: {' '.join(cmd)}[/]")
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
    sys_p = STATE["sys_prompt"]
    if STATE["use_env"]:
        sys_p += "\n\n" + STATE["env_text"]
    msgs = [{"role":"system","content":sys_p}]
    msgs.extend(STATE["history"][-2:])
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

DANGER = re.compile(r"rm\s+-rf\s+/[^sd]|mkfs|dd\s+if=|shutdown|reboot|halt|poweroff|fdisk|parted|>\s*/dev/sd", re.I)
EXEC = re.compile(r"```exec\s*\n(.*?)\n```", re.DOTALL)

def process(gen):
    tb, ab = "", ""; it = False; st = time.time(); ft = {"t":None}
    def render():
        el = int(time.time() - st); parts = []
        status = f"⏱ {el}с · ⏳ обработка..." if ft["t"] is None else f"⏱ {el}с · TTFT {ft['t']-st:.1f}с"
        parts.append(Text(status, style="bold yellow"))
        if it or tb:
            tail = tb[-500:] if len(tb) > 500 else tb
            parts.append(Panel(Text(tail or "...", style="dim italic yellow"),
                title="[bold yellow]💭 РАЗМЫШЛЕНИЯ[/]", border_style="yellow", padding=(0,1)))
        if ab:
            try: parts.append(Panel(Markdown(ab), title="[bold green]🧠 ОТВЕТ[/]",
                border_style="green", padding=(0,1)))
            except: parts.append(Panel(Text(ab), title="[bold green]🧠 ОТВЕТ[/]",
                border_style="green", padding=(0,1)))
        elif not it:
            parts.append(Panel(Text("...", style="dim"), title="[bold green]🧠 ОТВЕТ[/]",
                border_style="green", padding=(0,1)))
        return Group(*parts)
    with Live(render(), console=console, refresh_per_second=10) as live:
        live.update(render())
        for p in gen:
            if ft["t"] is None: ft["t"] = time.time()
            if "<think>" in p and not it:
                sp = p.split("<think>",1); ab += sp[0]; tb += sp[1]; it = True
            elif "</think>" in p and it:
                sp = p.split("</think>",1); tb += sp[0]; ab += sp[1]; it = False
            else:
                if it: tb += p
                else: ab += p
            live.update(render())
    tb = tb.replace("<think>","").replace("</think>","").strip()
    ab = ab.replace("<think>","").replace("</think>","").strip()
    if not ab and tb: ab = tb; tb = ""
    return tb, ab

def execute(cmd):
    console.print()
    if DANGER.search(cmd):
        console.print(Panel(f"[red]⚠ ОПАСНАЯ[/]\n[white]{cmd}[/]",
            title="[bold red]🛑[/]", border_style="red")); return False
    console.print(Panel(f"[bold cyan]{cmd}[/]", title="[bold yellow]⚡ КОМАНДА[/]", border_style="yellow"))
    try:
        a = console.input("[bold magenta]Выполнить? (y/N)> [/]").strip().lower()
    except: return False
    if a != "y": console.print("[dim]Отменено[/]\n"); return False
    console.print(f"[dim]$ {cmd}[/]\n")
    try:
        p = subprocess.Popen(cmd, shell=True)
        p.wait(timeout=600)
        console.print(f"[green]✔ Готово[/]\n" if p.returncode == 0 else f"[red]✘ Код {p.returncode}[/]\n")
    except subprocess.TimeoutExpired:
        console.print("[red]✘ Таймаут[/]\n")
        try: p.kill()
        except: pass
    except Exception as e: console.print(f"[red]✘ {e}[/]\n")
    return True

COMMANDS = ["думать","think","быстро","fast","авто","auto","команды","agent",
            "контекст","context","env","модель","model","очистить","clear",
            "статистика","stats","помощь","help","выход","q"]

class Comp(Completer):
    def get_completions(self, doc, ev):
        t = doc.text_before_cursor
        if " " in t: return
        for c in sorted(COMMANDS):
            if c.startswith(t.lower()): yield Completion(c, start_position=-len(t))

def title_block():
    mode = "🤖 АВТО" if STATE["auto"] else ("💭 ВСЕГДА" if STATE["thinking"] else "⚡ БЫСТРО")
    agent = "⚡ АГЕНТ" if STATE["agent"] else "— выкл"
    env = "📎 вкл" if STATE["use_env"] else "— выкл"
    mn = os.path.basename(STATE['model_path'] or '?').replace('.gguf','')
    t = Text()
    t.append("▓▒░ ", style="bold bright_green")
    t.append(mn.upper(), style="bold bright_green")
    t.append(" ░▒▓ AI", style="bold green")
    t.append(f"\n  Режим: ", style="bold yellow"); t.append(mode, style="bold bright_cyan")
    t.append(f"  ·  🛠 ", style="bold yellow"); t.append(agent, style="bright_green" if STATE["agent"] else "dim")
    t.append(f"  ·  📎 ", style="bold yellow"); t.append(env, style="bright_cyan" if STATE["use_env"] else "dim")
    t.append(f"\n  📝 {len(STATE['history'])} сообщ.  ·  ОЗУ: {free_ram()} МБ  ·  ctx: {STATE['ctx_size']}  ·  threads: {STATE['threads']}", style="dim")
    return Panel(t, border_style="green", padding=(0,1))

def switch_model(cfg):
    models = find_models()
    if not models: return False
    console.print()
    t = Table(box=SIMPLE_HEAD, border_style="cyan", padding=(0,2))
    t.add_column("#", style="bold yellow", width=4, justify="right")
    t.add_column("Модель"); t.add_column("Размер", style="cyan", justify="right", width=10)
    for i, (fp, sz) in enumerate(models, 1):
        m = "✔" if fp == STATE["model_path"] else ""
        t.add_row(str(i), os.path.basename(fp), hsize(sz), m)
    console.print(t); console.print()
    try:
        ch = console.input("[bold magenta]Какую? (Enter — отмена)> [/]").strip()
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
        console.print(f"[green]✔ Загружена за {w:.1f}с[/]\n"); return True
    except: return False

def main():
    console.clear()
    cfg = load_cfg()
    STATE["model_path"] = ask_model(cfg)
    if not STATE["model_path"]: return
    cfg["last_model"] = STATE["model_path"]; save_cfg(cfg)

    console.print("[yellow]⚙ Собираю контекст...[/]")
    STATE["ctx"] = collect()
    STATE["sys_prompt"] = build_short_prompt()
    STATE["env_text"] = build_env_block(STATE["ctx"])
    # Оценка размера промпта
    prompt_tokens = len(STATE["sys_prompt"]) // 3
    console.print(f"[green]✔ pip={len(STATE['ctx']['pip'])} pkg={len(STATE['ctx']['pkg'])} скриптов={len(STATE['ctx']['scripts'])}[/]")
    console.print(f"[dim]Промпт: ~{prompt_tokens} токенов (было ~250)[/]")

    if not start_server(STATE["model_path"]): return
    console.print("[yellow]⏳ Загружаю модель...[/]")
    t0 = time.time()
    def rw():
        el = int(time.time() - t0)
        return Panel(Group(Text(f"⏱ {el} сек", style="bold yellow"),
                            Text("Загрузка в ОЗУ", style="dim")),
            title="[bold yellow]⏳ ЗАГРУЗКА[/]", border_style="yellow", padding=(0,1))
    with Live(rw(), console=console, refresh_per_second=2) as live:
        res = {"w": None}
        def w(): res["w"] = warmup()
        th = threading.Thread(target=w, daemon=True); th.start()
        while th.is_alive(): live.update(rw()); time.sleep(0.5)
        th.join()
    if res["w"] is None:
        console.print("[red]❌ Прогрев не удался[/]"); return
    console.print(f"[green]✔ Модель в ОЗУ за {res['w']:.1f} сек[/]")
    time.sleep(0.5)

    console.clear(); console.print()
    console.print(title_block()); console.print()
    console.print("[bold green]Готов.[/] Tab — команды.\n")

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
            console.print(f"[green]⚡ Команды: {'вкл' if STATE['agent'] else 'выкл'}[/]\n"); continue
        if lo in ("контекст","context"):
            STATE["use_env"] = not STATE["use_env"]
            console.print(f"[green]📎 Env: {'вкл (медленнее)' if STATE['use_env'] else 'выкл (быстро)'}[/]\n")
            continue
        if lo == "env":
            c = STATE["ctx"]; console.print()
            console.print(f"[cyan]Python:[/] {c['python']}")
            console.print(f"[cyan]pip:[/]  " + ", ".join(c["pip"]))
            console.print(f"[cyan]pkg:[/]  " + ", ".join(c["pkg"]))
            console.print(f"[cyan]Скрипты:[/] " + ", ".join(c["scripts"]))
            console.print(f"[cyan]Модели:[/] " + ", ".join(c["models"])); console.print(); continue
        if lo in ("модель","model"):
            if switch_model(cfg):
                console.clear(); console.print(); console.print(title_block()); console.print()
                console.print("[green]✔[/]\n")
            continue
        if lo in ("очистить","clear"):
            STATE["history"]=[]
            console.clear(); console.print(); console.print(title_block()); console.print()
            console.print("[green]✔[/]\n"); continue
        if lo in ("статистика","stats"):
            console.print(Panel.fit(
                f"Модель: {os.path.basename(STATE['model_path'])}\n"
                f"Сообщений: {len(STATE['history'])}\nОЗУ: {free_ram()} МБ\n"
                f"ctx: {STATE['ctx_size']}  ·  threads: {STATE['threads']}\n"
                f"Промпт: ~{len(STATE['sys_prompt'])//3} токенов",
                border_style="cyan"))
            console.print(); continue
        if lo in ("помощь","help","?"):
            console.print("  авто/быстро/думать · команды · контекст · модель · env · очистить · выход\n"); continue
        if lo.startswith("токены ") or lo.startswith("tokens "):
            try: STATE["max_tokens"] = max(128, min(2048, int(ui.split(" ",1)[1])))
            except: pass
            continue

        STATE["history"].append({"role":"user","content":ui})
        console.print()
        t0 = time.time()
        try: tb, ab = process(stream(ui))
        except KeyboardInterrupt: console.print("\n[yellow]⏹[/]\n"); STATE["history"].pop(); continue
        el = time.time() - t0
        if ab.startswith("__ERROR__"):
            console.print(f"[red]❌ {ab[10:]}[/]\n"); STATE["history"].pop(); continue
        STATE["history"].append({"role":"assistant","content":ab})
        console.print(f"\n  [dim]⏱ {el:.1f}с[/]\n")

        cmds = [m.strip() for m in EXEC.findall(ab) if m.strip()]
        if cmds and STATE["agent"]:
            for cmd in cmds: execute(cmd)

    stop_server()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано[/]"); stop_server()
