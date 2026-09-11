#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crypto Informer — крипта в реальном времени с live-обновлением"""

import os, sys, json, time, subprocess, threading
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

console = Console()
WATCHLIST_FILE = os.path.expanduser("~/.crypto_watchlist.json")

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"; ORANGE = "dark_orange"

DEFAULT_WATCHLIST = ["bitcoin", "ethereum", "solana", "binancecoin", "cardano"]

COIN_ICONS = {
    "bitcoin": "₿", "ethereum": "Ξ", "solana": "◎", "binancecoin": "🅑",
    "cardano": "₳", "ripple": "✕", "dogecoin": "Ð", "polkadot": "●",
    "tron": "◈", "litecoin": "Ł", "chainlink": "⬡", "matic-network": "⬢",
    "avalanche-2": "▲", "uniswap": "🦄", "shiba-inu": "🐕",
    "toncoin": "💎", "near": "Ⓝ", "cosmos": "⚛", "stellar": "✦",
}

# ═══════════ WATCHLIST ═══════════
def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return list(DEFAULT_WATCHLIST)
    try:
        with open(WATCHLIST_FILE, encoding="utf-8") as f:
            d = json.load(f)
            if isinstance(d, list) and d: return d
    except Exception:
        pass
    return list(DEFAULT_WATCHLIST)

def save_watchlist(lst):
    try:
        with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(lst, f, ensure_ascii=False, indent=1)
    except Exception:
        pass

# ═══════════ API ═══════════
def fetch_prices(ids):
    """Возвращает {coin: {usd, rub, usd_24h_change, usd_7d_change, market_cap, volume}}"""
    if not ids: return {}
    try:
        import requests
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "ids": ",".join(ids),
                "price_change_percentage": "24h,7d",
                "sparkline": "true",
            },
            timeout=12,
        )
        if r.status_code != 200:
            return {"__error__": f"HTTP {r.status_code}"}
        data = r.json()
        out = {}
        for c in data:
            cid = c.get("id")
            if not cid: continue
            out[cid] = {
                "symbol": (c.get("symbol") or "").upper(),
                "name": c.get("name", ""),
                "price_usd": c.get("current_price", 0),
                "price_rub": 0,  # отдельный запрос ниже
                "change_24h": c.get("price_change_percentage_24h_in_currency") or 0,
                "change_7d": c.get("price_change_percentage_7d_in_currency") or 0,
                "market_cap": c.get("market_cap", 0),
                "volume": c.get("total_volume", 0),
                "high_24h": c.get("high_24h", 0),
                "low_24h": c.get("low_24h", 0),
                "sparkline": (c.get("sparkline_in_7d") or {}).get("price", []),
            }
        return out
    except Exception as e:
        return {"__error__": str(e)}

def fetch_rub_rates():
    """Курс USD → RUB"""
    try:
        import requests
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=8)
        return r.json().get("rates", {}).get("RUB", 0)
    except Exception:
        return 0

# ═══════════ SPARKLINE ═══════════
SPARK_CHARS = "▁▂▃▄▅▆▇█"

