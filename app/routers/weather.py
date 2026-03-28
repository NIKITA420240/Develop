from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories import WeatherRepository
from app.services import WeatherService
from app.schemas import WeatherResponse

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/", response_model=WeatherResponse)
async def get_weather(
    city: str | None = Query(None, description="City name"),
    lat: float | None = Query(None, description="Latitude"),
    lon: float | None = Query(None, description="Longitude"),
    db: AsyncSession = Depends(get_db)
):
    # 1. Получаем погоду (Бизнес-логика)
    temperature = await WeatherService.get_weather(city=city, lat=lat, lon=lon)
    
    # Формируем строку запроса для логов (как просили в ТЗ)
    query_str = city if city else f"{lat},{lon}"

    # 2. Сохраняем в БД (Репозиторий)
    repository = WeatherRepository(db)
    log_entry = await repository.add_log(query_input=query_str, temperature=temperature)

    # 3. Возвращаем ответ
    # Pydantic сам преобразует модель ORM log_entry в JSON
    return WeatherResponse(
        location=log_entry.query_input,
        temperature=log_entry.temperature,
        saved_at=log_entry.timestamp
    )