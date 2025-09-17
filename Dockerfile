# Базовый образ с Python
FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    wget gnupg curl ca-certificates fonts-liberation libnss3 libatk-bridge2.0-0 libxss1 libasound2 libxshmfence-dev \
    libgtk-3-0 libdrm-dev libgbm-dev libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libxinerama1 libpango-1.0-0 \
    libpangocairo-1.0-0 libatk1.0-0 libatspi2.0-0 libxext6 libxfixes3 libx11-6 libxcb1 libxrender1 libxi6 libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# Установка Playwright и Chromium
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install --with-deps

# Копируем проект
COPY . /app
WORKDIR /app

# Указываем порт
ENV PORT=10000

# Запуск через Gunicorn
CMD ["sh", "-c", "python startup.py && gunicorn main:app --bind 0.0.0.0:$PORT"]
