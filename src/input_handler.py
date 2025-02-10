import os
import cv2
from telegram import Update
from telegram.ext import ContextTypes
from config import TEMP_DIR
from src.data_collector import collect_face_data
from src.handle_photo import handle_photo, load_models  # Added model loading function
from src.utils import is_user_authorized

detector, arcface_model = load_models()  # Load models

LAST_NAME, FIRST_NAME, MIDDLE_NAME, BIRTH_DATE, ADDRESS, PHONE, CATEGORY = range(7)

async def check_user_authorization(user_id, update, context):
    if context.user_data.get('authorized'):
        return True  # User is already authorized

    if is_user_authorized(user_id):
        context.user_data['authorized'] = True  # Store authorization info
        return True

    await update.message.reply_text(
        "This bot is not for the general public. To get authorization, contact @episcop_py"
    )
    return False  # User is not authorized


async def text_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Get user ID

    # Check user authorization
    if not await check_user_authorization(user_id, update, context):
        return

    """Processes text if the bot is in the correct step"""
    step = context.user_data.get('step', None)  # Get current step from context

    if step is None:
        # If no step is set, bot expects a photo
        await update.message.reply_text("Currently, I am expecting a photo. Please send a photo for processing.")
    else:
        # If a step is set, process text (e.g., if data collection has started)
        await collect_face_data(update, context)

async def image_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Check user authorization
    if not await check_user_authorization(user_id, update, context):
        return

    # Check if a photo is present in the message
    if update.message and update.message.photo:
        photo = await update.message.photo[-1].get_file()
        await photo.download_to_drive('temp.jpg')

        # Check if the file exists
        if not os.path.exists('temp.jpg'):
            await update.message.reply_text("File temp.jpg not found.")
            return

        try:
            image = cv2.imread('temp.jpg')
            if image is None:
                await update.message.reply_text("Failed to load image. Please try again.")
                return

            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            faces = detector.get(rgb_image)

            if len(faces) == 0:
                await update.message.reply_text("No face detected in the photo. Please try again.")
                return

            if len(faces) > 1:
                await update.message.reply_text("Multiple faces detected. Please upload an image with a single face.")
                return

            await update.message.reply_text("Face detected. Checking database...")

            image_file_path = os.path.join(TEMP_DIR, f'{user_id}/face_image.jpg')
            os.makedirs(os.path.dirname(image_file_path), exist_ok=True)
            cv2.imwrite(image_file_path, image)

            # Verify image saving
            if not os.path.exists(image_file_path):
                await update.message.reply_text("Failed to save image to temporary folder.")
                return

            await handle_photo(image_file_path, update, context, arcface_model)  # Pass model

        except Exception as e:
            await update.message.reply_text(f"An error occurred while processing the photo: {e}")
        finally:
            os.remove('temp.jpg')  # Remove temporary file
