#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Music Library v6 — Terminal Argonov + live прогресс + Tab-автодополнение"""

import os, sys, json, random, subprocess, time
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.markup import escape
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

console = Console()
CACHE_FILE = os.path.expanduser("~/music_cache/library.json")
PAGE_SIZE = 15

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; ORANGE = "dark_orange"; PURPLE = "medium_purple1"
WHITE = "bright_white"; GRAY = "grey50"

GENRE_COLORS = {
    "rock":"bright_red","metal":"bright_red","hardcore":"bright_red","punk":"bright_red",
    "pop":"bright_yellow","dance":"bright_yellow","disco":"bright_yellow",
    "hip-hop":"dark_orange","hip hop":"dark_orange","rap":"dark_orange","r&b":"dark_orange",
    "electronic":"bright_blue","edm":"bright_blue","house":"bright_blue","techno":"bright_blue",
    "anime":"medium_purple1","j-pop":"medium_purple1","j-rock":"medium_purple1",
    "soundtrack":"medium_purple1","ost":"medium_purple1",
    "classical":"bright_green","jazz":"bright_green","blues":"bright_green",
    "country":"bright_green","folk":"bright_green","reggae":"green",
    "ambient":"cyan","instrumental":"cyan",
}
def genre_color(g):
    if not g: return GRAY
    gl = g.lower()
    for k, c in GENRE_COLORS.items():
        if k in gl: return c
    return CYAN

TYPE_LABELS = {
    "opening":"🎌 Опенинг","ending":"🎬 Эндинг","ost":"🎼 OST","theme":"🎵 Тема",
    "game":"🎮 Игра","anime":"🌸 Аниме","film":"🎞 Кино","classical":"🎻 Классика",
    "remix":"🎛 Ремикс","live":"🎤 Live","acoustic":"🎸 Акустика","cover":"🎙 Кавер",
    "instrumental":"🎹 Инстр.","song":"🎵 Песня",
}

def run(cmd, timeout=10):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except Exception: return None

def has_cmd(cmd):
    r = run(f"which {cmd}")
    return r is not None and r.stdout.strip() != ""

def human_size(b):
    try: b = int(b)
    except: return "?"
    for u in ["B","KB","MB","GB"]:
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} TB"

def fmt_duration(s):
    if not s: return "--:--"
    try: s = int(s)
    except: return "--:--"
    m, sec = divmod(s, 60); h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"

def nkey(s): return " ".join(str(s).lower().split()).strip()

def load_cache():
    if not os.path.exists(CACHE_FILE):
        console.print(Panel("[red]❌ Кэш не найден. Запусти music-meta[/]", border_style="red"))
        return None
    try:
        with open(CACHE_FILE, encoding="utf-8") as f: return json.load(f)
    except Exception as e:
        console.print(f"[red]❌ {e}[/]"); return None

def build_library(cache):
    artists = {}
    for path, m in cache["tracks"].items():
        if not os.path.exists(path): continue
        a = (m.get("artist") or "Неизвестен").strip()
        ak = nkey(a)
        if ak not in artists:
            artists[ak] = {"display": a, "albums": {}, "genres": set()}
        alb = (m.get("album") or "Без альбома").strip()
        alk = nkey(alb)
        if alk not in artists[ak]["albums"]:
            artists[ak]["albums"][alk] = {"display": alb, "tracks": []}
        try: size = os.path.getsize(path)
        except: size = 0
        track = {
            "title": m.get("title") or os.path.basename(path),
            "path": path, "duration": m.get("duration") or 0,
            "size": size, "genre": (m.get("genre") or "").strip(),
            "year": (m.get("year") or "").strip(),
            "type": m.get("type") or "song", "source": m.get("source") or "local",
            "album": alb, "artist": a,
        }
        artists[ak]["albums"][alk]["tracks"].append(track)
        if track["genre"]: artists[ak]["genres"].add(track["genre"])
    for a in artists.values():
        for alb in a["albums"].values():
            alb["tracks"].sort(key=lambda x: x["title"].lower())
    return artists

def all_tracks(artists):
    o = []
    for a in artists.values():
        for alb in a["albums"].values(): o.extend(alb["tracks"])
    return o

