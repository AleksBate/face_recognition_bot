import os
import shutil
from datetime import datetime
import pytz
import numpy as np
from telegram.ext import ContextTypes
from config import PHOTOS_DIR, TEMP_DIR
from database import FaceEmbedding, get_session

async def add_face_to_database(context: ContextTypes.DEFAULT_TYPE):
    """Функция для добавления лица в базу данных"""
    data = context.user_data['add_face_data']

    # Чтение вектора из файла (пример)
    user_id = context.user_data['user_id']
    vector_file_path = os.path.join(TEMP_DIR, f'{user_id}/face_vector.txt')
    face_descriptor = np.loadtxt(vector_file_path)

    # Преобразуем вектор в байты с типом float32
    face_descriptor_bytes = np.array(face_descriptor, dtype=np.float32).tobytes()

    # Здесь идет логика подключения к базе и сохранения данных
    session = get_session()

    new_face = FaceEmbedding(
        last_name=data['last_name'],
        first_name=data['first_name'],
        middle_name=data['middle_name'],
        birth_date=data['birth_date'],
        address=data['address'],
        phone=data['phone'],
        category=data['category'],
        embedding=face_descriptor_bytes,  # Запись вектора в байтах
        added_by=user_id
    )

    session.add(new_face)
    session.commit()

    # Получаем id новой записи
    face_id = new_face.id
    print(f"Добавлена запись с ID: {face_id}")

    # Создаем папку для фото
    folder_name = os.path.join(PHOTOS_DIR, f'{face_id}+{data["last_name"]}+{data["first_name"]}')
    os.makedirs(folder_name, exist_ok=True)

    # Устанавливаем временную зону для Челябинска (Asia/Yekaterinburg)
    chelyabinsk_tz = pytz.timezone('Asia/Yekaterinburg')
    current_time = datetime.now(chelyabinsk_tz).strftime('%Y-%m-%d_%H-%M-%S')  # Формат: ГГГГ-ММ-ДД_ЧЧ-ММ-СС

    # Генерируем имя файла с текущей датой и временем
    new_photo_name = f'photo_{current_time}.jpg'

    # Перемещаем фото в новую папку
    photo_path = os.path.join(TEMP_DIR, f'{user_id}/face_image.jpg')
    os.rename(photo_path, os.path.join(folder_name, new_photo_name))

    # Удаляем временную папку пользователя
    temp_dir = os.path.join(TEMP_DIR, f'{user_id}')
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"Временная папка {temp_dir} удалена.")

    session.close()
