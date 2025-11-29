from datetime import datetime
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class WeatherLog(Base):
    __tablename__ = "weather_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # 1. Время запроса 
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # 2. Содержание запроса (город или координаты) 
    # Мы можем хранить сырой запрос пользователя, например "London" или "55.75,37.61"
    query_input: Mapped[str] = mapped_column(String, index=True)
    
    # 3. Результат (температура) 
    temperature: Mapped[float] = mapped_column(Float)
    
    # Дополнительно: ответ API целиком (по желанию, для отладки полезно), но пока пропустим
    
    def __repr__(self):
        return f"<WeatherLog(query={self.query_input}, temp={self.temperature})>"