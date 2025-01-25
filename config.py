import os

# Путь к корневой директории проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Путь к директории resources, где хранятся базы данных и фотографии
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')

# Путь к папке DB в resources
DB_DIR = os.path.join(RESOURCES_DIR, 'DB')

# Путь к папке для хранения фотографий
PHOTOS_DIR = os.path.join(RESOURCES_DIR, 'photos')

# Путь к временной папке temp
TEMP_DIR = os.path.join(RESOURCES_DIR, 'temp')

MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Определяем токен для админского бота
TOKEN_ENV_VAR = "TELEGRAM_BOT_TOKEN_CHECKER"

# Пробуем получить токен из переменной окружения
token = os.getenv(TOKEN_ENV_VAR)

if not token:
    # Если токен не найден в ENV, пытаемся загрузить его из текстового файла
    try:
        token_file_path = os.path.join(BASE_DIR, 'token.txt')
        with open(token_file_path, 'r') as f:
            # Парсим строку вида checker=токен
            for line in f:
                if line.startswith("checker="):
                    token = line.split('=')[1].strip()
                    break
        if not token:
            raise ValueError(f"Токен для админского бота не найден в файле.")
    except FileNotFoundError:
        raise ValueError(f"Файл для админского бота не найден.")
