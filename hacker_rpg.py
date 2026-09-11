#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HACKER SIMULATOR RPG — текстовый квест в стиле Terminal Argonov"""

import os, sys, json, time, random, hashlib
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.markdown import Markdown
from rich.progress import Progress, BarColumn
from rich.box import SIMPLE_HEAD
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

console = Console()
HOME = os.path.expanduser("~")
SAVE_FILE = os.path.join(HOME, ".hacker_rpg_save.json")

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"; ORANGE = "dark_orange"

# ═══════════ ИГРОВЫЕ ДАННЫЕ ═══════════
SKILLS = {
    "cracking":    {"name": "🔐 Cracking",    "desc": "Взлом паролей и защит"},
    "stealth":     {"name": "🕵️  Stealth",     "desc": "Снижает риск обнаружения"},
    "trading":     {"name": "💰 Trading",     "desc": "Больше денег с миссий"},
    "programming": {"name": "🛠 Programming", "desc": "Открывает сложные цели"},
    "network":     {"name": "🌐 Network",     "desc": "Доступ к сетевым миссиям"},
    "social":      {"name": "💬 Social",      "desc": "Фишинг, манипуляции"},
}

FACTIONS = {
    "crimson":   {"name": "🔴 Crimson",   "desc": "Русские хакеры. Сильные, дорогие",  "bonus": "+25% денег, +10% риск"},
    "ghost":     {"name": "🔵 Ghost",     "desc": "Анонимные. Скрытные, дешёвые",       "bonus": "-25% риск, -10% денег"},
    "whitehat":  {"name": "🟢 White Hat", "desc": "Пентестеры. Легальные, стабильные", "bonus": "-50% геймовер-риск"},
    "syndicate": {"name": "🟡 Syndicate", "desc": "Корпорация. Максимум денег",          "bonus": "+50% денег, +25% риск"},
}

