import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    OPENWEATHERMAP_BASE_URL = "http://api.openweathermap.org/data/2.5"
