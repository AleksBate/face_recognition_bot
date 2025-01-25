from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_DIR, PHOTOS_DIR
import sqlite3
import os


FACES_DB_PATH = os.path.join(DB_DIR, 'faces.db')  # Полный путь к файлу базы данных для лиц
USERS_DB_PATH = os.path.join(DB_DIR, 'users.db')  # Полный путь к файлу базы данных для пользователей

# Проверка существования папки DB и создание, если её нет
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    print(f"Папка 'DB' создана по пути {DB_DIR}")

# Подключение к базе данных для лиц через SQLAlchemy
Base = declarative_base()
faces_engine = create_engine(f"sqlite:///{FACES_DB_PATH}")
SessionLocal = sessionmaker(bind=faces_engine)

def get_session():
    """Возвращает сессию для работы с базой данных"""
    return SessionLocal()

# Проверка существования папки для хранения фото и её создание
if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)
    print(f"Папка 'photos' создана по пути {PHOTOS_DIR}")
else:
    print(f"Папка 'photos' существовала по пути {PHOTOS_DIR}")

# Модель для таблицы лиц (faces)
class FaceEmbedding(Base):
    __tablename__ = 'faces'
    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    birth_date = Column(String)
    address = Column(String)
    phone = Column(String)
    category = Column(String)
    embedding = Column(LargeBinary)
    added_by = Column(String)

def init_faces_db():
    """Инициализирует таблицу лиц"""
    Base.metadata.create_all(faces_engine)
    print("Таблица лиц (faces) инициализирована.")

def init_users_db():
    """Инициализирует таблицу пользователей через sqlite3"""
    conn = sqlite3.connect(USERS_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            position TEXT,
            department TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Таблица пользователей (users) инициализирована.")

def init_all_db():
    """Инициализирует все базы данных"""
    init_faces_db()  # Инициализация базы данных лиц через SQLAlchemy
    init_users_db()  # Инициализация базы данных пользователей через sqlite3
    print("Все базы данных успешно инициализированы.")
