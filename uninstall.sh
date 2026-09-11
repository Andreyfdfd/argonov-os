#!/data/data/com.termux/files/usr/bin/bash
# Удаление Argonov OS из $HOME
R="\033[91m"; Y="\033[93m"; G="\033[92m"; RST="\033[0m"

echo -e "${R}⚠ УДАЛЕНИЕ Argonov OS из \$HOME${RST}"
echo ""
echo "Будут удалены:"
echo "  • Все скрипты в ~/ (*.py, argonov)"
echo "  • Fish-конфиг (~/.config/fish/config.fish)"
echo "  • Termux-тема (~/.termux/colors.properties)"
echo ""
echo -e "${Y}НЕ будут удалены (личные данные):${RST}"
echo "  • ~/.pm.vault (пароли)"
echo "  • ~/.todo.json (задачи)"
echo "  • ~/.notes.json (заметки)"
echo "  • ~/.hacker_rpg_save.json (RPG прогресс)"
echo "  • ~/*.gguf (модели AI)"
echo "  • ~/storage (файлы телефона)"
echo ""
echo -ne "${R}Продолжить? (yes/n)> ${RST}"
read -r ans
if [ "$ans" != "yes" ]; then
    echo "Отменено"
    exit 0
fi

# Удаление скриптов
for f in ai.py crypto_informer.py randomaudio.py todo.py notes.py \
         passmanager.py hacktool.py hacker_rpg.py download_zone.py \
         matrix.py passgen.py sysinfo.py utils.py music_meta.py art.py; do
    rm -f "$HOME/$f"
done
rm -f "$HOME/argonov"
rm -f "$PREFIX/bin/argonov"

# Fish config
rm -f "$HOME/.config/fish/config.fish"

# Termux theme
rm -f "$HOME/.termux/colors.properties"
rm -f "$HOME/.termux/termux.properties"

echo ""
echo -e "${G}✔ Argonov OS удалён${RST}"
echo -e "${Y}Личные данные и модели сохранены${RST}"
