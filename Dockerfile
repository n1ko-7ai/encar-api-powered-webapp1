# 📦 Базовый образ с Python
FROM python:3.11-slim

# 🛠️ Установка системных зависимостей для headed Chromium и виртуального дисплея
RUN apt-get update && apt-get install -y \
    wget gnupg curl ca-certificates fonts-liberation \
    libgtk-3-0 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libxinerama1 \
    libpango-1.0-0 libpangocairo-1.0-0 libatk1.0-0 libatspi2.0-0 libxext6 libxfixes3 \
    libx11-6 libxcb1 libxrender1 libxi6 libxtst6 libasound2 libnss3 libxss1 \
    libxshmfence-dev libdrm-dev libgbm-dev \
    libxv1 libxvmc1 libxpm4 libxmu6 libxaw7 libxft2 libxkbcommon0 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# 🐍 Обновление pip и установка Python-зависимостей
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# 🧭 Установка Playwright и Chromium с зависимостями
RUN playwright install --with-deps

# 📁 Копирование проекта
COPY . /app
WORKDIR /app

# 🌐 Установка порта
ENV PORT=10000

# 🚀 Запуск приложения с виртуальным дисплеем
CMD ["sh", "-c", "xvfb-run -a python startup.py && gunicorn main:app --bind 0.0.0.0:$PORT"]
