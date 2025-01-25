import os
from telegram import Update
from telegram.ext import CallbackContext
from config import PHOTOS_DIR


async def show_previous_photos(update: Update, context: CallbackContext, face_id: int, last_name: str, first_name: str):
    """Функция для отображения предыдущих фото пользователя, начиная с самых новых"""
    # Путь к папке с фотографиями
    folder_path = os.path.join(PHOTOS_DIR, f'{face_id}+{last_name}+{first_name}')

    # Проверяем, существует ли папка
    if not os.path.exists(folder_path):
        await update.message.reply_text("Фотографии не найдены.")
        return

    # Получаем список всех файлов в папке и сортируем их в обратном порядке для показа с самых свежих
    photo_files = sorted(os.listdir(folder_path), reverse=True)

    # Проходим по всем файлам в папке
    for photo_file in photo_files:
        # Извлекаем дату из имени файла (формат: photo_YYYY-MM-DD_HH-MM-SS.jpg)
        file_name = os.path.splitext(photo_file)[0]  # Убираем расширение
        photo_date = file_name.split('_')[1]  # Извлекаем часть с датой

        # Отправляем сообщение с датой
        await update.message.reply_text(f"Фото от {photo_date}")

        # Отправляем само фото
        photo_path = os.path.join(folder_path, photo_file)
        await update.message.reply_photo(photo=open(photo_path, 'rb'))
