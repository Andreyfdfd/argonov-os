#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HackTool v3 — с Tab-автодополнением через prompt_toolkit"""

import os, sys, time, random, subprocess, socket, secrets, string, json, re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

console = Console()

# ═══════════ БАННЕР ═══════════
def banner():
    console.clear()
    art = r"""
    ██╗  ██╗ █████╗  ██████╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗
    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝╚══██╔══╝██╔═══██╗██╔═══██╗██║
    ███████║███████║██║     █████╔╝    ██║   ██║   ██║██║   ██║██║
    ██╔══██║██╔══██║██║     ██╔═██╗    ██║   ██║   ██║██║   ██║██║
    ██║  ██║██║  ██║╚██████╗██║  ██╗   ██║   ╚██████╔╝╚██████╔╝███████╗
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    console.print(Align.center(f"[bold green]{art}[/]"))
    console.print(Align.center("[bold cyan]⚡ Терминальный мультитул v3 ⚡[/]"))
    console.print(Align.center(f"[dim]{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}[/]"))
    console.print()

def menu():
    t = Table(box=box.DOUBLE_EDGE, border_style="green", show_header=False, padding=(0, 2))
    t.add_column("Команда", style="bold yellow", width=24, justify="center")
    t.add_column("Описание", style="white")
    t.add_row("[cyan]scan <домен>[/]",       "🌐 WHOIS + DNS + IP о домене")
    t.add_row("[cyan]crt <домен>[/]",        "🕵️  Certificate Transparency — поддомены")
    t.add_row("[cyan]crypto[/]",             "💰 Курс BTC/ETH")
    t.add_row("[cyan]news[/]",               "📰 IT-новости (RU)")
    t.add_row("[cyan]qr <текст>[/]",         "📱 QR-код в терминал")
    t.add_row("[cyan]pass <длина>[/]",       "🔐 Криптостойкий пароль")
    t.add_row("[cyan]pass-audit <пароль>[/]", "🔍 Анализ надёжности")
    t.add_row("[cyan]hash <текст>[/]",       "🧮 MD5 / SHA1 / SHA256")
    t.add_row("[cyan]b64 enc|dec <текст>[/]", "🔡 Base64")
    t.add_row("[cyan]ip[/]",                 "📍 Внешний IP + геолокация")
    t.add_row("[cyan]ping <хост>[/]",        "🏓 Пинг")
    t.add_row("[cyan]ports <хост>[/]",       "⚙️  Скан портов")
    t.add_row("[cyan]headers <url>[/]",      "📋 HTTP-заголовки")
    t.add_row("[cyan]robots <url>[/]",       "🤖 robots.txt")
    t.add_row("[cyan]trace <хост>[/]",       "🛰 Traceroute")
    t.add_row("[cyan]speed[/]",              "⚡ Скорость интернета")
    t.add_row("[cyan]weather <город>[/]",    "☀️  Погода")
    t.add_row("[cyan]matrix[/]",             "🌧 5 сек матрицы")
    t.add_row("[cyan]sysinfo[/]",            "💻 Центр управления")
    t.add_row("[cyan]clear[/]",              "🧹 Очистить")
    t.add_row("[cyan]exit[/]",               "🚪 Выход")
    console.print(Panel(t, title="[bold green]🎮 Команды (Tab — автодополнение)[/]", border_style="green"))
    console.print()

# ═══════════ КОМАНДЫ ═══════════
def run(cmd, timeout=15):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except Exception:
        return None

def cmd_scan(domain):
    if not domain: console.print("[red]❌ scan <домен>[/]"); return
    domain = domain.replace("http://","").replace("https://","").split("/")[0]
    console.print(f"\n[bold yellow]🔍 {domain}[/]\n")
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"  [green]✔[/] IP: [cyan]{ip}[/]")
    except Exception: console.print("  [red]✘[/] IP не разрешён")
    try:
        import dns.resolver
        for rt in ["A","MX","NS","TXT"]:
            try:
                ans = dns.resolver.resolve(domain, rt, lifetime=5)
                vals = [str(a) for a in ans][:3]
                console.print(f"  [green]✔[/] DNS {rt}: [cyan]{', '.join(vals)}[/]")
            except Exception: pass
    except ImportError: pass
    try:
        import whois
        w = whois.whois(domain)
        for k in ("registrar","creation_date","expiration_date"):
            v = w.get(k)
            if isinstance(v, list): v = v[0]
            if v: console.print(f"  [green]✔[/] {k}: [cyan]{v}[/]")
    except Exception: pass
    console.print()

def cmd_crt(domain):
    if not domain: console.print("[red]❌ crt <домен>[/]"); return
    domain = domain.replace("http://","").replace("https://","").split("/")[0]
    console.print(f"\n[bold yellow]🕵️  crt.sh: {domain}[/]\n")
    try:
        import requests
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=20)
        data = r.json()
        names = set()
        for item in data:
            for n in item.get("name_value","").split("\n"):
                n = n.strip().lstrip("*.").lower()
                if n.endswith(domain): names.add(n)
        console.print(f"[green]✔ Поддоменов: {len(names)}[/]\n")
        for i, n in enumerate(sorted(names)[:40], 1):
            console.print(f"  [cyan]{i:3}.[/] {n}")
        console.print()
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

def cmd_crypto():
    console.print("\n[bold yellow]💰 Крипта...[/]\n")
    try:
        import requests
        r = requests.get("https://api.coingecko.com/api/v3/simple/price",
            params={"ids":"bitcoin,ethereum,solana","vs_currencies":"usd,rub","include_24hr_change":"true"},
            timeout=10)
        d = r.json()
        t = Table(box=box.ROUNDED, border_style="yellow")
        t.add_column("Монета", style="bold cyan")
        t.add_column("USD", style="green", justify="right")
        t.add_column("RUB", style="green", justify="right")
        t.add_column("24ч", justify="right")
        names = {"bitcoin":"BTC","ethereum":"ETH","solana":"SOL"}
        for cid, label in names.items():
            if cid in d:
                x = d[cid]; ch = x.get("usd_24h_change",0)
                col = "[green]" if ch>=0 else "[red]"
                t.add_row(label, f"${x['usd']:,.0f}", f"{x['rub']:,.0f}₽", f"{col}{ch:+.2f}%[/]")
        console.print(t); console.print()
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_news():
    console.print("\n[bold yellow]📰 IT-новости...[/]\n")
    feeds = [
        ("Хабр", "https://habr.com/ru/rss/all/all/"),
        ("N+1",  "https://nplus1.ru/rss"),
        ("3DNews","https://3dnews.ru/news/rss/"),
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
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_qr(text):
    if not text: console.print("[red]❌ qr <текст>[/]"); return
    try:
        import qrcode
        q = qrcode.QRCode(border=1); q.add_data(text); q.make(fit=True)
        q.print_ascii(invert=True); console.print()
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_pass(length_str):
    try:
        length = int(length_str) if length_str else 20
        if not 4 <= length <= 128: raise ValueError
    except ValueError: console.print("[red]❌ Длина 4-128[/]"); return
    ab = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"
    pwd = "".join(secrets.choice(ab) for _ in range(length))
    console.print()
    console.print(Panel(f"[bold green]{pwd}[/]", title=f"🔐 {length}", border_style="green"))
    try:
        import pyperclip; pyperclip.copy(pwd)
        console.print("[dim]✔ Скопировано[/]")
    except Exception: pass
    console.print()

def cmd_pass_audit(pwd):
    if not pwd: console.print("[red]❌ pass-audit <пароль>[/]"); return
    import math
    lo = any(c.islower() for c in pwd); up = any(c.isupper() for c in pwd)
    di = any(c.isdigit() for c in pwd); sy = any(c in string.punctuation for c in pwd)
    common = {"123456","password","qwerty","admin","пароль"}
    is_c = pwd.lower() in common
    pool = (26 if lo else 0)+(26 if up else 0)+(10 if di else 0)+(32 if sy else 0)
    ent = math.log2(pool)*len(pwd) if pool else 0
    if is_c: lbl, col = "КАТАСТРОФА", "red"
    elif ent < 30: lbl, col = "Слабый", "red"
    elif ent < 50: lbl, col = "Средний", "yellow"
    elif ent < 70: lbl, col = "Хороший", "green"
    else: lbl, col = "Отличный", "bold green"
    t = Table(box=box.ROUNDED, show_header=False, border_style=col)
    t.add_column("", style="bold yellow", width=20); t.add_column("", style="white")
    t.add_row("Длина", str(len(pwd)))
    t.add_row("Строчные", "✔" if lo else "✘"); t.add_row("Прописные", "✔" if up else "✘")
    t.add_row("Цифры", "✔" if di else "✘"); t.add_row("Символы", "✔" if sy else "✘")
    t.add_row("Энтропия", f"{ent:.1f} бит")
    t.add_row("Словарь", "[red]ДА[/]" if is_c else "[green]нет[/]")
    t.add_row("Оценка", f"[{col}]{lbl}[/]")
    console.print(); console.print(Panel(t, title="🔍 Аудит", border_style=col)); console.print()

def cmd_hash(text):
    if not text: console.print("[red]❌ hash <текст>[/]"); return
    import hashlib
    t = Table(title=f"🧮 {text[:40]}", box=box.ROUNDED, border_style="cyan")
    t.add_column("Алгоритм", style="bold yellow", width=10); t.add_column("Хэш", style="cyan")
    for algo in ("md5","sha1","sha256","sha512"):
        t.add_row(algo.upper(), hashlib.new(algo, text.encode()).hexdigest()[:64])
    console.print(); console.print(t); console.print()

def cmd_b64(args):
    p = args.split(maxsplit=1)
    if len(p) < 2: console.print("[red]❌ b64 enc|dec <текст>[/]"); return
    import base64
    mode, text = p[0].lower(), p[1]
    try:
        if mode in ("enc","e"): res = base64.b64encode(text.encode()).decode()
        elif mode in ("dec","d"): res = base64.b64decode(text.encode()).decode()
        else: console.print("[red]❌ enc|dec[/]"); return
        console.print(); console.print(Panel(f"[bold cyan]{res}[/]", border_style="cyan")); console.print()
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_ip():
    console.print("\n[bold yellow]📍 IP...[/]\n")
    try:
        import requests
        d = requests.get("https://ipinfo.io/json", timeout=10).json()
        t = Table(box=box.ROUNDED, show_header=False, border_style="cyan")
        t.add_column("", style="bold yellow", width=15); t.add_column("", style="cyan")
        for k, lbl in [("ip","🌐 IP"),("city","🏙 Город"),("region","🌍 Регион"),
                       ("country","🏳 Страна"),("org","📡 Провайдер"),("timezone","⏰ TZ")]:
            t.add_row(lbl, d.get(k,"?"))
        console.print(t); console.print()
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_ping(host):
    if not host: console.print("[red]❌ ping <хост>[/]"); return
    console.print(f"\n[bold yellow]🏓 {host}[/]\n")
    r = run(f"ping -c 4 {host}", timeout=20)
    console.print(r.stdout if r and r.stdout else "[red]❌ нет ответа[/]")

def cmd_ports(host):
    if not host: console.print("[red]❌ ports <хост>[/]"); return
    console.print(f"\n[bold yellow]⚙️  {host}[/]")
    console.print("[dim]⚠️  Только свои серверы[/]\n")
    ports = {21:"FTP",22:"SSH",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",
             143:"IMAP",443:"HTTPS",3306:"MySQL",5432:"PostgreSQL",
             6379:"Redis",8080:"HTTP-Alt",27017:"MongoDB"}
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
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_headers(url):
    if not url: console.print("[red]❌ headers <url>[/]"); return
    if not url.startswith("http"): url = "https://" + url
    console.print(f"\n[bold yellow]📋 {url}[/]\n")
    try:
        import requests
        r = requests.head(url, timeout=10, allow_redirects=True)
        t = Table(box=box.ROUNDED, border_style="cyan")
        t.add_column("Заголовок", style="bold yellow"); t.add_column("Значение", style="cyan")
        for k, v in r.headers.items(): t.add_row(k, str(v)[:70])
        console.print(t)
        console.print("\n[bold]🔒 Безопасность:[/]")
        for h, lbl in [("Strict-Transport-Security","HSTS"),
                       ("Content-Security-Policy","CSP"),
                       ("X-Frame-Options","Anti-Clickjack"),
                       ("X-Content-Type-Options","Anti-MIME")]:
            if h in r.headers: console.print(f"  [green]✔[/] {lbl}")
            else: console.print(f"  [red]✘[/] {lbl}")
        console.print()
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_robots(url):
    if not url: console.print("[red]❌ robots <url>[/]"); return
    if not url.startswith("http"): url = "https://" + url
    console.print(f"\n[bold yellow]🤖 {url}/robots.txt[/]\n")
    try:
        import requests
        r = requests.get(url.rstrip("/") + "/robots.txt", timeout=10)
        console.print(r.text[:2500] if r.status_code == 200 else f"[red]HTTP {r.status_code}[/]")
        console.print()
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_trace(host):
    if not host: console.print("[red]❌ trace <хост>[/]"); return
    console.print(f"\n[bold yellow]🛰 {host}[/]\n")
    r = run(f"traceroute -m 15 {host}", timeout=60)
    if r and r.stdout: console.print(r.stdout)
    else:
        r2 = run(f"ping -c 1 -R {host}", timeout=20)
        console.print(r2.stdout if r2 and r2.stdout else "[red]❌[/]")

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
        t = Table(box=box.ROUNDED, show_header=False, border_style="green")
        t.add_column("", style="bold yellow", width=15); t.add_column("", style="green")
        t.add_row("📥 Скорость", f"{mbps:.2f} Мбит/с")
        t.add_row("📡 Ping", f"{pm:.0f} мс")
        t.add_row("📦 Скачано", f"{sz/1024/1024:.2f} МБ")
        console.print(t); console.print()
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_weather(city):
    if not city: city = "Penza"
    console.print(f"\n[bold yellow]☀️  {city}[/]\n")
    try:
        import requests
        d = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10).json()
        c = d["current_condition"][0]
        t = Table(box=box.ROUNDED, show_header=False, border_style="cyan")
        t.add_column("", style="bold yellow", width=18); t.add_column("", style="cyan")
        t.add_row("🌡 Температура", f"{c['temp_C']}°C (ощущ. {c['FeelsLikeC']}°C)")
        t.add_row("💧 Влажность", f"{c['humidity']}%")
        t.add_row("💨 Ветер", f"{c['windspeedKmph']} км/ч")
        t.add_row("📝 Описание", c["weatherDesc"][0]["value"])
        console.print(t); console.print()
    except Exception as e: console.print(f"[red]❌ {e}[/]")

def cmd_matrix():
    import curses
    def _run(stdscr):
        curses.curs_set(0); stdscr.nodelay(True); stdscr.timeout(0)
        curses.start_color()
        try: curses.use_default_colors()
        except Exception: pass
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        CH = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"
        my, mx = stdscr.getmaxyx()
        drops = [{"y": random.randint(-20,0), "s": random.choice([0.5,1,1.5])} for _ in range(mx)]
        end = time.time() + 5
        while time.time() < end:
            try:
                if stdscr.getch() in (ord('q'), 27): break
            except Exception: pass
            my, mx = stdscr.getmaxyx()
            for x in range(min(mx, len(drops))):
                d = drops[x]; d["y"] += d["s"]; y = int(d["y"])
                if 0 <= y < my:
                    try: stdscr.addstr(y, x, random.choice(CH), curses.color_pair(1)|curses.A_BOLD)
                    except curses.error: pass
                e = y - 8
                if 0 <= e < my:
                    try: stdscr.addstr(e, x, " ", curses.color_pair(2))
                    except curses.error: pass
                if y - 8 >= my:
                    d["y"] = random.randint(-10,-1); d["s"] = random.choice([0.5,1,1.5])
            stdscr.refresh(); time.sleep(0.05)
    try: curses.wrapper(_run)
    except KeyboardInterrupt: pass

def cmd_sysinfo():
    console.print("\n[dim]sysinfo.py...[/]\n")
    time.sleep(0.2)
    try: subprocess.run(["python", os.path.expanduser("~/sysinfo.py")])
    except Exception as e: console.print(f"[red]❌ {e}[/]")

# ═══════════ ГЛАВНЫЙ ЦИКЛ ═══════════
COMMANDS = [
    "scan","crt","crypto","news","qr","pass","pass-audit","hash","b64",
    "ip","ping","ports","headers","robots","trace","speed","weather",
    "matrix","sysinfo","clear","exit","help"
]

def main():
    banner(); menu()

    # ─── prompt_toolkit: Tab-автодополнение ───
    completer = WordCompleter(COMMANDS, ignore_case=True, sentence=True)
    style = Style.from_dict({
        "prompt": "bold ansibrightgreen",
        "completion-menu.completion": "bg:#000000 #00ff88",
        "completion-menu.completion.current": "bg:#00aa55 #000000 bold",
        "completion-menu.meta.completion": "bg:#000000 #557755",
        "completion-menu.meta.completion.current": "bg:#00aa55 #000000",
        "scrollbar.background": "bg:#003322",
        "scrollbar.button": "bg:#00ff88",
    })

    session = PromptSession(completer=completer, style=style, complete_while_typing=True)

    while True:
        try:
            cmd_line = session.prompt(HTML('<prompt>hacktool></prompt> ')).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Выход.[/]"); break

        if not cmd_line: continue
        p = cmd_line.split(maxsplit=1)
        cmd = p[0].lower(); arg = p[1] if len(p) > 1 else ""

        if cmd in ("exit","quit","q","выход"):
            console.print("[dim]До связи, хакер. 🖖[/]"); break
        elif cmd in ("clear","cls"): banner(); menu()
        elif cmd == "scan": cmd_scan(arg)
        elif cmd == "crt": cmd_crt(arg)
        elif cmd == "crypto": cmd_crypto()
        elif cmd == "news": cmd_news()
        elif cmd == "qr": cmd_qr(arg)
        elif cmd in ("pass","password"): cmd_pass(arg)
        elif cmd == "pass-audit": cmd_pass_audit(arg)
        elif cmd == "hash": cmd_hash(arg)
        elif cmd == "b64": cmd_b64(arg)
        elif cmd == "ip": cmd_ip()
        elif cmd == "ping": cmd_ping(arg)
        elif cmd == "ports": cmd_ports(arg)
        elif cmd == "headers": cmd_headers(arg)
        elif cmd == "robots": cmd_robots(arg)
        elif cmd == "trace": cmd_trace(arg)
        elif cmd == "speed": cmd_speed()
        elif cmd == "weather": cmd_weather(arg)
        elif cmd == "matrix": cmd_matrix()
        elif cmd == "sysinfo": cmd_sysinfo()
        elif cmd in ("help","h","?"): menu()
        else:
            console.print(f"[red]❌ {cmd}[/] Введи [cyan]help[/]")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано.[/]")
