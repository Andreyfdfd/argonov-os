#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TODO — трекер задач с Tab-автодополнением и уведомлениями"""

import os, sys, json, re, subprocess, time
from datetime import datetime, timedelta
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

console = Console()
TODO_FILE = os.path.expanduser("~/.todo.json")

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"
ORANGE = "dark_orange"

PRIORITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🟢"}
PRIORITY_LABEL = {"high": "Высокий", "medium": "Средний", "low": "Низкий"}
PRIORITY_COLOR = {"high": RED, "medium": YELLOW, "low": GREEN_BRIGHT}

# ═══════════ ХРАНИЛИЩЕ ═══════════
def load_todo():
    if not os.path.exists(TODO_FILE):
        return {"next_id": 1, "tasks": []}
    try:
        with open(TODO_FILE, encoding="utf-8") as f:
            d = json.load(f)
            d.setdefault("next_id", 1)
            d.setdefault("tasks", [])
            return d
    except Exception:
        return {"next_id": 1, "tasks": []}

def save_todo(data):
    try:
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

# ═══════════ ПАРСИНГ ═══════════
def parse_date(s):
    """Поддержка: today, tomorrow, +3d, +2h, +1w, 15.09, 15.09.2026, 15.09 18:00"""
    s = s.lower().strip()
    now = datetime.now()
    if s in ("today", "сегодня"):     return now.strftime("%Y-%m-%d 23:59")
    if s in ("tomorrow", "завтра"):   return (now + timedelta(days=1)).strftime("%Y-%m-%d 23:59")
    m = re.match(r"\+(\d+)([dhmw])", s)
    if m:
        n = int(m.group(1)); u = m.group(2)
        delta = {"d": timedelta(days=n), "h": timedelta(hours=n),
                 "m": timedelta(minutes=n), "w": timedelta(weeks=n)}[u]
        return (now + delta).strftime("%Y-%m-%d %H:%M")
    m = re.match(r"(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?(?:\s+(\d{1,2}):(\d{2}))?$", s)
    if m:
        d = int(m.group(1)); mo = int(m.group(2))
        y  = int(m.group(3)) if m.group(3) else now.year
        h  = int(m.group(4)) if m.group(4) else 23
        mi = int(m.group(5)) if m.group(5) else 59
        try:
            return datetime(y, mo, d, h, mi).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return None
    return None

def parse_add(text):
    """add Купить молоко !high @tomorrow #покупки"""
    title_parts = []; priority = "medium"; deadline = None; tags = []
    for w in text.split():
        if w.startswith("!"):
            p = w[1:].lower()
            if p in ("h","high","1","в","высокий"): priority = "high"
            elif p in ("m","mid","medium","2","с","средний"): priority = "medium"
            elif p in ("l","low","3","н","низкий"): priority = "low"
        elif w.startswith("@") and not deadline:
            deadline = parse_date(w[1:])
        elif w.startswith("#") and len(w) > 1:
            tags.append(w[1:])
        else:
            title_parts.append(w)
    return {"title": " ".join(title_parts).strip(),
            "priority": priority, "deadline": deadline, "tags": tags}

# ═══════════ ДАТЫ / ПРИОРИТЕТЫ ═══════════
def is_overdue(task):
    if task.get("done") or not task.get("deadline"): return False
    try:
        return datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M") < datetime.now()
    except Exception:
        return False

def is_today(task):
    if task.get("done") or not task.get("deadline"): return False
    try:
        d = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
        return d.date() == datetime.now().date()
    except Exception:
        return False

def is_soon(task, hours=24):
    if task.get("done") or not task.get("deadline"): return False
    try:
        d = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
        delta = d - datetime.now()
        return timedelta(0) <= delta <= timedelta(hours=hours)
    except Exception:
        return False

def fmt_deadline(s):
    if not s: return "—"
    try:
        d = datetime.strptime(s, "%Y-%m-%d %H:%M")
        now = datetime.now()
        delta = d - now
        # Короткий формат
        date_s = d.strftime("%d.%m %H:%M")
        if d.date() == now.date():   date_s = f"сегодня {d.strftime('%H:%M')}"
        elif d.date() == (now + timedelta(days=1)).date(): date_s = f"завтра {d.strftime('%H:%M')}"
        if delta.total_seconds() < 0:
            return f"❗ {date_s}"
        if delta.total_seconds() < 3600:
            return f"⏰ {date_s} ({int(delta.total_seconds()//60)} мин)"
        if delta < timedelta(days=1):
            return f"⏰ {date_s}"
        return date_s
    except Exception:
        return s

