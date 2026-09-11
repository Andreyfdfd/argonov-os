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