# ═══════════ МИССИИ (по уровням) ═══════════
MISSIONS = {
    0: [  # Newbie
        {"id":"m01","name":"Ломаем дверь","story":"Древний форум на PHP. Админка на /admin, пароль 12345?","target":"forum.local","reward":15,"xp":10,"diff":1,"req":{},"skills":["cracking"]},
        {"id":"m02","name":"Старый WordPress","story":"Блог соседа. Плагин не обновлялся 3 года.","target":"blog.local","reward":25,"xp":15,"diff":2,"req":{},"skills":["cracking","programming"]},
        {"id":"m03","name":"Wi-Fi кафе","story":"Открытая сеть кафе. Перехватить трафик и войти в роутер.","target":"cafe-wifi","reward":30,"xp":20,"diff":2,"req":{},"skills":["network"]},
        {"id":"m04","name":"Фишинговый сайт","story":"Поддельная страница банка. Найти и обрушить.","target":"fake-bank.xyz","reward":40,"xp":25,"diff":3,"req":{},"skills":["social","cracking"]},
        {"id":"m05","name":"Разведка портов","story":"Просканировать открытые порты сервера конкурента.","target":"rival-server","reward":50,"xp":30,"diff":3,"req":{},"skills":["network"]},
    ],
    1: [  # Script Kiddie
        {"id":"m06","name":"SQL-инъекция","story":"Интернет-магазин с дырявой формой поиска.","target":"shop-online.ru","reward":120,"xp":60,"diff":4,"req":{"cracking":3},"skills":["cracking","programming"]},
        {"id":"m07","name":"Социальная инженерия","story":"Убедить сотрудника выдать пароль.","target":"office.corp","reward":200,"xp":80,"diff":5,"req":{"social":3},"skills":["social"]},
        {"id":"m08","name":"DDoS-заказ","story":"Положить игровой сервер на 2 часа.","target":"game-server.io","reward":300,"xp":100,"diff":5,"req":{"network":3},"skills":["network"]},
        {"id":"m09","name":"Кража API-ключей","story":"Из чужого репозитория на GitHub.","target":"github.com/user/repo","reward":400,"xp":120,"diff":6,"req":{"programming":3},"skills":["programming","cracking"]},
        {"id":"m10","name":"Брутфорс-атака","story":"Подобрать пароль к корп-почте.","target":"mail.corp.ru","reward":500,"xp":150,"diff":6,"req":{"cracking":5},"skills":["cracking"]},
    ],
    2: [  # Hacker
        {"id":"m11","name":"Пентест банка","story":"Внутренний аудит безопасности.","target":"bank.internal","reward":1500,"xp":300,"diff":8,"req":{"cracking":7,"programming":5},"skills":["cracking","programming","stealth"]},
        {"id":"m12","name":"Кража базы данных","story":"3 миллиона пользователей.","target":"social-media.db","reward":2500,"xp":400,"diff":9,"req":{"programming":7,"network":5},"skills":["programming","network","stealth"]},
        {"id":"m13","name":"Взлом смарт-контракта","story":"Крипто-биржа с багом в контракте.","target":"crypto-exchange.eth","reward":5000,"xp":600,"diff":10,"req":{"programming":9},"skills":["programming","cracking"]},
        {"id":"m14","name":"APT-атака на корпорацию","story":"Многоступенчатая атака. 3 недели подготовки.","target":"megacorp.com","reward":8000,"xp":900,"diff":11,"req":{"cracking":10,"network":8,"stealth":8},"skills":["cracking","network","stealth","social"]},
        {"id":"m15","name":"Заряженный ransomware","story":"Развернуть вирус-вымогатель на 500 машинах.","target":"hospital.network","reward":12000,"xp":1200,"diff":12,"req":{"programming":11,"network":9},"skills":["programming","network"]},
    ],
    3: [  # Elite
        {"id":"m16","name":"Госструктура","story":"Взлом системы министерства.","target":"gov.system","reward":30000,"xp":2500,"diff":14,"req":{"cracking":13,"stealth":12},"skills":["cracking","stealth","programming"]},
        {"id":"m17","name":"Атака на SWIFT","story":"Межбанковские переводы. Только для настоящих мастеров.","target":"swift.network","reward":100000,"xp":5000,"diff":16,"req":{"cracking":15,"network":14,"programming":13},"skills":["cracking","network","programming","stealth"]},
        {"id":"m18","name":"Кража прототипа ИИ","story":"Секретная модель из лаборатории.","target":"research-lab.ai","reward":150000,"xp":7000,"diff":17,"req":{"programming":16,"social":12},"skills":["programming","social","stealth"]},
    ],
    4: [  # Legend
        {"id":"m19","name":"Anonymous-операция","story":"Атака на международную сеть. 1000 хакеров вместе.","target":"worldwide.anonymous","reward":500000,"xp":20000,"diff":20,"req":{"cracking":20,"stealth":20,"programming":20,"network":20,"social":15},"skills":["cracking","network","programming","stealth","social"]},
        {"id":"m20","name":"Взлом спутника","story":"Управление спутником связи. Финальный босс.","target":"satellite.sky","reward":1000000,"xp":50000,"diff":25,"req":{"cracking":25,"network":22,"programming":22,"stealth":20},"skills":["cracking","network","programming","stealth"]},
    ],
}

# ═══════════ МАГАЗИН ═══════════
SHOP_SOFT = [
    {"id":"s1","name":"🔧 Nmap Pro","price":500,"desc":"+1 к Cracking, открывает сетевые миссии","effect":{"cracking":1}},
    {"id":"s2","name":"🔍 SQLMap","price":800,"desc":"+2 к Cracking","effect":{"cracking":2}},
    {"id":"s3","name":"🎭 Proxy Chain","price":1200,"desc":"+2 к Stealth","effect":{"stealth":2}},
    {"id":"s4","name":"🔐 Hashcat","price":2000,"desc":"+3 к Cracking","effect":{"cracking":3}},
    {"id":"s5","name":"🕶  Tor Browser+","price":3000,"desc":"+3 к Stealth","effect":{"stealth":3}},
    {"id":"s6","name":"💬 SocialBot","price":4000,"desc":"+3 к Social","effect":{"social":3}},
    {"id":"s7","name":"🛠 CodeInjector","price":6000,"desc":"+3 к Programming","effect":{"programming":3}},
    {"id":"s8","name":"🌐 VPN-Ultra","price":8000,"desc":"+3 к Network","effect":{"network":3}},
    {"id":"s9","name":"💰 Trader-X","price":10000,"desc":"+3 к Trading","effect":{"trading":3}},
    {"id":"s10","name":"🚀 Quantum-Crack","price":25000,"desc":"+5 к Cracking","effect":{"cracking":5}},
]