def all_genres(artists):
    g = {}
    for a in artists.values():
        for alb in a["albums"].values():
            for t in alb["tracks"]:
                if t.get("genre"): g[t["genre"]] = g.get(t["genre"],0)+1
    return g

def all_types(artists):
    tp = {}
    for a in artists.values():
        for alb in a["albums"].values():
            for t in alb["tracks"]:
                k = t.get("type") or "song"; tp[k] = tp.get(k,0)+1
    return tp

PS = {"playing":False,"path":None,"title":None,"artist":None,"album":None,
      "genre":None,"year":None,"type":None,"source":None,"duration":0,"started_at":0}

def play_track(path, track=None):
    run("termux-media-player stop"); time.sleep(0.2)
    r = run(f'termux-media-player play "{path}"', timeout=10)
    if r is not None and r.returncode == 0:
        PS.update({"playing":True,"path":path,"started_at":time.time()})
        if track:
            for k in ("title","artist","album","genre","year","type","source"):
                PS[k] = track.get(k)
            PS["duration"] = track.get("duration") or 0
        return True
    return False

def stop_playback():
    run("termux-media-player stop")
    PS.update({"playing":False,"path":None,"started_at":0})

def cur_pos():
    return max(0, int(time.time() - PS["started_at"])) if PS["playing"] else 0

# ─── Live NP ───
def make_np_render():
    def render():
        pos = cur_pos(); dur = PS["duration"] or 1
        if pos > dur: pos = dur
        bw = 44; filled = min(int((pos/dur)*bw), bw) if dur else 0
        bar = "▓"*filled + "░"*(bw-filled)
        gc = genre_color(PS["genre"])
        lines = [
            Text(""),
            Text("  ▶  С Е Й Ч А С   И Г Р А Е Т", style=f"bold {GREEN_BRIGHT}"),
            Text(""),
            Text(f"    🎵  {PS['artist']} — {PS['title']}", style=f"bold {WHITE}"),
            Text(f"    💿  {PS['album'] or '—'}  ({PS['year'] or '—'})", style=f"dim {GRAY}"),
        ]
        if PS["genre"]:
            lines.append(Text(f"    🎼  {PS['genre']}  •  {TYPE_LABELS.get(PS['type'],'')}", style=gc))
        lines += [
            Text(""),
            Text(f"    {bar}   {fmt_duration(pos)} / {fmt_duration(dur)}", style=GREEN_BRIGHT),
            Text(""),
            Text("    [s] стоп   [n] след.   [Enter] назад   [q] выход", style=f"dim {CYAN}"),
            Text(""),
        ]
        return Panel(Group(*lines),
                     title=f"[bold {YELLOW}]┃  M U S I C   P L A Y E R  ┃[/]",
                     border_style=GREEN_DIM, padding=(0, 1))
    return render

def run_now_playing(artists, pool):
    render = make_np_render()
    action = {"a": "back"}
    try:
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

    with Live(render(), console=console, refresh_per_second=4) as live:
        while PS["playing"]:
            live.update(render())
            k = read_key()
            if k:
                if k in ("\r","\n","\x1b"): action["a"]="back"; break
                if k.lower()=="q": action["a"]="quit"; break
                if k.lower()=="s": action["a"]="stop"; break
                if k.lower()=="n": action["a"]="next"; break
            if PS["duration"] and cur_pos() >= PS["duration"]:
                action["a"]="back"; PS["playing"]=False; break
            time.sleep(0.15)

    if action["a"]=="stop": stop_playback()
    elif action["a"]=="next" and pool:
        tr = random.choice(pool); play_track(tr["path"], tr)
        return run_now_playing(artists, pool)
    return action["a"]

# ─── Панели ───
def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("═"*60, style=GREEN_DIM))
    return Group(*lines)

def stats_panel(artists):
    tt = sum(len(alb["tracks"]) for a in artists.values() for alb in a["albums"].values())
    ts = sum(t["size"] for a in artists.values() for alb in a["albums"].values() for t in alb["tracks"])
    g = all_genres(artists)
    t = Table(box=None, show_header=False, padding=(0,3))
    t.add_column("", style=f"bold {YELLOW}"); t.add_column("", style=f"bold {CYAN}")
    t.add_column("", style=f"bold {YELLOW}"); t.add_column("", style=f"bold {CYAN}")
    t.add_row("🎤 Исполнителей", str(len(artists)), "🎵 Треков", str(tt))
    t.add_row("💾 Вес", human_size(ts), "🎼 Жанров", str(len(g)))
    return t

