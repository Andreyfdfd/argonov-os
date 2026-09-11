#!/data/data/com.termux/files/usr/bin/bash
# ═══════════════════════════════════════════════════════
#  ARGONOV OS — установщик v1.0
#  Устанавливает всё с нуля на чистый Termux
# ═══════════════════════════════════════════════════════

set -e

G="\033[92m"; C="\033[96m"; Y="\033[93m"; R="\033[91m"; DIM="\033[2m"; RST="\033[0m"
BLD="\033[1m"

# Корень репозитория (папка где лежит install.sh)
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

log()  { echo -e "${Y}[$1/9]${RST} $2"; }
ok()   { echo -e "${G}✔${RST} $1"; }
err()  { echo -e "${R}✘${RST} $1"; }

echo ""
echo -e "${C}┌─────────────────────────────────────────────────┐${RST}"
echo -e "${C}│${RST}        ${BLD}⚡ УСТАНОВКА ARGONOV OS ⚡${RST}          ${C}│${RST}"
echo -e "${C}│${RST}       ${DIM}Кастомная оболочка для Termux${RST}         ${C}│${RST}"
echo -e "${C}└─────────────────────────────────────────────────┘${RST}"
echo ""

# ═══════════ 1. СИСТЕМНЫЕ ПАКЕТЫ ═══════════
log 1 "Обновление pkg и установка базовых пакетов..."
pkg update -y >/dev/null 2>&1 || true

pkg install -y \
    python python-pip git fish starship neovim tmux nano \
    chafa ffmpeg curl wget aria2 jq yq ripgrep fd fzf zoxide \
    eza bat imagemagick tree openssl libffi \
    clang rust binutils cmake \
    dnsutils nmap whois \
    gh termux-api llama-cpp \
    2>&1 | grep -vE "^Hit|^Get|^Reading|^Preparing|^Unpacking|^Setting|^Selecting|^Processing" || true
ok "Базовые пакеты установлены"

# ═══════════ 2. PYTHON-БИБЛИОТЕКИ ═══════════
log 2 "Установка Python-библиотек..."
pip install --upgrade pip >/dev/null 2>&1 || true

pip install \
    rich requests httpx aiohttp beautifulsoup4 lxml \
    fastapi uvicorn pydantic aiogram sqlalchemy \
    psutil colorama tqdm halo pyfiglet qrcode pillow pyperclip \
    feedparser python-whois dnspython python-dotenv \
    mutagen cryptography prompt_toolkit \
    2>&1 | grep -vE "Requirement already|Collecting|Downloading|Installing collected" || true
ok "Python-библиотеки установлены"

# ═══════════ 3. VIU (показ картинок) ═══════════
log 3 "Установка viu (показ картинок)..."
if command -v viu &>/dev/null; then
    ok "viu уже установлен"
else
    echo -e "${DIM}   Компиляция viu через cargo (это займёт 5-10 мин)...${RST}"
    cargo install viu 2>&1 | tail -3 || true
    if command -v viu &>/dev/null || [ -f "$HOME/.cargo/bin/viu" ]; then
        ok "viu установлен"
    else
        err "viu не установился (можно потом: cargo install viu)"
    fi
fi

# ═══════════ 4. КОПИРОВАНИЕ СКРИПТОВ ═══════════
log 4 "Копирование скриптов в \$HOME..."

# Список всех скриптов (при отсутствии — пропустит)
SCRIPTS="ai.py crypto_informer.py randomaudio.py todo.py notes.py \
         passmanager.py hacktool.py hacker_rpg.py download_zone.py \
         matrix.py passgen.py sysinfo.py utils.py music_meta.py art.py"

for f in $SCRIPTS; do
    if [ -f "$REPO_DIR/$f" ]; then
        cp "$REPO_DIR/$f" "$HOME/"
    fi
done

# Главная команда
if [ -f "$REPO_DIR/argonov" ]; then
    cp "$REPO_DIR/argonov" "$HOME/"
    chmod +x "$HOME/argonov"
fi

# Symlink в $PREFIX/bin, чтобы команда работала откуда угодно
if [ -f "$HOME/argonov" ]; then
    ln -sf "$HOME/argonov" "$PREFIX/bin/argonov"
    ok "argonov доступен глобально"
fi
ok "Скрипты скопированы"

