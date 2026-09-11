#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Net Helper v2.2 — fallback + кэш + force-refresh"""

import json, time, os, sys, hashlib
import urllib.request, urllib.error, urllib.parse

DEFAULT_UA = "Mozilla/5.0 (Linux; Android 10; Termux) AppleWebKit/537.36"

CACHE_DIR         = os.path.expanduser("~/.cache/argonov")
CACHE_DEFAULT_TTL = 300
CACHE_MAX_AGE     = 86400
CACHE_DISABLED    = os.environ.get("ARGONOV_NO_CACHE") == "1"

_set_counter = 0

def _cache_path(key):
    safe  = hashlib.md5(key.encode("utf-8")).hexdigest()[:16]
    clean = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)[:32]
    return os.path.join(CACHE_DIR, f"{clean}_{safe}.json")

def cache_get_meta(key, ttl=CACHE_DEFAULT_TTL, allow_stale=False):
    if CACHE_DISABLED: return None, None
    p = _cache_path(key)
    if not os.path.exists(p): return None, None
    try:
        with open(p, encoding="utf-8") as f:
            obj = json.load(f)
    except Exception:
        return None, None
    ts = obj.get("ts", 0)
    age = time.time() - ts
    if age <= ttl:
        return obj.get("data"), {"ts": ts, "age": age, "fresh": True, "stale": False}
    if allow_stale and age <= CACHE_MAX_AGE:
        return obj.get("data"), {"ts": ts, "age": age, "fresh": False, "stale": True}
    return None, None

def cache_get(key, ttl=CACHE_DEFAULT_TTL):
    data, _ = cache_get_meta(key, ttl)
    return data

def cache_set(key, data):
    global _set_counter
    if CACHE_DISABLED: return
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        p   = _cache_path(key)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "data": data}, f, ensure_ascii=False)
        os.replace(tmp, p)
        _set_counter += 1
        if _set_counter % 50 == 0: cache_cleanup()
    except Exception:
        pass

def cache_clear():
    if not os.path.isdir(CACHE_DIR): return 0
    n = 0
    for f in os.listdir(CACHE_DIR):
        try: os.remove(os.path.join(CACHE_DIR, f)); n += 1
        except Exception: pass
    return n

def cache_cleanup(max_age=CACHE_MAX_AGE):
    if not os.path.isdir(CACHE_DIR): return 0
    now = time.time(); n = 0
    for f in os.listdir(CACHE_DIR):
        p = os.path.join(CACHE_DIR, f)
        try:
            if now - os.path.getmtime(p) > max_age:
                os.remove(p); n += 1
        except Exception: pass
    return n

def cache_info():
    if not os.path.isdir(CACHE_DIR):
        return {"files": 0, "size": 0, "dir": CACHE_DIR}
    files = [os.path.join(CACHE_DIR, f) for f in os.listdir(CACHE_DIR)]
    size  = sum(os.path.getsize(f) for f in files if os.path.isfile(f))
    return {"files": len(files), "size": size, "dir": CACHE_DIR}

# ═══════════════════════════════════════════════════════
def fetch(url, timeout=10, headers=None, parse="json"):
    h = {"User-Agent": DEFAULT_UA, "Accept": "*/*"}
    if headers: h.update(headers)
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read().decode("utf-8", errors="ignore")
        if parse == "json":
            try: return json.loads(data)
            except Exception: return None
        return data
    except Exception:
        return None

def get_json_cached(url, ttl=CACHE_DEFAULT_TTL, cache_key=None, timeout=10, headers=None):
    key = cache_key or f"json:{url}"
    cached = cache_get(key, ttl)
    if cached is not None: return cached
    data = fetch(url, timeout=timeout, headers=headers, parse="json")
    if data is not None: cache_set(key, data)
    return data

def get_text_cached(url, ttl=CACHE_DEFAULT_TTL, cache_key=None, timeout=10, headers=None):
    key = cache_key or f"text:{url}"
    cached = cache_get(key, ttl)
    if cached is not None: return cached
    data = fetch(url, timeout=timeout, headers=headers, parse="text")
    if data is not None: cache_set(key, data)
    return data

def try_sources(sources, timeout=8):
    for name, fn in sources:
        try:
            data = fn(timeout)
            if data: return data, name
        except Exception:
            continue
    return None, None

