import string
import secrets
import sys

# Настройка цветов в терминале
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"

def generate_password(length=16, use_digits=True, use_special=True):
    # Базовый набор символов (строчные и прописные английские буквы)
    letters = string.ascii_letters
    digits = string.digits if use_digits else ""
    special = "!@#$%^&*()-_=+[{]};:,.<>?" if use_special else ""
    
    all_chars = letters + digits + special
    
    if not all_chars:
        return "Ошибка: нет символов для генерации!"
    
    # Секретная генерация (secrets надежнее, чем модуль random)
    password = "".join(secrets.choice(all_chars) for _ in range(length))
    return password

print(f"{CYAN}=== ГЕНЕРАТОР НАДЁЖНЫХ ПАРОЛЕЙ ==={RESET}\n")

try:
    # Запрашиваем длину пароля
    length_input = input(f"{YELLOW}Введите длину пароля (по умолчанию 16): {RESET}")
    length = int(length_input) if length_input.strip().isdigit() else 16
    
    # Генерируем пароль
    password = generate_password(length)
    
    # Выводим результат
    print(f"\n{GREEN}[+] Сгенерированный пароль:{RESET}")
    print(f"{GREEN}-----------------------------------{RESET}")
    print(password)
    print(f"{GREEN}-----------------------------------{RESET}")
    print(f"{CYAN}Скопируйте его и сохраните в надёжном месте.{RESET}")

except KeyboardInterrupt:
    print(f"\n{RESET}Выход...")
