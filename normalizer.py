import os
import numpy as np
import cv2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, FaceEmbedding, get_session
from config import PHOTOS_DIR, MODELS_DIR, DB_DIR
from insightface.app import FaceAnalysis

from src.handle_photo import ensure_vector_size, normalize_vector

# Путь к новой базе данных
NEW_DB_PATH = os.path.join(DB_DIR, 'new_faces.db')

# Создаем подключение к новой базе данных
new_engine = create_engine(f'sqlite:///{NEW_DB_PATH}')
NewSession = sessionmaker(bind=new_engine)
Base.metadata.create_all(new_engine)

app = FaceAnalysis(name='buffalo_l', root=MODELS_DIR)
app.prepare(ctx_id=0, det_size=(640, 640))

def migrate_and_update_face_embeddings():
    old_session = get_session()  # Сессия для старой базы данных
    new_session = NewSession()   # Сессия для новой базы данных

    all_faces = old_session.query(FaceEmbedding).all()

    for face in all_faces:
        photo_dir = os.path.join(PHOTOS_DIR, f'{face.id}+{face.last_name}+{face.first_name}')
        success = False

        if os.path.exists(photo_dir):
            photos = os.listdir(photo_dir)
            if photos:
                photo_path = os.path.join(photo_dir, photos[0])
                image = cv2.imread(photo_path)
                faces = app.get(image)

                if faces:
                    new_embedding = faces[0].embedding

                    # Нормализация и приведение к нужному размеру
                    new_embedding = normalize_vector(new_embedding)
                    new_embedding = ensure_vector_size(new_embedding, target_size=512)

                    # Записываем преобразованный вектор в новую базу
                    new_face = FaceEmbedding(
                        id=face.id,
                        last_name=face.last_name,
                        first_name=face.first_name,
                        middle_name=face.middle_name,
                        birth_date=face.birth_date,
                        address=face.address,
                        phone=face.phone,
                        category=face.category,
                        embedding=np.array(new_embedding, dtype=np.float32).tobytes(),
                        added_by=face.added_by
                    )
                    new_session.add(new_face)
                    success = True

        if not success:
            print(f"Не удалось преобразовать вектор для записи ID: {face.id}")

    # Коммитим изменения в новой базе данных
    new_session.commit()
    old_session.close()
    new_session.close()
    print("Миграция и обновление векторов завершены.")


if __name__ == "__main__":
    migrate_and_update_face_embeddings()
