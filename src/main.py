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
    user_id = update.message.from_user.id  # Get user ID
    context.user_data.clear()
    # Check if the user is authorized
    if not context.user_data.get('authorized'):
        if is_user_authorized(user_id):
            context.user_data['authorized'] = True  # Store authorization info
        else:
            await update.message.reply_text(
                "This bot is not for the general public. To get authorization, contact @episcop_py")
            return  # Stop execution if the user is not authorized
    await update.message.reply_text("Hello! Please send an image.")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id  # Get user ID

    # Check if the user is authorized
    if not context.user_data.get('authorized'):
        if is_user_authorized(user_id):
            context.user_data['authorized'] = True  # Store authorization info
        else:
            await update.message.reply_text(
                "This bot is not for the general public. To get authorization, contact @episcop_py")
            return  # Stop execution if the user is not authorized

    # Help text
    help_text = (
        "👤 **Helping the Homeless and Vulnerable Individuals**\n\n"
        "This bot is designed to assist in identifying individuals in need of social services and reconnecting them with support networks.\n\n"
        "🔍 **How the bot works:**\n"
        "1. Upload a photo of the individual in need.\n"
        "2. The bot will attempt to identify the person using a secure database.\n"
        "3. If a match is found, relevant information will be provided to assist in locating support services. If no match is found, you may add the individual to the database.\n\n"
        "📥 **How to add a person:**\n"
        "1. Follow the bot’s instructions to add an individual to the database.\n"
        "2. Ensure accuracy in the details provided to improve identification efforts.\n"
        "3. Once successfully added, the information will be available to authorized personnel helping to reconnect people with their families and support organizations.\n\n"
        "❓ **Additional commands:**\n"
        "- `/start` — Start interacting with the bot.\n"
        "- `/help` — Get this help message.\n\n"
        "This project is constantly evolving to better assist those in need. By contributing, you help create a stronger network for social aid.\n"
        "If you have questions or suggestions for improvement, please reach out. Regards, @episcop_py"
    )

    await update.message.reply_text(help_text, parse_mode='HTML')


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

    application.run_polling()


if __name__ == '__main__':
    main()
