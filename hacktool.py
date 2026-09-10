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
    console.print(Align.center("[bold cyan]⚡ OSINT Мультитул v2 ⚡[/]"))
    console.print(Align.center(f"[dim]{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}[/]"))
    console.print()

def menu():
    t = Table(box=DOUBLE_EDGE, border_style="green", show_header=False, padding=(0, 1))
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
                        border_style="green"))
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
        t = Table(box=SIMPLE_HEAD, border_style="cyan", header_style="bold cyan", padding=(0,1))
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
        t = Table(box=SIMPLE_HEAD, show_header=False, border_style="cyan", padding=(0,2))
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
        t = Table(box=SIMPLE_HEAD, show_header=False, border_style="green", padding=(0,2))
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
    t = Table(title=f"🧮 Хэши: {text[:40]}", box=SIMPLE_HEAD, border_style="cyan",
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

    t = Table(box=SIMPLE_HEAD, border_style="cyan", header_style="bold cyan")
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
        console.print(); console.print(Panel(f"[bold cyan]{res}[/]", border_style="cyan")); console.print()
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
    console.print(Panel(f"[bold green]{pwd}[/]", title=f"🔐 {length} символов", border_style="green"))
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
    t = Table(box=SIMPLE_HEAD, show_header=False, border_style=col, padding=(0,2))
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
        t = Table(box=SIMPLE_HEAD, border_style="yellow", header_style="bold yellow")
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
    console.clear()
    console.print()
    console.print(Align.center(Panel.fit(
        "[bold green]📚  РОАДМАП ПЕНТЕСТЕРА  📚[/]\n"
        "[dim]Полный путь от новичка до профессионала[/]",
        border_style="green")))
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
    console.clear()
    console.print()
    console.print(Align.center(Panel.fit(
        "[bold green]🏆  ПЛОЩАДКИ CTF  🏆[/]\n"
        "[dim]Где учиться и соревноваться[/]",
        border_style="green")))
    console.print()

    t = Table(box=SIMPLE_HEAD, border_style="cyan", header_style="bold cyan")
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
