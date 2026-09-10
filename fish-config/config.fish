# ~/.config/fish/config.fish
# ============================================================
# TERMINAL ARGONOV

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

# ─── PATH для cargo (viu) ───
if test -d ~/.cargo/bin
    if not contains ~/.cargo/bin $PATH
        set -gx PATH ~/.cargo/bin $PATH
    end
end

# ═══════════════════════════════════════════════════════
#  ART — Fantasy.png на полный экран
# ═══════════════════════════════════════════════════════
function art --description '🎨 Fantasy.png fullscreen (viu)'
    if not test -f ~/fantasy.png
        echo "❌ Нет файла: ~/fantasy.png"
        return
    end
    command clear
    set -l cols (tput cols)
    set -l rows (tput lines)
    set -l sw (math "$cols - 2")
    set -l sh (math "$rows - 3")
    viu -w $sw -h $sh -b -t ~/fantasy.png
    echo ''
    set_color brblack
    echo "   viu  •  $sw×$sh  •  TrueColor"
    set_color normal
end

# ─── Плашка команд ───
function plate --description '📌 Показать плашку команд'
    set_color brblack
    echo '  ┌─ 📌 Доступные команды ──────────────────────────────────'
    set_color cyan
    echo -n '  │  ⚡ s       '
    set_color brblack
    echo -n '— центр управления    '
    set_color cyan
    echo -n '📝 notes  '
    set_color brblack
    echo '— заметки'
    set_color cyan
    echo -n '  │  📦 util    '
    set_color brblack
    echo -n '— сканер утилит       '
    set_color cyan
    echo -n '📥 d      '
    set_color brblack
    echo '— загрузчик'
    set_color cyan
    echo -n '  │  🎮 hack    '
    set_color brblack
    echo -n '— хакерский тул       '
    set_color cyan
    echo -n '🌧 m      '
    set_color brblack
    echo '— матрица'
    set_color cyan
    echo -n '  │  🎵 music   '
    set_color brblack
    echo -n '— музыкальный плеер   '
    set_color cyan
    echo -n '🔐 p      '
    set_color brblack
    echo '— пароли'
    set_color cyan
    echo -n '  │  📌 todo    '
    set_color brblack
    echo -n '— трекер задач        '
    set_color cyan
    echo -n '🔒 pm     '
    set_color brblack
    echo '— менеджер паролей'
    set_color cyan
    echo -n '  │  📈 crypto  '
    set_color brblack
    echo -n '— крипта live         '
    set_color cyan
    echo -n '🧠 ai     '
    set_color brblack
    echo '— AI-ассистент'
    set_color cyan
    echo -n '  │  🎨 art    '
    set_color brblack
    echo '— Fantasy full'
    set_color brblack
    echo '  └─ Tab — автодополнение  •  ↑↓ — выбор ──────────────────'
    set_color normal
end

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

alias ls='eza --icons'
alias ll='eza -lh --icons --git'
alias la='eza -lah --icons --git'
alias cat='bat'

function s --description '⚡ Центр управления системой'
    python ~/sysinfo.py
end
function util --description '📦 Сканер всех утилит'
    python ~/utils.py
end
function hack --description '🎮 Хакерский мультитул'
    python ~/hacktool.py
end
function music --description '🎵 Музыкальный плеер'
    python ~/randomaudio.py
end
function music-meta --description '🌐 Метаданные для музыки'
    python ~/music_meta.py
end
function music-force --description '🔄 Переискать метаданные'
    python ~/music_meta.py --force
end
function todo --description '📌 Трекер задач'
    python ~/todo.py
end
function notes --description '📝 Заметки'
    python ~/notes.py
end
function pm --description '🔒 Менеджер паролей (AES-256)'
    python ~/passmanager.py
end
function crypto --description '📈 Крипта в реальном времени'
    python ~/crypto_informer.py
end
function ai --description '🧠 AI-ассистент (VibeThinker)'
    python ~/ai.py $argv
end
function d --description '📥 Загрузчик файлов'
    python ~/download_zone.py
end
function m --description '🌧 Цифровой дождь'
    python ~/matrix.py
end
function p --description '🔐 Генератор паролей'
    python ~/passgen.py
end

complete -c hack -f -a 'scan'       -d '🌐 WHOIS + DNS + IP'
complete -c hack -f -a 'crt'        -d '🕵️  Certificate Transparency'
complete -c hack -f -a 'crypto'     -d '💰 Курс BTC/ETH'
complete -c hack -f -a 'news'       -d '📰 IT-новости'
complete -c hack -f -a 'qr'         -d '📱 QR-код'
complete -c hack -f -a 'pass'       -d '🔐 Пароль'
complete -c hack -f -a 'pass-audit' -d '🔍 Анализ пароля'
complete -c hack -f -a 'hash'       -d '🧮 MD5/SHA'
complete -c hack -f -a 'b64'        -d '🔡 Base64'
complete -c hack -f -a 'ip'         -d '📍 IP + геолокация'
complete -c hack -f -a 'ping'       -d '🏓 Пинг'
complete -c hack -f -a 'ports'      -d '⚙️  Порты'
complete -c hack -f -a 'headers'    -d '📋 HTTP-заголовки'
complete -c hack -f -a 'robots'     -d '🤖 robots.txt'
complete -c hack -f -a 'trace'      -d '🛰 Traceroute'
complete -c hack -f -a 'speed'      -d '⚡ Скорость'
complete -c hack -f -a 'weather'    -d '☀️  Погода'
complete -c hack -f -a 'matrix'     -d '🌧 Матрица'
complete -c hack -f -a 'sysinfo'    -d '💻 Центр управления'
complete -c hack -f -a 'clear'      -d '🧹 Очистить'
complete -c hack -f -a 'exit'       -d '🚪 Выход'

# ═══════════════════════════════════════════════════════
#  ЗАПУСК TERMUX
# ═══════════════════════════════════════════════════════

# 1. Очистка экрана
command clear

# 2. Логотип
set_color green --bold
echo '  ▓▒░ TERMINAL ARGONOV ░▒▓'
set_color brblack
echo '  ────────────────────────────────────────'
set_color normal

# 3. Fantasy.png
if test -f ~/fantasy.png
    set -l cols (tput cols)
    set -l bw (math "$cols - 2")
    set -l bh 22
    viu -w $bw -h $bh -b -t ~/fantasy.png
end

# 4. Информация о запуске
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

# 5. Sysinfo + плашка
python ~/sysinfo.py
plate