# ═══════════ СОСТОЯНИЕ ═══════════
STATE = {
    "hp": 100,
    "money": 50,
    "xp": 0,
    "level": 0,
    "skills": {k: 0 for k in SKILLS.keys()},
    "faction": None,
    "completed": [],
    "owned_software": [],
    "equipment": [],
    "started_at": None,
    "total_missions": 0,
    "deaths": 0,
    "wins": 0,
}

LEVEL_NAMES = ["🟢 NEWBIE", "🟡 SCRIPT KIDDIE", "🟠 HACKER", "🔴 ELITE", "🏆 LEGEND"]
LEVEL_XP = [0, 200, 2000, 20000, 100000]

# ═══════════ УТИЛИТЫ ═══════════
def clear():
    os.system("clear")

def hp_bar(hp, width=30):
    filled = int((hp/100)*width)
    if hp > 70: color = "bright_green"
    elif hp > 40: color = "bright_yellow"
    elif hp > 15: color = "dark_orange"
    else: color = "bright_red"
    return Text("▓"*filled + "░"*(width-filled), style=color)

def save_game(silent=False):
    STATE["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(STATE, f, ensure_ascii=False, indent=1)
        if not silent:
            console.print(f"[green]💾 Прогресс сохранён[/]")
        return True
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")
        return False

def load_game():
    global STATE
    if not os.path.exists(SAVE_FILE): return False
    try:
        with open(SAVE_FILE, encoding="utf-8") as f:
            data = json.load(f)
        for k in STATE.keys():
            if k in data: STATE[k] = data[k]
        return True
    except: return False

def check_level_up():
    """Возвращает True если уровень повысился"""
    old_level = STATE["level"]
    new_level = 0
    for i, thresh in enumerate(LEVEL_XP):
        if STATE["xp"] >= thresh: new_level = i
    if new_level > old_level:
        STATE["level"] = new_level
        console.print()
        console.print(Panel(Align.center(Text(f"🎉 УРОВЕНЬ ПОВЫШЕН: {LEVEL_NAMES[new_level]}", style="bold bright_green")),
                            border_style="bright_green"))
        console.print()
        save_game(silent=True)
        return True
    return False

def get_available_missions():
    """Возвращает список доступных миссий с их сложностью (относительно скиллов)"""
    available = []
    for level, missions in MISSIONS.items():
        for m in missions:
            if m["id"] in STATE["completed"]: continue
            # Проверяем требования
            req_ok = True
            for skill, val in m["req"].items():
                if STATE["skills"].get(skill, 0) < val:
                    req_ok = False; break
            if req_ok:
                available.append((level, m))
    return available

# ═══════════ МИНИ-ИГРЫ ═══════════
def minigame_crack(diff):
    """Mastermind: угадать 4-значный код (0-9). 10 попыток."""
    code = [random.randint(0,9) for _ in range(4)]
    tries = max(3, 11 - diff)  # сложнее → меньше попыток

    console.print()
    console.print(Panel.fit(
        f"[bold cyan]🔐 ВЗЛОМ ПАРОЛЯ[/]\n"
        f"[dim]Код из 4 цифр (0-9). Угадай за {tries} попыток.[/]\n"
        f"[dim]● = правильная цифра на месте · ○ = правильная не на месте[/]",
        border_style="cyan"))
    console.print()

    for attempt in range(1, tries+1):
        try:
            guess_str = console.input(f"[bold magenta]Попытка {attempt}/{tries} > [/]").strip()
        except: return False
        if not guess_str.isdigit() or len(guess_str) != 4:
            console.print("[red]❌ Нужно ровно 4 цифры[/]")
            continue
        guess = [int(c) for c in guess_str]
        if guess == code:
            console.print(f"[bold green]✅ ВЗЛОМАНО за {attempt} попыток![/]\n")
            return True
        # Подсказки
        bulls = sum(1 for i in range(4) if guess[i] == code[i])
        code_c = code.copy(); guess_c = guess.copy()
        for i in range(4):
            if guess_c[i] == code_c[i]: code_c[i] = None; guess_c[i] = None
        cows = sum(1 for g in guess_c if g is not None and g in code_c)
        console.print(f"  [green]{'●'*bulls}[/][yellow]{'○'*cows}[/][dim]{'·'*(4-bulls-cows)}[/]")

    console.print(f"[red]❌ Не удалось взломать за {tries} попыток. Код был: {''.join(map(str,code))}[/]\n")
    return False

def minigame_infiltrate(diff):
    """Simon: запомнить последовательность символов"""
    seq_len = min(4 + diff, 12)
    chars = "ABCDEFGH"
    sequence = [random.choice(chars) for _ in range(seq_len)]

    console.print()
    console.print(Panel.fit(
        f"[bold cyan]🕵️  ПРОНИКНОВЕНИЕ[/]\n"
        f"[dim]Запомни последовательность {seq_len} символов.[/]",
        border_style="cyan"))
    console.print()
    console.print(f"[bold yellow]{' '.join(sequence)}[/]")
    time.sleep(2 + seq_len * 0.3)
    clear()
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]🕵️  ПРОНИКНОВЕНИЕ[/]\n"
        f"[dim]Введи последовательность через пробел.[/]",
        border_style="cyan"))
    console.print()
    try:
        answer = console.input("[bold magenta]> [/]").strip().upper().split()
    except: return False
    if answer == sequence:
        console.print("[bold green]✅ ПРОНИКНОВЕНИЕ УСПЕШНО![/]\n")
        return True
    console.print(f"[red]❌ Неверно. Было: {' '.join(sequence)}[/]\n")
    return False

