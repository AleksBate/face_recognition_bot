import os
import cv2
from telegram import Update
from telegram.ext import ContextTypes
from config import TEMP_DIR
from src.data_collector import collect_face_data
from src.handle_photo import handle_photo, load_models  # Добавим новую функцию загрузки моделей
from src.utils import is_user_authorized

detector, arcface_model = load_models()  # Загружаем модели

LAST_NAME, FIRST_NAME, MIDDLE_NAME, BIRTH_DATE, ADDRESS, PHONE, CATEGORY = range(7)

async def check_user_authorization(user_id, update, context):
    if context.user_data.get('authorized'):
        return True  # Пользователь уже авторизован

    if is_user_authorized(user_id):
        context.user_data['authorized'] = True  # Сохраняем информацию об авторизации
        return True

    await update.message.reply_text(
        "Этот бот не для широкого круга лиц. Для авторизации свяжитесь с пользователем @episcop_py"
    )
    return False  # Пользователь не авторизован


async def text_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Получаем ID пользователя

    # Проверяем авторизацию пользователя
    if not await check_user_authorization(user_id, update, context):
        return

    
    """Обрабатывает текст, если бот находится в правильном шаге"""

    step = context.user_data.get('step', None)  # Получаем текущий шаг из контекста, по умолчанию None
   

    if step is None:
        # Если шаг не установлен, значит бот ожидает фото
        await update.message.reply_text("В данный момент я ожидаю фото. Пожалуйста, отправьте фото для обработки.")
    else:
        # Если шаг установлен, обрабатываем текст (например, если уже начали сбор данных)
        await collect_face_data(update, context)

async def image_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Проверка авторизации пользователя
    if not await check_user_authorization(user_id, update, context):
        return

    # Проверка, что в сообщении есть фото
    if update.message and update.message.photo:
        photo = await update.message.photo[-1].get_file()
        await photo.download_to_drive('temp.jpg')

        # Проверка существования файла
        if not os.path.exists('temp.jpg'):
            await update.message.reply_text("Файл temp.jpg не найден.")
            return

        try:
            image = cv2.imread('temp.jpg')
            if image is None:
                await update.message.reply_text("Не удалось загрузить изображение. Попробуйте снова.")
                return

            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            faces = detector.get(rgb_image)

            if len(faces) == 0:
                await update.message.reply_text("Лицо не обнаружено на фото. Пожалуйста, попробуйте снова.")
                return

            if len(faces) > 1:
                await update.message.reply_text("Обнаружено несколько лиц. Загрузите изображение с одним лицом.")
                return

            await update.message.reply_text("Лицо обнаружено. Проверяем базу данных...")

            image_file_path = os.path.join(TEMP_DIR, f'{user_id}/face_image.jpg')
            os.makedirs(os.path.dirname(image_file_path), exist_ok=True)
            cv2.imwrite(image_file_path, image)

            # Проверка сохранения изображения
            if not os.path.exists(image_file_path):
                await update.message.reply_text("Не удалось сохранить изображение во временную папку.")
                return

            await handle_photo(image_file_path, update, context, arcface_model)  # Передаем модель

        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка при обработке фотографии: {e}")
        finally:
            os.remove('temp.jpg')  # Удаляем временный файл