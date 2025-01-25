import asyncio
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, CallbackQueryHandler, ContextTypes
)
from handle_photo import *
from database import init_all_db
from src.button_handler import *
from src.input_handler import text_input_handler, image_input_handler
from src.utils import is_user_authorized
from config import token





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id  # Получаем ID пользователя
    context.user_data.clear()
    # Проверяем, авторизован ли пользователь
    if not context.user_data.get('authorized'):
        if is_user_authorized(user_id):
            context.user_data['authorized'] = True  # Сохраняем информацию об авторизации
        else:
            await update.message.reply_text("Этот бот не для широкого круга лиц. Для авторизации свяжитесь с пользователем @episcop_py")
            return  # Останавливаем выполнение функции, если пользователь не авторизован
    await update.message.reply_text("Привет! Пожалуйста, отправьте изображение.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id  # Получаем ID пользователя
    
    # Проверяем, авторизован ли пользователь
    if not context.user_data.get('authorized'):
        if is_user_authorized(user_id):
            context.user_data['authorized'] = True  # Сохраняем информацию об авторизации
        else:
            await update.message.reply_text("Этот бот не для широкого круга лиц. Для авторизации свяжитесь с пользователем @episcop_py")
            return  # Останавливаем выполнение функции, если пользователь не авторизован

    # Текст помощи
    help_text = (
        "👤 **Помощь по работе с ботом распознавания лиц**\n\n"
        "Добро пожаловать в нашего бота! Этот бот поможет вам распознавать лица, представляющие оперативный интерес, на изображениях.\n\n"
        "🔍 **Как работает бот:**\n"
        "1. Отправьте изображение с лицом, которое вы хотите распознать.\n"
        "2. Бот проверит наличие этого лица в базе данных.\n"
        "3. Если лицо найдено, вы получите информацию о нем. Если нет — соответствующее сообщение и предложение добавить лицо.\n\n"
        "📥 **Как добавить лицо:**\n"
        "1. Для добавления нового лица следуйте инструкциям бота.\n"
        "2. Помните, что добавляя лицо, вы пополняете базу данных. Тем самым возможно в будущем вам скажут спасибо за проявленную ответственность сейчас.\n"
        "3. При введении данных будьте внимательны.\n"
        "4. После успешного добавления вы получите подтверждение.\n\n"
        "❓ **Дополнительные команды:**\n"
        "- `/start` — начать работу с ботом.\n"
        "- `/help` — получить эту помощь.\n\n"
        "В настоящее время это версия V1.1. Бот несовершенен, но он постоянно дорабатывается в свободное от основной работы время.\n"
        "Не забудь поделиться ссылкой на бот с коллегами. Ведь чем быстрее мы наполним базу тем легче будет всем.\n"
        "Если у вас возникли вопросы или вы столкнулись с ошибками кода, не стесняйтесь спрашивать! С уважением, @episcop_py"

    )
    
    await update.message.reply_text(help_text, parse_mode='HTML')

#user_ids = set()

#async def send_weekly_message(context: ContextTypes.DEFAULT_TYPE):
#    while True:
#        for user_id in user_ids:
#            await context.bot.send_message(chat_id=user_id, text="Доброго дня. Не забывайте пополнять базу данных, ведь это важно в нашей работе.")
#      await asyncio.sleep(604800)  # Ждем 604800 секунд (1 неделя)

#async def start_sending_messages(context: ContextTypes.DEFAULT_TYPE):
#    await send_weekly_message(context)

def main() -> None:
    init_all_db()
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(filters.PHOTO, image_input_handler))
    application.add_handler(CallbackQueryHandler(button_click_handler, pattern='add_face'))
    application.add_handler(CallbackQueryHandler(cancel_input_handler, pattern='cancel_input'))
    application.add_handler(CallbackQueryHandler(additional_photo_handler, pattern='additional_photo_'))
    application.add_handler(CallbackQueryHandler(cancel_additional_photo_handler, pattern='no_additional_photo'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_input_handler))

    # Запускаем задачу отправки сообщений после запуска приложения
    #application.add_handler(CommandHandler("start", lambda update, context: asyncio.create_task(start_sending_messages(context))))

    application.run_polling()

if __name__ == '__main__':
    main()