def minigame_social(diff):
    """Выбрать правильную реплику из 3"""
    scenarios = [
        {"q":"Сотрудник банка: 'Кто вы такой?'",
         "options":[
             ("Я из IT-отдела, проверяю систему", True),
             ("Привет! Я хакер, дай пароль", False),
             ("Ты что, не узнал меня?", False),
         ]},
        {"q":"Админ: 'Назовите ваш отдел.'",
         "options":[
             ("Не помню точно, но начальник сказал...", False),
             ("Финансовый. У нас аудит на следующей неделе.", True),
             ("А какая разница?", False),
         ]},
        {"q":"Секретарь: 'Могу я увидеть ваш пропуск?'",
         "options":[
             ("Забыл в машине, сейчас вернусь", False),
             ("Конечно, вот он. Слушайте, у меня к вам личное дело...", True),
             ("Не ваше дело", False),
         ]},
        {"q":"Охранник: 'Стойте! Куда собрались?'",
         "options":[
             ("Домой, я устал", False),
             ("К начальнику, он сам меня вызвал", True),
             ("Тебе что, зарплату мало платят?", False),
         ]},
    ]
    rounds = min(2 + diff // 3, 5)
    console.print()
    console.print(Panel.fit(f"[bold cyan]💬 СОЦИАЛЬНАЯ ИНЖЕНЕРИЯ[/]\n[dim]Выбери правильный ответ. Раундов: {rounds}[/]",
                            border_style="cyan"))
    console.print()

    correct = 0
    for r in range(rounds):
        sc = random.choice(scenarios)
        console.print(f"[bold yellow]Раунд {r+1}/{rounds}[/]")
        console.print(f"  {sc['q']}\n")
        opts = sc["options"][:]
        random.shuffle(opts)
        for i, (o, _) in enumerate(opts, 1):
            console.print(f"  [cyan]{i}.[/] {o}")
        try:
            ch = console.input("\n[bold magenta]Выбор> [/]").strip()
        except: return False
        if ch.isdigit() and 1 <= int(ch) <= len(opts):
            if opts[int(ch)-1][1]:
                console.print("  [green]✔ Хорошо[/]\n"); correct += 1
            else:
                console.print("  [red]✘ Провал реплики[/]\n")

    needed = (rounds * 2) // 3
    if correct >= needed:
        console.print(f"[bold green]✅ ПРОШЛО: {correct}/{rounds}[/]\n")
        return True
    console.print(f"[red]❌ Провал: {correct}/{rounds} (нужно {needed})[/]\n")
    return False

def get_minigame(skill_type, diff):
    if skill_type == "cracking": return minigame_crack(diff)
    if skill_type in ("network", "stealth"): return minigame_infiltrate(diff)
    if skill_type == "social": return minigame_social(diff)
    if skill_type == "programming": return minigame_crack(diff)  # тоже код
    if skill_type == "trading": return minigame_social(diff)    # переговоры
    return minigame_crack(diff)

# ═══════════ МИССИИ — ИСПОЛНЕНИЕ ═══════════
def do_mission(level, mission):
    """Возвращает True если миссия пройдена"""
    clear()
    console.print()
    console.print(Panel(
        Group(
            Text(f"📋 МИССИЯ: {mission['name']}", style="bold bright_cyan"),
            Text(""),
            Text(f"🎯 Цель: {mission['target']}", style="yellow"),
            Text(f"💀 Сложность: {mission['diff']}/25", style="red"),
            Text(""),
            Text(mission['story'], style="white"),
            Text(""),
            Text(f"💰 Награда: ${mission['reward']}", style="green"),
            Text(f"⭐ Опыт: {mission['xp']}", style="cyan"),
        ),
        border_style="cyan", padding=(1,2)))
    console.print()

    try:
        ans = console.input("[bold magenta]Начать взлом? (y/n)> [/]").strip().lower()
    except: return False
    if ans != "y":
        console.print("[dim]Отмена[/]"); return False

    # Определяем какой скилл использовать
    main_skill = mission["skills"][0] if mission["skills"] else "cracking"

    # Мини-игра
    won = get_minigame(main_skill, mission["diff"])

    if not won:
        # Провал миссии → урон
        dmg = random.randint(10, 30)
        STATE["hp"] = max(0, STATE["hp"] - dmg)
        console.print(f"[red]💥 Провал! Потеряно {dmg} HP (осталось {STATE['hp']})[/]\n")

        # Проверка геймовера
        if STATE["hp"] <= 0:
            gameover()
            return False

        # Провал с шансом обнаружения (зависит от stealth)
        stealth = STATE["skills"].get("stealth", 0)
        detect_chance = max(5, 60 - stealth * 3 - mission["diff"] * 2)
        if random.randint(1, 100) <= detect_chance:
            console.print("[red bold]🚨 ТЕБЯ ОБНАРУЖИЛИ![/]\n")
            time.sleep(1.5)
            gameover()
            return False

        console.print("[yellow]⚠ Тебе удалось скрыться, но миссия провалена[/]\n")
        save_game(silent=True)
        return False

    # Успех!
    money = mission["reward"]
    xp = mission["xp"]

    # Множители от фракции
    if STATE["faction"] == "crimson": money = int(money * 1.25)
    elif STATE["faction"] == "ghost": money = int(money * 0.9)
    elif STATE["faction"] == "syndicate": money = int(money * 1.5)

    # Множители от скиллов
    trading = STATE["skills"].get("trading", 0)
    money = int(money * (1 + trading * 0.05))

    STATE["money"] += money
    STATE["xp"] += xp
    STATE["completed"].append(mission["id"])
    STATE["total_missions"] += 1
    STATE["wins"] += 1

    console.print()
    console.print(Panel(
        Group(
            Text("✅ МИССИЯ ВЫПОЛНЕНА", style="bold bright_green"),
            Text(""),
            Text(f"💰 Получено: ${money}", style="green"),
            Text(f"⭐ Опыт: +{xp}", style="cyan"),
            Text(f"💼 Всего денег: ${STATE['money']}", style="yellow"),
        ),
        border_style="green", padding=(1,2)))
    console.print()

    # Автосохранение при успехе
    save_game(silent=True)
    console.print("[dim]💾 Автосохранение[/]\n")

    check_level_up()
    time.sleep(2)
    return True

def gameover():
    clear()
    console.print()
    console.print(Align.center(Panel.fit(
        "[bold red]💀 GAME OVER 💀[/]\n\n"
        "[white]Ты попался. Суд, приговор, всё кончено.[/]\n\n"
        f"[yellow]Всего миссий: {STATE['total_missions']}[/]\n"
        f"[green]Успешных: {STATE['wins']}[/]\n"
        f"[cyan]Заработано: ${STATE['money']}[/]\n"
        f"[magenta]Уровень: {LEVEL_NAMES[STATE['level']]}[/]\n\n"
        "[dim]Прогресс удалён.[/]",
        border_style="red", padding=(2,4))))
    console.print()
    STATE["deaths"] += 1
    # Удаляем сейв
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    console.print("[dim]Нажми Enter чтобы начать заново...[/]")
    try: console.input()
    except: pass
    reset_game()
    main_menu()

def reset_game():
    global STATE
    STATE.update({
        "hp": 100, "money": 50, "xp": 0, "level": 0,
        "skills": {k: 0 for k in SKILLS.keys()},
        "faction": None, "completed": [], "owned_software": [],
        "equipment": [], "started_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_missions": 0, "deaths": STATE.get("deaths", 0), "wins": 0,
    })

# ═══════════ ЭКРАНЫ ═══════════
def banner():
    clear()
    console.print()
    art = r"""
    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗
    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
    ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                 S I M U L A T O R
    """
    console.print(Align.center(f"[bold bright_green]{art}[/]"))
    console.print(Align.center("[dim]Текстовая RPG хакера в Termux[/]"))
    console.print()

def status_panel():
    lvl_name = LEVEL_NAMES[STATE["level"]]
    faction = FACTIONS.get(STATE["faction"], {}).get("name", "— не в фракции")
    t = Table(box=None, show_header=False, padding=(0,2))
    t.add_column("", style="bold yellow", width=20)
    t.add_column("", width=30)
    t.add_column("", style="bold yellow", width=18)
    t.add_column("", width=20)

    t.add_row("👤 Уровень", lvl_name, "💰 Деньги", f"[green]${STATE['money']}[/]")
    t.add_row("⭐ Опыт", f"[cyan]{STATE['xp']}[/]", "🎯 Миссий", str(STATE['total_missions']))
    t.add_row("🩸 HP", hp_bar(STATE["hp"]), "🏴 Фракция", faction)
    t.add_row("💀 Смертей", str(STATE['deaths']), "🏆 Побед", str(STATE['wins']))
    return Panel(t, title="[bold yellow]┃ ПРОФИЛЬ ┃[/]", border_style="yellow", padding=(0,1))

def skills_panel():
    t = Table(box=SIMPLE_HEAD, border_style="cyan", header_style="bold cyan", padding=(0,2))
    t.add_column("Навык", style="bold cyan", width=20)
    t.add_column("Уровень", justify="right", width=10)
    t.add_column("Описание", style="dim")
    for k, v in STATE["skills"].items():
        s = SKILLS[k]
        t.add_row(s["name"], f"[bright_green]{v}[/]", s["desc"])
    return t

def missions_screen():
    available = get_available_missions()
    if not available:
        console.print("[yellow]⚠ Нет доступных миссий. Прокачай скиллы в магазине.[/]\n")
        return []

    # Сортируем по сложности
    available.sort(key=lambda x: x[1]["diff"])

    t = Table(box=SIMPLE_HEAD, border_style="magenta", header_style="bold magenta", padding=(0,1))
    t.add_column("#", style="bold yellow", width=4, justify="right")
    t.add_column("Миссия", style="white", width=28)
    t.add_column("Цель", style="cyan", width=24)
    t.add_column("Сложность", justify="center", width=10)
    t.add_column("💰", style="green", justify="right", width=10)
    t.add_column("⭐", style="cyan", justify="right", width=8)

    for i, (level, m) in enumerate(available, 1):
        lvl_mark = "🟢" if level == 0 else "🟡" if level == 1 else "🟠" if level == 2 else "🔴"
        diff_str = f"{lvl_mark} {m['diff']}"
        t.add_row(str(i), m["name"], m["target"], diff_str, f"${m['reward']}", str(m['xp']))
    console.print(t)
    console.print()
    return available

def shop_screen():
    t = Table(box=SIMPLE_HEAD, border_style="green", header_style="bold green", padding=(0,1))
    t.add_column("#", style="bold yellow", width=4, justify="right")
    t.add_column("Софт", style="white", width=24)
    t.add_column("Цена", style="green", justify="right", width=10)
    t.add_column("Описание", style="dim")
    t.add_column("Куплен", justify="center", width=8)

    for i, s in enumerate(SHOP_SOFT, 1):
        owned = "✔" if s["id"] in STATE["owned_software"] else ""
        t.add_row(str(i), s["name"], f"${s['price']}", s["desc"], owned)
    console.print(t)
    console.print()

def factions_screen():
    t = Table(box=SIMPLE_HEAD, border_style="magenta", header_style="bold magenta", padding=(0,1))
    t.add_column("#", style="bold yellow", width=4, justify="right")
    t.add_column("Фракция", style="white", width=18)
    t.add_column("Описание", width=44)
    t.add_column("Бонус", style="green", width=24)
    for i, (fid, f) in enumerate(FACTIONS.items(), 1):
        current = "✔" if STATE["faction"] == fid else ""
        t.add_row(str(i), f["name"] + " " + current, f["desc"], f["bonus"])
    console.print(t)
    console.print()

# ═══════════ TAB-COMPLETER ═══════════
COMMANDS = [
    "missions","m","shop","s","status","st","skills","sk",
    "factions","f","join","attack","a","save","load",
    "reset","help","h","q","quit","exit"
]

class RPGComp(Completer):
    def get_completions(self, doc, ev):
        t = doc.text_before_cursor
        if " " in t: return
        for c in sorted(COMMANDS):
            if c.startswith(t.lower()):
                yield Completion(c, start_position=-len(t))

# ═══════════ ГЛАВНОЕ МЕНЮ ═══════════
def main_menu():
    global STATE
    while True:
        banner()
        console.print(status_panel())
        console.print()

        # Подсказки
        c = Table(box=None, show_header=False, padding=(0,2))
        c.add_column("", style="bold yellow", width=20)
        c.add_column("", style="cyan", width=30)
        c.add_column("", style="bold yellow", width=20)
        c.add_column("", style="cyan", width=30)
        c.add_row("[m]issions","📋 Список миссий", "[sh]op","🛒 Магазин")
        c.add_row("[st]atus","👤 Профиль", "[sk]ills","🎯 Скиллы")
        c.add_row("[f]actions","🏴 Фракции", "[s]ave","💾 Сохранить")
        c.add_row("[h]elp","❓ Помощь", "[q]uit","🚪 Выход")
        console.print(Panel(c, title="[bold cyan]⌨  КОМАНДЫ[/]", border_style="cyan", padding=(0,1)))
        console.print()

        prompt_txt = "╰─🎮> "
        try:
            cmd = console.input(f"[bold magenta]{prompt_txt}[/]").strip().lower()
        except (EOFError, KeyboardInterrupt):
            save_game(silent=True)
            console.print("\n[dim]💾 Автосохранение при выходе. До связи! 🖖[/]")
            break

        if not cmd: continue

        if cmd in ("q","quit","exit"):
            save_game(silent=True)
            console.print("[dim]💾 Автосохранение. До связи! 🖖[/]")
            break

        elif cmd in ("missions","m"):
            avail = missions_screen()
            if avail:
                try:
                    ch = console.input("[bold magenta]Номер миссии (Enter — назад)> [/]").strip()
                except: continue
                if ch.isdigit() and 1 <= int(ch) <= len(avail):
                    level, m = avail[int(ch)-1]
                    do_mission(level, m)

        elif cmd in ("shop","sh","s"):
            shop_screen()
            try:
                ch = console.input("[bold magenta]Номер для покупки (Enter — назад)> [/]").strip()
            except: continue
            if ch.isdigit() and 1 <= int(ch) <= len(SHOP_SOFT):
                item = SHOP_SOFT[int(ch)-1]
                if item["id"] in STATE["owned_software"]:
                    console.print("[yellow]Уже куплено[/]\n"); time.sleep(1); continue
                if STATE["money"] < item["price"]:
                    console.print(f"[red]❌ Не хватает ${item['price'] - STATE['money']}[/]\n"); time.sleep(1.5); continue
                STATE["money"] -= item["price"]
                STATE["owned_software"].append(item["id"])
                for skill, val in item["effect"].items():
                    STATE["skills"][skill] = STATE["skills"].get(skill, 0) + val
                console.print(f"[green]✔ Куплено: {item['name']}[/]\n")
                save_game(silent=True)
                time.sleep(1.5)

        elif cmd in ("status","st"):
            clear()
            console.print()
            console.print(status_panel())
            console.print()
            console.print(skills_panel())
            console.print()
            console.input("[dim]Enter — назад[/] ")

        elif cmd in ("skills","sk"):
            clear()
            console.print()
            console.print(Panel.fit("[bold cyan]🎯 СКИЛЛЫ[/]", border_style="cyan"))
            console.print()
            console.print(skills_panel())
            console.print()
            console.input("[dim]Enter — назад[/] ")

        elif cmd in ("factions","f"):
            clear()
            console.print()
            console.print(Panel.fit("[bold magenta]🏴 ФРАКЦИИ[/]", border_style="magenta"))
            console.print()
            factions_screen()
            try:
                ch = console.input("[bold magenta]Номер для вступления (Enter — назад)> [/]").strip()
            except: continue
            if ch.isdigit() and 1 <= int(ch) <= len(FACTIONS):
                fid = list(FACTIONS.keys())[int(ch)-1]
                if STATE["faction"] == fid:
                    console.print("[yellow]Уже в этой фракции[/]\n"); time.sleep(1); continue
                STATE["faction"] = fid
                console.print(f"[green]✔ Вступил в {FACTIONS[fid]['name']}[/]\n")
                save_game(silent=True)
                time.sleep(1.5)

        elif cmd in ("save","sv"):
            save_game()

        elif cmd in ("load","l"):
            if load_game():
                console.print("[green]✔ Загрузка успешна[/]\n"); time.sleep(1)
            else:
                console.print("[red]❌ Сейв не найден[/]\n"); time.sleep(1)

        elif cmd in ("reset","r"):
            try:
                a = console.input("[red bold]Точно сбросить весь прогресс? (yes/n)> [/]").strip()
            except: continue
            if a == "yes":
                reset_game()
                if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
                console.print("[green]✔ Сброшено[/]\n"); time.sleep(1)

        elif cmd in ("help","h"):
            clear()
            console.print()
            console.print(Panel(
                Group(
                    Text("🎮 HACKER RPG — помощь", style="bold bright_green"),
                    Text(""),
                    Text("🎯 Цель: пройти все миссии, заработать $, стать LEGEND.", style="white"),
                    Text(""),
                    Text("📋 missions — список контрактов", style="cyan"),
                    Text("🛒 shop — купить софт (+ скиллы)", style="cyan"),
                    Text("🏴 factions — вступить во фракцию (+ бонусы)", style="cyan"),
                    Text("💾 save — сохранить прогресс", style="cyan"),
                    Text("💀 Если HP = 0 или тебя поймают — GAME OVER, прогресс стирается.", style="red"),
                    Text(""),
                    Text("⚙ Автосохранение после каждой успешной миссии.", style="dim"),
                ),
                border_style="bright_green", padding=(1,2)))
            console.print()
            console.input("[dim]Enter — назад[/] ")

        else:
            console.print(f"[red]❌ Неизвестно: {cmd}. Набери 'h' для помощи[/]\n")
            time.sleep(1)

# ═══════════ ЗАПУСК ═══════════
def main():
    global STATE
    clear()

    # Загрузка или новая игра
    if os.path.exists(SAVE_FILE):
        banner()
        console.print(Panel.fit(
            f"[bold green]💾 Найден сохранённый прогресс[/]\n\n"
            f"Уровень: {LEVEL_NAMES[STATE.get('level',0)]}\n"
            f"Деньги: ${STATE.get('money',0)}\n"
            f"Миссий пройдено: {STATE.get('total_missions',0)}",
            border_style="green"))
        console.print()
        console.print("  [cyan]1[/])  Продолжить")
        console.print("  [cyan]2[/])  Новая игра")
        console.print()
        try:
            ch = console.input("[bold magenta]Выбор> [/]").strip()
        except: ch = "1"
        if ch == "2":
            reset_game()
        else:
            load_game()
    else:
        reset_game()
        STATE["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    main_menu()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано.[/]")
        save_game(silent=True)
