# ARGONOV OS · ПРАВИЛА РАЗРАБОТКИ

_Обязательное чтение для нейронки, работающей над проектом._

---

## 1. ФОРМАТ ОТВЕТА

### 1.1 Любая правка = снос + создание с нуля

НИКОГДА не редактировать файл точечно.
ВСЕГДА: удалить → создать заново → дать права → проверить.

### 1.2 Один файл за раз

Для каждого файла — три блока подряд:

1. 🗑 СНОС — команда `rm`
2. 📝 СОЗДАНИЕ + КОД — `nano` + код
3. 🚀 ПРОВЕРКА — chmod + py_compile + запуск

Только после проверки — следующий файл.
Не смешивать два файла в одном ответе.

### 1.3 rm и nano в одном блоке

Разрешено писать подряд:

    rm -f ~/имя.py
    nano ~/имя.py

### 1.4 Не обрезать файл

Если ответ не влезает — писать «продолжение в следующем сообщении» и дописывать с точной строки.

### 1.5 Проверка после правки

- Python: python -m py_compile ~/имя.py && echo "✅ OK"
- Bash: bash -n ~/argonov && echo "✅ OK"
- Тест: python ~/имя.py

---

## 2. СТАНДАРТ ФАЙЛОВ

### 2.1 Шапка Python

    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    # ═══════════════════════════════════════════════════════
    #  ARGONOV OS · <Название модуля>
    #  <Одна строка — что делает>
    #  Версия: X.Y  ·  Обновлён: YYYY-MM-DD
    # ═══════════════════════════════════════════════════════

### 2.2 Шапка Bash

    #!/data/data/com.termux/files/usr/bin/bash
    # ═══════════════════════════════════════════════════════
    #  ARGONOV OS · <Название>
    #  <Одна строка — что делает>
    #  Версия: X.Y  ·  Обновлён: YYYY-MM-DD
    # ═══════════════════════════════════════════════════════

### 2.3 Секции

Разделять блоки через:

    # ═══ НАЗВАНИЕ СЕКЦИИ ═══

Стандарт: КОНСТАНТЫ · УТИЛИТЫ · ЯДРО · MAIN

### 2.4 Импорты — три группы

    # stdlib
    import os, sys, json

    # third-party
    from rich.console import Console

    # локальные
    from net_helper import get_fx_rates

### 2.5 Цвета — константами сверху

Не хардкодить в функциях. Всё в секции КОНСТАНТЫ.

---

## 3. ДАМП + PUSH

После любого крупного обновления:

    python ~/argonov-dump

Что делает:

1. Собирает все скрипты в ~/ARGONOV_FULL_DUMP.md
2. В начало дампа вставляет ~/ARGONOV_RULES.md
3. Копирует в ~/argonov-os/
4. git add + commit + push

---

## 4. СТРУКТУРА

### 4.1 Локально (~/)

- argonov — точка входа (bash)
- argonov-dump — дамп + push (python)
- doctor.py — диагностика
- net_helper.py — fallback API + кэш
- ai.py — AI-ассистент
- 15 скриптов на Python

### 4.2 Репозиторий

- GitHub: https://github.com/Andreyfdfd/argonov-os
- Локально: ~/argonov-os/
- fish-config/config.fish
- termux-config/colors.properties

### 4.3 Данные (не в git)

- ~/.pm.vault — пароли (AES-256)
- ~/.todo.json — задачи
- ~/.notes.json — заметки
- ~/.hacker_rpg_save.json — RPG
- ~/.ai_config.json — настройки AI
- ~/music_cache/ — метаданные музыки
- ~/ai_chats/ — история AI-сессий
- ~/argonov_backups/ — бэкапы

---

## 5. ОГРАНИЧЕНИЯ

### 5.1 Платформа

- Android 10+ / Termux (F-Droid)
- Python 3.13
- Fish + starship
- Termux:API + Termux:Styling

### 5.2 AI

- Модель: Qwen 2.5 Coder 3B Q4_K_M
- Движок: llama.cpp (CPU, без GPU)
- GPU не работает (Android блокирует /vendor)
- TTFT 5-15 сек
- Sandbox: только ~/ и ~/storage

### 5.3 Не работает

- GPU (OpenCL) — Android SELinux
- Запись в /system, /vendor
- Контексты > 4096 токенов

---

## 6. ЦВЕТА

- #00FF88 — зелёный (основной)
- #00D9FF — циан (акценты)
- #FFD700 — жёлтый (внимание)
- #FF3355 — красный (ошибки)
- #557755 — dim

В rich: bright_green · bright_cyan · bright_yellow · bright_red · grey50

---

## 7. СТИЛЬ КОДА

### 7.1 Комментарии

- Не дублировать код словами
- Комментировать только неочевидное
- Секции — крупные, не по строке

### 7.2 Имена

- Функции: snake_case, глаголы (load_, save_, print_, check_)
- Константы: UPPER_CASE

### 7.3 Ошибки

- try/except Exception в утилитах
- KeyboardInterrupt — везде в main()
- Файлы сохранять через tmp + os.replace

---

## 8. ИСТОРИЯ

### v1.0–1.3

- 15+ скриптов, меню argonov, fish + CRT

### v1.4 (2026-09-11)

- Doctor v2, симлинки в $PREFIX/bin

### v1.5 (2026-09-11)

- Единый стандарт оформления
- argonov-dump (дамп + push)
- ARGONOV_RULES.md

### Roadmap

- net_helper.py v3 (кэш)
- ai.py v16 (сессии)
- ai.py -c (continue)

---

_Обновляется при крупных изменениях._
