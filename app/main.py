from fastapi import FastAPI
from app.routers import weather

app = FastAPI(title="Weather API Service")

# Подключаем наш роутер
app.include_router(weather.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}