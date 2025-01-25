import os
import numpy as np
import cv2
import insightface

from config import TEMP_DIR, MODELS_DIR
from src.search_handler import image_search


def load_models():
    # Загрузка модели ArcFace и детектора лиц
    arcface_model = insightface.app.FaceAnalysis(name='buffalo_l', root=MODELS_DIR)
    arcface_model.prepare(ctx_id=-1)  # Используем CPU для обработки

    detector = arcface_model  # ArcFace используется как детектор и для извлечения векторов
    return detector, arcface_model


def normalize_vector(face_descriptor):
    """Нормализация вектора до единичной длины."""
    norm = np.linalg.norm(face_descriptor)
    if norm > 0:
        face_descriptor = face_descriptor / norm
    return face_descriptor


def ensure_vector_size(face_descriptor, target_size=512):
    """Функция для приведения вектора к определенной размерности."""
    current_size = face_descriptor.shape[0]
    if current_size < target_size:
        # Дополняем вектор нулями, если он меньше требуемой размерности
        face_descriptor = np.pad(face_descriptor, (0, target_size - current_size), mode='constant')
    elif current_size > target_size:
        # Обрезаем вектор до нужной длины, если он больше
        face_descriptor = face_descriptor[:target_size]

    return face_descriptor


async def handle_photo(image_file_path, update, context, arcface_model):
    detector, arcface_model = load_models()  # Загрузка моделей

    image = cv2.imread(image_file_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Используем ArcFace для извлечения вектора лица
    faces = arcface_model.get(rgb_image)
    if not faces:
        await update.message.reply_text("Не удалось извлечь вектор лица. Попробуйте снова.")
        return

    face_descriptor = faces[0].embedding  # Получаем вектор лица

    # Нормализация вектора
    face_descriptor = normalize_vector(face_descriptor)

    # Приводим вектор к нужному размеру (например, 512)
    face_descriptor = ensure_vector_size(face_descriptor, target_size=512)

    # Сохранение вектора в текстовый файл
    directory = os.path.join(TEMP_DIR, f'{update.message.from_user.id}')
    os.makedirs(directory, exist_ok=True)
    vector_file_path = os.path.join(directory, 'face_vector.txt')
    np.savetxt(vector_file_path, face_descriptor)

    await image_search(face_descriptor, update, context)
