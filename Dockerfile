# 1. Базовый образ Python
FROM python:3.11-slim

# 2. Рабочая директория внутри контейнера
WORKDIR /app

# 3. Установим системные зависимости для Playwright Chromium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxfixes3 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# 4. Скопировать файл зависимостей и установить пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Установить Chromium для Playwright
RUN playwright install chromium

# 6. Скопировать весь проект в контейнер
COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]


