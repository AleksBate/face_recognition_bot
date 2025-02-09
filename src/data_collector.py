from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.add_face import add_face_to_database

LAST_NAME, FIRST_NAME, MIDDLE_NAME, BIRTH_DATE, ADDRESS, PHONE, CATEGORY = range(7)
# Create a variable to store the previous step's context in case of invalid input
previous_context = None

async def collect_face_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Step-by-step data collection function"""

    # Button to cancel input
    keyboard = [[InlineKeyboardButton("Cancel input", callback_data='cancel_input')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Get the current step from the context
    step = context.user_data.get('step', LAST_NAME)

    # Retrieve the current input
    current_context = update.message.text

    # Check if the context is None. If so, use the previously stored context in case of an unexpected input flow.
    global previous_context
    if not current_context:
        current_context = previous_context

    # Logic for each step with the "Cancel input" button
    if step == LAST_NAME:
        context.user_data['add_face_data']['last_name'] = current_context
        previous_context = current_context
        await update.message.reply_text("Enter the first name or cancel input:", reply_markup=reply_markup)
        context.user_data['step'] = FIRST_NAME

    elif step == FIRST_NAME:
        context.user_data['add_face_data']['first_name'] = current_context
        previous_context = current_context
        await update.message.reply_text("Enter middle name or cancel input:", reply_markup=reply_markup)
        context.user_data['step'] = MIDDLE_NAME

    elif step == MIDDLE_NAME:
        context.user_data['add_face_data']['middle_name'] = current_context
        previous_context = current_context
        await update.message.reply_text("Enter date of birth (YYYY-MM-DD) or cancel input:", reply_markup=reply_markup)
        context.user_data['step'] = BIRTH_DATE

    elif step == BIRTH_DATE:
        context.user_data['add_face_data']['birth_date'] = current_context
        previous_context = current_context
        await update.message.reply_text("Enter address or cancel input:", reply_markup=reply_markup)
        context.user_data['step'] = ADDRESS

    elif step == ADDRESS:
        context.user_data['add_face_data']['address'] = current_context
        previous_context = current_context
        await update.message.reply_text("Enter phone number or cancel input:", reply_markup=reply_markup)
        context.user_data['step'] = PHONE

    elif step == PHONE:
        context.user_data['add_face_data']['phone'] = current_context
        previous_context = current_context
        await update.message.reply_text("Enter category or cancel input:", reply_markup=reply_markup)
        context.user_data['step'] = CATEGORY

    elif step == CATEGORY:
        context.user_data['add_face_data']['category'] = current_context
        previous_context = current_context

        # All data collected — call the function to add the face to the database
        await add_face_to_database(context)

        await update.message.reply_text("Face successfully added to the database!")
        context.user_data['step'] = None  # Reset steps, process completed
