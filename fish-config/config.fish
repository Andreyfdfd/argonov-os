# ~/.config/fish/config.fish
# ═══════════════════════════════════════════════════════
#  ARGONOV OS — Fish config v1.3
# ═══════════════════════════════════════════════════════

# ─── ЦВЕТА FISH ───
set -g fish_color_normal        E6E6E6
set -g fish_color_command       00FF88
set -g fish_color_keyword       00FF88
set -g fish_color_quote         FFD700
set -g fish_color_redirection   00D9FF
set -g fish_color_end           00D9FF
set -g fish_color_error         FF3355
set -g fish_color_param         00D9FF
set -g fish_color_comment       557755
set -g fish_color_match         --background=003322
set -g fish_color_operator      00D9FF
set -g fish_color_escape        00FF88
set -g fish_color_autosuggestion 557755
set -g fish_color_selection     --background=003322
set -g fish_color_search_match  --background=00AA55

set -g fish_pager_color_progress            FFCC00
set -g fish_pager_color_background          --background=000000
set -g fish_pager_color_prefix              00FF88 --bold
set -g fish_pager_color_completion          E6E6E6
set -g fish_pager_color_description          557755
set -g fish_pager_color_selected_background --background=00AA55
set -g fish_pager_color_selected_prefix     000000 --bold
set -g fish_pager_color_selected_completion 000000
set -g fish_pager_color_selected_description 003300

# ─── PATH ДЛЯ CARGO (viu) ───
if test -d ~/.cargo/bin
    if not contains ~/.cargo/bin $PATH
        set -gx PATH ~/.cargo/bin $PATH
    end
end

# ═══════════════════════════════════════════════════════
#  ПЛАШКА КОМАНД
# ═══════════════════════════════════════════════════════
function plate --description '📌 Показать плашку команд'
    set_color brblack
    echo '  ┌─ 📌 Доступные команды ──────────────────────────────────'
    set_color cyan
    echo -n '  │  ⚡ argonov  '
    set_color brblack
    echo -n '— меню всех команд    '
    set_color cyan
    echo -n '🧠 ai     '
    set_color brblack
    echo '— AI-ассистент'
    set_color cyan
    echo -n '  │  🎵 music    '
    set_color brblack
    echo -n '— плеер               '
    set_color cyan
    echo -n '📝 notes  '
    set_color brblack
    echo '— заметки'
    set_color cyan
    echo -n '  │  📌 todo     '
    set_color brblack
    echo -n '— задачи              '
    set_color cyan
    echo -n '🔒 pm     '
    set_color brblack
    echo '— пароли'
    set_color cyan
    echo -n '  │  🎮 hack     '
    set_color brblack
    echo -n '— хакерский тул       '
    set_color cyan
    echo -n '🕹  rpg    '
    set_color brblack
    echo '— симулятор хакера'
    set_color cyan
    echo -n '  │  📈 crypto   '
    set_color brblack
    echo -n '— крипта              '
    set_color cyan
    echo -n '🎨 art    '
    set_color brblack
    echo '— картинка'
    set_color brblack
    echo '  └─ Tab — автодополнение  •  ↑↓ — выбор ──────────────────'
    set_color normal
end

# ═══════════════════════════════════════════════════════
#  ОБЁРТКИ clear / reset
# ═══════════════════════════════════════════════════════
function clear --description '🧹 Очистить + плашка'
    command clear
    plate
end

function reset --description '🔄 Reset + плашка'
    command reset
    plate
end

# ═══════════════════════════════════════════════════════
#  PROMPT
# ═══════════════════════════════════════════════════════
function fish_prompt
    set -l last_status $status
    set -l t (date +%H:%M)
    set -l arrow_color magenta
    if test $last_status -ne 0
        set arrow_color red
    end
    echo ''
    echo ''
    set_color magenta --bold
    echo -n '╭─[ ⚡ '
    set_color brmagenta --bold
    echo -n 'termux'
    set_color magenta --bold
    echo -n ' ]──[ '
    set_color bryellow --bold
    echo -n '☀ ESCANOR'
    set_color magenta --bold
    echo -n ' ]──[ '
    set_color yellow
    echo -n $t
    set_color magenta --bold
    echo -n ' ]'
    if command -sq git
        set -l branch (command git rev-parse --abbrev-ref HEAD 2>/dev/null)
        if test -n "$branch"
            echo -n '──[ '
            set_color brmagenta --bold
            echo -n "🌿 $branch"
            set_color magenta --bold
            echo -n ' ]'
        end
    end
    echo ''
    set_color $arrow_color --bold
    echo -n '╰─❯ '
    set_color normal
end

function fish_right_prompt
    set -l dur $CMD_DURATION
    if test -n "$dur"; and test $dur -gt 1000
        set -l secs (math "round($dur / 100) / 10")
        set_color brblack
        echo -n "$secs s"
    end
end

# ═══════════════════════════════════════════════════════
#  АЛИАСЫ
# ═══════════════════════════════════════════════════════
alias ls='eza --icons'
alias ll='eza -lh --icons --git'
alias la='eza -lah --icons --git'
alias cat='bat'

