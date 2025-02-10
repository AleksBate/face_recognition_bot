import os
from telegram import Update
from telegram.ext import CallbackContext
from config import PHOTOS_DIR


async def show_previous_photos(update: Update, context: CallbackContext, face_id: int, last_name: str, first_name: str):
    """Function to display a user's previous photos, starting from the most recent."""
    # Path to the folder containing photos
    folder_path = os.path.join(PHOTOS_DIR, f'{face_id}+{last_name}+{first_name}')

    # Check if the folder exists
    if not os.path.exists(folder_path):
        await update.message.reply_text("No photos found.")
        return

    # Retrieve all files in the folder and sort them in reverse order to show the latest first
    photo_files = sorted(os.listdir(folder_path), reverse=True)

    # Iterate through all files in the folder
    for photo_file in photo_files:
        # Extract the date from the filename (format: photo_YYYY-MM-DD_HH-MM-SS.jpg)
        file_name = os.path.splitext(photo_file)[0]  # Remove the extension
        photo_date = file_name.split('_')[1]  # Extract the date part

        # Send a message with the date
        await update.message.reply_text(f"Photo from {photo_date}")

        # Send the actual photo
        photo_path = os.path.join(folder_path, photo_file)
        await update.message.reply_photo(photo=open(photo_path, 'rb'))
