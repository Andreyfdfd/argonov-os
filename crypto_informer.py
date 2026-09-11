#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════
#  ARGONOV OS · Crypto Informer
#  Курсы крипты + фиатных валют (multi-source)
#  Версия: 3.0  ·  Обновлён: 2026-09-11
# ═══════════════════════════════════════════════════════
"""
Курсы криптовалют и валют с индикатором свежести LIVE/КЭШ.

Использование:
    crypto                       # один показ + подсказка
    crypto --watch [N]           # watch-режим, интервал N сек
    crypto -w 30                 # то же, короче

Зависимости:
    - rich
    - net_helper (локальный)
"""

import os
import sys
import time
import subprocess
from datetime import datetime

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import SIMPLE_HEAD

# локальные
sys.path.insert(0, os.path.expanduser("~"))
from net_helper import get_crypto_prices, get_fx_rates, freshness_badge

# ═══ КОНСТАНТЫ ═══
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

# ═══ УТИЛИТЫ ═══
def clear():
    subprocess.run("clear", shell=True)


def fmt_price(p):
    if p is None:
        return "—"
    if p < 0.01:
        return f"${p:.8f}"
    if p < 1:
        return f"${p:.4f}"
    if p < 1000:
        return f"${p:,.2f}"
    return f"${p:,.0f}"


def fmt_change(pct):
    if pct is None:
        return "—"
    color = GREEN_BRIGHT if pct >= 0 else RED
    arrow = "▲" if pct >= 0 else "▼"
    return f"[{color}]{arrow}{abs(pct):.2f}%[/]"

# ═══ РИСОВКА ═══
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

# ═══ ЯДРО ═══
def fetch_all(force=False):
    """Возвращает (prices, source, crypto_meta, fx, fx_src, fx_meta)."""
    p, s, m = get_crypto_prices(with_meta=True, force=force)
    f, fs, fm = get_fx_rates(with_meta=True, force=force)
    return p, s, m, f, fs, fm


def show_once(force=False):
    with console.status(f"[bold {GREEN_BRIGHT}]📡 Загружаю...[/]", spinner="dots"):
        prices, source, crypto_meta, fx, fx_src, fx_meta = fetch_all(force=force)

    print_header(watch=False)
    print_freshness(crypto_meta, fx_meta)
    print_fx(fx)
    print_prices(prices, fx, source)


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
            console.print(f"  [dim]⏱ обновление каждые {interval}с  ·  [/][bold {YELLOW}]Ctrl+C[/][dim] — выход[/]")
            console.print()

            time.sleep(interval)
    except KeyboardInterrupt:
        console.print()
        console.print("[dim]⏹ Watch остановлен.[/]")
        console.print()

# ═══ MAIN ═══
def one_shot():
    clear()
    show_once(force=False)

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