# ═══════════════════════════════════════════════════════
#  КОМАНДЫ
# ═══════════════════════════════════════════════════════
function ai     --description '🧠 AI-ассистент'    ; command argonov ai ; end
function crypto --description '📈 Крипта'           ; command argonov crypto ; end
function music  --description '🎵 Музыка'           ; command argonov music ; end
function todo   --description '📌 Задачи'           ; command argonov todo $argv ; end
function notes  --description '📝 Заметки'          ; command argonov notes ; end
function pm     --description '🔒 Пароли'           ; command argonov pm ; end
function hack   --description '🎮 Хакерский тул'    ; command argonov hack ; end
function rpg    --description '🕹  RPG Симулятор'   ; command argonov rpg ; end
function d      --description '📥 Загрузчик'        ; command argonov d ; end
function m      --description '🌧 Матрица'          ; command argonov m ; end
function p      --description '🔐 Пароль'           ; command argonov p ; end
function util   --description '📦 Утилиты'          ; command argonov util ; end
function art    --description '🎨 Картинка'         ; command argonov art ; end

function s --description '⚡ Центр управления'
    command argonov s
    plate
end

function backup --description '💾 Бэкап'            ; command argonov backup ; end
function doctor --description '🩺 Проверка'         ; command argonov doctor ; end

# ═══════════════════════════════════════════════════════
#  АВТОДОПОЛНЕНИЕ
# ═══════════════════════════════════════════════════════
complete -c argonov -f -a 'ai'      -d '🧠 AI'
complete -c argonov -f -a 'crypto'  -d '📈 Крипта'
complete -c argonov -f -a 'music'   -d '🎵 Музыка'
complete -c argonov -f -a 'todo'    -d '📌 Задачи'
complete -c argonov -f -a 'notes'   -d '📝 Заметки'
complete -c argonov -f -a 'pm'      -d '🔒 Пароли'
complete -c argonov -f -a 'hack'    -d '🎮 Hack'
complete -c argonov -f -a 'rpg'     -d '🕹  RPG'
complete -c argonov -f -a 'd'       -d '📥 Download'
complete -c argonov -f -a 'm'       -d '🌧 Матрица'
complete -c argonov -f -a 'p'       -d '🔐 Пароль'
complete -c argonov -f -a 's'       -d '⚡ Sysinfo'
complete -c argonov -f -a 'util'    -d '📦 Утилиты'
complete -c argonov -f -a 'art'     -d '🎨 Картинка'
complete -c argonov -f -a 'push'    -d '🚀 Git push'
complete -c argonov -f -a 'pull'    -d '⬇️  Git pull'
complete -c argonov -f -a 'status'  -d '📊 Git status'
complete -c argonov -f -a 'backup'  -d '💾 Бэкап'
complete -c argonov -f -a 'restore' -d '♻️  Restore'
complete -c argonov -f -a 'doctor'  -d '🩺 Doctor'
complete -c argonov -f -a 'help'    -d '❓ Справка'
complete -c argonov -f -a 'version' -d '📌 Версия'

complete -c hack -f -a 'scan'         -d '🌐 WHOIS + DNS'
complete -c hack -f -a 'crt'          -d '🕵️  CRT'
complete -c hack -f -a 'subdomain'    -d '🔎 Поддомены'
complete -c hack -f -a 'dns-enum'     -d '📡 DNS'
complete -c hack -f -a 'robots'       -d '🤖 robots.txt'
complete -c hack -f -a 'headers'      -d '📋 Headers'
complete -c hack -f -a 'nmap'         -d '🔍 Nmap'
complete -c hack -f -a 'ports'        -d '⚙️  Порты'
complete -c hack -f -a 'ping'         -d '🏓 Ping'
complete -c hack -f -a 'trace'        -d '🛰 Traceroute'
complete -c hack -f -a 'ip'           -d '📍 IP'
complete -c hack -f -a 'speed'        -d '⚡ Speed'
complete -c hack -f -a 'hash'         -d '🧮 Hash'
complete -c hack -f -a 'hashid'       -d '🔐 HashID'
complete -c hack -f -a 'b64'          -d '🔡 Base64'
complete -c hack -f -a 'pass'         -d '🎲 Pass'
complete -c hack -f -a 'pass-audit'   -d '🔍 Audit'
complete -c hack -f -a 'crypto'       -d '💰 Crypto'
complete -c hack -f -a 'news'         -d '📰 News'
complete -c hack -f -a 'qr'           -d '📱 QR'
complete -c hack -f -a 'pentest-guide' -d '📚 Guide'
complete -c hack -f -a 'ctf-links'    -d '🏆 CTF'
complete -c hack -f -a 'matrix'       -d '🌧 Matrix'
complete -c hack -f -a 'sysinfo'      -d '💻 Sysinfo'
complete -c hack -f -a 'exit'         -d '🚪 Exit'

# ═══════════════════════════════════════════════════════
#  ЗАПУСК TERMUX
# ═══════════════════════════════════════════════════════
command clear

set_color green --bold
echo '  ▓▒░ TERMINAL ARGONOV ░▒▓'
set_color brblack
echo '  ────────────────────────────────────────'
set_color normal

if test -f ~/fantasy.png
    set -l cols (tput cols)
    set -l bw (math "$cols - 2")
    viu -w $bw -h 22 -b -t ~/fantasy.png
end

set_color green --bold
echo ""
echo "════════════════════════════════════════════════"
set_color normal
set_color cyan
echo "  Время запуска: "(date +%H:%M:%S)
echo "  Дата:          "(date +%d.%m.%Y)
echo "  Устройство:    Android | Termux"
set_color normal
set_color green --bold
echo "════════════════════════════════════════════════"
set_color normal
echo ""

python ~/sysinfo.py
plate
