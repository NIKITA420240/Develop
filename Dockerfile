# Используем легкий образ Python
FROM python:3.11-slim

# Отключаем создание .pyc файлов и буферизацию вывода (чтобы логи видеть сразу)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем зависимости (чтобы кэшировать этот слой)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код проекта
COPY . .

# Команда, которая запустится по умолчанию (запуск сервера)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]