def sparkline(prices, width=30):
    """ASCII-график из символов"""
    if not prices or len(prices) < 2: return ""
    # сжимаем до width точек
    step = max(1, len(prices) // width)
    samples = prices[::step][:width]
    mn, mx = min(samples), max(samples)
    if mx == mn: return SPARK_CHARS[0] * len(samples)
    out = []
    for p in samples:
        idx = int((p - mn) / (mx - mn) * (len(SPARK_CHARS) - 1))
        out.append(SPARK_CHARS[idx])
    return "".join(out)

def big_chart(prices, width=50, height=8):
    """ASCII-график побольше"""
    if not prices or len(prices) < 2: return []
    step = max(1, len(prices) // width)
    samples = prices[::step][:width]
    mn, mx = min(samples), max(samples)
    if mx == mn: mx = mn + 1
    rows = []
    for level in range(height, 0, -1):
        threshold = mn + (mx - mn) * (level / height)
        row = ""
        for p in samples:
            if p >= threshold:
                row += "█"
            elif p >= threshold - (mx - mn) / height * 0.5:
                row += "▓"
            elif p >= threshold - (mx - mn) / height * 0.85:
                row += "▒"
            else:
                row += " "
        rows.append(row)
    rows.append("─" * len(samples))
    return rows

# ═══════════ ФОРМАТ ═══════════
def fmt_price(p):
    if p is None: return "—"
    if p < 0.01: return f"${p:.8f}"
    if p < 1:    return f"${p:.4f}"
    if p < 1000: return f"${p:,.2f}"
    return f"${p:,.0f}"

def fmt_price_rub(p):
    if not p: return "—"
    if p < 1: return f"{p:.4f}₽"
    if p < 1000: return f"{p:,.2f}₽"
    return f"{p:,.0f}₽"

def fmt_change(pct):
    if pct is None: return "—"
    color = GREEN_BRIGHT if pct >= 0 else RED
    arrow = "▲" if pct >= 0 else "▼"
    return f"[{color}]{arrow}{abs(pct):.2f}%[/]"

def fmt_cap(v):
    if not v: return "—"
    for unit, div in [("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)]:
        if v >= div: return f"${v/div:.2f}{unit}"
    return f"${v:.0f}"

# ═══════════ РИСОВКА ═══════════
def clear(): os.system("clear")

def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("═" * 60, style=GREEN_DIM))
    return Group(*lines)

def prices_table(prices, rub_rate, watchlist):
    if "__error__" in prices:
        return Panel(Text(f"  ❌ Ошибка: {prices['__error__']}", style=RED),
                     border_style=RED)

    t = Table(box=box.SIMPLE_HEAD, border_style=CYAN,
              header_style=f"bold {CYAN}", padding=(0, 1), expand=True)
    t.add_column("Монета", style=WHITE, width=22)
    t.add_column("Цена USD", style=GREEN_BRIGHT, justify="right", width=16)
    t.add_column("Цена RUB", style=YELLOW, justify="right", width=16)
    t.add_column("24ч", justify="right", width=10)
    t.add_column("7д", justify="right", width=10)
    t.add_column("График (7д)", style=CYAN, width=28)

    for cid in watchlist:
        c = prices.get(cid)
        if not c:
            t.add_row(f"{cid[:20]}", "[dim]—[/]", "[dim]—[/]", "[dim]—[/]", "[dim]—[/]", "")
            continue
        icon = COIN_ICONS.get(cid, "●")
        name = f"{icon} {c['symbol']:<6} {c['name'][:12]}"
        price_usd = fmt_price(c["price_usd"])
        price_rub = fmt_price_rub(c["price_usd"] * rub_rate) if rub_rate else "—"
        ch24 = fmt_change(c.get("change_24h"))
        ch7d = fmt_change(c.get("change_7d"))
        spark = sparkline(c.get("sparkline", []), 26)
        t.add_row(name, price_usd, price_rub, ch24, ch7d, spark)
    return t

def commands_panel():
    t = Table(box=box.DOUBLE_EDGE, border_style="black",
              show_header=False, padding=(0, 2))
    t.add_column("Команда", style="bold yellow", width=26, justify="right")
    t.add_column("Действие", style="white")
    t.add_row("[cyan]live[/]",              "🔄 Live-обновление (Ctrl+C — стоп)")
    t.add_row("[cyan]coin <id>[/]",         "🔍 Детали монеты + график 7д")
    t.add_row("[cyan]add <id>[/]",          "➕ Добавить монету (напр. dogecoin)")
    t.add_row("[cyan]del <id>[/]",          "➖ Убрать из watchlist")
    t.add_row("[cyan]reset[/]",             "↩ Сбросить watchlist")
    t.add_row("[cyan]top[/]",               "🏆 Топ-10 по капитализации")
    t.add_row("[cyan]refresh[/]",           "🔄 Обновить сейчас")
    t.add_row("[cyan]q[/]",                 "🚪 Выход")
    console.print(Panel(t, title="[bold green]⌨  КОМАНДЫ  (Tab — автодополнение)[/]",
                        border_style="black"))
    console.print()

# ═══════════ TAB ═══════════
class CryptoCompleter(Completer):
    def __init__(self, get_watchlist):
        self.get_watchlist = get_watchlist

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        if not words or (len(words) == 1 and not text.endswith(" ")):
            partial = words[0] if words else ""
            for c in ["live","coin","add","del","reset","top","refresh","clear","q"]:
                if c.startswith(partial.lower()):
                    yield Completion(c, start_position=-len(partial))
            return

        cmd = words[0].lower()
        partial = words[-1] if not text.endswith(" ") else ""

        if cmd in ("coin","del"):
            for cid in self.get_watchlist():
                if cid.startswith(partial.lower()):
                    yield Completion(cid, start_position=-len(partial))
            # популярные монеты
            if cmd == "del": return
            popular = ["bitcoin","ethereum","solana","binancecoin","cardano",
                       "ripple","dogecoin","polkadot","tron","litecoin",
                       "chainlink","matic-network","avalanche-2","uniswap",
                       "shiba-inu","toncoin","near","cosmos","stellar"]
            for cid in popular:
                if cid.startswith(partial.lower()) and cid not in self.get_watchlist():
                    yield Completion(cid, start_position=-len(partial))

        if cmd == "add":
            popular = ["bitcoin","ethereum","solana","binancecoin","cardano",
                       "ripple","dogecoin","polkadot","tron","litecoin",
                       "chainlink","matic-network","avalanche-2","uniswap",
                       "shiba-inu","toncoin","near","cosmos","stellar"]
            for cid in popular:
                if cid.startswith(partial.lower()):
                    yield Completion(cid, start_position=-len(partial))

# ═══════════ LIVE MODE ═══════════
def live_mode(watchlist, rub_rate_ref):
    """Live-обновление каждые 8 секунд."""
    try:
        from prompt_toolkit import PromptSession as _PS
        import termios, tty, select
        has_t = True
    except Exception:
        has_t = False

    def read_key():
        if not has_t: return None
        fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            rl, _, _ = select.select([sys.stdin], [], [], 0.15)
            if rl: return sys.stdin.read(1)
        except Exception: return None
        finally:
            try: termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except Exception: pass
        return None

    stop_flag = {"stop": False}

    def render(pr, rub_rate):
        os.system("clear")
        console.print()
        console.print(title_block("C R Y P T O   L I V E", f"обновление каждые 8 сек  •  {datetime.now().strftime('%H:%M:%S')}"))
        console.print()
        console.print(prices_table(pr, rub_rate, watchlist))
        console.print()
        console.print(Text("  [s] стоп  •  [r] обновить сейчас  •  [q] выход", style=f"dim {CYAN}"))
        console.print()

    last = {"data": None, "rub": 0}
    last_refresh = {"t": 0}

    with Live(console=console, refresh_per_second=4) as live_:
        while not stop_flag["stop"]:
            now = time.time()
            if now - last_refresh["t"] > 8 or last["data"] is None:
                data = fetch_prices(watchlist)
                rub = fetch_global_rub()
                last["data"] = data
                last["rub"] = rub
                last_refresh["t"] = now
            # рендер
            os.system("clear")
            console.print()
            console.print(title_block("C R Y P T O   L I V E",
                f"обновление каждые 8 сек  •  {datetime.now().strftime('%H:%M:%S')}"))
            console.print()
            console.print(prices_table(last["data"] or {}, last["rub"], watchlist))
            console.print()
            console.print(Text("  [s] стоп  •  [r] обновить сейчас  •  [q] выход", style=f"dim {CYAN}"))
            console.print()

            k = read_key()
            if k:
                kl = k.lower()
                if kl in ("s","q"): stop_flag["stop"] = True
                elif kl == "r": last_refresh["t"] = 0
            time.sleep(0.15)

_rub_cache = {"value": 0, "ts": 0}
def fetch_global_rub():
    now = time.time()
    if now - _rub_cache["ts"] < 3600 and _rub_cache["value"]:
        return _rub_cache["value"]
    r = fetch_rub_rates()
    if r:
        _rub_cache["value"] = r
        _rub_cache["ts"] = now
    return r

# ═══════════ MAIN ═══════════
def main():
    watchlist = load_watchlist()
    rub_rate = fetch_global_rub()

    style = Style.from_dict({
        "prompt": "bold ansibrightmagenta",
        "completion-menu.completion": "bg:#000000 #00ff88",
        "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
    })

    while True:
        clear()
        console.print()
        console.print(title_block("C R Y P T O   I N F O R M E R",
                                  "Terminal Argonov  •  CoinGecko"))
        console.print()

        console.print(f"[dim]💵 1 USD ≈ {rub_rate:.2f}₽   •   🕐 {datetime.now().strftime('%H:%M:%S')}[/]")
        console.print()

        # Свежие данные — fetch раз в минуту
        if time.time() - _rub_cache["ts"] > 60:
            rub_rate = fetch_global_rub()
        prices = fetch_prices(watchlist)
        console.print(prices_table(prices, rub_rate, watchlist))
        console.print()
        commands_panel()

        session = PromptSession(
            completer=CryptoCompleter(lambda: watchlist),
            style=style, complete_while_typing=True)
        try:
            cmd = session.prompt(HTML("<prompt>╰─❯</prompt> ")).strip()
        except (EOFError, KeyboardInterrupt):
            console.print(Text("\n Пока! 💰", style=f"dim {GREEN_DIM}")); break

        if not cmd: continue
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if c in ("q","exit","quit","выход"):
            console.print(Text(" Пока! 💰", style=f"dim {GREEN_DIM}")); break
        if c == "clear": continue

        if c == "refresh":
            console.print(Text("  🔄 Обновлено", style=GREEN_BRIGHT))
            time.sleep(0.4); continue

        if c == "live":
            live_mode(watchlist, rub_rate)
            continue

        if c == "reset":
            watchlist = list(DEFAULT_WATCHLIST)
            save_watchlist(watchlist)
            console.print(Text("  ↩ Watchlist сброшен", style=GREEN_BRIGHT))
            time.sleep(0.5); continue

        if c == "add":
            if not arg:
                console.print(Text("  ❌ add <id>", style=RED)); time.sleep(1); continue
            cid = arg.strip().lower()
            if cid in watchlist:
                console.print(Text(f"  ⚠ {cid} уже в списке", style=YELLOW)); time.sleep(1); continue
            # Проверим, что монета существует
            test = fetch_prices([cid])
            if cid not in test:
                console.print(Text(f"  ❌ Монета «{cid}» не найдена на CoinGecko", style=RED))
                time.sleep(1.2); continue
            watchlist.append(cid)
            save_watchlist(watchlist)
            console.print(Text(f"  ✔ Добавлено: {cid}", style=GREEN_BRIGHT))
            time.sleep(0.8); continue

        if c == "del":
            if not arg:
                console.print(Text("  ❌ del <id>", style=RED)); time.sleep(1); continue
            cid = arg.strip().lower()
            if cid not in watchlist:
                console.print(Text(f"  ⚠ {cid} нет в списке", style=YELLOW)); time.sleep(1); continue
            watchlist.remove(cid)
            save_watchlist(watchlist)
            console.print(Text(f"  🗑 Удалено: {cid}", style=RED))
            time.sleep(0.8); continue

        if c == "coin":
            if not arg:
                console.print(Text("  ❌ coin <id>", style=RED)); time.sleep(1); continue
            cid = arg.strip().lower()
            data = fetch_prices([cid])
            if cid not in data:
                console.print(Text(f"  ❌ Монета не найдена", style=RED)); time.sleep(1); continue
            co = data[cid]
            clear()
            console.print()
            icon = COIN_ICONS.get(cid, "●")
            console.print(title_block(f"{icon}  {co['name']} ({co['symbol']})"))
            console.print()

            t = Table(box=box.ROUNDED, show_header=False, border_style=CYAN, padding=(0, 2))
            t.add_column("", style=f"bold {YELLOW}", width=18)
            t.add_column("", style=WHITE)
            t.add_row("💵 Цена USD", f"[bold]{fmt_price(co['price_usd'])}[/]")
            t.add_row("🇷🇺 Цена RUB", f"[bold]{fmt_price_rub(co['price_usd'] * rub_rate)}[/]")
            t.add_row("📈 24ч", fmt_change(co.get("change_24h")))
            t.add_row("📈 7д", fmt_change(co.get("change_7d")))
            t.add_row("💎 Капитализация", fmt_cap(co.get("market_cap")))
            t.add_row("📊 Объём 24ч", fmt_cap(co.get("volume")))
            t.add_row("🔺 High 24ч", fmt_price(co.get("high_24h")))
            t.add_row("🔻 Low 24ч", fmt_price(co.get("low_24h")))
            console.print(t)
            console.print()

            spark = co.get("sparkline", [])
            if spark:
                console.print(Text("📉 График 7 дней:", style=f"bold {CYAN}"))
                console.print()
                chart_lines = big_chart(spark, width=50, height=8)
                for line in chart_lines:
                    console.print(Text("   " + line, style=GREEN_BRIGHT))
                console.print()
                # info о диапазоне
                mn, mx = min(spark), max(spark)
                console.print(Text(f"   Мин: {fmt_price(mn)}   Макс: {fmt_price(mx)}", style=GRAY))
            console.print()
            try: console.input("[dim]Enter — назад[/] ")
            except (KeyboardInterrupt, EOFError): pass
            continue

        if c == "top":
            try:
                import requests
                r = requests.get("https://api.coingecko.com/api/v3/coins/markets",
                    params={"vs_currency":"usd","order":"market_cap_desc",
                            "per_page":10,"page":1,
                            "price_change_percentage":"24h"}, timeout=12)
                data = r.json()
                clear()
                console.print()
                console.print(title_block("🏆 ТОП-10 ПО КАПИТАЛИЗАЦИИ"))
                console.print()
                t = Table(box=box.SIMPLE_HEAD, border_style=YELLOW,
                          header_style=f"bold {YELLOW}", padding=(0, 1), expand=True)
                t.add_column("#", style=f"bold {YELLOW}", width=3, justify="right")
                t.add_column("Монета", style=WHITE)
                t.add_column("Цена", style=GREEN_BRIGHT, justify="right")
                t.add_column("24ч", justify="right", width=10)
                t.add_column("Капитализация", style=CYAN, justify="right")
                for i, co in enumerate(data, 1):
                    icon = COIN_ICONS.get(co.get("id",""), "●")
                    t.add_row(str(i),
                              f"{icon} {co.get('symbol','').upper():<6} {co.get('name','')[:16]}",
                              fmt_price(co.get("current_price", 0)),
                              fmt_change(co.get("price_change_percentage_24h", 0)),
                              fmt_cap(co.get("market_cap", 0)))
                console.print(t); console.print()
                try: console.input("[dim]Enter — назад[/] ")
                except (KeyboardInterrupt, EOFError): pass
            except Exception as e:
                console.print(f"[red]❌ {e}[/]"); time.sleep(1)
            continue

        console.print(Text(f"  ❌ Неизвестно: {c}", style=RED))
        time.sleep(0.6)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print(Text("\n Пока! 💰", style=f"dim {GREEN_DIM}"))
