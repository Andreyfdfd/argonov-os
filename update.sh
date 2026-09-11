#!/data/data/com.termux/files/usr/bin/bash
# Обновление Argonov OS из GitHub
G="\033[92m"; Y="\033[93m"; R="\033[91m"; RST="\033[0m"

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR" || exit 1

echo -e "${Y}⚙ Обновление из GitHub...${RST}"
git pull origin main || { echo -e "${R}✘ git pull failed${RST}"; exit 1; }

echo -e "${Y}⚙ Копирую обновлённые скрипты...${RST}"
for f in ai.py crypto_informer.py randomaudio.py todo.py notes.py \
         passmanager.py hacktool.py hacker_rpg.py download_zone.py \
         matrix.py passgen.py sysinfo.py utils.py music_meta.py art.py argonov; do
    [ -f "$REPO_DIR/$f" ] && cp "$REPO_DIR/$f" "$HOME/"
done
chmod +x "$HOME/argonov"
ln -sf "$HOME/argonov" "$PREFIX/bin/argonov"

# Обновить fish config
[ -f "$REPO_DIR/fish-config/config.fish" ] && \
    cp "$REPO_DIR/fish-config/config.fish" "$HOME/.config/fish/config.fish"

echo -e "${G}✔ Обновление завершено${RST}"
echo -e "${Y}Перезапусти Termux чтобы применить изменения${RST}"
