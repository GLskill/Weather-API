import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.db import Base, get_db
from app.main import app
from app.models.weather import WeatherRecord

# Добавление пути к проекту
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Настройка тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_weather.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Тестовый клиент FastAPI
client = TestClient(app)


# Зависимость для подмены базы данных
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Тесты
def test_get_all_weather_records(db):
    # Добавление записи в тестовую базу данных
    new_record = WeatherRecord(city="Test City", temperature=20.5, humidity=60, description="clear sky")
    db.add(new_record)
    db.commit()

    response = client.get("/api/weather/all")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["city"] == "Test City"


def test_get_current_weather():
    response = client.get("/api/weather/current/London")
    assert response.status_code == 200
    assert "main" in response.json()

