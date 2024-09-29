from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

Base = declarative_base()  # Используем новую версию функции


class WeatherRecord(Base):
    __tablename__ = 'weather_records'

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime)


# Создаем движок для подключения к базе данных
engine = create_engine(Config.DATABASE_URL)

# Создаем сессию для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)
