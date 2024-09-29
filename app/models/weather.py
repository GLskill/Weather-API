from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base  # Обновлено с правильного пути

Base = declarative_base()  # Используем новую версию функции


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime)

