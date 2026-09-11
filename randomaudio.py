#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Music Player v9 — обложки (iTunes) + favorites + экспорт"""

import os, sys, json, random, subprocess, time, re, hashlib
import urllib.request, urllib.parse, urllib.error
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markup import escape
from rich.box import SIMPLE_HEAD
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

console = Console()
CACHE_FILE = os.path.expanduser("~/music_cache/library.json")
COVERS_DIR = os.path.expanduser("~/music_cache/covers")
FAV_FILE = os.path.expanduser("~/.music_favorites.json")
EXPORT_DIR = os.path.expanduser("~/music_cache/exports")
PAGE_SIZE = 15

GREEN_BRIGHT = "bright_green"; GREEN_DIM = "green"
CYAN = "bright_cyan"; YELLOW = "bright_yellow"; MAGENTA = "bright_magenta"
RED = "bright_red"; WHITE = "bright_white"; GRAY = "grey50"

GENRE_COLORS = {
    "rock":"bright_red","metal":"bright_red","punk":"bright_red",
    "pop":"bright_yellow","dance":"bright_yellow",
    "hip-hop":"dark_orange","rap":"dark_orange",
    "electronic":"bright_blue","edm":"bright_blue","techno":"bright_blue",
    "anime":"medium_purple1","soundtrack":"medium_purple1","ost":"medium_purple1",
    "classical":"bright_green","jazz":"bright_green",
    "instrumental":"cyan",
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
    except: return None

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

# ═══════════ ФИЛЬТР ГОЛОСОВЫХ ═══════════
NON_MUSIC_KEYWORDS = [
    "whatsapp audio", "voice", "recording", "запись", "record",
    "голосовое", "voice message", "dictaphone", "диктофон",
    "note_to_self", "audio_20", "rec_20", "запись_20", "голос_20",
]

def is_music_track(track):
    path = (track.get("path") or "").lower()
    title = (track.get("title") or "").lower()
    artist = (track.get("artist") or "").lower()
    album = (track.get("album") or "").lower()
    dur = track.get("duration") or 0
    genre = track.get("genre") or ""
    source = track.get("source") or "local"

    if 0 < dur < 30: return False
    hay = f"{path} {title}"
    for kw in NON_MUSIC_KEYWORDS:
        if kw in hay: return False
    if "whatsapp/media" in path.replace("\\", "/"): return False
    if (artist in ("неизвестен","unknown","") and
        album in ("без альбома","") and not genre and source == "local"):
        if any(x in path for x in ["/dcim/", "/recordings/", "/record/", "/voice/"]):
            return False
        if re.match(r"^\d+[\d_\-\.]+$", os.path.basename(path).rsplit(".",1)[0]):
            return False
    return True

# ═══════════ ОБЛОЖКИ (iTunes API) ═══════════
def cover_cache_path(artist, album, title):
    key = f"{artist}|{album}|{title}".lower()
    h = hashlib.md5(key.encode()).hexdigest()[:16]
    return os.path.join(COVERS_DIR, f"{h}.jpg")

def fetch_cover_url(artist, album, title):
    """Ищет обложку на iTunes. Возвращает URL или None."""
    try:
        q = f"{artist} {album}" if album and album != "Без альбома" else f"{artist} {title}"
        params = urllib.parse.urlencode({"term": q, "entity":"album", "limit":1})
        url = f"https://itunes.apple.com/search?{params}"
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
            results = data.get("results", [])
            if results:
                art = results[0].get("artworkUrl100", "")
                if art:
                    return art.replace("100x100", "600x600")
    except Exception:
        pass
    return None

def ensure_cover(artist, album, title):
    """Возвращает путь к обложке или None. Скачивает если надо."""
    if not artist or artist == "Неизвестен": return None
    os.makedirs(COVERS_DIR, exist_ok=True)
    cp = cover_cache_path(artist, album, title)
    if os.path.exists(cp) and os.path.getsize(cp) > 1000:
        return cp
    url = fetch_cover_url(artist, album, title)
    if not url: return None
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read()
        with open(cp, "wb") as f: f.write(data)
        return cp
    except Exception:
        return None

def show_cover(path, width=40, height=20):
    """Показывает обложку через chafa."""
    if not path or not os.path.exists(path): return
    if not has_cmd("chafa"): return
    try:
        subprocess.run(
            ["chafa", f"--size={width}x{height}", "--symbols=block",
             "--fg-only", "--dither=fs", "--colors=256", path])
    except Exception:
        pass

# ═══════════ FAVORITES ═══════════
def load_favs():
    if not os.path.exists(FAV_FILE): return set()
    try:
        with open(FAV_FILE, encoding="utf-8") as f:
            d = json.load(f)
            return set(d.get("paths", []))
    except: return set()

def save_favs(favs):
    try:
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump({"paths": sorted(favs)}, f, ensure_ascii=False, indent=1)
    except: pass

# ═══════════ ЭКСПОРТ ═══════════
def export_m3u(tracks, name="playlist"):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{name}.m3u")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for t in tracks:
                dur = int(t.get("duration") or -1)
                f.write(f"#EXTINF:{dur},{t.get('artist','')} - {t.get('title','')}\n")
                f.write(f"{t['path']}\n")
        return path
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")
        return None

def export_csv(tracks, name="library"):
    import csv
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{name}.csv")
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Artist","Title","Album","Genre","Year","Duration","Type","Path"])
            for t in tracks:
                w.writerow([
                    t.get("artist",""), t.get("title",""), t.get("album",""),
                    t.get("genre",""), t.get("year",""), t.get("duration",""),
                    t.get("type",""), t.get("path","")
                ])
        return path
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")
        return None

# ═══════════ БИБЛИОТЕКА ═══════════
def load_cache():
    if not os.path.exists(CACHE_FILE):
        console.print("[red]❌ Кэш не найден. Запусти music-meta[/]")
        return None
    try:
        with open(CACHE_FILE, encoding="utf-8") as f: return json.load(f)
    except Exception as e:
        console.print(f"[red]❌ {e}[/]"); return None

def build_library(cache):
    artists = {}; skipped = 0
    for path, m in cache["tracks"].items():
        if not os.path.exists(path): continue
        a = (m.get("artist") or "Неизвестен").strip()
        alb = (m.get("album") or "Без альбома").strip()
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
        if not is_music_track(track):
            skipped += 1; continue
        ak = nkey(a)
        if ak not in artists:
            artists[ak] = {"display": a, "albums": {}, "genres": set()}
        alk = nkey(alb)
        if alk not in artists[ak]["albums"]:
            artists[ak]["albums"][alk] = {"display": alb, "tracks": []}
        artists[ak]["albums"][alk]["tracks"].append(track)
        if track["genre"]: artists[ak]["genres"].add(track["genre"])
    for a in artists.values():
        for alb in a["albums"].values():
            alb["tracks"].sort(key=lambda x: x["title"].lower())
    return artists, skipped

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

# ═══════════ ПЛЕЕР ═══════════
PS = {"playing":False,"path":None,"title":None,"artist":None,"album":None,
      "genre":None,"year":None,"type":None,"duration":0,"started_at":0}

def play_track(path, track=None):
    run("termux-media-player stop"); time.sleep(0.2)
    r = run(f'termux-media-player play "{path}"', timeout=10)
    if r is not None and r.returncode == 0:
        PS.update({"playing":True,"path":path,"started_at":time.time()})
        if track:
            for k in ("title","artist","album","genre","year","type"):
                PS[k] = track.get(k)
            PS["duration"] = track.get("duration") or 0
        return True
    return False

def stop_playback():
    run("termux-media-player stop")
    PS.update({"playing":False,"path":None,"started_at":0})

def cur_pos():
    return max(0, int(time.time() - PS["started_at"])) if PS["playing"] else 0

def now_playing_panel(show_cover_img=False):
    if not PS["playing"]: return None
    pos = cur_pos(); dur = PS["duration"] or 0
    if dur > 0:
        bw = 40; filled = min(int((pos/dur)*bw), bw)
        bar = "▓"*filled + "░"*(bw-filled)
    else:
        bar = "▓"*8 + "░"*32
    gc = genre_color(PS["genre"])
    lines = [
        Text(f"  ▶  {PS['artist']} — {PS['title']}", style=f"bold {WHITE}"),
        Text(f"     💿 {PS['album'] or '—'}", style=f"dim {GRAY}"),
    ]
    if PS["genre"]:
        lines.append(Text(f"     🎼 {PS['genre']}", style=gc))
    lines.append(Text(f"     {bar}  {fmt_duration(pos)} / {fmt_duration(dur) if dur else '--:--'}", style=GREEN_BRIGHT))
    return Panel(Group(*lines), title=f"[bold {YELLOW}]┃ PLAYING ┃[/]",
                 border_style=GREEN_DIM, padding=(0,1))

def play_and_wait(track, pool=None):
    if not play_track(track["path"], track):
        console.print(f"[red]❌ Не удалось запустить[/]"); return

    console.clear()
    console.print()
    # ⬅️ Обложка слева, панель справа
    cover_path = ensure_cover(track.get("artist",""), track.get("album",""), track.get("title",""))
    if cover_path and has_cmd("chafa"):
        console.print(f"[dim]🎨 Обложка: {os.path.basename(cover_path)}[/]")
        console.print()
        show_cover(cover_path, width=40, height=18)
        console.print()
    console.print(now_playing_panel())
    console.print()
    console.print(f"  [dim]s = стоп  ·  n = след.  ·  f = ♥  ·  Enter = назад[/]\n")

    try:
        import termios, tty, select
        has_t = True
    except: has_t = False

    def read_key():
        if not has_t: return None
        fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            rl, _, _ = select.select([sys.stdin], [], [], 0.3)
            if rl: return sys.stdin.read(1)
        except: return None
        finally:
            try: termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except: pass
        return None

    max_dur = PS["duration"] if PS["duration"] > 0 else 300
    start = time.time()
    favs = load_favs()

    try:
        while PS["playing"]:
            elapsed = time.time() - start
            if PS["duration"] > 0 and cur_pos() >= PS["duration"]:
                stop_playback(); console.print(f"  [dim]✔ Завершён[/]")
                return "done"
            if PS["duration"] == 0 and elapsed > max_dur:
                stop_playback(); console.print(f"  [dim]✔ Таймаут[/]")
                return "done"

            k = read_key()
            if k:
                kl = k.lower()
                if kl in ("s","q"):
                    stop_playback(); console.print(f"  [yellow]⏹ Стоп[/]")
                    return "stop"
                elif kl == "n" and pool:
                    tr = random.choice(pool); stop_playback(); time.sleep(0.3)
                    return play_and_wait(tr, pool)
                elif kl == "f":
                    p = track["path"]
                    if p in favs:
                        favs.discard(p); console.print(f"  [dim]💔 Убран из favorites[/]")
                    else:
                        favs.add(p); console.print(f"  [magenta]♥ Добавлен в favorites[/]")
                    save_favs(favs); time.sleep(0.5)
                elif k in ("\r","\n","\x1b"):
                    return "back"
            time.sleep(0.2)
    except KeyboardInterrupt:
        stop_playback(); console.print(f"\n  [yellow]⏹[/]")
        return "stop"
    return "done"

# ═══════════ ТАБЛИЦЫ ═══════════
def title_block(main, sub=""):
    lines = [Text("▓▒░ " + main.upper() + " ░▒▓", style=f"bold {GREEN_BRIGHT}")]
    if sub: lines.append(Text(sub, style=f"dim {GREEN_DIM}"))
    lines.append(Text("─"*60, style=GREEN_DIM))
    return Group(*lines)

def stats_panel(artists, favs):
    tt = sum(len(alb["tracks"]) for a in artists.values() for alb in a["albums"].values())
    ts = sum(t["size"] for a in artists.values() for alb in a["albums"].values() for t in alb["tracks"])
    g = all_genres(artists)
    t = Table(box=None, show_header=False, padding=(0,3))
    t.add_column("", style=f"bold {YELLOW}"); t.add_column("", style=f"bold {CYAN}")
    t.add_column("", style=f"bold {YELLOW}"); t.add_column("", style=f"bold {CYAN}")
    t.add_row("🎤 Исполнителей", str(len(artists)), "🎵 Треков", str(tt))
    t.add_row("💾 Вес", human_size(ts), "🎼 Жанров", str(len(g)))
    t.add_row("♥ Favorites", str(len(favs)), "", "")
    return t

def commands_panel(extra=None):
    rows = [("<номер>","🎤 Выбрать")]
    if extra: rows.extend(extra)
    rows += [("random","🎲 Случайный"),("favorites","♥ Favorites"),
             ("export","💾 Экспорт"),("stop","⏹ Стоп"),("q","🚪 Выход")]
    c = Table(box=None, show_header=False, padding=(0,2))
    c.add_column("", style=f"bold {YELLOW}", width=16, justify="right")
    c.add_column("", style=f"{CYAN}")
    half = (len(rows)+1)//2
    for i in range(half):
        L = rows[i]; R = rows[i+half] if i+half < len(rows) else None
        c.add_row(escape(f"[{L[0]}]"), L[1], escape(f"[{R[0]}]") if R else "", R[1] if R else "")
    return Panel(c, title=f"[bold {CYAN}]⌨  КОМАНДЫ[/]", border_style=CYAN, padding=(0,1))

def artists_table(items, page, favs):
    tp = max(1, (len(items)+PAGE_SIZE-1)//PAGE_SIZE)
    page = max(1, min(page, tp)); s = (page-1)*PAGE_SIZE; e = s+PAGE_SIZE
    t = Table(box=SIMPLE_HEAD, border_style=GREEN_DIM,
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

def tracks_table(tracks, start_idx=1, favs=None):
    favs = favs or set()
    t = Table(box=SIMPLE_HEAD, border_style=MAGENTA,
              header_style=f"bold {MAGENTA}", padding=(0,1),
              expand=True, show_header=False)
    t.add_column("♥", width=3, justify="center")
    t.add_column("#", justify="right", width=4, style=f"bold {YELLOW}")
    t.add_column("НАЗВАНИЕ", style=WHITE)
    t.add_column("ЖАНР", width=16); t.add_column("ТИП", width=14)
    t.add_column("ВРЕМЯ", justify="right", width=8, style=GRAY)
    for i, tr in enumerate(tracks, start_idx):
        heart = "[magenta]♥[/]" if tr["path"] in favs else " "
        t.add_row(heart, str(i), tr["title"][:55],
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

COMMANDS = ["bygenre","bytype","random","favorites","export","stop","q","back","n","p","f","help"]

class MusicComp(Completer):
    def get_completions(self, doc, ev):
        t = doc.text_before_cursor
        if " " in t: return
        for c in sorted(COMMANDS):
            if c.startswith(t.lower()): yield Completion(c, start_position=-len(t))
        if t.isdigit() or t == "":
            for i in range(1,21):
                si = str(i)
                if si.startswith(t): yield Completion(si, start_position=-len(t))

def main():
    if not has_cmd("termux-media-player"):
        console.clear(); console.print("[red]❌ termux-media-player не найден[/]"); return
    cache = load_cache()
    if not cache: return
    console.clear()
    with console.status(f"[bold {GREEN_BRIGHT}]🎵 Загрузка...[/]", spinner="dots"):
        artists, skipped = build_library(cache)
    if not artists:
        console.print("[red]❌ Нет музыки (всё отфильтровано)[/]"); return
    favs = load_favs()
    console.print(f"[green]✔ Загружено[/]  ·  [dim]пропущено: {skipped}  ·  favorites: {len(favs)}[/]")
    time.sleep(0.8)

    state = {"mode":"main","artist_key":None,"page":1,"search":"","fg":None,"ft":None,
             "current_tracks":[],"current_filtered":[],"filter_page":1}

    session = PromptSession(
        completer=MusicComp(), complete_while_typing=True,
        style=Style.from_dict({
            "prompt": "bold ansibrightmagenta",
            "completion-menu.completion": "bg:#000000 #00ff88",
            "completion-menu.completion.current": "bg:#aa00aa #ffffff bold",
        }))

    while True:
        console.clear()
        if state["mode"]=="main":
            title = "М У З Ы К А Л Ь Н А Я   Б И Б Л И О Т Е К А"
            sub = "Terminal Argonov  •  Music Edition  •  с обложками"
        elif state["mode"]=="favorites":
            title = "♥  F A V O R I T E S"
            sub = f"{len(favs)} треков"
        else:
            d = artists[state["artist_key"]]
            title = f"🎤  {d['display']}"
            sub = ", ".join(sorted(d["genres"]))[:60] or ""

        console.print(); console.print(title_block(title, sub)); console.print()
        if PS["playing"]:
            np = now_playing_panel()
            if np: console.print(np); console.print()

        # ── FAVORITES ──
        if state["mode"]=="favorites":
            fav_tracks = [t for t in all_tracks(artists) if t["path"] in favs]
            if not fav_tracks:
                console.print(Text("💔 Favorites пусто. Нажми 'f' при воспроизведении.", style=GRAY))
            else:
                console.print(tracks_table(fav_tracks, favs=favs))
                state["current_filtered"] = fav_tracks
            console.print()
            console.print(commands_panel([("back","◀ К библиотеке"),("export","💾 Экспорт")]))
        # ── MAIN ──
        elif state["mode"]=="main":
            console.print(stats_panel(artists, favs)); console.print()
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
                else:
                    tp = max(1,(len(tracks)+PAGE_SIZE-1)//PAGE_SIZE)
                    state["filter_page"] = max(1,min(state["filter_page"],tp))
                    s = (state["filter_page"]-1)*PAGE_SIZE; e = s+PAGE_SIZE
                    state["current_filtered"] = tracks
                    console.print(tracks_table(tracks[s:e], start_idx=s+1, favs=favs)); console.print()
                    console.print(Text(f"   Стр. {state['filter_page']}/{tp}  ·  всего {len(tracks)}", style=f"dim {GRAY}")); console.print()
                console.print(commands_panel([("n/p","◀ ▶"),("f","Сброс"),
                                               ("/слово","Поиск"),("bygenre","Жанр"),("bytype","Тип")]))
            else:
                items = sorted(artists.items(), key=lambda x: x[1]["display"].lower())
                tbl, p, tp = artists_table(items, state["page"], favs); state["page"] = p
                console.print(tbl); console.print()
                console.print(Text(f"   Стр. {p}/{tp}  ·  всего {len(items)}", style=f"dim {GRAY}")); console.print()
                console.print(commands_panel([("n/p","◀ ▶"),("/слово","Поиск"),
                                               ("bygenre","Жанр"),("bytype","Тип")]))
        # ── ARTIST ──
        else:
            d = artists[state["artist_key"]]
            state["current_tracks"] = []; flat = []; idx = 1
            albums = sorted(d["albums"].items(),
                            key=lambda x: (x[1]["display"]=="Без альбома", x[1]["display"].lower()))
            for alk, alb in albums:
                console.print(Text(f"💿 {alb['display']}  ({len(alb['tracks'])})", style=f"bold {MAGENTA}"))
                console.print(tracks_table(alb["tracks"], start_idx=idx, favs=favs)); console.print()
                flat.extend(alb["tracks"]); idx += len(alb["tracks"])
            state["current_tracks"] = flat
            console.print(commands_panel([("back","◀ К списку")]))

        try:
            cmd = session.prompt(FormattedText([("bold ansibrightmagenta","╰─❯ ")])).strip()
        except: console.print(Text("\n До связи. 🖖", style=f"dim {GREEN_DIM}")); stop_playback(); break

        if not cmd: continue
        cl = cmd.lower()

        if cl in ("q","exit","quit","выход"): stop_playback(); break
        if cl=="stop": stop_playback(); console.print(Text("  ⏹ Стоп", style=YELLOW)); time.sleep(0.4); continue

        if cl=="random":
            pool = (state["current_filtered"] if state.get("current_filtered")
                    else state["current_tracks"] if state["mode"]=="artist"
                    else [t for t in all_tracks(artists) if t["path"] in favs] if state["mode"]=="favorites"
                    else all_tracks(artists))
            if pool:
                tr = random.choice(pool)
                play_and_wait(tr, pool)
            continue

        if cl=="favorites":
            state["mode"] = "favorites"
            state["current_filtered"] = []
            continue

        if cl=="back":
            if state["mode"] in ("favorites","artist"):
                state["mode"] = "main"
                state["artist_key"] = None
                state["page"] = 1
            continue

        if cl=="export":
            # Что экспортируем: filtered / favorites / всё
            pool = (state["current_filtered"] if state.get("current_filtered")
                    else state["current_tracks"] if state["mode"]=="artist"
                    else [t for t in all_tracks(artists) if t["path"] in favs] if state["mode"]=="favorites"
                    else all_tracks(artists))
            console.print()
            console.print("[yellow]💾 Экспорт:[/]")
            console.print(f"  [cyan]1[/])  M3U playlist")
            console.print(f"  [cyan]2[/])  CSV (Excel)")
            console.print(f"  [cyan]0[/])  Отмена")
            try:
                ch = console.input("[bold magenta]Выбери> [/]").strip()
            except: continue
            name = f"export_{int(time.time())}"
            if ch == "1":
                p = export_m3u(pool, name)
                if p: console.print(f"[green]✔ {p}[/] ({len(pool)} треков)")
            elif ch == "2":
                p = export_csv(pool, name)
                if p: console.print(f"[green]✔ {p}[/] ({len(pool)} треков)")
            console.print()
            console.input("[dim]Enter — назад[/] ")
            continue

        if cl=="bygenre":
            g = all_genres(artists)
            if not g: continue
            console.clear(); console.print(); console.print(title_block("ВЫБОР ЖАНРА")); console.print()
            t = Table(box=SIMPLE_HEAD, border_style=MAGENTA, header_style=f"bold {MAGENTA}", padding=(0,2))
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
            except: pass
            continue

        if cl=="bytype":
            tp = all_types(artists)
            if not tp: continue
            console.clear(); console.print(); console.print(title_block("ВЫБОР ТИПА")); console.print()
            t = Table(box=SIMPLE_HEAD, border_style=CYAN, header_style=f"bold {CYAN}", padding=(0,2))
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
            except: pass
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

        if cl.isdigit():
            num = int(cl)
            if state["mode"]=="main":
                hf = state["fg"] or state["ft"] or state["search"]
                if hf:
                    tracks = state["current_filtered"] or filter_tracks(artists,
                        {"fg":state["fg"],"ft":state["ft"],"s":state["search"]})
                    if 1<=num<=len(tracks):
                        tr = tracks[num-1]
                        play_and_wait(tr, tracks)
                    else: console.print(f"[red]❌ 1..{len(tracks)}[/]"); time.sleep(0.8)
                else:
                    items = sorted(artists.items(), key=lambda x: x[1]["display"].lower())
                    s = (state["page"]-1)*PAGE_SIZE; e = s+PAGE_SIZE
                    if s+1<=num<=min(e, len(items)):
                        state["artist_key"]=items[num-1][0]; state["mode"]="artist"
                    else: console.print("[red]❌ вне страницы[/]"); time.sleep(0.8)
            elif state["mode"]=="favorites":
                fav_tracks = [t for t in all_tracks(artists) if t["path"] in favs]
                if 1<=num<=len(fav_tracks):
                    play_and_wait(fav_tracks[num-1], fav_tracks)
                else: console.print(f"[red]❌ 1..{len(fav_tracks)}[/]"); time.sleep(0.8)
            else:
                if 1<=num<=len(state["current_tracks"]):
                    play_and_wait(state["current_tracks"][num-1], state["current_tracks"])
                else: console.print(f"[red]❌ 1..{len(state['current_tracks'])}[/]"); time.sleep(0.8)
            continue

        console.print(Text(f"  ❌ {cmd}", style=RED)); time.sleep(0.6)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        stop_playback(); console.print(Text("\n Прервано.", style=f"dim {GREEN_DIM}"))
