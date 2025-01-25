from telegram import Update
from telegram.ext import ContextTypes

LAST_NAME, FIRST_NAME, MIDDLE_NAME, BIRTH_DATE, ADDRESS, PHONE, CATEGORY = range(7)

# Функция обработки нажатия кнопки
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатия кнопки 'Добавить лицо'"""
    query = update.callback_query
    await query.answer()

    # Инициализация данных для добавления лица
    context.user_data['add_face_data'] = {}
    context.user_data['step'] = LAST_NAME
    context.user_data['user_id'] = query.from_user.id

    await query.message.reply_text("Введите фамилию для начала.")
    return LAST_NAME



async def cancel_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатия кнопки 'Прервать ввод'"""
    query = update.callback_query
    await query.answer()

    # Сброс процесса сбора данных
    context.user_data['add_face_data'] = None
    context.user_data['step'] = None

    await query.message.reply_text("Ввод данных отменен. Пожалуйста, отправьте новое фото.")

async def cancel_additional_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатия кнопки 'Нет' на вопрос о дополнительных фото"""
    query = update.callback_query
    await query.answer()

    # Сброс процесса сбора данных
    context.user_data['add_face_data'] = None
    context.user_data['step'] = None

    # Отправка подтверждения пользователю
    await query.message.reply_text("Вы отказались ввести дополнительные фото. Пожалуйста, отправьте новое лицо.")

async def additional_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатия кнопки 'Нет' на вопрос о дополнительных фото"""
    query = update.callback_query
    await query.answer()

    # Сброс процесса сбора данных
    context.user_data['add_face_data'] = None
    context.user_data['step'] = None

    # Отправка подтверждения пользователю
    await query.message.reply_text("В следующих версиях нашего бота тут будет функция по вводу дополнительных фото лица. Пожалуйста, отправьте новое лицо.")

