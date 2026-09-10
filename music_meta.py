#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Music Metadata Fetcher v2 — iTunes + Deezer + MusicBrainz, потокобезопасный"""

import os, re, json, time, sys
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn
from rich import box

console = Console()

CACHE_DIR = os.path.expanduser("~/music_cache")
CACHE_FILE = os.path.join(CACHE_DIR, "library.json")
CACHE_VERSION = 2

AUDIO_EXTS = {".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac",
              ".wav", ".wma", ".amr", ".3gp", ".3gpp", ".mp4a"}

SEARCH_DIRS = [
    os.path.expanduser("~/storage/music"),
    os.path.expanduser("~/storage/shared/Music"),
    os.path.expanduser("~/storage/shared/Download"),
    os.path.expanduser("~/storage/shared/Downloads"),
    os.path.expanduser("~/storage/shared/WhatsApp/Media/WhatsApp Audio"),
    os.path.expanduser("~/storage/shared/Telegram"),
    os.path.expanduser("~/storage/shared/DCIM"),
    os.path.expanduser("~/storage/shared/Ringtones"),
    os.path.expanduser("~/storage/shared/Notifications"),
    os.path.expanduser("~/storage/shared/Alarms"),
    os.path.expanduser("~/storage/shared/Podcasts"),
    os.path.expanduser("~/storage/shared"),
]

# ═══════════ ТИПЫ ТРЕКОВ ═══════════
TYPE_PATTERNS = [
    ("opening", [r"\bop\s?\d", r"\bopening\b", r"опенинг", r"\bop\d+\b", r"\bop\b"]),
    ("ending",  [r"\bed\s?\d", r"\bending\b", r"эндинг", r"\bed\d+\b", r"\bed\b"]),
    ("ost",     [r"\bost\b", r"soundtrack", r"саундтрек", r"original soundtrack"]),
    ("theme",   [r"\btheme\b", r"\bтема\b", r"main theme"]),
    ("game",    [r"\bgame\b", r"игров", r"game ost", r"игра\b"]),
    ("anime",   [r"\banime\b", r"аниме"]),
    ("film",    [r"\bfilm\b", r"\bmovie\b", r"кино\b", r"из фильма"]),
    ("classical", [r"classical", r"классика", r"симфони"]),
    ("remix",   [r"\bremix\b", r"ремикс", r"\bmix\b"]),
    ("live",    [r"\blive\b", r"концерт"]),
    ("acoustic", [r"acoustic", r"акустик"]),
    ("cover",   [r"\bcover\b", r"кавер"]),
    ("instrumental", [r"instrumental", r"инструментал"]),
]

def detect_type(title, path):
    parts = [p.lower() for p in path.split(os.sep)]
    for part in parts:
        for t, patterns in TYPE_PATTERNS:
            for p in patterns:
                if re.search(p, part, re.IGNORECASE):
                    return t
    text = (str(title) + " " + str(path)).lower()
    for t, patterns in TYPE_PATTERNS:
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                return t
    return "song"

# ═══════════ HTTP ═══════════
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "TermuxMusicMeta/2.0 ( https://termux.dev )",
    "Accept": "application/json",
})