# ═══ КРИПТА ═══
def crypto_coingecko(timeout=8):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin,cardano&vs_currencies=usd,rub&include_24hr_change=true"
    data = fetch(url, timeout=timeout)
    if not data: return None
    out = {}
    for cid, d in data.items():
        out[cid] = {
            "symbol": {"bitcoin":"BTC","ethereum":"ETH","solana":"SOL",
                       "binancecoin":"BNB","cardano":"ADA"}.get(cid, cid.upper()[:4]),
            "name": {"bitcoin":"Bitcoin","ethereum":"Ethereum","solana":"Solana",
                     "binancecoin":"BNB","cardano":"Cardano"}.get(cid, cid.title()),
            "usd": d.get("usd", 0), "rub": d.get("rub", 0),
            "change_24h": d.get("usd_24h_change", 0),
        }
    return out if out else None

def crypto_coincap(timeout=8):
    url = "https://api.coincap.io/v2/assets?ids=bitcoin,ethereum,solana,binance-coin,cardano"
    data = fetch(url, timeout=timeout)
    if not data or "data" not in data: return None
    out = {}
    for a in data["data"]:
        cid = a["id"]
        cid_key = "binancecoin" if cid == "binance-coin" else cid
        out[cid_key] = {
            "symbol": a["symbol"], "name": a["name"],
            "usd": float(a["priceUsd"] or 0), "rub": 0,
            "change_24h": float(a.get("changePercent24Hr") or 0),
        }
    return out if out else None

def crypto_paprika(timeout=8):
    url = "https://api.coinpaprika.com/v1/tickers?quotes=USD,RUB"
    data = fetch(url, timeout=timeout)
    if not data: return None
    targets = {"btc-bitcoin":"bitcoin","eth-ethereum":"ethereum",
               "sol-solana":"solana","bnb-binance-coin":"binancecoin",
               "ada-cardano":"cardano"}
    out = {}
    for a in data:
        if a["id"] in targets:
            key = targets[a["id"]]
            q = a.get("quotes", {})
            out[key] = {
                "symbol": a["symbol"], "name": a["name"],
                "usd": q.get("USD", {}).get("price", 0),
                "rub": q.get("RUB", {}).get("price", 0),
                "change_24h": q.get("USD", {}).get("percent_change_24h", 0),
            }
    return out if out else None

def crypto_binance(timeout=8):
    symbols = {"BTCUSDT":"bitcoin","ETHUSDT":"ethereum","SOLUSDT":"solana",
               "BNBUSDT":"binancecoin","ADAUSDT":"cardano"}
    out = {}
    for sym, key in symbols.items():
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={sym}"
        d = fetch(url, timeout=timeout)
        if d and "lastPrice" in d:
            out[key] = {
                "symbol": key.upper()[:4], "name": key.title(),
                "usd": float(d["lastPrice"]), "rub": 0,
                "change_24h": float(d.get("priceChangePercent", 0)),
            }
    return out if out else None

def get_crypto_prices(ttl=CACHE_DEFAULT_TTL, with_meta=False, force=False):
    """
    force=True → игнорирует свежий кэш, делает live fetch.
    При падении сети всё равно берёт stale кэш.
    """
    key = "prices:crypto"
    if not force:
        cached, meta = cache_get_meta(key, ttl, allow_stale=True)
        if cached:
            src = cached.get("source", "кэш")
            label = f"{src} (STALE)" if meta["stale"] else f"{src} (кэш)"
            if with_meta: return cached.get("data"), label, meta
            return cached.get("data"), label

    sources = [
        ("CoinGecko",   crypto_coingecko),
        ("CoinPaprika", crypto_paprika),
        ("CoinCap",     crypto_coincap),
        ("Binance",     crypto_binance),
    ]
    data, source = try_sources(sources)
    if data:
        cache_set(key, {"data": data, "source": source})
        live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
        if with_meta: return data, source, live_meta
        return data, source

    stale = cache_get(key, ttl=CACHE_MAX_AGE)
    if stale:
        label = f"{stale.get('source','?')} (STALE)"
        stale_meta = {"fresh": False, "stale": True, "age": CACHE_MAX_AGE, "ts": 0}
        if with_meta: return stale.get("data"), label, stale_meta
        return stale.get("data"), label

    if with_meta: return None, None, None
    return None, None

