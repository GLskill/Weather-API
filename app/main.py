from fastapi import FastAPI
from app.controllers.weather_controller import router as weather_router

app = FastAPI()
# маршрутизатор контроллера погоды
app.include_router(weather_router, prefix="/api", tags=["weather"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
