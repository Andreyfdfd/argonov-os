#!/data/data/com.termux/files/usr/bin/bash
read -p "Удалить Argonov OS? (y/N): " ans
if [ "$ans" != "y" ]; then exit 0; fi
rm -f "$HOME"/{ai,crypto_informer,download_zone,hacktool,matrix,music_meta,notes,passmanager,passgen,randomaudio,sysinfo,todo,utils}.py
rm -f "$HOME/argonov"
echo "Удалено. Личные данные сохранены."
