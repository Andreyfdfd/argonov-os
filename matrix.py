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
