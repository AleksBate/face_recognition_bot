import numpy as np
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.database import get_session, FaceEmbedding
from src.show_previous_photo import show_previous_photos


async def image_search(face_descriptor, update, context):
    session = get_session()
    all_faces = session.query(FaceEmbedding).all()

    threshold = 0.5  # Порог для косинусного сходства

    # Создаем список совпадений
    matches = []
    for db_face in all_faces:
        db_embedding = np.frombuffer(db_face.embedding, dtype=np.float32)

        # Вычисляем косинусное сходство
        dot_product = np.dot(face_descriptor, db_embedding)
        norm_a = np.linalg.norm(face_descriptor)
        norm_b = np.linalg.norm(db_embedding)
        cosine_similarity = dot_product / (norm_a * norm_b)

        if cosine_similarity > threshold:
            matches.append((db_face, cosine_similarity))

    # Сортируем совпадения по убыванию
    matches = sorted(matches, key=lambda x: x[1], reverse=True)[:5]

    if matches:
        best_match = matches[0]
        await update.message.reply_text(
            f"Наиболее вероятное совпадение:\n"
            f"Фамилия: {best_match[0].last_name}\n"
            f"Имя: {best_match[0].first_name}\n"
            f"Отчество: {best_match[0].middle_name}\n"
            f"Дата рождения: {best_match[0].birth_date}\n"
            f"Адрес места жительства: {best_match[0].address}\n"
            f"Телефон: {best_match[0].phone}\n"
            f"Категория учета: {best_match[0].category}\n"
            f"Добавлено пользователем: {best_match[0].added_by}\n"
            f"Процент совпадения: {best_match[1] * 100:.2f}%"
        )

        # Показ предыдущих фото
        await show_previous_photos(update, context, best_match[0].id, best_match[0].last_name, best_match[0].first_name)

        # Устанавливаем контекст для пользователя и добавляем кнопки для добавления нового фото
        context.user_data['step'] = 'ADDITIONAL_PHOTO'
        keyboard = [
            [InlineKeyboardButton("Добавить новое фото", callback_data=f'additional_photo_{best_match[0].id}')],
            [InlineKeyboardButton("Нет, спасибо", callback_data='no_additional_photo')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Хотите добавить дополнительное фото?", reply_markup=reply_markup)

    else:
        # Если совпадение не найдено, предлагаем добавить новое лицо
        keyboard = [
            [InlineKeyboardButton("Добавить лицо", callback_data='add_face')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Лицо не найдено в базе данных. Вы можете добавить это лицо.",
                                        reply_markup=reply_markup)

    session.close()

