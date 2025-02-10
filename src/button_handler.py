from telegram import Update
from telegram.ext import ContextTypes

LAST_NAME, FIRST_NAME, MIDDLE_NAME, BIRTH_DATE, ADDRESS, PHONE, CATEGORY = range(7)

# Function to handle button clicks
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the 'Add Face' button click"""
    query = update.callback_query
    await query.answer()

    # Initialize data for adding a face
    context.user_data['add_face_data'] = {}
    context.user_data['step'] = LAST_NAME
    context.user_data['user_id'] = query.from_user.id

    await query.message.reply_text("Please enter the last name to start.")
    return LAST_NAME


async def cancel_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the 'Cancel Input' button click"""
    query = update.callback_query
    await query.answer()

    # Reset data collection process
    context.user_data['add_face_data'] = None
    context.user_data['step'] = None

    await query.message.reply_text("Data entry has been canceled. Please send a new photo.")

async def cancel_additional_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the 'No' button when asked about additional photos"""
    query = update.callback_query
    await query.answer()

    # Reset data collection process
    context.user_data['add_face_data'] = None
    context.user_data['step'] = None

    # Send confirmation to the user
    await query.message.reply_text("You have declined to add additional photos. Please send a new face.")

async def additional_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the 'No' button when asked about additional photos"""
    query = update.callback_query
    await query.answer()

    # Reset data collection process
    context.user_data['add_face_data'] = None
    context.user_data['step'] = None

    # Send confirmation to the user
    await query.message.reply_text("In future versions of our bot, this function will allow adding additional face photos. Please send a new face.")
