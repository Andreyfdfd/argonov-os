#!/data/data/com.termux/files/usr/bin/bash
set -e
G="\033[92m"; C="\033[96m"; Y="\033[93m"; RST="\033[0m"

echo ""
echo -e "${C}Установка Argonov OS${RST}"
echo ""

echo -e "${Y}[1/5]${RST} Системные пакеты..."
pkg update -y
pkg install -y python python-pip git fish starship neovim tmux \
    chafa ffmpeg curl wget aria2 jq ripgrep fd fzf zoxide \
    eza bat imagemagick nano tree

echo -e "${Y}[2/5]${RST} Python-библиотеки..."
pip install --upgrade pip
pip install rich requests httpx aiohttp beautifulsoup4 lxml \
    fastapi uvicorn pydantic aiogram sqlalchemy \
    psutil colorama tqdm halo pyfiglet qrcode pillow pyperclip \
    feedparser python-whois dnspython python-dotenv \
    mutagen cryptography prompt_toolkit

echo -e "${Y}[3/5]${RST} Скрипты в HOME..."
cp ai.py crypto_informer.py download_zone.py hacktool.py matrix.py \
   music_meta.py notes.py passmanager.py passgen.py randomaudio.py \
   sysinfo.py todo.py utils.py argonov "$HOME/"
chmod +x "$HOME/argonov"

echo -e "${Y}[4/5]${RST} Fish config..."
mkdir -p "$HOME/.config/fish"
cp fish-config/config.fish "$HOME/.config/fish/" 2>/dev/null || true

echo -e "${Y}[5/5]${RST} Termux config..."
mkdir -p "$HOME/.termux"
cp termux-config/colors.properties "$HOME/.termux/" 2>/dev/null || true
cp termux-config/termux.properties "$HOME/.termux/" 2>/dev/null || true

echo ""
echo -e "${G}Установка завершена!${RST}"
echo -e "Запусти: ${C}argonov${RST}"