def now_playing_mini():
    if not PS["playing"]: return None
    pos = cur_pos(); dur = PS["duration"] or 1
    if pos > dur: pos = dur
    bw = 40; filled = min(int((pos/dur)*bw), bw) if dur else 0
    bar = "▓"*filled + "░"*(bw-filled)
    gc = genre_color(PS["genre"])
    lines = [
        Text(f"  ▶  {PS['artist']} — {PS['title']}", style=f"bold {WHITE}"),
        Text(f"     🎼 {PS['genre'] or '—'}", style=gc),
        Text(f"     {bar}  {fmt_duration(pos)} / {fmt_duration(dur)}", style=GREEN_BRIGHT),
        Text("     [np] live-прогресс", style=f"dim {CYAN}"),
    ]
    return Panel(Group(*lines), title=f"[bold {YELLOW}]┃ PLAYING ┃[/]",
                 border_style=GREEN_DIM, padding=(0,1))

def commands_panel(extra=None):
    rows = [("<номер>","🎤 Выбрать")]
    if extra: rows.extend(extra)
    rows += [("random","🎲 Случайный"),("stop","⏹ Стоп"),("q","🚪 Выход")]
    c = Table(box=None, show_header=False, padding=(0,2))
    c.add_column("", style=f"bold {YELLOW}", width=16, justify="right")
    c.add_column("", style=f"{CYAN}")
    half = (len(rows)+1)//2
    for i in range(half):
        L = rows[i]; R = rows[i+half] if i+half < len(rows) else None
        c.add_row(escape(f"[{L[0]}]"), L[1], escape(f"[{R[0]}]") if R else "", R[1] if R else "")
    return Panel(c, title=f"[bold {CYAN}]⌨  КОМАНДЫ  (Tab — автодополнение)[/]",
                 border_style=CYAN, padding=(0,1))