# ═══ КУРС ВАЛЮТ ═══
def fx_cbr_xml(timeout=8):
    data = fetch("https://www.cbr-xml-daily.ru/daily_json.js", timeout=timeout)
    if not data or "Valute" not in data: return None
    v = data["Valute"]
    usd_rub = v.get("USD", {}).get("Value")
    eur_rub = v.get("EUR", {}).get("Value")
    if not usd_rub: return None
    return {
        "USD_RUB": usd_rub, "EUR_RUB": eur_rub,
        "USD_EUR": (usd_rub / eur_rub) if eur_rub else None,
        "updated": data.get("Date", "")[:10], "source": "ЦБ РФ",
    }

def fx_erapi(timeout=8):
    data = fetch("https://open.er-api.com/v6/latest/USD", timeout=timeout)
    if not data or data.get("result") != "success": return None
    rates = data.get("rates", {})
    usd_rub = rates.get("RUB"); usd_eur = rates.get("EUR")
    if not usd_rub: return None
    return {
        "USD_RUB": usd_rub,
        "EUR_RUB": (usd_rub / usd_eur) if usd_eur else None,
        "USD_EUR": usd_eur,
        "updated": data.get("time_last_update_utc", "")[:16],
        "source": "open.er-api.com",
    }

def fx_frankfurter(timeout=8):
    data = fetch("https://api.frankfurter.app/latest?from=USD&to=RUB,EUR", timeout=timeout)
    if not data or "rates" not in data: return None
    rates = data["rates"]
    usd_rub = rates.get("RUB"); usd_eur = rates.get("EUR")
    if not usd_rub: return None
    return {
        "USD_RUB": usd_rub,
        "EUR_RUB": (usd_rub / usd_eur) if usd_eur else None,
        "USD_EUR": usd_eur,
        "updated": data.get("date", ""), "source": "ECB (Frankfurter)",
    }

def fx_exhost(timeout=8):
    data = fetch("https://api.exchangerate.host/latest?base=USD&symbols=RUB,EUR", timeout=timeout)
    if not data or "rates" not in data: return None
    rates = data["rates"]
    usd_rub = rates.get("RUB"); usd_eur = rates.get("EUR")
    if not usd_rub: return None
    return {
        "USD_RUB": usd_rub,
        "EUR_RUB": (usd_rub / usd_eur) if usd_eur else None,
        "USD_EUR": usd_eur,
        "updated": data.get("date", ""), "source": "exchangerate.host",
    }

def get_fx_rates(ttl=1800, with_meta=False, force=False):
    key = "prices:fx"
    if not force:
        cached, meta = cache_get_meta(key, ttl, allow_stale=True)
        if cached:
            src = cached.get("source", "кэш")
            label = f"{src} (STALE)" if meta["stale"] else f"{src} (кэш)"
            if with_meta: return cached.get("data"), label, meta
            return cached.get("data"), label

    sources = [
        ("ЦБ РФ",            fx_cbr_xml),
        ("open.er-api",      fx_erapi),
        ("Frankfurter",      fx_frankfurter),
        ("exchangerate.host",fx_exhost),
    ]
    data, source = try_sources(sources)
    if data:
        cache_set(key, {"data": data, "source": source})
        live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
        if with_meta: return data, source, live_meta
        return data, source

    stale = cache_get(key, ttl=CACHE_MAX_AGE)
    if stale:
        label = f"{stale.get('source','?')} (STALE)"
        stale_meta = {"fresh": False, "stale": True, "age": CACHE_MAX_AGE, "ts": 0}
        if with_meta: return stale.get("data"), label, stale_meta
        return stale.get("data"), label

    if with_meta: return None, None, None
    return None, None

# ═══ ГЕО IP ═══
def ip_ipinfo(timeout=8):
    d = fetch("https://ipinfo.io/json", timeout=timeout)
    if not d or "ip" not in d: return None
    return {"ip": d.get("ip"), "city": d.get("city"), "region": d.get("region"),
            "country": d.get("country"), "org": d.get("org"),
            "timezone": d.get("timezone"), "loc": d.get("loc"),
            "source": "ipinfo.io"}

