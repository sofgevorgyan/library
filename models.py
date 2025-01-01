from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL подключения к базе данных
DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/library"

# Создаем движок и базовый класс
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Модель автора
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    biography = Column(String)

# Модель книги
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    description = Column(String)
    published_year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
# Создаем все таблицы
Base.metadata.create_all(bind=engine)

# Сессия
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