# ═══════════ УВЕДОМЛЕНИЯ ═══════════
def notify(task):
    """Отправить уведомление через termux-notification"""
    title = f"📌 TODO #{task['id']}: {task['title']}"
    content = f"Приоритет: {PRIORITY_LABEL.get(task['priority'],'—')}"
    if task.get("deadline"): content += f"\nДедлайн: {fmt_deadline(task['deadline'])}"
    if task.get("tags"):     content += f"\nТеги: {', '.join(task['tags'])}"
    try:
        subprocess.run(["termux-notification",
            "--title", title, "--content", content,
            "--id", str(task["id"])], check=False)
        return True
    except Exception:
        return False

# ═══════════ РИСОВКА ═══════════
def clear(): console.clear()

def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("═"*60, style=GREEN_DIM))
    return Group(*lines)

def stats_panel(tasks):
    total = len(tasks)
    active = sum(1 for t in tasks if not t.get("done"))
    done = sum(1 for t in tasks if t.get("done"))
    overdue = sum(1 for t in tasks if is_overdue(t))
    today = sum(1 for t in tasks if is_today(t))
    t = Table(box=None, show_header=False, padding=(0, 3))
    for _ in range(4): t.add_column("")
    t.add_row(f"📋 Всего [bold]{total}[/]", f"⏳ Активных [bold]{active}[/]",
              f"✅ Выполнено [bold]{done}[/]", f"❗ Просрочено [bold]{overdue}[/]")
    t.add_row(f"📅 Сегодня [bold]{today}[/]", "", "", "")
    return t

def tasks_table(tasks, filter_mode="active"):
    """filter_mode: active, done, all, today, overdue"""
    now = datetime.now()
    if filter_mode == "active":
        shown = [t for t in tasks if not t.get("done")]
    elif filter_mode == "done":
        shown = [t for t in tasks if t.get("done")]
    elif filter_mode == "today":
        shown = [t for t in tasks if is_today(t)]
    elif filter_mode == "overdue":
        shown = [t for t in tasks if is_overdue(t)]
    else:
        shown = tasks

    # Сортировка: активные → по дедлайну → по приоритету
    def sort_key(t):
        pri = {"high": 0, "medium": 1, "low": 2}.get(t.get("priority"), 1)
        d = t.get("deadline") or "9999-99-99 99:99"
        return (t.get("done", False), d, pri)
    shown = sorted(shown, key=sort_key)

    if not shown:
        console.print(Text(f"  📭 Задач нет (фильтр: {filter_mode})", style=f"dim {GRAY}"))
        console.print()
        return

    t = Table(box=box.SIMPLE_HEAD, border_style=CYAN,
              header_style=f"bold {CYAN}", padding=(0, 1), expand=True)
    t.add_column("ID", style=f"bold {YELLOW}", width=4, justify="right")
    t.add_column("✓",  width=3, justify="center")
    t.add_column("!",  width=3, justify="center")
    t.add_column("Задача", style=WHITE)
    t.add_column("Дедлайн", width=22)
    t.add_column("Теги", style=MAGENTA, width=18)

    for task in shown:
        mark = "[green]✔[/]" if task.get("done") else "[ ]"
        pri_icon = PRIORITY_ICON.get(task.get("priority"), "⚪")
        title = task["title"]
        if task.get("done"):
            title = f"[dim strikethrough]{title}[/]"
        deadline_s = fmt_deadline(task.get("deadline"))
        if is_overdue(task):
            deadline_s = f"[bold {RED}]{deadline_s}[/]"
        elif is_soon(task):
            deadline_s = f"[{YELLOW}]{deadline_s}[/]"
        else:
            deadline_s = f"[{GRAY}]{deadline_s}[/]"
        tags_s = " ".join(f"#{x}" for x in task.get("tags", []))[:18] or "[dim]—[/]"
        t.add_row(str(task["id"]), mark, pri_icon, title, deadline_s, tags_s)
    console.print(t)
    console.print()

