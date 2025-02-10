from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_DIR, PHOTOS_DIR
import sqlite3
import os


FACES_DB_PATH = os.path.join(DB_DIR, 'faces.db')  # Full path to the faces database file
USERS_DB_PATH = os.path.join(DB_DIR, 'users.db')  # Full path to the users database file

# Check if the DB folder exists, create it if not
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    print(f"Folder 'DB' created at {DB_DIR}")

# Connect to the faces database using SQLAlchemy
Base = declarative_base()
faces_engine = create_engine(f"sqlite:///{FACES_DB_PATH}")
SessionLocal = sessionmaker(bind=faces_engine)

def get_session():
    """Returns a session for database operations"""
    return SessionLocal()

# Check if the photos directory exists, create it if not
if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)
    print(f"Folder 'photos' created at {PHOTOS_DIR}")
else:
    print(f"Folder 'photos' already exists at {PHOTOS_DIR}")

# Model for the faces table
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
    """Initializes the faces table"""
    Base.metadata.create_all(faces_engine)
    print("Faces table initialized.")

def init_users_db():
    """Initializes the users table using sqlite3"""
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
    print("Users table initialized.")

def init_all_db():
    """Initializes all databases"""
    init_faces_db()  # Initialize faces database using SQLAlchemy
    init_users_db()  # Initialize users database using sqlite3
    print("All databases successfully initialized.")
