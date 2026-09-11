#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════
#  ARGONOV OS · Password Generator
#  Криптостойкий генератор паролей
#  Версия: 2.0  ·  Обновлён: 2026-09-11
# ═══════════════════════════════════════════════════════
"""Интерактивный генератор паролей на базе secrets."""

import string
import secrets

# ═══════════════════════════════════════════════════════
#  КОНСТАНТЫ
# ═══════════════════════════════════════════════════════
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RED = "\033[91m"
DIM = "\033[2m"
RST = "\033[0m"

DEFAULT_LENGTH = 16
MIN_LENGTH = 4
MAX_LENGTH = 128
SYMBOLS = "!@#$%^&*()-_=+[{]};:,.<>?"

# ═══════════════════════════════════════════════════════
#  ЯДРО
# ═══════════════════════════════════════════════════════
def generate_password(length=16, use_digits=True, use_special=True):
    letters = string.ascii_letters
    digits = string.digits if use_digits else ""
    special = SYMBOLS if use_special else ""
    pool = letters + digits + special
    if not pool:
        return None
    return "".join(secrets.choice(pool) for _ in range(length))


def prompt_length():
    try:
        raw = input(f"{YELLOW}Длина пароля [{DEFAULT_LENGTH}]: {RST}").strip()
    except (EOFError, KeyboardInterrupt):
        return None
    if not raw:
        return DEFAULT_LENGTH
    if not raw.isdigit():
        print(f"{RED}❌ Нужно число{RST}")
        return None
    n = int(raw)
    if not MIN_LENGTH <= n <= MAX_LENGTH:
        print(f"{RED}❌ Допустимо {MIN_LENGTH}-{MAX_LENGTH}{RST}")
        return None
    return n

# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
def main():
    print()
    print(f"{CYAN}═══════════════════════════════════════════════{RST}")
    print(f"{CYAN}  🔐  ГЕНЕРАТОР ПАРОЛЕЙ{RST}")
    print(f"{CYAN}═══════════════════════════════════════════════{RST}")
    print()

    length = prompt_length()
    if length is None:
        return

    password = generate_password(length)
    if not password:
        print(f"{RED}❌ Ошибка генерации{RST}")
        return

    print()
    print(f"{GREEN}✔ Сгенерировано:{RST}")
    print(f"{DIM}─────────────────────────────────────────────{RST}")
    print(f"  {GREEN}{password}{RST}")
    print(f"{DIM}─────────────────────────────────────────────{RST}")
    print()
    print(f"{DIM}Скопируй и сохрани в надёжном месте.{RST}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RST}Отменено.{RST}")
