from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.add_face import add_face_to_database

LAST_NAME, FIRST_NAME, MIDDLE_NAME, BIRTH_DATE, ADDRESS, PHONE, CATEGORY = range(7)
#Создаем переменную для хранения контекста предыдущего шага на случай неверного ввода
previous_context = None

async def collect_face_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция обработки по шагам"""

    # Кнопка для прерывания ввода
    keyboard = [[InlineKeyboardButton("Прервать ввод", callback_data='cancel_input')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Получаем текущий шаг из контекста
    step = context.user_data.get('step', LAST_NAME)

    #Получаем текущий контекст
    current_context = update.message.text

    #Проверяем текущий контест на None. Если мы оказались тут, а контекст равен None, значит эта функция вызвана после/
    #несвоевременного ввода фотографии. Тогда мы используем контекст, сохраненный с предыдущего раза

    global previous_context
    if not current_context:
        current_context = previous_context

    # Логика по каждому шагу с кнопкой "Прервать ввод"
    if step == LAST_NAME:
        context.user_data['add_face_data']['last_name'] = current_context
        previous_context = current_context
        await update.message.reply_text("Введите имя или прервите ввод:", reply_markup=reply_markup)
        context.user_data['step'] = FIRST_NAME

    elif step == FIRST_NAME:
        context.user_data['add_face_data']['first_name'] = current_context
        previous_context = current_context
        await update.message.reply_text("Введите отчество или прервите ввод:", reply_markup=reply_markup)
        context.user_data['step'] = MIDDLE_NAME

    elif step == MIDDLE_NAME:
        context.user_data['add_face_data']['middle_name'] = current_context
        previous_context = current_context
        await update.message.reply_text("Введите дату рождения (гггг-мм-дд) или прервите ввод:", reply_markup=reply_markup)
        context.user_data['step'] = BIRTH_DATE

    elif step == BIRTH_DATE:
        context.user_data['add_face_data']['birth_date'] = current_context
        previous_context = current_context
        await update.message.reply_text("Введите адрес или прервите ввод:", reply_markup=reply_markup)
        context.user_data['step'] = ADDRESS

    elif step == ADDRESS:
        context.user_data['add_face_data']['address'] = current_context
        previous_context = current_context
        await update.message.reply_text("Введите телефон или прервите ввод:", reply_markup=reply_markup)
        context.user_data['step'] = PHONE

    elif step == PHONE:
        context.user_data['add_face_data']['phone'] = current_context
        previous_context = current_context
        await update.message.reply_text("Введите категорию учета или прервите ввод:", reply_markup=reply_markup)
        context.user_data['step'] = CATEGORY

    elif step == CATEGORY:
        context.user_data['add_face_data']['category'] = current_context
        previous_context = current_context

        # Все данные собраны — вызываем функцию для добавления лица в базу
        await add_face_to_database(context)

        await update.message.reply_text("Лицо успешно добавлено в базу данных!")
        context.user_data['step'] = None  # Сбрасываем шаги, процесс завершен