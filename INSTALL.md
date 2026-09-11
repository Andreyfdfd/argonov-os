# 🚀 INSTALL — Argonov OS

## Минимальные требования

| Параметр | Значение |
|----------|----------|
| Android | 10+ |
| Termux | F-Droid версия |
| RAM | 4+ ГБ |
| Свободное место | 8+ ГБ |
| Интернет | Для установки |

---

## 📥 Шаг 1: Установка Termux

**ВАЖНО:** Скачивай **только из F-Droid** — версия из Google Play устарела.

Ссылки:
- [Termux](https://f-droid.org/packages/com.termux/)
- [Termux:API](https://f-droid.org/packages/com.termux.api/)
- [Termux:Styling](https://f-droid.org/packages/com.termux.styling/)
- [Termux:Boot](https://f-droid.org/packages/com.termux.boot/)

---

## 📥 Шаг 2: Установка Argonov OS

Открой Termux и выполни:

```bash
# Обновление пакетов
pkg update -y && pkg upgrade -y

# Установка git
pkg install git -y

# Клонирование
git clone https://github.com/Andreyfdfd/argonov-os.git
cd argonov-os

# Установка
bash install.sh
```

Установщик поставит:
- Системные пакеты (python, git, fish, chafa, ffmpeg, ...)
- Python-библиотеки (rich, requests, fastapi, ...)
- Скрипты в `~/`
- Fish-конфиг с темой и плашкой
- Termux-тему

---

## 📥 Шаг 3: Модель AI (опционально)

Для AI-ассистента нужна модель Qwen 2.5 Coder 3B (~2 ГБ):

```bash
cd ~
wget -O qwen3b.gguf "https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF/resolve/main/qwen2.5-coder-3b-instruct-q4_k_m.gguf"
```

Скачивание: ~5-15 минут в зависимости от скорости.

---

## 📥 Шаг 4: Доступ к памяти

```bash
termux-setup-storage
```

Разреши доступ в Android-диалоге — нужно для музыки, art, download.

---

## 📥 Шаг 5: Запуск

```bash
argonov
```

Откроется главное меню.

---

## 🎯 ПРОВЕРКА УСТАНОВКИ

```bash
argonov doctor
```

Должно показать:
- ✅ 14 скриптов на месте
- ✅ Утилиты установлены
- ✅ Модели найдены
- ✅ Git репо синхронизирован

---

## ❌ УДАЛЕНИЕ

```bash
cd ~/argonov-os
bash uninstall.sh
```

Или вручную:

```bash
rm -f ~/*.py ~/argonov
rm -rf ~/.config/fish ~/.termux
```

Личные данные (`.pm.vault`, `.todo.json`, `.notes.json`) **НЕ удаляются** — удали вручную если нужно.

---

## 🔧 РЕШЕНИЕ ПРОБЛЕМ

### "llama-server not found"
```bash
pkg install llama-cpp -y
```

### "viu not found"
```bash
cargo install viu
```

### Music: "Аудиофайлы не найдены"
```bash
termux-setup-storage
python ~/music_meta.py  # Пересобрать библиотеку (10-20 мин)
```

### "No module named X"
```bash
pip install X
```

### "Permission denied"
```bash
termux-setup-storage
chmod +x ~/argonov
```

### Ошибка в fish config
```bash
exec fish
# или закрой/открой Termux
```

---

## 📞 ПОДДЕРЖКА

- GitHub Issues: [создать](https://github.com/Andreyfdfd/argonov-os/issues)
- Автор: [@Andreyfdfd](https://github.com/Andreyfdfd)