def commands_panel():
    t = Table(box=box.DOUBLE_EDGE, border_style="green",
              show_header=False, padding=(0, 2))
    t.add_column("Команда", style="bold yellow", width=26, justify="right")
    t.add_column("Действие", style="white")
    t.add_row("[cyan]add <текст> !high @tomorrow #tag[/]", "➕ Добавить задачу")
    t.add_row("[cyan]done <id>[/]",     "✅ Отметить выполненной")
    t.add_row("[cyan]undone <id>[/]",   "↩ Вернуть в работу")
    t.add_row("[cyan]del <id>[/]",      "🗑 Удалить задачу")
    t.add_row("[cyan]edit <id>[/]",     "✏ Изменить задачу")
    t.add_row("[cyan]notify <id>[/]",   "🔔 Отправить уведомление")
    t.add_row("[cyan]notify-all[/]",    "🔔 Уведомить о всех активных")
    t.add_row("[cyan]filter <mode>[/]", "🔎 filter: active/done/all/today/overdue")
    t.add_row("[cyan]clear-done[/]",    "🧹 Удалить все выполненные")
    t.add_row("[cyan]q[/]",             "🚪 Выход")
    console.print(Panel(t, title="[bold green]⌨  КОМАНДЫ  (Tab — автодополнение)[/]",
                        border_style="green"))
    console.print()

# ═══════════ TAB-COMPLETER ═══════════
class TodoCompleter(Completer):
    def __init__(self, get_tasks):
        self.get_tasks = get_tasks

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        # Первое слово — команда
        if not words or (len(words) == 1 and not text.endswith(" ")):
            partial = words[0] if words else ""
            commands = [
                "add","done","undone","del","edit","notify","notify-all",
                "filter","clear-done","clear","help","q",
            ]
            for c in commands:
                if c.startswith(partial.lower()):
                    yield Completion(c, start_position=-len(partial))
            return
        cmd = words[0].lower()
        partial = words[-1] if not text.endswith(" ") else ""

        if cmd in ("done","undone","del","edit","notify"):
            tasks = self.get_tasks()
            for t in tasks:
                sid = str(t["id"])
                if sid.startswith(partial):
                    label = f'{sid}  {t["title"][:50]}'
                    yield Completion(sid, start_position=-len(partial),
                                     display=label, display_meta=PRIORITY_LABEL.get(t.get("priority"),""))
            return

        if cmd == "filter":
            for m in ("active","done","all","today","overdue"):
                if m.startswith(partial.lower()):
                    yield Completion(m, start_position=-len(partial))

