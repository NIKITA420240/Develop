from pydantic import BaseModel
from datetime import datetime

# Модель ответа (то, что увидит пользователь)
class WeatherResponse(BaseModel):
    location: str
    temperature: float
    saved_at: datetime

    class Config:
        from_attributes = True # Позволяет Pydantic читать данные из ORM-объектов