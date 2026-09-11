#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NOTES — заметки с тегами, поиском, экспортом + Tab-автодополнение"""

import os, sys, json, re, subprocess, time
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

console = Console()
NOTES_FILE  = os.path.expanduser("~/.notes.json")
EXPORT_DIR  = os.path.expanduser("~/notes_export")

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

# ═══════════ ХРАНИЛИЩЕ ═══════════
def load_notes():
    if not os.path.exists(NOTES_FILE):
        return {"next_id": 1, "notes": []}
    try:
        with open(NOTES_FILE, encoding="utf-8") as f:
            d = json.load(f)
            d.setdefault("next_id", 1)
            d.setdefault("notes", [])
            return d
    except Exception:
        return {"next_id": 1, "notes": []}

def save_notes(data):
    try:
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")

# ═══════════ ПАРСИНГ ═══════════
def parse_new(text):
    """new Заголовок | Тело заметки #тег1 #тег2"""
    # Теги ищем в конце
    tags = re.findall(r"#(\S+)", text)
    text_no_tags = re.sub(r"#\S+", "", text).strip()
    if "|" in text_no_tags:
        title, body = text_no_tags.split("|", 1)
    else:
        title = text_no_tags
        body = ""
    return {"title": title.strip(), "body": body.strip(), "tags": tags}

