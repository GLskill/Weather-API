from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.weather_service import WeatherService

router = APIRouter()


# Controller 1 (GET): Получение текущей погоды по городу
@router.get("/weather/current/{city}")
def get_weather(city: str, db: Session = Depends(get_db)):
    data = WeatherService.get_current_weather(city)
    if "main" not in data:
        raise HTTPException(status_code=404, detail="City not found")
    return data


# Controller 2 (POST): Сохранение погоды в базу данных (LOCAL)
@router.post("/weather/save")
def save_weather(city: str, db: Session = Depends(get_db)):
    data = WeatherService.get_current_weather(city)
    if "main" not in data:
        raise HTTPException(status_code=404, detail="City not found")

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]

    record = WeatherService.save_weather_record(db, city, temp, humidity, description)
    return record


# Controller 3 (PUT): Обновление записи о погоде
@router.put("/weather/update/{record_id}")
def update_weather(
        record_id: int,
        temperature: float = Body(...),
        humidity: float = Body(...),
        description: str = Body(...),
        db: Session = Depends(get_db)
):
    updated_record = WeatherService.update_weather_record(db, record_id, temperature, humidity, description)
    if not updated_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated_record


# Controller 4 (DELETE): Удаление старых записей о погоде
@router.delete("/weather/delete_old/{days}")
async def delete_old_records(days: int, db: Session = Depends(get_db)):
    WeatherService.delete_old_records(db, days)
    return {"message": f"Records older than {days} days deleted."}


# Controller 5 HEAD: Проверка существования записи
@router.head("/weather/check/{city}")
def check_weather(city: str):
    data = WeatherService.get_current_weather(city)
    if "main" not in data:
        raise HTTPException(status_code=404, detail="City not found")
    return None


# Controller 6 OPTIONS: Поддерживаемые методы
@router.options("/weather/options")
def weather_options():
    return {
        "methods": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
    }


# Controller 7  PATCH: Частичное обновление записи о погоде
@router.patch("/weather/patch/{record_id}")
def patch_weather(record_id: int, temperature: float = None, humidity: float = None, description: str = None,
                  db: Session = Depends(get_db)):
    record = WeatherService.update_weather_record(db, record_id, temperature, humidity, description)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


# Controller для получения всех записей о погоде
@router.get("/weather/all")
def get_all_weather(db: Session = Depends(get_db)):
    records = WeatherService.get_all_weather_records(db)
    return records
