# Простий та надійний Dockerfile для цього Flask-проєкту
FROM python:3.11-slim

WORKDIR /app

# Копіюємо залежності окремим шаром для кешування
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копіюємо код застосунку
COPY . /app

# Змінні середовища
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATABASE_PATH=/app/data/database.db

# Порт Flask
EXPOSE 5000

# Для dev/demo: вбудований сервер Flask (запускається як `python app.py`)
CMD ["python", "app.py"]