def ip_ipapi(timeout=8):
    d = fetch("http://ip-api.com/json/?fields=status,country,regionName,city,isp,query,timezone", timeout=timeout)
    if not d or d.get("status") != "success": return None
    return {"ip": d.get("query"), "city": d.get("city"), "region": d.get("regionName"),
            "country": d.get("country"), "org": d.get("isp"),
            "timezone": d.get("timezone"), "loc": "", "source": "ip-api.com"}

def ip_ipwhois(timeout=8):
    d = fetch("https://ipwhois.app/json/", timeout=timeout)
    if not d or not d.get("ip"): return None
    return {"ip": d.get("ip"), "city": d.get("city"), "region": d.get("region"),
            "country": d.get("country"), "org": d.get("org"),
            "timezone": d.get("timezone"),
            "loc": f"{d.get('latitude','')},{d.get('longitude','')}",
            "source": "ipwhois.app"}

def get_ip_info(ttl=3600, with_meta=False, force=False):
    key = "ip:info"
    if not force:
        cached, meta = cache_get_meta(key, ttl, allow_stale=True)
        if cached:
            src = cached.get("source", "кэш")
            label = f"{src} (STALE)" if meta["stale"] else f"{src} (кэш)"
            if with_meta: return cached.get("data"), label, meta
            return cached.get("data"), label

    sources = [("ipinfo.io", ip_ipinfo), ("ip-api.com", ip_ipapi), ("ipwhois.app", ip_ipwhois)]
    data, source = try_sources(sources)
    if data:
        cache_set(key, {"data": data, "source": source})
        live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
        if with_meta: return data, source, live_meta
        return data, source
    if with_meta: return None, None, None
    return None, None

# ═══ НОВОСТИ ═══
NEWS_FEEDS_RU = [
    ("Хабр",         "https://habr.com/ru/rss/all/all/"),
    ("N+1 Наука",    "https://nplus1.ru/rss"),
    ("3DNews",       "https://3dnews.ru/news/rss/"),
    ("IXBT",         "https://www.ixbt.com/export/news.rss"),
    ("Ferra",        "https://www.ferra.ru/rss/"),
    ("Код Дурова",   "https://kod.ru/rss"),
]
NEWS_FEEDS_GLOBAL = [
    ("TechCrunch",   "https://techcrunch.com/feed/"),
    ("MIT Tech",     "https://www.technologyreview.com/feed/"),
]

def get_news_feeds(include_global=False):
    feeds = list(NEWS_FEEDS_RU)
    if include_global: feeds += NEWS_FEEDS_GLOBAL
    return feeds

# ═══ ОБЛОЖКИ ═══
def cover_itunes(artist, title, timeout=8):
    q = urllib.parse.quote(f"{artist} {title}")
    url = f"https://itunes.apple.com/search?term={q}&entity=song&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("results"): return None
    art = d["results"][0].get("artworkUrl100", "")
    if art: return art.replace("100x100", "600x600")
    return None

def cover_deezer(artist, title, timeout=8):
    q = urllib.parse.quote(f"{artist} {title}")
    url = f"https://api.deezer.com/search?q={q}&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("data"): return None
    first = d["data"][0]
    return first.get("album", {}).get("cover_xl") or first.get("album", {}).get("cover_big")

def cover_lastfm(artist, title, timeout=8, api_key=None):
    if not api_key: return None
    q = urllib.parse.quote(artist)
    url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={q}&api_key={api_key}&format=json"
    d = fetch(url, timeout=timeout)
    if not d: return None
    imgs = d.get("artist", {}).get("image", [])
    for img in reversed(imgs):
        if img.get("#text"): return img["#text"]
    return None

def get_cover(artist, title, ttl=604800, with_meta=False, force=False):
    key = f"cover:{artist.lower()}|{title.lower()}"
    if not force:
        cached, meta = cache_get_meta(key, ttl)
        if cached:
            label = f"{cached.get('source','кэш')} (кэш)"
            if with_meta: return cached.get("url"), label, meta
            return cached.get("url"), label
    sources = [
        ("iTunes", lambda t: cover_itunes(artist, title, timeout=t)),
        ("Deezer", lambda t: cover_deezer(artist, title, timeout=t)),
    ]
    for name, fn in sources:
        try:
            url = fn(8)
            if url:
                cache_set(key, {"url": url, "source": name})
                live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
                if with_meta: return url, name, live_meta
                return url, name
        except Exception:
            continue
    if with_meta: return None, None, None
    return None, None

