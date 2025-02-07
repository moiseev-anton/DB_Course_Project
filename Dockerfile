FROM python:3.9-slim

WORKDIR /app

# У нас подключен bind mount том. Не надо копировать файлы в контейнер
#COPY . .

COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