def edit_note_interactive(note):
    """Интерактивное редактирование через мультистрочный ввод"""
    console.print(Text(f"  ✏ Текущий заголовок: {note['title']}", style=WHITE))
    try:
        new_title = console.input("[bold magenta]Новый заголовок (Enter — оставить)> [/]").strip()
        if new_title: note["title"] = new_title
    except (EOFError, KeyboardInterrupt):
        console.print(Text("  Отменено", style=YELLOW)); return False

    console.print(Text("  Текущее тело:", style=WHITE))
    console.print(Panel(note.get("body","") or "[dim](пусто)[/]", border_style=GRAY))
    console.print(Text("  Введи новый текст (Enter на пустой строке — конец):", style=CYAN))
    lines = []
    try:
        while True:
            line = console.input("[bold magenta]...[/] ")
            if not line: break
            lines.append(line)
    except (EOFError, KeyboardInterrupt):
        pass
    if lines:
        note["body"] = "\n".join(lines)

    try:
        new_tags = console.input(f"[bold magenta]Теги через пробел (текущие: {', '.join(note.get('tags',[])) or '—'})> [/]").strip()
        if new_tags:
            note["tags"] = [t.lstrip("#") for t in new_tags.split()]
    except (EOFError, KeyboardInterrupt):
        pass
    note["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return True

# ═══════════ ЭКСПОРТ ═══════════
def export_notes(fmt="md"):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    data = load_notes()
    notes = data["notes"]
    if not notes:
        console.print(Text("  ⚠ Нечего экспортировать", style=YELLOW)); return

    if fmt == "json":
        path = os.path.join(EXPORT_DIR, f"notes_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
    elif fmt == "md":
        path = os.path.join(EXPORT_DIR, f"notes_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Мои заметки\n\n_Экспорт: {datetime.now().strftime('%d.%m.%Y %H:%M')}_\n\n")
            for n in notes:
                f.write(f"## #{n['id']} — {n['title']}\n\n")
                if n.get("tags"):
                    f.write("**Теги:** " + " ".join(f"`#{t}`" for t in n["tags"]) + "\n\n")
                if n.get("body"):
                    f.write(n["body"] + "\n\n")
                f.write(f"_Создано: {n.get('created','—')}_\n\n---\n\n")
    elif fmt == "txt":
        path = os.path.join(EXPORT_DIR, f"notes_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
        with open(path, "w", encoding="utf-8") as f:
            for n in notes:
                f.write(f"=== #{n['id']} — {n['title']} ===\n")
                if n.get("tags"): f.write("Теги: " + ", ".join(n["tags"]) + "\n")
                if n.get("body"): f.write(n["body"] + "\n")
                f.write("\n")
    else:
        console.print(Text(f"  ❌ Неизвестный формат: {fmt}", style=RED)); return

    console.print(Text(f"  ✔ Экспортировано: {path}", style=GREEN_BRIGHT))

# ═══════════ РИСОВКА ═══════════
def clear(): os.system("clear")

def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("═" * 60, style=GREEN_DIM))
    return Group(*lines)

def stats_panel(notes):
    total = len(notes)
    tags_count = {}
    for n in notes:
        for t in n.get("tags", []):
            tags_count[t] = tags_count.get(t, 0) + 1
    top_tags = sorted(tags_count.items(), key=lambda x: -x[1])[:5]
    top_s = " ".join(f"#{t}({c})" for t, c in top_tags) or "[dim]нет[/]"

    t = Table(box=None, show_header=False, padding=(0, 3))
    t.add_column(""); t.add_column("")
    t.add_row(f"📝 Заметок: [bold]{total}[/]",
              f"🏷 Тегов: [bold]{len(tags_count)}[/]")
    t.add_row(f"🔝 Топ теги: {top_s}", "")
    return t

def notes_table(notes, filter_mode=None):
    """filter_mode: None (все), 'tag:xxx', search-строка"""
    shown = notes
    if filter_mode and filter_mode.startswith("tag:"):
        tag = filter_mode[4:].lower()
        shown = [n for n in notes if tag in [x.lower() for x in n.get("tags", [])]]
    elif filter_mode:
        q = filter_mode.lower()
        shown = [n for n in notes
                 if q in n["title"].lower() or q in n.get("body","").lower()
                 or any(q in t.lower() for t in n.get("tags", []))]

    shown = sorted(shown, key=lambda x: x.get("updated") or x.get("created",""), reverse=True)

    if not shown:
        console.print(Text(f"  📭 Заметок нет (фильтр: {filter_mode or 'нет'})", style=f"dim {GRAY}"))
        console.print()
        return

    t = Table(box=box.SIMPLE_HEAD, border_style=CYAN,
              header_style=f"bold {CYAN}", padding=(0, 1), expand=True)
    t.add_column("ID", style=f"bold {YELLOW}", width=4, justify="right")
    t.add_column("Заголовок", style=WHITE)
    t.add_column("Теги", style=MAGENTA, width=20)
    t.add_column("Обновлено", style=GRAY, width=17)

    for n in shown:
        title = n["title"][:55]
        tags_s = " ".join(f"#{x}" for x in n.get("tags", []))[:20] or "[dim]—[/]"
        upd = n.get("updated") or n.get("created", "—")
        t.add_row(str(n["id"]), title, tags_s, upd[:16])
    console.print(t)
    console.print()

def commands_panel():
    t = Table(box=box.DOUBLE_EDGE, border_style="black",
              show_header=False, padding=(0, 2))
    t.add_column("Команда", style="bold yellow", width=26, justify="right")
    t.add_column("Действие", style="white")
    t.add_row("[cyan]new <заголовок> | <тело> #tag[/]", "➕ Новая заметка")
    t.add_row("[cyan]show <id>[/]",     "👁 Показать заметку")
    t.add_row("[cyan]edit <id>[/]",     "✏ Редактировать")
    t.add_row("[cyan]del <id>[/]",      "🗑 Удалить")
    t.add_row("[cyan]tag <тег>[/]",     "🏷 Фильтр по тегу")
    t.add_row("[cyan]search <текст>[/]", "🔍 Поиск по всем полям")
    t.add_row("[cyan]tags[/]",          "📋 Список всех тегов")
    t.add_row("[cyan]reset[/]",         "↩ Сбросить фильтр")
    t.add_row("[cyan]export md|txt|json[/]", "💾 Экспорт в ~/notes_export/")
    t.add_row("[cyan]q[/]",             "🚪 Выход")
    console.print(Panel(t, title="[bold green]⌨  КОМАНДЫ  (Tab — автодополнение)[/]",
                        border_style="black"))
    console.print()

# ═══════════ TAB-COMPLETER ═══════════
class NotesCompleter(Completer):
    def __init__(self, get_data):
        self.get_data = get_data

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        if not words or (len(words) == 1 and not text.endswith(" ")):
            partial = words[0] if words else ""
            commands = ["new","show","edit","del","tag","search","tags",
                        "reset","export","clear","help","q"]
            for c in commands:
                if c.startswith(partial.lower()):
                    yield Completion(c, start_position=-len(partial))
            return

        cmd = words[0].lower()
        partial = words[-1] if not text.endswith(" ") else ""

        if cmd in ("show","edit","del"):
            data = self.get_data()
            for n in data["notes"]:
                sid = str(n["id"])
                if sid.startswith(partial):
                    label = f'{sid}  {n["title"][:55]}'
                    yield Completion(sid, start_position=-len(partial),
                                     display=label)
            return

        if cmd == "tag":
            data = self.get_data()
            tags = set()
            for n in data["notes"]:
                tags.update(n.get("tags", []))
            for t in sorted(tags):
                if t.lower().startswith(partial.lower()):
                    yield Completion(t, start_position=-len(partial))
            return

        if cmd == "export":
            for m in ("md","txt","json"):
                if m.startswith(partial.lower()):
                    yield Completion(m, start_position=-len(partial))

# ═══════════ MAIN ═══════════
def main():
    data = load_notes()
    current_filter = None

    style = Style.from_dict({
        "prompt": "bold ansibrightmagenta",
        "completion-menu.completion": "bg:#000000 #00ff88",
        "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
        "completion-menu.meta.completion": "bg:#000000 #557755",
        "completion-menu.meta.completion.current": "bg:#aa00aa #000000",
    })

    while True:
        data = load_notes()
        notes = data["notes"]

        clear()
        console.print()
        console.print(title_block("N O T E S", "Terminal Argonov  •  Notes"))
        console.print()
        console.print(stats_panel(notes))
        console.print()

        if current_filter:
            console.print(f"[dim]Фильтр: [bold]{current_filter}[/][/]")
            console.print()

        notes_table(notes, filter_mode=current_filter)
        commands_panel()

        session = PromptSession(
            completer=NotesCompleter(lambda: load_notes()),
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

        if c == "new":
            if not arg:
                console.print(Text("  ❌ new <заголовок> | <тело> #тег", style=RED))
                time.sleep(1); continue
            p = parse_new(arg)
            if not p["title"]:
                console.print(Text("  ❌ Пустой заголовок", style=RED)); time.sleep(1); continue
            note = {
                "id": data["next_id"],
                "title": p["title"],
                "body": p["body"],
                "tags": p["tags"],
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            data["next_id"] += 1
            data["notes"].append(note)
            save_notes(data)
            console.print(Text(f"  ✔ Заметка #{note['id']} создана", style=GREEN_BRIGHT))
            time.sleep(0.8); continue

        if c == "show":
            if not arg.isdigit():
                console.print(Text("  ❌ show <id>", style=RED)); time.sleep(1); continue
            tid = int(arg)
            note = next((n for n in data["notes"] if n["id"] == tid), None)
            if not note:
                console.print(Text(f"  ❌ #{tid} не найдена", style=RED)); time.sleep(1); continue
            clear()
            console.print()
            console.print(title_block(f"#{note['id']}  {note['title']}"))
            console.print()
            if note.get("tags"):
                console.print(Text("🏷 " + " ".join(f"#{t}" for t in note["tags"]), style=MAGENTA))
                console.print()
            body = note.get("body") or "[dim](пусто)[/]"
            try:
                console.print(Markdown(body))
            except Exception:
                console.print(body)
            console.print()
            console.print(Text(f"📅 Создано: {note.get('created','—')}", style=GRAY))
            console.print(Text(f"🕐 Обновлено: {note.get('updated','—')}", style=GRAY))
            console.print()
            try: console.input("[dim]Enter — назад[/] ")
            except (EOFError, KeyboardInterrupt): pass
            continue

        if c in ("edit","del"):
            if not arg.isdigit():
                console.print(Text(f"  ❌ {c} <id>", style=RED)); time.sleep(1); continue
            tid = int(arg)
            note = next((n for n in data["notes"] if n["id"] == tid), None)
            if not note:
                console.print(Text(f"  ❌ #{tid} не найдена", style=RED)); time.sleep(1); continue
            if c == "edit":
                if edit_note_interactive(note):
                    save_notes(data)
                    console.print(Text(f"  ✔ Заметка #{tid} обновлена", style=GREEN_BRIGHT))
                time.sleep(1); continue
            if c == "del":
                try:
                    ans = console.input(f"[bold red]Удалить #{tid} «{note['title'][:40]}»? (y/N)> [/]").strip().lower()
                    if ans == "y":
                        data["notes"] = [n for n in data["notes"] if n["id"] != tid]
                        save_notes(data)
                        console.print(Text(f"  🗑 #{tid} удалена", style=RED))
                    else:
                        console.print(Text("  Отменено", style=YELLOW))
                except (EOFError, KeyboardInterrupt):
                    console.print(Text("  Отменено", style=YELLOW))
                time.sleep(0.8); continue

        if c == "tag":
            if not arg:
                console.print(Text("  ❌ tag <тег>", style=RED)); time.sleep(1); continue
            current_filter = f"tag:{arg.lstrip('#')}"
            console.print(Text(f"  🏷 Фильтр по тегу: {arg}", style=GREEN_BRIGHT))
            time.sleep(0.5); continue

        if c == "search":
            if not arg:
                console.print(Text("  ❌ search <текст>", style=RED)); time.sleep(1); continue
            current_filter = arg
            console.print(Text(f"  🔍 Поиск: {arg}", style=GREEN_BRIGHT))
            time.sleep(0.5); continue

        if c == "tags":
            tags_count = {}
            for n in data["notes"]:
                for t in n.get("tags", []):
                    tags_count[t] = tags_count.get(t, 0) + 1
            if not tags_count:
                console.print(Text("  ⚠ Тегов нет", style=YELLOW)); time.sleep(1); continue
            clear()
            console.print(); console.print(title_block("🏷 ВСЕ ТЕГИ")); console.print()
            t = Table(box=box.SIMPLE_HEAD, border_style=MAGENTA,
                      header_style=f"bold {MAGENTA}", padding=(0, 2))
            t.add_column("Тег", style=MAGENTA)
            t.add_column("Заметок", style=CYAN, justify="right", width=10)
            for tg, cnt in sorted(tags_count.items(), key=lambda x: -x[1]):
                t.add_row(f"#{tg}", str(cnt))
            console.print(t); console.print()
            try: console.input("[dim]Enter — назад[/] ")
            except (EOFError, KeyboardInterrupt): pass
            continue

        if c == "reset":
            current_filter = None
            console.print(Text("  ↩ Фильтр сброшен", style=GREEN_BRIGHT))
            time.sleep(0.5); continue

        if c == "export":
            fmt = (arg or "md").lower()
            export_notes(fmt)
            time.sleep(1.2); continue

        if c in ("help","h","?"):
            console.print(Text("  Tab — автодополнение. Пример: new Рецепт блинов | 2 яйца, мука, молоко #кухня", style=CYAN))
            time.sleep(2); continue

        console.print(Text(f"  ❌ Неизвестно: {c}", style=RED))
        time.sleep(0.6)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print(Text("\n Прервано.", style=f"dim {GREEN_DIM}"))