# ═══ МЕТАДАННЫЕ ═══
def meta_itunes(title, artist, timeout=8):
    q = urllib.parse.quote(f"{artist} {title}" if artist else title)
    url = f"https://itunes.apple.com/search?term={q}&entity=song&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("results"): return None
    r = d["results"][0]
    return {"title":  r.get("trackName","").strip(),
            "artist": r.get("artistName","").strip(),
            "album":  r.get("collectionName","").strip(),
            "genre":  r.get("primaryGenreName","").strip(),
            "year":   (r.get("releaseDate") or "")[:4],
            "source": "iTunes"}

def meta_deezer(title, artist, timeout=8):
    q = urllib.parse.quote(f"{artist} {title}" if artist else title)
    url = f"https://api.deezer.com/search?q={q}&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("data"): return None
    r = d["data"][0]
    return {"title":  r.get("title","").strip(),
            "artist": r.get("artist",{}).get("name","").strip(),
            "album":  r.get("album",{}).get("title","").strip(),
            "genre":  "", "year": "", "source": "Deezer"}

def meta_musicbrainz(title, artist, timeout=10):
    q = urllib.parse.quote(f"{artist} {title}" if artist else title)
    url = f"https://musicbrainz.org/ws/2/recording?query={q}&fmt=json&limit=1"
    d = fetch(url, timeout=timeout)
    if not d or not d.get("recordings"): return None
    rec = d["recordings"][0]
    credits = rec.get("artist-credit", [])
    artist_name = "".join((c.get("name","") + (c.get("joinphrase","") or "")) for c in credits).strip()
    releases = rec.get("releases", [])
    album = releases[0].get("title","").strip() if releases else ""
    year = ""
    if releases and releases[0].get("date"): year = releases[0]["date"][:4]
    genre = ""
    if rec.get("tags"): genre = rec["tags"][0].get("name","").capitalize()
    return {"title":  rec.get("title","").strip(),
            "artist": artist_name, "album": album,
            "genre":  genre, "year": year, "source": "MusicBrainz"}

def get_track_meta(title, artist="", ttl=604800, with_meta=False, force=False):
    key = f"meta:{artist.lower()}|{title.lower()}"
    if not force:
        cached, meta = cache_get_meta(key, ttl)
        if cached:
            label = f"{cached.get('source','кэш')} (кэш)"
            if with_meta: return cached.get("meta"), label, meta
            return cached.get("meta"), label
    sources = [
        ("iTunes",      lambda t: meta_itunes(title, artist, t)),
        ("Deezer",      lambda t: meta_deezer(title, artist, t)),
        ("MusicBrainz", lambda t: meta_musicbrainz(title, artist, t)),
    ]
    for name, fn in sources:
        try:
            meta_data = fn(10)
            if meta_data and meta_data.get("title"):
                cache_set(key, {"meta": meta_data, "source": name})
                live_meta = {"fresh": True, "stale": False, "age": 0.0, "ts": time.time()}
                if with_meta: return meta_data, name, live_meta
                return meta_data, name
        except Exception:
            continue
    if with_meta: return None, None, None
    return None, None

# ═══ БЕЙДЖ СВЕЖЕСТИ ═══
def freshness_badge(meta):
    if not meta:
        return "[dim]· нет данных[/]"
    if meta.get("fresh"):
        return "[bright_green]● LIVE[/]"
    if meta.get("stale"):
        age = meta.get("age", 0)
        if age < 3600:
            return f"[bright_red]⚠ STALE {int(age/60)}мин[/]"
        return f"[bright_red]⚠ STALE {age/3600:.1f}ч[/]"
    age = meta.get("age", 0)
    if age < 60:
        return "[bright_yellow]○ КЭШ <1мин[/]"
    if age < 3600:
        return f"[bright_yellow]○ КЭШ {int(age/60)}мин[/]"
    return f"[bright_yellow]○ КЭШ {age/3600:.1f}ч[/]"

def freshness_badge_plain(meta):
    if not meta: return "· нет"
    if meta.get("fresh"): return "● LIVE"
    if meta.get("stale"):
        age = meta.get("age", 0)
        return f"⚠ STALE {int(age/60)}мин" if age < 3600 else f"⚠ STALE {age/3600:.1f}ч"
    age = meta.get("age", 0)
    if age < 60: return "○ КЭШ <1мин"
    if age < 3600: return f"○ КЭШ {int(age/60)}мин"
    return f"○ КЭШ {age/3600:.1f}ч"

