import httpx
import os
from fastapi import HTTPException

# Ключ лучше хранить в .env файле
API_KEY = os.getenv("OPENWEATHER_API_KEY") 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherService:
    @staticmethod
    async def get_weather(city: str = None, lat: float = None, lon: float = None) -> float:
        """
        Делает запрос к OpenWeatherMap и возвращает температуру (в Цельсиях).
        """
        params = {"appid": API_KEY, "units": "metric"} # units=metric дает Цельсии
        
        if city:
            params["q"] = city
        elif lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise HTTPException(status_code=400, detail="City or Coordinates required")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(BASE_URL, params=params)
                response.raise_for_status() # Вызовет ошибку, если статус не 200
                data = response.json()
                return data["main"]["temp"]
            except httpx.HTTPStatusError as e:
                # Если город не найден (404) или ошибка ключа (401)
                raise HTTPException(status_code=e.response.status_code, detail="External API Error")
            except Exception as e:
                raise HTTPException(status_code=503, detail="Weather service unavailable")