from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os

# Лучше брать из переменных окружения, но для примера пока так (потом вынесем в config.py)
# Формат: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/weather_db")

engine = create_async_engine(DATABASE_URL, echo=True) # echo=True выводит SQL запросы в консоль (удобно для отладки)

# Фабрика сессий
async_session_factory = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Базовый класс для моделей (SQLAlchemy 2.0 style)
class Base(DeclarativeBase):
    pass

# Зависимость (Dependency) для FastAPI, чтобы получать сессию в эндпоинтах
async def get_db():
    async with async_session_factory() as session:
        yield session