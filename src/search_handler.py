import numpy as np
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.database import get_session, FaceEmbedding
from src.show_previous_photo import show_previous_photos


async def image_search(face_descriptor, update, context):
    session = get_session()
    all_faces = session.query(FaceEmbedding).all()

    threshold = 0.5  # Cosine similarity threshold

    # Create a list of matches
    matches = []
    for db_face in all_faces:
        db_embedding = np.frombuffer(db_face.embedding, dtype=np.float32)

        # Compute cosine similarity
        dot_product = np.dot(face_descriptor, db_embedding)
        norm_a = np.linalg.norm(face_descriptor)
        norm_b = np.linalg.norm(db_embedding)
        cosine_similarity = dot_product / (norm_a * norm_b)

        if cosine_similarity > threshold:
            matches.append((db_face, cosine_similarity))

    # Sort matches in descending order
    matches = sorted(matches, key=lambda x: x[1], reverse=True)[:5]

    if matches:
        best_match = matches[0]
        await update.message.reply_text(
            f"Most likely match:\n"
            f"Last Name: {best_match[0].last_name}\n"
            f"First Name: {best_match[0].first_name}\n"
            f"Middle Name: {best_match[0].middle_name}\n"
            f"Date of Birth: {best_match[0].birth_date}\n"
            f"Address: {best_match[0].address}\n"
            f"Phone: {best_match[0].phone}\n"
            f"Category: {best_match[0].category}\n"
            f"Added by: {best_match[0].added_by}\n"
            f"Match Percentage: {best_match[1] * 100:.2f}%"
        )

        # Show previous photos
        await show_previous_photos(update, context, best_match[0].id, best_match[0].last_name, best_match[0].first_name)

        # Set user context and add buttons for new photo upload
        context.user_data['step'] = 'ADDITIONAL_PHOTO'
        keyboard = [
            [InlineKeyboardButton("Add new photo", callback_data=f'additional_photo_{best_match[0].id}')],
            [InlineKeyboardButton("No, thanks", callback_data='no_additional_photo')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Would you like to add an additional photo?", reply_markup=reply_markup)

    else:
        # If no match is found, offer to add a new face
        keyboard = [
            [InlineKeyboardButton("Add face", callback_data='add_face')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Face not found in the database. You can add this face.",
                                        reply_markup=reply_markup)

    session.close()
