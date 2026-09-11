# ⚡ ARGONOV OS

**Кастомная оболочка для Termux на Android с локальным AI, хакерскими инструментами, музыкой, RPG и 10+ утилитами.**

---

## 🚀 УСТАНОВКА (одна команда)

### Способ 1: Быстрая установка (Termux)

Открой Termux и выполни:

```bash
pkg install git -y && \
git clone https://github.com/Andreyfdfd/argonov-os.git && \
cd argonov-os && \
bash install.sh
```

После установки запусти:

```bash
argonov
```

### Способ 2: Пошаговая установка

**Шаг 1. Установка Termux**
- Скачай **Termux** из [F-Droid](https://f-droid.org/packages/com.termux/) (НЕ из Google Play — там устаревшая версия!)
- Установи также: **Termux:API**, **Termux:Styling** (из F-Droid)

**Шаг 2. Клонирование репозитория**

```bash
pkg install git -y
git clone https://github.com/Andreyfdfd/argonov-os.git
cd argonov-os
```

**Шаг 3. Запуск установщика**

```bash
bash install.sh
```

**Шаг 4. Запуск**

```bash
argonov
```

---

## 📦 ЧТО УСТАНАВЛИВАЕТСЯ

### Системные пакеты (pkg)
- `python` — основной язык
- `git`, `fish`, `starship` — оболочка
- `neovim`, `tmux`, `nano` — редакторы
- `chafa`, `ffmpeg` — работа с медиа
- `curl`, `wget`, `aria2` — загрузка
- `jq`, `yq`, `ripgrep`, `fd`, `fzf` — утилиты
- `llama-cpp` — локальный AI
- `viu` — показ картинок (через cargo)
- `clang`, `rust`, `cargo` — компиляторы

### Python-библиотеки (pip)
- `rich`, `prompt_toolkit` — UI
- `requests`, `httpx`, `aiohttp` — сеть
- `fastapi`, `uvicorn` — веб-серверы
- `aiogram` — Telegram-боты
- `sqlalchemy`, `aiosqlite` — БД
- `psutil`, `tqdm`, `halo` — мониторинг
- `pyfiglet`, `qrcode`, `pillow` — визуал
- `cryptography` — шифрование
- `mutagen` — метаданные музыки

---

## 🎮 ВОЗМОЖНОСТИ

| Утилита | Команда | Что делает |
|---------|---------|-----------|
| 🧠 **AI-ассистент** | `ai` | Qwen 2.5 Coder 3B локально + exec/write/read |
| 🎮 **HackTool** | `hack` | 28 команд OSINT: scan, nmap, subdomain, hashid, ctf-links |
| 🎵 **Music** | `music` | Библиотека с обложками iTunes, favorites, экспорт M3U/CSV |
| 📌 **Todo** | `todo` | Трекер задач с приоритетами и уведомлениями |
| 📝 **Notes** | `notes` | Заметки с тегами, поиском, экспортом |
| 🔒 **PassManager** | `pm` | AES-256 хранилище паролей |
| 📈 **Crypto** | `crypto` | Курсы BTC/ETH/SOL в реальном времени |
| 🕹 **RPG** | `rpg` | Симулятор Хакера — 20 миссий, мини-игры, фракции |
| 📥 **Download** | `d` | Многопоточный загрузчик через aria2c |
| 🌧 **Matrix** | `m` | Цифровой дождь |
| ⚡ **Sysinfo** | `s` | Центр управления системой |
| 📦 **Utils** | `util` | Сканер пакетов с размерами |
| 🎨 **Art** | `art` | Поиск картинок по телефону + welcome-картинка |

---

## 🎯 ИСПОЛЬЗОВАНИЕ

### Главное меню

```bash
argonov
```

Открывает интерактивное меню со всеми командами.

### Прямой запуск

```bash
argonov ai       # AI-ассистент
argonov music    # Музыка
argonov todo     # Задачи
argonov hack     # Хакерский тул
argonov rpg      # RPG
argonov push     # Сохранить в GitHub
argonov doctor   # Проверка целостности
```

### Горячие команды (из fish)

```bash
ai       # AI
music    # Музыка
todo     # Задачи
notes    # Заметки
pm       # Пароли
hack     # Hack
rpg      # RPG
crypto   # Крипта
util     # Утилиты
s        # Sysinfo
art      # Картинка
clear    # Очистка + плашка
```

---

## 🧠 AI — УМНАЯ ИНТЕГРАЦИЯ

AI понимает команды и **сам выполняет** их. Примеры:

```
Ты:  запусти матрицу
AI:  ```exec
     python ~/matrix.py
     ```
     [Подтверди y] → матрица запускается

Ты:  создай файл ~/test.py с print('hello') и запусти
AI:  ```write
     ~/test.py
     print('hello')
     ```
     ```exec
     python ~/test.py
     ```
     [Подтверди] → файл создан и запущен
```

**AI умеет:**
- ✅ `exec` — выполнять любые команды
- ✅ `write` — создавать/изменять файлы
- ✅ `read` — читать файлы для контекста
- ✅ Работать в PTY (запускает curses-программы)
- ✅ Sandbox: только `~/` и `~/storage`

**Команды AI:**
- `sudo` — режим БЕЗ подтверждения (осторожно!)
- `sandbox` — вкл/выкл sandbox
- `команды` — вкл/выкл exec
- `модель` — переключить модель
- `env` — показать окружение

---

## 🔧 ТРЕБОВАНИЯ

- Android 10+
- Termux (F-Droid версия)
- 4+ ГБ ОЗУ (для AI)
- 8+ ГБ свободного места
- **Опционально:** llama-cpp + модель Qwen 2.5 Coder 3B (~2 ГБ)

### Установка AI-модели

```bash
cd ~
wget -O qwen3b.gguf "https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF/resolve/main/qwen2.5-coder-3b-instruct-q4_k_m.gguf"
```

---

## 🌐 GIT И БЭКАПЫ

```bash
argonov push      # Закоммитить и отправить в GitHub
argonov pull      # Забрать обновления
argonov status    # Показать статус git
argonov backup    # Создать бэкап всех данных
argonov restore   # Восстановить из бэкапа
argonov doctor    # Проверить целостность системы
```

---

## 📁 СТРУКТУРА

```
~/argonov-os/              # Репозиторий
├── argonov                # Главная команда
├── ai.py                  # AI-ассистент
├── hacktool.py            # Хакерский тул
├── randomaudio.py         # Музыка
├── todo.py                # Задачи
├── notes.py               # Заметки
├── passmanager.py         # Пароли
├── crypto_informer.py     # Крипта
├── hacker_rpg.py          # RPG
├── download_zone.py       # Загрузчик
├── matrix.py              # Матрица
├── passgen.py             # Генератор паролей
├── sysinfo.py             # Sysinfo
├── utils.py               # Утилиты
├── art.py                 # Картинки
├── music_meta.py          # Метаданные музыки
├── install.sh             # Установщик
├── update.sh              # Обновление
├── uninstall.sh           # Удаление
├── fish-config/           # Fish config
└── termux-config/         # Termux theme
```

---

## 🎨 ТЕМА TERMUX

Для полного CRT-стиля:
1. Установи **Termux:Styling** (F-Droid)
2. В Termux выбери шрифт **JetBrains Mono** или **Fira Code**

Цвета автоматически применятся через `~/.termux/colors.properties`.

---

## 🐛 РЕШЕНИЕ ПРОБЛЕМ

**AI не запускается:**
```bash
pkg install llama-cpp -y
ls ~/*.gguf  # Проверь что модель есть
```

**Music не находит треки:**
```bash
termux-setup-storage  # Дать доступ к памяти
python ~/music_meta.py  # Пересобрать библиотеку
```

**Не работает viu (картинки):**
```bash
cargo install viu
```

**Ошибка PermissionError:**
```bash
termux-setup-storage
```

---

## 📜 ЛИЦЕНЗИЯ

MIT License — используй свободно.

---

## ⭐ ПОДДЕРЖКА

Если проект полезен — поставь ⭐ на GitHub.

**Автор:** [@Andreyfdfd](https://github.com/Andreyfdfd)

**Версия:** v1.3.0
