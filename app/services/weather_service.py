import requests
from config import Config
from app.models.weather import WeatherRecord
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

class WeatherService:
    @staticmethod
    def get_current_weather(city: str):
        url = f"{Config.OPENWEATHERMAP_BASE_URL}/weather"
        params = {
            "q": city,
            "appid": Config.OPENWEATHERMAP_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        data = response.json()
        return data

    @staticmethod
    def save_weather_record(db: Session, city: str, temperature: float, humidity: float, description: str):
        weather_record = WeatherRecord(
            city=city,
            temperature=temperature,
            humidity=humidity,
            description=description,
            timestamp=datetime.now()
        )
        db.add(weather_record)
        db.commit()
        db.refresh(weather_record)
        return weather_record

    @staticmethod
    def update_weather_record(db: Session, record_id: int, temperature: float, humidity: float, description: str):
        weather_record = db.query(WeatherRecord).filter(WeatherRecord.id == record_id).first()
        if weather_record:
            weather_record.temperature = temperature
            weather_record.humidity = humidity
            weather_record.description = description
            weather_record.timestamp = datetime.now()
            db.commit()
            db.refresh(weather_record)
        return weather_record

    @staticmethod
    def delete_old_records(db: Session, days: int):
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        db.query(WeatherRecord).filter(WeatherRecord.timestamp < cutoff_date).delete()
        db.commit()

    @staticmethod
    def get_all_weather_records(db: Session):
        return db.query(WeatherRecord).all()
