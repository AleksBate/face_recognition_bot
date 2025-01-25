# Используем базовый образ с Python 3.12
FROM python:3.9-slim

# Устанавливаем необходимые пакеты для компиляции C зависимостей и OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-python-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app/src

# Копируем только requirements.txt для кэширования слоев с зависимостями
COPY requirements.txt ..

# Устанавливаем зависимости до копирования кода проекта
RUN pip install --upgrade pip && pip install -r ../requirements.txt

# Копируем файлы проекта из текущей дирректории в текущую директорию образа

COPY models ../models
COPY resources ../resources
ENV PYTHONPATH=/app:/app/src


COPY src .
COPY config.py ..
COPY token.txt ..

# Указываем команду для запуска приложения
CMD ["sh", "-c", "python main.py || sleep infinity"]

