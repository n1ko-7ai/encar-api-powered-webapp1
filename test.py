import requests
from flask import Flask, render_template
import requests, json, threading, time
from playwright.async_api import async_playwright
import xml.etree.ElementTree as ET
from datetime import date, datetime
import asyncio
import os
from playwright_stealth import Stealth

async def update_cookies_and_tokens():
    ENCAR_PAGE = "https://www.encar.com"
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] ▶️ Старт функции update_cookies_and_tokens")

    async with Stealth().use_async(async_playwright()) as p:
        print(f"[{time.strftime('%H:%M:%S')}] 🧠 Инициализация браузера")
        browser = await p.chromium.launch(
            headless=True,
            # --- НАСТРОЙКИ ПРОКСИ ---
            proxy={
                "server": "http://res.proxy-seller.io:10000",
                "username": "58272ea5b2cac129",
                "password": "QbhuX4Ha"
            },
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--window-size=1280,800",
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-gpu",
                "--use-gl=swiftshader"
            ]
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
            locale="ko-KR",
            java_script_enabled=True
        )

        page = await context.new_page()
        print(f"[{time.strftime('%H:%M:%S')}] 🌐 Навигация на {ENCAR_PAGE}")

        try:
            await page.goto(ENCAR_PAGE, wait_until="domcontentloaded", timeout=20000)
            print(f"[{time.strftime('%H:%M:%S')}] ✅ Страница загружена (DOMContentLoaded)")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ Ошибка загрузки страницы: {e}")

        await page.wait_for_timeout(5000)
        print(f"[{time.strftime('%H:%M:%S')}] ⏳ Ждём 5 секунд перед взаимодействием")

        try:
            await page.mouse.move(300, 400)
            await page.mouse.click(300, 400)
            await page.keyboard.press("PageDown")
            await page.keyboard.press("ArrowDown")
            await page.wait_for_timeout(3000)
            print(f"[{time.strftime('%H:%M:%S')}] 🖱️ Имитация действий завершена")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Ошибка при имитации действий: {e}")

        try:
            await page.wait_for_selector("body", timeout=30000)
            print(f"[{time.strftime('%H:%M:%S')}] ✅ Селектор <body> найден")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ Селектор <body> не найден: {e}")

        cookies_list = await context.cookies()
        cookies_dict = {c["name"]: c["value"] for c in cookies_list}
        print(f"[{time.strftime('%H:%M:%S')}] 🍪 Получено {len(cookies_list)} cookies:")
        for k, v in cookies_dict.items():
            print(f"  {k} = {v}")

        try:
            local_raw = await page.evaluate("() => JSON.stringify({...localStorage})")
            session_raw = await page.evaluate("() => JSON.stringify({...sessionStorage})")
            local = json.loads(local_raw) if local_raw else {}
            session_storage = json.loads(session_raw) if session_raw else {}
            print(f"[{time.strftime('%H:%M:%S')}] 📦 localStorage: {list(local.keys())}")
            print(f"[{time.strftime('%H:%M:%S')}] 📦 sessionStorage: {list(session_storage.keys())}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ Ошибка чтения storages: {e}")
            local = {}
            session_storage = {}

        await browser.close()
        print(f"[{time.strftime('%H:%M:%S')}] 🧹 Браузер закрыт")
        print(f"[{time.strftime('%H:%M:%S')}] ⏱️ Время выполнения: {round(time.time() - start_time, 2)} сек")

        return {
            "cookies_list": cookies_list,
            "cookies_dict": cookies_dict,
            "localStorage": local,
            "sessionStorage": session_storage,
        }

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9',
    'origin': 'https://www.encar.com',
    'priority': 'u=1, i',
    'referer': 'https://www.encar.com/',
    'sec-ch-ua': '"Not=A?Brand";v="24", "Chromium";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

proxies = {
    "http": "58272ea5b2cac129:QbhuX4Ha@res.proxy-seller.io:10000",
    "https": "58272ea5b2cac129:QbhuX4Ha@res.proxy-seller.io:10000",
}

session = requests.Session()

asyncio.run(update_cookies_and_tokens())

response = session.get(
    'https://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.CarType.Y.)&sr=%7CModifiedDate%7C0%7C20',
    headers=headers,
    proxies=proxies
)

print(response.status_code)
print(response.text)