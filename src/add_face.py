import os
import shutil
from datetime import datetime
import pytz
import numpy as np
from telegram.ext import ContextTypes
from config import PHOTOS_DIR, TEMP_DIR
from database import FaceEmbedding, get_session

async def add_face_to_database(context: ContextTypes.DEFAULT_TYPE):
    """Function to add a face to the database"""
    data = context.user_data['add_face_data']

    # Read vector from file (example)
    user_id = context.user_data['user_id']
    vector_file_path = os.path.join(TEMP_DIR, f'{user_id}/face_vector.txt')
    face_descriptor = np.loadtxt(vector_file_path)

    # Convert vector to bytes with float32 type
    face_descriptor_bytes = np.array(face_descriptor, dtype=np.float32).tobytes()

    # Database connection and data storage logic
    session = get_session()

    new_face = FaceEmbedding(
        last_name=data['last_name'],
        first_name=data['first_name'],
        middle_name=data['middle_name'],
        birth_date=data['birth_date'],
        address=data['address'],
        phone=data['phone'],
        category=data['category'],
        embedding=face_descriptor_bytes,  # Store vector in bytes
        added_by=user_id
    )

    session.add(new_face)
    session.commit()

    # Retrieve new record ID
    face_id = new_face.id
    print(f"Record added with ID: {face_id}")

    # Create a folder for photos
    folder_name = os.path.join(PHOTOS_DIR, f'{face_id}+{data["last_name"]}+{data["first_name"]}')
    os.makedirs(folder_name, exist_ok=True)

    # Set the time zone for San Francisco (America/Los_Angeles)
    sf_tz = pytz.timezone('America/Los_Angeles')
    current_time = datetime.now(sf_tz).strftime('%Y-%m-%d_%H-%M-%S')  # Format: YYYY-MM-DD_HH-MM-SS

    # Generate file name with current date and time
    new_photo_name = f'photo_{current_time}.jpg'

    # Move photo to new folder
    photo_path = os.path.join(TEMP_DIR, f'{user_id}/face_image.jpg')
    os.rename(photo_path, os.path.join(folder_name, new_photo_name))

    # Delete user's temporary folder
    temp_dir = os.path.join(TEMP_DIR, f'{user_id}')
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"Temporary folder {temp_dir} deleted.")

    session.close()
