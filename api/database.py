# =============================================================================
# API VERİTABANI BAĞLANTISI
# =============================================================================
# Bu dosya FastAPI için SQLAlchemy veritabanı bağlantısını sağlar
# Django'nun SQLite veritabanını kullanır

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Django projesinin kök dizinini bul
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SQLite veritabanı dosyasının yolu
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"

# SQLAlchemy engine oluştur
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite için gerekli
)

# SessionLocal sınıfı oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base sınıfı oluştur (model sınıfları için)
Base = declarative_base()


def get_db():
    """
    Veritabanı session'ı döndürür
    
    Bu fonksiyon FastAPI dependency injection için kullanılır
    Her API isteği için yeni bir session oluşturur
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 