def clean_query(s):
    if not s: return ""
    s = str(s).strip()
    s = re.sub(r"^\d{1,3}[\s.\-_]+\s*", "", s)
    s = re.sub(r"[\(\[].*?[\)\]]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# ═══════════ iTUNES ═══════════
def search_itunes(query):
    if not query: return None
    for attempt in range(2):
        try:
            r = SESSION.get("https://itunes.apple.com/search",
                params={"term": query, "entity": "song", "limit": 1}, timeout=8)
            if r.status_code != 200: return None
            results = r.json().get("results", [])
            if not results: return None
            f = results[0]
            return {
                "artist": f.get("artistName", "").strip(),
                "title":  f.get("trackName", "").strip(),
                "album":  f.get("collectionName", "").strip(),
                "genre":  f.get("primaryGenreName", "").strip(),
                "year":   (f.get("releaseDate") or "")[:4],
                "source": "itunes",
            }
        except Exception:
            if attempt == 0: time.sleep(0.5)
    return None

# ═══════════ DEEZER ═══════════
def search_deezer(query):
    if not query: return None
    for attempt in range(2):
        try:
            r = SESSION.get("https://api.deezer.com/search",
                params={"q": query, "limit": 1}, timeout=8)
            if r.status_code != 200: return None
            items = r.json().get("data", [])
            if not items: return None
            f = items[0]
            return {
                "artist": f.get("artist", {}).get("name", "").strip(),
                "title":  f.get("title", "").strip(),
                "album":  f.get("album", {}).get("title", "").strip(),
                "genre":  "",
                "year":   "",
                "source": "deezer",
            }
        except Exception:
            if attempt == 0: time.sleep(0.5)
    return None

# ═══════════ MUSICBRAINZ ═══════════
def search_musicbrainz(query):
    if not query: return None
    for attempt in range(2):
        try:
            # MusicBrainz любит Lucene-синтаксис
            r = SESSION.get("https://musicbrainz.org/ws/2/recording",
                params={"query": query, "fmt": "json", "limit": 1}, timeout=10)
            if r.status_code != 200: return None
            recordings = r.json().get("recordings", [])
            if not recordings: return None
            rec = recordings[0]
            title = rec.get("title", "").strip()
            # Artist
            credits = rec.get("artist-credit", [])
            artist = ""
            if credits:
                artist = "".join(
                    (c.get("name") or "") + (c.get("joinphrase") or "")
                    for c in credits
                ).strip()
            # Album
            album = ""
            releases = rec.get("releases", [])
            if releases:
                album = (releases[0].get("title") or "").strip()
            # Year
            year = ""
            if releases:
                date = releases[0].get("date", "")
                if date: year = date[:4]
            # Genre — из tags
            genre = ""
            tags = rec.get("tags", [])
            if tags:
                genre = tags[0].get("name", "").capitalize()
            return {
                "artist": artist,
                "title":  title,
                "album":  album,
                "genre":  genre,
                "year":   year,
                "source": "musicbrainz",
            }
        except Exception:
            if attempt == 0: time.sleep(0.5)
    return None

def fetch_metadata(title, artist):
    """Каскад: iTunes → Deezer → MusicBrainz"""
    if not title and not artist:
        return None

    # Пробуем artist + title
    if artist and title:
        q = clean_query(f"{artist} {title}")
        for fn in (search_itunes, search_deezer, search_musicbrainz):
            res = fn(q)
            if res and res.get("title"):
                return res

    # Только title
    if title:
        q = clean_query(title)
        for fn in (search_itunes, search_deezer, search_musicbrainz):
            res = fn(q)
            if res and res.get("title"):
                return res

    return None

# ═══════════ ЛОКАЛЬНЫЕ ТЕГИ ═══════════
def read_local_metadata(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    artist = album = title = None
    duration = 0
    try:
        from mutagen import File as MutagenFile
        audio = MutagenFile(path, easy=True)
        if audio:
            if audio.get("artist"):  artist = audio["artist"][0].strip()
            if audio.get("album"):   album  = audio["album"][0].strip()
            if audio.get("title"):   title  = audio["title"][0].strip()
        audio2 = MutagenFile(path)
        if audio2 and hasattr(audio2, "info") and audio2.info:
            duration = int(audio2.info.length)
    except Exception:
        pass

    if not title or not artist:
        name = re.sub(r"^\d{1,3}[\s.\-_]+\s*", "", filename)
        if " - " in name:
            left, right = name.split(" - ", 1)
            if not artist: artist = left.strip()
            if not title:  title  = right.strip()
        else:
            if not title: title = name

    return artist or "", album or "", title or filename, duration

# ═══════════ КЭШ ═══════════
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {"version": CACHE_VERSION, "tracks": {}}
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            data = json.load(f)
            if data.get("version") != CACHE_VERSION:
                # Мигрируем: старые версии совместимы
                data["version"] = CACHE_VERSION
            data.setdefault("tracks", {})
            return data
    except Exception:
        return {"version": CACHE_VERSION, "tracks": {}}

def save_cache(cache):
    """Сохраняет кэш. Делает снимок dict чтобы избежать ошибок."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = CACHE_FILE + ".tmp"
    # Снимок — теперь точно никто не изменит во время записи
    snapshot = {"version": cache.get("version", CACHE_VERSION),
                "tracks": dict(cache["tracks"])}
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=1)
    os.replace(tmp, CACHE_FILE)

# ═══════════ ФАЙЛЫ ═══════════
def find_all_audio():
    found, seen = [], set()
    for base in SEARCH_DIRS:
        if not os.path.isdir(base): continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in
                       ("Android/data", "Android/obb", ".thumbnails", ".cache")]
            for f in files:
                if os.path.splitext(f)[1].lower() in AUDIO_EXTS:
                    full = os.path.join(root, f)
                    if full not in seen:
                        seen.add(full); found.append(full)
    return found

# ═══════════ ВОРКЕР (НЕ пишет в кэш!) ═══════════
def worker(path, force):
    """
    Читает метаданные и ищет в интернете.
    ВАЖНО: возвращает (path, entry) или None. НЕ трогает общий кэш.
    """
    local_artist, local_album, local_title, dur = read_local_metadata(path)
    track_type = detect_type(local_title, path)

    # Убираем "Неизвестен" из запроса, чтобы не мусорить
    q_artist = local_artist if local_artist and local_artist.lower() not in ("неизвестен", "unknown") else ""

    # Если в локальных тегах уже есть artist + title — попробуем сначала найти только жанр
    remote = fetch_metadata(local_title, q_artist)

    if remote:
        entry = {
            "title":  remote.get("title") or local_title,
            "artist": remote.get("artist") or local_artist or "Неизвестен",
            "album":  remote.get("album") or local_album or "",
            "genre":  remote.get("genre") or "",
            "year":   remote.get("year") or "",
            "type":   track_type,
            "source": remote.get("source"),
            "duration": dur,
        }
    else:
        entry = {
            "title":  local_title,
            "artist": local_artist or "Неизвестен",
            "album":  local_album or "",
            "genre":  "",
            "year":   "",
            "type":   track_type,
            "source": "local",
            "duration": dur,
        }
    return (path, entry)

# ═══════════ ГЛАВНОЕ ═══════════
def main():
    console.clear()
    force = "--force" in sys.argv

    console.print()
    console.print(Align.center(Panel.fit(
        "[bold green]🌐  MUSIC METADATA FETCHER v2  🌐[/]\n"
        "[dim]iTunes + Deezer + MusicBrainz → кэш в ~/music_cache/[/]",
        border_style="green")))
    console.print()

    console.print("[bold yellow]🔍 Сканирую память телефона...[/]")
    files = find_all_audio()
    console.print(f"   Найдено аудиофайлов: [green]{len(files)}[/]\n")

    cache = load_cache()
    cached_count = len(cache["tracks"])
    console.print(f"💾 В кэше уже: [green]{cached_count}[/] записей\n")

    # Отбираем треки для поиска
    to_process = []
    for f in files:
        existing = cache["tracks"].get(f)
        if force:
            to_process.append(f)
        else:
            # Ищем только те, у которых нет данных из интернета
            if not existing or existing.get("source") in (None, "local", "filename", "filename-only"):
                to_process.append(f)

    if not to_process:
        console.print("[green]✔ Всё уже найдено. Нечего искать.[/]")
        console.print("[dim]Запусти music-force для полного переискивания.[/]")
        return

    console.print(f"[bold cyan]📡 Ищу: {len(to_process)} треков (параллельно в 6 потоков)[/]")
    console.print("[dim]Можно прервать Ctrl+C — прогресс сохранится.[/]\n")

    done = 0
    found_remote = 0
    found_mb = 0
    not_found = 0
    save_every = 20

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            console=console,
        ) as prog:
            task = prog.add_task("Поиск...", total=len(to_process))

            # ВАЖНО: воркеры только возвращают результат, кэш мутирует ГЛАВНЫЙ поток
            with ThreadPoolExecutor(max_workers=6) as pool:
                futures = {pool.submit(worker, f, force): f for f in to_process}
                for fut in as_completed(futures):
                    try:
                        result = fut.result()
                        if result:
                            key, entry = result
                            # Мутация кэша — только в этом потоке
                            cache["tracks"][key] = entry
                            if entry.get("source") in ("itunes", "deezer", "musicbrainz"):
                                found_remote += 1
                                if entry.get("source") == "musicbrainz":
                                    found_mb += 1
                            else:
                                not_found += 1
                    except Exception:
                        pass

                    done += 1
                    prog.update(
                        task, advance=1,
                        description=f"[cyan]✔ {found_remote}  ✘ {not_found}  (MB: {found_mb})"
                    )

                    if done % save_every == 0:
                        try: save_cache(cache)
                        except Exception: pass
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Прервано. Сохраняю...[/]")

    try: save_cache(cache)
    except Exception as e:
        console.print(f"[red]❌ Ошибка сохранения: {e}[/]")

    console.print()
    t = Table(box=box.ROUNDED, show_header=False, border_style="green")
    t.add_column("", style="bold yellow", width=24)
    t.add_column("", style="white")
    t.add_row("✅ Найдено в интернете", f"[green]{found_remote}[/]")
    t.add_row("   из них MusicBrainz",  f"[cyan]{found_mb}[/]")
    t.add_row("⚠ Не найдено",          f"[yellow]{not_found}[/]")
    t.add_row("💾 Всего в кэше",         f"[cyan]{len(cache['tracks'])}[/]")
    t.add_row("📁 Файл",                 f"[dim]{CACHE_FILE}[/]")
    console.print(t)
    console.print()
    console.print("[green]✔ Готово. Запусти [cyan]music[/][/]")
    console.print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]Прервано.[/]")