# ═══ SELFTEST + CLI ═══
def selftest():
    print("=" * 55)
    print("  net_helper v2.2 — self-test")
    print("=" * 55)
    print()
    info = cache_info()
    print(f"📁 Cache: {info['dir']}")
    print(f"   Файлов: {info['files']}  ·  Размер: {info['size']} байт")
    print(f"   Отключён: {CACHE_DISABLED}")
    print()

    print("🔍 1. fetch() — сеть...")
    t0 = time.time()
    d = fetch("https://api.ipify.org?format=json", timeout=8)
    print(f"   {'✔' if d else '✘'} [{time.time()-t0:.2f}с] {d}")
    print()

    print("🔍 2. get_fx_rates() — live...")
    t0 = time.time()
    fx, src, meta = get_fx_rates(with_meta=True, force=True)
    print(f"   {'✔' if fx else '✘'} [{time.time()-t0:.2f}с] {src}")
    print(f"     Бейдж: {freshness_badge_plain(meta)}")
    if fx: print(f"     USD_RUB = {fx.get('USD_RUB')}")
    print()

    print("🔍 3. get_fx_rates() — из кэша...")
    t0 = time.time()
    fx2, src2, meta2 = get_fx_rates(with_meta=True)
    dt = time.time() - t0
    print(f"   ✔ [{dt:.2f}с] {src2}")
    print(f"     Бейдж: {freshness_badge_plain(meta2)}")
    print(f"     {'✅ КЭШ РАБОТАЕТ' if dt < 0.5 else '⚠ Медленно'}")
    print()

    print("🔍 4. get_crypto_prices() — live (force)...")
    t0 = time.time()
    cr, src, meta = get_crypto_prices(with_meta=True, force=True)
    print(f"   {'✔' if cr else '✘'} [{time.time()-t0:.2f}с] {src}")
    print(f"     Бейдж: {freshness_badge_plain(meta)}")
    if cr:
        for cid, c in list(cr.items())[:3]:
            print(f"     {c['symbol']:5} = ${c['usd']:,.2f}")
    print()

    print("🔍 5. get_crypto_prices() — из кэша...")
    t0 = time.time()
    cr2, src2, meta2 = get_crypto_prices(with_meta=True)
    dt = time.time() - t0
    print(f"   ✔ [{dt:.2f}с] {src2}")
    print(f"     Бейдж: {freshness_badge_plain(meta2)}")
    print(f"     {'✅ КЭШ РАБОТАЕТ' if dt < 0.5 else '⚠ Медленно'}")
    print()

    print("🔍 6. get_crypto_prices(force=True) — обход кэша...")
    t0 = time.time()
    cr3, src3, meta3 = get_crypto_prices(with_meta=True, force=True)
    dt = time.time() - t0
    print(f"   ✔ [{dt:.2f}с] {src3}")
    print(f"     Бейдж: {freshness_badge_plain(meta3)}")
    print(f"     {'✅ FORCE РАБОТАЕТ (пошёл в сеть)' if dt > 0.2 else '⚠ Не пошёл в сеть'}")
    print()

    info = cache_info()
    print(f"📁 Итог: {info['files']} файлов · {info['size']} байт")
    print()
    print("=" * 55)

if __name__ == "__main__":
    if "--selftest" in sys.argv:        selftest()
    elif "--cache-info" in sys.argv:
        i = cache_info()
        print(f"Dir:   {i['dir']}\nFiles: {i['files']}\nSize:  {i['size']} байт")
    elif "--cache-clear" in sys.argv:
        print(f"✔ Удалено: {cache_clear()}")
    elif "--cache-cleanup" in sys.argv:
        print(f"✔ Удалено старого: {cache_cleanup()}")
    else:
        print("net_helper v2.2 — fallback + кэш + force")
        print()
        print("  python net_helper.py --selftest       — тест")
        print("  python net_helper.py --cache-info     — инфо")
        print("  python net_helper.py --cache-clear    — очистить")
        print("  python net_helper.py --cache-cleanup  — удалить старое")
        print()
        print("  ARGONOV_NO_CACHE=1                    — отключить кэш")