# ═══════════ 5. FISH CONFIG ═══════════
log 5 "Установка Fish-конфига..."
mkdir -p "$HOME/.config/fish"
if [ -f "$REPO_DIR/fish-config/config.fish" ]; then
    cp "$REPO_DIR/fish-config/config.fish" "$HOME/.config/fish/config.fish"
    ok "Fish-конфиг установлен"
fi

# ═══════════ 6. TERMUX THEME ═══════════
log 6 "Установка темы Termux..."
mkdir -p "$HOME/.termux"
if [ -f "$REPO_DIR/termux-config/colors.properties" ]; then
    cp "$REPO_DIR/termux-config/colors.properties" "$HOME/.termux/"
fi
if [ -f "$REPO_DIR/termux-config/termux.properties" ]; then
    cp "$REPO_DIR/termux-config/termux.properties" "$HOME/.termux/"
fi
termux-reload-settings 2>/dev/null || true
ok "Тема применена"

# ═══════════ 7. УСТАНОВКА FISH ПО УМОЛЧАНИЮ ═══════════
log 7 "Настройка fish как оболочки по умолчанию..."
CURRENT_SHELL=$(basename "$SHELL" 2>/dev/null || echo "bash")
if [ "$CURRENT_SHELL" != "fish" ]; then
    FISH_PATH=$(command -v fish)
    if [ -n "$FISH_PATH" ]; then
        chsh -s fish 2>/dev/null || true
        ok "fish установлен как оболочка по умолчанию"
    fi
else
    ok "fish уже используется"
fi

# ═══════════ 8. AI-МОДЕЛЬ (ОПЦИОНАЛЬНО) ═══════════
log 8 "Проверка AI-модели..."
if ls "$HOME"/*.gguf >/dev/null 2>&1; then
    ok "Модели найдены в \$HOME"
    ls -lh "$HOME"/*.gguf | awk '{print "   " $NF " (" $5 ")"}'
else
    echo -e "${Y}   Модели AI не найдены.${RST}"
    echo -e "${DIM}   Скачать Qwen 2.5 Coder 3B (~2 ГБ)?${RST}"
    echo -ne "${C}   Скачать? (y/N)> ${RST}"
    read -r ans
    if [ "$ans" = "y" ]; then
        echo -e "${DIM}   Загрузка (~5-15 мин)...${RST}"
        wget -O "$HOME/qwen3b.gguf" \
            "https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF/resolve/main/qwen2.5-coder-3b-instruct-q4_k_m.gguf" \
            || err "Не удалось скачать (можно потом вручную)"
    else
        echo -e "${DIM}   Пропущено. AI не будет работать без модели.${RST}"
    fi
fi

# ═══════════ 9. ФИНАЛЬНАЯ НАСТРОЙКА ═══════════
log 9 "Финальная настройка..."

# Дать доступ к памяти
echo -e "${DIM}   Настройка доступа к памяти телефона...${RST}"
termux-setup-storage 2>/dev/null || true
sleep 1

# Создать директории
mkdir -p "$HOME/music_cache/covers" "$HOME/music_cache/exports"
mkdir -p "$HOME/ai_chats" "$HOME/argonov_backups"
ok "Директории созданы"

# Проверка argonov
if [ -f "$HOME/argonov" ]; then
    chmod +x "$HOME/argonov"
fi

echo ""
echo -e "${G}════════════════════════════════════════════════${RST}"
echo -e "${BLD}${G}   ✅ УСТАНОВКА ЗАВЕРШЕНА!${RST}"
echo -e "${G}════════════════════════════════════════════════${RST}"
echo ""
echo -e "  ${C}Запуск:${RST}      ${G}argonov${RST}"
echo -e "  ${C}Проверка:${RST}    ${G}argonov doctor${RST}"
echo -e "  ${C}Справка:${RST}     ${G}argonov help${RST}"
echo ""
echo -e "  ${DIM}Если не работает 'argonov' — перезапусти Termux${RST}"
echo -e "  ${DIM}Или используй полный путь: ~/argonov${RST}"
echo ""

# Автоматический запуск если доступен
if [ -f "$HOME/argonov" ]; then
    echo -ne "${C}Запустить Argonov сейчас? (y/N)> ${RST}"
    read -r ans
    if [ "$ans" = "y" ]; then
        cd "$HOME" && ./argonov
    fi
fi