def artists_table(items, page):
    tp = max(1, (len(items)+PAGE_SIZE-1)//PAGE_SIZE)
    page = max(1, min(page, tp)); s = (page-1)*PAGE_SIZE; e = s+PAGE_SIZE
    t = Table(box=box.SIMPLE_HEAD, border_style=GREEN_DIM,
              header_style=f"bold {GREEN_BRIGHT}", padding=(0,2), expand=True)
    t.add_column("#", justify="right", width=4, style=f"bold {YELLOW}")
    t.add_column("ИСПОЛНИТЕЛЬ", style=WHITE)
    t.add_column("ТРЕКОВ", justify="right", width=8, style=CYAN)
    t.add_column("ЖАНР", width=20)
    for i, (ak, a) in enumerate(items[s:e], s+1):
        cnt = sum(len(alb["tracks"]) for alb in a["albums"].values())
        gl = list(a["genres"]); mg = gl[0] if gl else "—"
        t.add_row(str(i), a["display"], str(cnt), Text(mg[:18], style=genre_color(mg)))
    return t, page, tp

def tracks_table(tracks, start_idx=1):
    t = Table(box=box.SIMPLE, border_style=MAGENTA,
              header_style=f"bold {MAGENTA}", padding=(0,1),
              expand=True, show_header=False)
    t.add_column("#", justify="right", width=4, style=f"bold {YELLOW}")
    t.add_column("НАЗВАНИЕ", style=WHITE)
    t.add_column("ЖАНР", width=16); t.add_column("ТИП", width=14)
    t.add_column("ВРЕМЯ", justify="right", width=8, style=GRAY)
    for i, tr in enumerate(tracks, start_idx):
        t.add_row(str(i), tr["title"][:55],
                  Text((tr.get("genre") or "—")[:14], style=genre_color(tr.get("genre",""))),
                  Text(TYPE_LABELS.get(tr.get("type"),"—"), style=CYAN),
                  fmt_duration(tr["duration"]))
    return t

def filter_tracks(artists, st):
    o = []
    for t in all_tracks(artists):
        if st.get("fg") and t.get("genre","").lower() != st["fg"].lower(): continue
        if st.get("ft") and t.get("type") != st["ft"]: continue
        if st.get("s"):
            q = st["s"].lower()
            if q not in f"{t.get('title','')} {t.get('genre','')} {t.get('artist','')}".lower(): continue
        o.append(t)
    return o

# ─── Custom Completer для prompt_toolkit ───
class MusicCompleter(Completer):
    def __init__(self, state_getter):
        self.get_state = state_getter
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if " " in text: return  # автодополняем только команды
        base_cmds = ["bygenre","bytype","random","stop","q","back","np","n","p","f","help"]
        for c in sorted(base_cmds):
            if c.startswith(text.lower()):
                yield Completion(c, start_position=-len(text))
        # номера страниц
        if text.isdigit() or text == "":
            for i in range(1, 21):
                si = str(i)
                if si.startswith(text):
                    yield Completion(si, start_position=-len(text))

# ═══════════ MAIN ═══════════
def main():
    if not has_cmd("termux-media-player"):
        console.clear()
        console.print(Panel("[red]❌ termux-media-player не найден[/]", border_style="red"))
        return
    cache = load_cache()
    if not cache: return
    console.clear()
    with console.status(f"[bold {GREEN_BRIGHT}]🎵 Загрузка...[/]", spinner="dots"):
        artists = build_library(cache)
    if not artists: console.print("[red]❌ Библиотека пуста[/]"); return

    state = {"mode":"main","artist_key":None,"page":1,"search":"","fg":None,"ft":None,
             "current_tracks":[],"current_filtered":[],"filter_page":1}

    session = PromptSession(
        completer=MusicCompleter(lambda: state),
        complete_while_typing=True,
        style=Style.from_dict({
            "prompt": "bold ansibrightgreen",
            "completion-menu.completion": "bg:#000000 #00ff88",
            "completion-menu.completion.current": "bg:#00aa55 #000000 bold",
        })
    )

    while True:
        console.clear()
        if state["mode"]=="main":
            title = "М У З Ы К А Л Ь Н А Я   Б И Б Л И О Т Е К А"
            sub = "Terminal Argonov  •  Music Edition"
        else:
            d = artists[state["artist_key"]]
            title = f"🎤  {d['display']}"
            sub = ", ".join(sorted(d["genres"]))[:60] or "жанры не определены"
        console.print(); console.print(title_block(title, sub)); console.print()
        if PS["playing"]:
            np = now_playing_mini()
            if np: console.print(np); console.print()

        if state["mode"]=="main":
            console.print(stats_panel(artists)); console.print()
            hf = state["fg"] or state["ft"] or state["search"]
            if hf:
                fl = Text(); fl.append("🔎 ", style=YELLOW)
                if state["fg"]: fl.append(f"жанр: {state['fg']}  ", style=genre_color(state['fg']))
                if state["ft"]: fl.append(f"тип: {TYPE_LABELS.get(state['ft'],state['ft'])}  ", style=CYAN)
                if state["search"]: fl.append(f"поиск: {state['search']}", style=YELLOW)
                console.print(fl); console.print()
                tracks = filter_tracks(artists, {"fg":state["fg"],"ft":state["ft"],"s":state["search"]})
                if not tracks:
                    console.print(Text("❌ Ничего не найдено", style=RED)); console.print()
                    console.print(commands_panel([("f","🎚 Сбросить"),("/слово","🔍 Поиск"),
                                                  ("bygenre","🎼 Жанр"),("bytype","🎬 Тип")]))
                else:
                    tp = max(1,(len(tracks)+PAGE_SIZE-1)//PAGE_SIZE)
                    state["filter_page"] = max(1,min(state["filter_page"],tp))
                    s = (state["filter_page"]-1)*PAGE_SIZE; e = s+PAGE_SIZE
                    state["current_filtered"] = tracks
                    console.print(tracks_table(tracks[s:e], start_idx=s+1)); console.print()
                    console.print(Text(f"   Стр. {state['filter_page']} / {tp}   •   всего {len(tracks)}",
                                       style=f"dim {GRAY}")); console.print()
                    console.print(commands_panel([("n / p","◀ ▶ Страницы"),("f","🎚 Сбросить"),
                                                   ("/слово","🔍 Поиск"),("bygenre","🎼 Жанр"),
                                                   ("bytype","🎬 Тип")]))
            else:
                items = sorted(artists.items(), key=lambda x: x[1]["display"].lower())
                tbl, p, tp = artists_table(items, state["page"]); state["page"] = p
                console.print(tbl); console.print()
                console.print(Text(f"   Стр. {p} / {tp}   •   всего {len(items)}",
                                   style=f"dim {GRAY}")); console.print()
                console.print(commands_panel([("n / p","◀ ▶ Страницы"),("/слово","🔍 Поиск"),
                                               ("bygenre","🎼 Жанр"),("bytype","🎬 Тип")]))
        else:
            d = artists[state["artist_key"]]
            state["current_tracks"] = []; flat = []; idx = 1
            albums = sorted(d["albums"].items(),
                            key=lambda x: (x[1]["display"]=="Без альбома", x[1]["display"].lower()))
            for alk, alb in albums:
                console.print(Text(f"💿 {alb['display']}  ({len(alb['tracks'])})", style=f"bold {MAGENTA}"))
                console.print(tracks_table(alb["tracks"], start_idx=idx)); console.print()
                flat.extend(alb["tracks"]); idx += len(alb["tracks"])
            state["current_tracks"] = flat
            console.print(commands_panel([("back","◀ К списку")]))

        try:
            cmd = session.prompt(HTML('<prompt>╰─❯</prompt> ')).strip()
        except (EOFError, KeyboardInterrupt):
            console.print(Text("\n До связи. 🖖", style=f"dim {GREEN_DIM}")); stop_playback(); break

        if not cmd: continue
        cl = cmd.lower()

        if cl in ("q","exit","quit","выход"):
            console.print(Text(" До связи. 🖖", style=f"dim {GREEN_DIM}")); stop_playback(); break
        if cl=="stop": stop_playback(); console.print(Text("  ⏹ Стоп", style=YELLOW)); time.sleep(0.4); continue
        if cl=="np":
            if PS["playing"]:
                pool = (state["current_filtered"] if (state["mode"]=="main" and state.get("current_filtered"))
                        else state["current_tracks"] if state["mode"]=="artist" else all_tracks(artists))
                run_now_playing(artists, pool)
            else: console.print(Text("  ⚠ Не играет", style=YELLOW)); time.sleep(0.6)
            continue
        if cl=="random":
            pool = (state["current_filtered"] if (state["mode"]=="main" and state.get("current_filtered"))
                    else state["current_tracks"] if state["mode"]=="artist" else all_tracks(artists))
            if pool:
                tr = random.choice(pool)
                if play_track(tr["path"], tr):
                    console.print(Text(f"  🎲 {tr['artist']} — {tr['title']}", style=GREEN_BRIGHT))
                    time.sleep(0.6); run_now_playing(artists, pool)
            continue

        if cl=="bygenre":
            g = all_genres(artists)
            if not g: console.print(Text("  ⚠ нет жанров", style=YELLOW)); time.sleep(1); continue
            console.clear(); console.print(); console.print(title_block("ВЫБОР ЖАНРА")); console.print()
            t = Table(box=box.SIMPLE_HEAD, border_style=MAGENTA, header_style=f"bold {MAGENTA}", padding=(0,2))
            t.add_column("#", style=f"bold {YELLOW}", width=4, justify="right")
            t.add_column("ЖАНР", style=WHITE); t.add_column("ТРЕКОВ", style=CYAN, justify="right", width=10)
            gs = sorted(g.items(), key=lambda x: -x[1])
            for i, (gg, c) in enumerate(gs, 1): t.add_row(str(i), Text(gg, style=genre_color(gg)), str(c))
            console.print(t); console.print(Text("\n  0 — сброс  •  Enter — назад", style=f"dim {GRAY}")); console.print()
            try:
                ch = console.input(Text("╰─[жанр]❯ ", style=f"bold {GREEN_BRIGHT}")).strip()
                if ch=="0": state["fg"]=None
                elif ch.isdigit() and 1<=int(ch)<=len(gs): state["fg"]=gs[int(ch)-1][0]
                state["filter_page"]=1; state["current_filtered"]=[]
            except (EOFError, KeyboardInterrupt): pass
            continue

        if cl=="bytype":
            tp = all_types(artists)
            if not tp: console.print(Text("  ⚠ нет типов", style=YELLOW)); time.sleep(1); continue
            console.clear(); console.print(); console.print(title_block("ВЫБОР ТИПА")); console.print()
            t = Table(box=box.SIMPLE_HEAD, border_style=CYAN, header_style=f"bold {CYAN}", padding=(0,2))
            t.add_column("#", style=f"bold {YELLOW}", width=4, justify="right")
            t.add_column("ТИП", style=WHITE); t.add_column("ТРЕКОВ", style=CYAN, justify="right", width=10)
            ts = sorted(tp.items(), key=lambda x: -x[1])
            for i, (tt, c) in enumerate(ts, 1): t.add_row(str(i), TYPE_LABELS.get(tt,tt), str(c))
            console.print(t); console.print(Text("\n  0 — сброс  •  Enter — назад", style=f"dim {GRAY}")); console.print()
            try:
                ch = console.input(Text("╰─[тип]❯ ", style=f"bold {GREEN_BRIGHT}")).strip()
                if ch=="0": state["ft"]=None
                elif ch.isdigit() and 1<=int(ch)<=len(ts): state["ft"]=ts[int(ch)-1][0]
                state["filter_page"]=1; state["current_filtered"]=[]
            except (EOFError, KeyboardInterrupt): pass
            continue

        if cl=="f":
            state["fg"]=None; state["ft"]=None; state["search"]=""
            state["filter_page"]=1; state["current_filtered"]=[]
            continue
        if cmd.startswith("/"):
            state["search"]=cmd[1:].strip(); state["filter_page"]=1; state["current_filtered"]=[]
            continue

        if state["mode"]=="main":
            hf = state["fg"] or state["ft"] or state["search"]
            if hf:
                if cl=="n": state["filter_page"]+=1; continue
                if cl=="p" and state["filter_page"]>1: state["filter_page"]-=1; continue
            else:
                if cl=="n": state["page"]+=1; continue
                if cl=="p" and state["page"]>1: state["page"]-=1; continue
        if state["mode"]=="artist" and cl=="back":
            state["mode"]="main"; state["artist_key"]=None; state["page"]=1; state["current_tracks"]=[]
            continue

        if cl.isdigit():
            num = int(cl)
            if state["mode"]=="main":
                hf = state["fg"] or state["ft"] or state["search"]
                if hf:
                    tracks = state["current_filtered"] or filter_tracks(artists,
                        {"fg":state["fg"],"ft":state["ft"],"s":state["search"]})
                    if 1<=num<=len(tracks):
                        tr = tracks[num-1]
                        if play_track(tr["path"], tr):
                            console.print(Text(f"  ▶ {tr['artist']} — {tr['title']}", style=GREEN_BRIGHT))
                            time.sleep(0.6); run_now_playing(artists, tracks)
                    else: console.print(Text(f"  ❌ 1..{len(tracks)}", style=RED)); time.sleep(0.8)
                else:
                    items = sorted(artists.items(), key=lambda x: x[1]["display"].lower())
                    s = (state["page"]-1)*PAGE_SIZE; e = s+PAGE_SIZE
                    if s+1<=num<=min(e, len(items)):
                        state["artist_key"]=items[num-1][0]; state["mode"]="artist"
                    else: console.print(Text("  ❌ вне страницы", style=RED)); time.sleep(0.8)
            else:
                if 1<=num<=len(state["current_tracks"]):
                    tr = state["current_tracks"][num-1]
                    if play_track(tr["path"], tr):
                        console.print(Text(f"  ▶ {tr['title']}", style=GREEN_BRIGHT))
                        time.sleep(0.6); run_now_playing(artists, state["current_tracks"])
                else: console.print(Text(f"  ❌ 1..{len(state['current_tracks'])}", style=RED)); time.sleep(0.8)
            continue

        console.print(Text(f"  ❌ {cmd}", style=RED)); time.sleep(0.6)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        stop_playback(); console.print(Text("\n Прервано.", style=f"dim {GREEN_DIM}"))
