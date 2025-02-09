import os
import numpy as np
import cv2
import insightface

from config import TEMP_DIR, MODELS_DIR
from src.search_handler import image_search


def load_models():
    # Load the ArcFace model and face detector
    arcface_model = insightface.app.FaceAnalysis(name='buffalo_l', root=MODELS_DIR)
    arcface_model.prepare(ctx_id=-1)  # Use CPU for processing

    detector = arcface_model  # ArcFace is used as both detector and feature extractor
    return detector, arcface_model


def normalize_vector(face_descriptor):
    """Normalize the vector to unit length."""
    norm = np.linalg.norm(face_descriptor)
    if norm > 0:
        face_descriptor = face_descriptor / norm
    return face_descriptor


def ensure_vector_size(face_descriptor, target_size=512):
    """Ensure the vector has the required size."""
    current_size = face_descriptor.shape[0]
    if current_size < target_size:
        # Pad with zeros if smaller
        face_descriptor = np.pad(face_descriptor, (0, target_size - current_size), mode='constant')
    elif current_size > target_size:
        # Trim if larger
        face_descriptor = face_descriptor[:target_size]

    return face_descriptor


async def handle_photo(image_file_path, update, context, arcface_model):
    detector, arcface_model = load_models()  # Load models

    image = cv2.imread(image_file_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Use ArcFace to extract face vector
    faces = arcface_model.get(rgb_image)
    if not faces:
        await update.message.reply_text("Failed to extract face vector. Please try again.")
        return

    face_descriptor = faces[0].embedding  # Get face vector

    # Normalize the vector
    face_descriptor = normalize_vector(face_descriptor)

    # Adjust vector size (e.g., 512)
    face_descriptor = ensure_vector_size(face_descriptor, target_size=512)

    # Save the vector to a text file
    directory = os.path.join(TEMP_DIR, f'{update.message.from_user.id}')
    os.makedirs(directory, exist_ok=True)
    vector_file_path = os.path.join(directory, 'face_vector.txt')
    np.savetxt(vector_file_path, face_descriptor)

    await image_search(face_descriptor, update, context)
