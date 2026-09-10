#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")"
git pull origin main
cp *.py argonov "$HOME/"
chmod +x "$HOME/argonov"
echo "OK"