# ═══════════ MAIN ═══════════
def main():
    data = load_todo()
    current_filter = "active"

    style = Style.from_dict({
        "prompt": "bold ansibrightmagenta",
        "completion-menu.completion": "bg:#000000 #00ff88",
        "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
        "completion-menu.meta.completion": "bg:#000000 #557755",
        "completion-menu.meta.completion.current": "bg:#aa00aa #000000",
    })

    while True:
        data = load_todo()
        tasks = data["tasks"]

        clear()
        console.print()
        console.print(title_block("T O D O", "Terminal Argonov  •  Task Manager"))
        console.print()
        console.print(stats_panel(tasks))
        console.print()

        # Напоминание о близких
        soon = [t for t in tasks if (is_overdue(t) or is_today(t) or is_soon(t)) and not t.get("done")]
        if soon:
            console.print(f"[bold {YELLOW}]⏰ Требуют внимания ({len(soon)}):[/]")
            for t in soon[:3]:
                mark = "❗" if is_overdue(t) else "⏰"
                console.print(f"  {mark} [bold]#{t['id']}[/] {t['title'][:55]}  [dim]{fmt_deadline(t.get('deadline'))}[/]")
            console.print()

        console.print(f"[dim]Фильтр: [bold]{current_filter}[/][/]")
        console.print()
        tasks_table(tasks, filter_mode=current_filter)
        commands_panel()

        session = PromptSession(
            completer=TodoCompleter(lambda: load_todo()["tasks"]),
            style=style, complete_while_typing=True)
        try:
            cmd = session.prompt(HTML("<prompt>╰─❯</prompt> ")).strip()
        except (EOFError, KeyboardInterrupt):
            console.print(Text("\n До связи. 🖖", style=f"dim {GREEN_DIM}"))
            break

        if not cmd: continue
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if c in ("q","exit","quit","выход"):
            console.print(Text(" До связи. 🖖", style=f"dim {GREEN_DIM}")); break
        if c == "clear": continue

        if c == "add":
            if not arg:
                console.print(Text("  ❌ add <текст> [!high] [@tomorrow] [#tag]", style=RED))
                time.sleep(1); continue
            p = parse_add(arg)
            if not p["title"]:
                console.print(Text("  ❌ Пустой заголовок", style=RED)); time.sleep(1); continue
            task = {
                "id": data["next_id"],
                "title": p["title"],
                "priority": p["priority"],
                "deadline": p["deadline"],
                "tags": p["tags"],
                "done": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            data["next_id"] += 1
            data["tasks"].append(task)
            save_todo(data)
            console.print(Text(f"  ✔ Добавлено #{task['id']}: {task['title']}", style=GREEN_BRIGHT))
            if task["deadline"]:
                console.print(Text(f"     📅 {fmt_deadline(task['deadline'])}", style=YELLOW))
            time.sleep(0.8); continue

        if c in ("done","undone","del","edit","notify"):
            if not arg.isdigit():
                console.print(Text(f"  ❌ {c} <id>", style=RED)); time.sleep(1); continue
            tid = int(arg)
            task = next((t for t in data["tasks"] if t["id"] == tid), None)
            if not task:
                console.print(Text(f"  ❌ Задача #{tid} не найдена", style=RED)); time.sleep(1); continue

            if c == "done":
                task["done"] = True
                save_todo(data)
                console.print(Text(f"  ✅ #{tid} выполнено", style=GREEN_BRIGHT))
            elif c == "undone":
                task["done"] = False
                save_todo(data)
                console.print(Text(f"  ↩ #{tid} возвращено в работу", style=YELLOW))
            elif c == "del":
                data["tasks"] = [t for t in data["tasks"] if t["id"] != tid]
                save_todo(data)
                console.print(Text(f"  🗑 #{tid} удалено", style=RED))
            elif c == "edit":
                console.print(Text(f"  ✏ Текущий: {task['title']}", style=WHITE))
                try:
                    new_title = console.input("[bold magenta]Новый заголовок (Enter — оставить)> [/]").strip()
                    if new_title: task["title"] = new_title
                    new_pri = console.input("[bold magenta]Приоритет (h/m/l, Enter — оставить)> [/]").strip().lower()
                    if new_pri in ("h","high","1"): task["priority"] = "high"
                    elif new_pri in ("m","mid","2"): task["priority"] = "medium"
                    elif new_pri in ("l","low","3"): task["priority"] = "low"
                    new_dl = console.input("[bold magenta]Дедлайн (@tomorrow, @+3d, Enter — оставить)> [/]").strip()
                    if new_dl.startswith("@"):
                        pd = parse_date(new_dl[1:])
                        if pd: task["deadline"] = pd
                    save_todo(data)
                    console.print(Text(f"  ✔ #{tid} обновлено", style=GREEN_BRIGHT))
                except (EOFError, KeyboardInterrupt):
                    console.print(Text("  Отменено", style=YELLOW))
            elif c == "notify":
                if notify(task):
                    console.print(Text(f"  🔔 Уведомление отправлено: {task['title']}", style=GREEN_BRIGHT))
                else:
                    console.print(Text("  ⚠ termux-notification не сработал (установлен ли Termux:API?)", style=YELLOW))
            time.sleep(0.8); continue

        if c == "notify-all":
            active = [t for t in data["tasks"] if not t.get("done")]
            if not active:
                console.print(Text("  ⚠ Нет активных задач", style=YELLOW)); time.sleep(1); continue
            cnt = 0
            for t in active[:10]:
                if notify(t): cnt += 1
                time.sleep(0.3)
            console.print(Text(f"  🔔 Отправлено уведомлений: {cnt}", style=GREEN_BRIGHT))
            time.sleep(1); continue

        if c == "filter":
            if arg in ("active","done","all","today","overdue"):
                current_filter = arg
                console.print(Text(f"  🔎 Фильтр: {arg}", style=GREEN_BRIGHT))
                time.sleep(0.5)
            else:
                console.print(Text("  ❌ filter: active/done/all/today/overdue", style=RED))
                time.sleep(1)
            continue

        if c == "clear-done":
            before = len(data["tasks"])
            data["tasks"] = [t for t in data["tasks"] if not t.get("done")]
            save_todo(data)
            removed = before - len(data["tasks"])
            console.print(Text(f"  🧹 Удалено выполненных: {removed}", style=GREEN_BRIGHT))
            time.sleep(0.8); continue

        if c in ("help","h","?"):
            console.print(Text("  Tab — автодополнение. Пример: add Купить хлеб !high @tomorrow #покупки", style=CYAN))
            time.sleep(1.5); continue

        console.print(Text(f"  ❌ Неизвестно: {c}", style=RED))
        time.sleep(0.6)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print(Text("\n Прервано.", style=f"dim {GREEN_DIM}"))
