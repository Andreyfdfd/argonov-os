#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════
#  ARGONOV OS · Matrix Rain
#  Цифровой дождь в стиле «Матрицы» (curses)
#  Версия: 2.0  ·  Обновлён: 2026-09-11
# ═══════════════════════════════════════════════════════
"""Анимированный цифровой дождь. Выход — q / Esc / Ctrl+C."""

import curses
import random
import time

# ═══════════════════════════════════════════════════════
#  СИМВОЛЫ
# ═══════════════════════════════════════════════════════
KATAKANA = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ"
HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわん"
LATIN    = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
DIGITS   = "0123456789"
SYMBOLS  = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
GREEK    = "αβγδεζηθικλμνξοπρστυφχψω"
CYRILLIC = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

# Катаканы с большим весом — как в фильме
ALL_CHARS = (KATAKANA * 6 + HIRAGANA * 2 + LATIN + DIGITS * 3 +
             SYMBOLS * 2 + GREEK + CYRILLIC)

# ═══════════════════════════════════════════════════════
#  ПАРАМЕТРЫ
# ═══════════════════════════════════════════════════════
TAIL_LEN       = 22       # длина хвоста капли
FPS_DELAY      = 0.025    # ~40 FPS
FLASH_CHANCE   = 0.08     # шанс вспышки на голове
FLICKER_CHANCE = 0.15     # мерцание в хвосте

# Коды цветов curses
C_HEAD   = 1  # белый — голова
C_FLASH  = 2  # ярко-белый — вспышка
C_BRIGHT = 3  # ярко-зелёный
C_MID    = 4  # зелёный
C_DARK   = 5  # тёмно-зелёный
C_FAINT  = 6  # очень тёмный
C_FAINT2 = 7  # почти чёрный

# ═══════════════════════════════════════════════════════
#  ИНИЦИАЛИЗАЦИЯ ЦВЕТОВ
# ═══════════════════════════════════════════════════════
def init_colors():
    curses.start_color()
    try:
        curses.use_default_colors()
    except Exception:
        pass
    curses.init_pair(C_HEAD,   curses.COLOR_WHITE, -1)
    curses.init_pair(C_FLASH,  curses.COLOR_WHITE, -1)
    curses.init_pair(C_BRIGHT, curses.COLOR_GREEN, -1)
    curses.init_pair(C_MID,    curses.COLOR_GREEN, -1)
    curses.init_pair(C_DARK,   curses.COLOR_GREEN, -1)
    curses.init_pair(C_FAINT,  curses.COLOR_GREEN, -1)
    curses.init_pair(C_FAINT2, curses.COLOR_GREEN, -1)

# ═══════════════════════════════════════════════════════
#  ЯДРО
# ═══════════════════════════════════════════════════════
def new_drop(x, max_y, spread=False):
    """Создаёт новую каплю для колонки x."""
    return {
        "x": x,
        "y": random.randint(-max_y * 3, -1) if spread else random.randint(-25, -3),
        "speed": random.choice([0.2, 0.35, 0.5, 0.7, 0.9, 1.1, 1.4, 1.8, 2.2]),
        "counter": 0.0,
        "tail_len": random.randint(TAIL_LEN - 8, TAIL_LEN + 6),
        "flash_chance": random.random() * FLASH_CHANCE,
    }


def attr_for_tail(i, flicker):
    """Возвращает curses-attr для символа на позиции i от головы."""
    if flicker and i % 3 == 0:
        return curses.color_pair(C_BRIGHT) | curses.A_BOLD
    if i == 1:
        return curses.color_pair(C_BRIGHT) | curses.A_BOLD
    if i <= 3:
        return curses.color_pair(C_BRIGHT)
    if i <= 6:
        return curses.color_pair(C_MID)
    if i <= 10:
        return curses.color_pair(C_DARK)
    if i <= 15:
        return curses.color_pair(C_FAINT)
    return curses.color_pair(C_FAINT2) | curses.A_DIM


def main_loop(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)
    init_colors()

    max_y, max_x = stdscr.getmaxyx()

    drops = [new_drop(x, max_y, spread=True) for x in range(max_x)]
    # На широких экранах — доп. капли
    if max_x > 60:
        drops += [new_drop(random.randint(0, max_x - 1), max_y, spread=True)
                  for _ in range(max_x // 4)]

    while True:
        # Выход
        try:
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q'), 27):
                break
        except Exception:
            pass

        max_y, max_x = stdscr.getmaxyx()

        for idx, drop in enumerate(drops):
            drop["counter"] += drop["speed"]

            if drop["counter"] < 1.0:
                continue

            drop["counter"] = 0.0
            drop["y"] += 1
            x = drop["x"]
            y = drop["y"]

            if x >= max_x:
                continue

            flicker = random.random() < FLICKER_CHANCE

            # Голова
            if 0 <= y < max_y:
                if random.random() < drop["flash_chance"]:
                    attr = curses.color_pair(C_FLASH) | curses.A_BOLD | curses.A_REVERSE
                else:
                    attr = curses.color_pair(C_HEAD) | curses.A_BOLD
                try:
                    stdscr.addstr(y, x, random.choice(ALL_CHARS), attr)
                except curses.error:
                    pass

            # Хвост
            for i in range(1, drop["tail_len"] + 1):
                ty = y - i
                if not (0 <= ty < max_y):
                    continue
                try:
                    stdscr.addstr(ty, x, random.choice(ALL_CHARS),
                                  attr_for_tail(i, flicker))
                except curses.error:
                    pass

            # Стереть позади хвоста
            erase_y = y - drop["tail_len"]
            if 0 <= erase_y < max_y:
                try:
                    stdscr.addstr(erase_y, x, " ")
                except curses.error:
                    pass

            # Перезапуск капли
            if y - drop["tail_len"] >= max_y:
                drops[idx] = new_drop(x, max_y)

        # Случайная вспышка по экрану (молния)
        if random.random() < 0.015:
            fx = random.randint(0, max_x - 1)
            fy = random.randint(0, max_y - 1)
            try:
                stdscr.addstr(fy, fx, random.choice(ALL_CHARS),
                              curses.color_pair(C_FLASH) | curses.A_BOLD | curses.A_REVERSE)
            except curses.error:
                pass

        stdscr.refresh()
        time.sleep(FPS_DELAY)

# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        curses.wrapper(main_loop)
    except KeyboardInterrupt:
        pass
