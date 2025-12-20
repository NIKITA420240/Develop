import httpx
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

API_KEY = "69f16b8c1709a69d8a2166066035b82a"
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
            print(f"🔑 МОЙ КЛЮЧ: {API_KEY}")
            try:
                response = await client.get(BASE_URL, params=params)
                response.raise_for_status() # Вызовет ошибку, если статус не 200
                data = response.json()
                return data["main"]["temp"]
            except httpx.HTTPStatusError as e:
                print(f"🔴 ОШИБКА ОТ OPENWEATHER: {e.response.status_code}")
                print(f"🔴 ТЕКСТ ОШИБКИ: {e.response.text}")
                # Выводим реальный текст ошибки прямо в браузер
                raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
            # except httpx.HTTPStatusError as e:
            #     # Если город не найден (404) или ошибка ключа (401)
            #     raise HTTPException(status_code=e.response.status_code, detail="External API Error")
            except Exception as e:
                raise HTTPException(status_code=503, detail="Weather service unavailable")