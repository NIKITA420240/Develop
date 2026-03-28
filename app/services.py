# app/services.py
import os
import httpx
from fastapi import HTTPException

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherService:
    @staticmethod
    async def get_weather(city: str | None = None, lat: float | None = None, lon: float | None = None) -> float:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="OPENWEATHER_API_KEY is not configured")

        params = {"appid": api_key, "units": "metric"}

        if city:
            params["q"] = city
        elif lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise HTTPException(status_code=400, detail="City or coordinates required")

        timeout = httpx.Timeout(8.0, connect=5.0)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                r = await client.get(BASE_URL, params=params)

            if r.status_code == 401:
                raise HTTPException(status_code=502, detail="Weather provider auth error")
            if r.status_code == 404:
                raise HTTPException(status_code=404, detail="City not found")
            if r.status_code >= 500:
                raise HTTPException(status_code=503, detail="Weather provider unavailable")

            r.raise_for_status()
            data = r.json()

            temp = data.get("main", {}).get("temp")
            if temp is None:
                raise HTTPException(status_code=502, detail="Unexpected weather provider response")

            return float(temp)

        except httpx.TimeoutException:
            raise HTTPException(status_code=503, detail="Weather provider timeout")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Weather provider unavailable")
