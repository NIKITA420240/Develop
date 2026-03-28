from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import WeatherLog

class WeatherRepository:
    """
    Класс отвечает только за работу с БД.
    Никакой бизнес-логики или внешних API здесь быть не должно.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_log(self, query_input: str, temperature: float) -> WeatherLog:
        """
        Сохраняет запись о запросе погоды.
        """
        new_log = WeatherLog(
            query_input=query_input,
            temperature=temperature
        )
        self.session.add(new_log)
        await self.session.commit()
        await self.session.refresh(new_log) # Чтобы получить id и timestamp обратно
        return new_log

    async def get_all_logs(self, limit: int = 10):
        """
        Пример метода для получения истории запросов
        """
        stmt = select(WeatherLog).order_by(WeatherLog.timestamp.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()