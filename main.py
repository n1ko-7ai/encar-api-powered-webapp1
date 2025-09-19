from flask import Flask, render_template
import requests, json, threading, time
from playwright.async_api import async_playwright
import xml.etree.ElementTree as ET
from datetime import date, datetime
import asyncio
import os
from playwright_stealth import Stealth

os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

proxies = {
  "http": "",
  "https": "",
}

rate = {}

def get_exchange_rates():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Ошибка при запросе к Центробанку: {e}")

    response.encoding = "windows-1251"
    try:
        tree = ET.ElementTree(ET.fromstring(response.text))
    except ET.ParseError:
        raise ValueError("Некорректный XML от Центробанка")

    root = tree.getroot()
    rates = {}
    for currency in root.findall("Valute"):
        char_code = currency.find("CharCode").text
        rate = float(currency.find("Value").text.replace(",", "."))
        nominal = int(currency.find("Nominal").text)
        rates[char_code] = rate / nominal

    rates["RUB"] = 1.0
    return rates

# Функция для конвертации валюты
def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency not in rates:
        raise ValueError(f"Валюта {from_currency} не найдена в курсах валют.")
    if to_currency not in rates:
        raise ValueError(f"Валюта {to_currency} не найдена в курсах валют.")

    rub_amount = amount * rates[from_currency]
    result = rub_amount / rates[to_currency]
    return result

# Функция для конвертации чисел в российский формат цены.
def value_converter(number):
    number = round(number, 2)
    return "{:,}".format(number).replace(",", " ")

# Расчет импортной пошлины для старейших(не проходных) автомобилей
def calculate_import_duty_oldest(a):
    if a > 3000:
        return 5.7 * a
    elif a > 2300:
        return 5 * a
    elif a > 1800:
        return 4.8 * a
    elif a > 1500:
        return 3.5 * a
    elif a > 1000:
        return 3.2 * a
    else:
        return 3 * a

# Расчет импортной пошлины для старых(не проходных) автомобилей
def calculate_import_duty_old(a):
    if a > 3000:
        return 3.6 * a
    elif a > 2300:
        return 3.0 * a
    elif a > 1800:
        return 2.7 * a
    elif a > 1500:
        return 2.5 * a
    elif a > 1000:
        return 1.7 * a
    else:
        return 1.5 * a

# Расчет импортной пошлины для новых(проходных) автомобилей
def calculate_import_duty_new(auto_cost_usd, engine_capacity):
    if auto_cost_usd >= 178628:
        euro = 20
    elif auto_cost_usd >= 89314:
        euro = 15
    elif auto_cost_usd >= 44710:
        euro = 7.5
    elif auto_cost_usd >= 17652:
        euro = 5.5
    elif auto_cost_usd >= 8985:
        euro = 3.5
    else:
        euro = 2.5

    if auto_cost_usd < 8985:
        value = auto_cost_usd * 0.54
    else:
        value = auto_cost_usd * 0.48

    print(value)

    rates = get_exchange_rates()
    return max(value, convert_currency(engine_capacity * euro, 'EUR', 'USD', rates))

# Тут считаются таможенные сборы
def calculate_customs_fee(amount_rub):
    if amount_rub <= 200_000:
        return 775
    elif amount_rub <= 450_000:
        return 1550
    elif amount_rub <= 1_200_000:
        return 3100
    elif amount_rub <= 2_700_000:
        return 8530
    elif amount_rub <= 4_200_000:
        return 12_000
    elif amount_rub <= 5_500_000:
        return 15_500
    elif amount_rub <= 7_000_000:
        return 20_000
    elif amount_rub <= 8_000_000:
        return 23_000
    elif amount_rub <= 9_000_000:
        return 25_000
    elif amount_rub <= 10_000_000:
        return 27_000
    else:  # Для сумм выше 10 000 000
        return 30_000

# А тут считаются утилсборы для старых и старейших не проходных авто.
def calculate_recycling_fee_old(a):
    value = 20_000

    if a >= 3500:
        return 180.24 * value
    elif a >= 3000:
        return 164.84 * value
    else:
        return 0.26 * value

# А тут соответственно, для проходных, новых авто.
def calculate_recycling_fee_new(a):
    value = 20_000

    if a >= 3500:
        return 137.11 * value
    elif a >= 3000:
        return 107.67 * value
    else:
        return 0.17 * value

# Эта функция сравнивает дату авто для инициализации (проходной или не проходной).
def calculate_the_date(date):
    current = datetime.today()
    years_diff = current.year - date.year
    months_diff = current.month - date.month
    total_months_diff = years_diff * 12 + months_diff

    if total_months_diff >= 60:  # 60 месяцев = 5 лет
        return 'oldest'
    elif total_months_diff >= 36:  # 36 месяцев = 3 года
        return 'old'
    else:
        return 'newest'

# Тут происходит вся магия. Считается общая цена всех услуг. (ДЛЯ СТАРЫХ АВТО)
def calculate_overall_cost_old(auto_cost, engine_capacity):
    # Получаем обменные курсы
    rates = get_exchange_rates()

    # Рассчитываем пошлину, цену авто и дополнительные расходы
    import_duty = convert_currency(calculate_import_duty_old(engine_capacity), 'EUR', 'RUB', rates)
    auto_cost_rub = convert_currency(auto_cost, 'KRW', 'RUB', rates)

    # Фиксированная дополнительная цена
    additional_price = 300000.0

    # Таможенные сборы
    customs_fee = calculate_customs_fee(auto_cost_rub)

    # Считаем утилсбор
    recycling_fee = calculate_recycling_fee_old(engine_capacity)

    # Расчет дополнительных сборов
    results_cost = import_duty + customs_fee + recycling_fee

    # Общая стоимость
    overall_cost = results_cost + auto_cost_rub + additional_price

    # Это хэш-таблица с результатами разных расчетов
    data = {
        'Импортная пошлина': value_converter(import_duty),
        'Таможенные сборы': value_converter(customs_fee),
        'Утилизационный сбор': value_converter(recycling_fee),
        'Стоимость автомобиля в рублях': value_converter(auto_cost_rub),
        'Результат расчетов (ИТУ)': value_converter(results_cost),
        'Общая стоимость': value_converter(overall_cost)
    }

    return data

# Тут также, но для новых авто (проходных).
def calculate_overall_cost_new(auto_cost, engine_capacity):
    # Получаем обменные курсы
    rates = get_exchange_rates()

    # Конвертируем стоимость автомобиля в USD и RUB
    auto_cost_usd = convert_currency(auto_cost, 'KRW', 'USD', rates)
    auto_cost_rub = convert_currency(auto_cost, 'KRW', 'RUB', rates)

    # Рассчитываем импортную пошлину в USD и конвертируем её в RUB
    import_duty = calculate_import_duty_new(auto_cost_usd, engine_capacity)
    import_duty_rub = convert_currency(import_duty, 'USD', 'RUB', rates)

    # Фиксированные дополнительные расходы
    additional_cost = 300000.0

    # Считаем утилсбор
    recycling_fee = calculate_recycling_fee_new(engine_capacity)

    # Таможенные сборы
    customs_fee = calculate_customs_fee(auto_cost_rub)

    # Рассчитываем дополнительные сборы
    results_cost = import_duty_rub + recycling_fee + customs_fee

    # Общая стоимость
    overall_cost = results_cost + auto_cost_rub + additional_cost

    # Это хэш-таблица с результатами разных расчетов
    data = {
        'Импортная пошлина': value_converter(import_duty_rub),
        'Таможенные сборы': value_converter(customs_fee),
        'Утилизационный сбор': value_converter(recycling_fee),
        'Стоимость автомобиля в рублях': value_converter(auto_cost_rub),
        'Результат расчетов (ИТУ)': value_converter(results_cost),
        'Общая стоимость': value_converter(overall_cost)
    }

    return data

# Ну и тут для старейших авто. Думаю комментировать не стоит?
def calculate_overall_cost_oldest(auto_cost, engine_capacity):
    rates = get_exchange_rates()

    auto_cost_rub = convert_currency(auto_cost, 'KRW', 'RUB', rates)
    import_duty = convert_currency(calculate_import_duty_oldest(engine_capacity), 'EUR', 'RUB', rates)

    additional_price = 300000.0

    customs_fee = calculate_customs_fee(auto_cost_rub)
    recycling_fee = calculate_recycling_fee_old(engine_capacity)

    results_cost = import_duty + customs_fee + recycling_fee
    overall_cost = results_cost + auto_cost_rub + additional_price

    data = {
        'Импортная пошлина': value_converter(import_duty),
        'Таможенные сборы': value_converter(customs_fee),
        'Утилизационный сбор': value_converter(recycling_fee),
        'Стоимость автомобиля в рублях': value_converter(auto_cost_rub),
        'Результат расчетов (ИТУ)': value_converter(results_cost),
        'Общая стоимость': value_converter(overall_cost)
    }

    return data

REFRESH_INTERVAL = 3 * 60 * 60  # 3 часа

app = Flask(__name__)

HEADERS = {
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

session = requests.Session()

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)


async def update_cookies_and_tokens(save_state_path="/tmp/playwright_storage.json"):
    ENCAR_PAGE = "https://www.encar.com"
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] ▶️ Старт функции update_cookies_and_tokens")

    async with Stealth().use_async(async_playwright()) as p:
        print(f"[{time.strftime('%H:%M:%S')}] 🧠 Инициализация браузера")
        browser = await p.chromium.launch(
            headless=True,
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
            await page.wait_for_selector("body", timeout=10000)
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

        try:
            await context.storage_state(path=save_state_path)
            print(f"[{time.strftime('%H:%M:%S')}] 💾 storage_state сохранён в {save_state_path}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ Не удалось сохранить storage_state: {e}")

        await browser.close()
        print(f"[{time.strftime('%H:%M:%S')}] 🧹 Браузер закрыт")
        print(f"[{time.strftime('%H:%M:%S')}] ⏱️ Время выполнения: {round(time.time() - start_time, 2)} сек")

        return {
            "cookies_list": cookies_list,
            "cookies_dict": cookies_dict,
            "localStorage": local,
            "sessionStorage": session_storage,
            "saved_state_file": save_state_path
        }

def rates_refresher():
    while True:
        time.sleep(REFRESH_INTERVAL)
        log("Фоновое обновление курса")
        rate = get_exchange_rates()
        log("Фоновое обновление курса завершено.")

@app.route("/")
def index():
    return "This is main page, but not ready yet" # Пока тут ничего не будет

@app.route("/car-list/<string:car_brand>/<int:page>")
def car_list(car_brand, page):
    start = (page - 1) * 8

    API_URL = (
        f"https://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.Y._.Manufacturer.{car_brand}.)_.Year.range(202012..202210).)&sr=%7CModifiedDate%7C{start}%7C8"
    )

    try:
        log(f"Используется прокси: {proxies}")
        log(f"Куки: {session.cookies}")
        response = session.get(
            API_URL,
            timeout=10,
            proxies=proxies,
            headers=HEADERS
        )
        response.raise_for_status()
        data = response.json()
        cars = data.get("SearchResults", [])

        if not cars:
            log("WARNING: Не удалось получить данные от Encar: SearchResults пуст")
            return "Не удалось получить данные от Encar"

        log(f"Обновлены курсы валют: {rate}")

        car_ids = ",".join(str(car.get("Id")) for car in cars if car.get("Id"))
        log(f"ID: {car_ids}")

        url = (
            f"https://api.encar.com/v1/readside/vehicles"
            f"?vehicleIds={car_ids}&include=SPEC,ADVERTISEMENT,PHOTOS,CATEGORY,MANAGE,CONTACT,VIEW"
        )

        log(url)

        try:
            log(f"Используется прокси: {proxies}")
            response = session.get(
                url,
                headers=HEADERS,
                timeout=10,
                proxies=proxies,
            )
            response.raise_for_status()
            cars_data = response.json()
            log(f"Получено {len(cars_data)} объектов автомобилей из батч-запроса")

            cars_dict = {}
            for car_data in cars_data:
                manage = car_data.get("manage", {})
                # Выбираем правильный ключ: если dummy=True, то берем dummyVehicleId
                if manage.get("dummy"):
                    vehicle_id = str(manage.get("dummyVehicleId"))
                else:
                    vehicle_id = str(car_data.get("vehicleId"))

                if vehicle_id:
                    cars_dict[vehicle_id] = car_data

            log(cars_dict)

            for car in cars:
                car_id = str(car.get("Id"))
                car_data = None

                # Ищем машину в словаре: сначала как обычный vehicleId
                if car_id in cars_dict:
                    car_data = cars_dict[car_id]
                else:
                    # Если не нашли, ищем как dummyVehicleId
                    for v_id, data in cars_dict.items():
                        if data.get("manage", {}).get("dummy") and str(data["manage"].get("dummyVehicleId")) == car_id:
                            car_data = data
                            break

                if not car_data:
                    log(f"WARNING: Car ID {car_id} не найден в cars_dict")
                    continue

                category = car_data.get('category', {})
                car["Manufacturer_eng"] = category.get("manufacturerEnglishName")
                car["Model_eng"] = category.get("modelGroupEnglishName")
                car["grade_eng"] = category.get("gradeEnglishName")

                price = car.get("Price", 0)
                price_rub = convert_currency(price * 1000, "KRW", "RUB", rate)
                car["Price_RUB"] = value_converter(price_rub)

                log(car)

        except Exception as e:
            log(f"Ошибка при получении батч-данных авто: {e}")

    except Exception as e:
        log(f"Ошибка запроса API: {e}")
        cars = []

    return render_template("car_list.html", cars=cars, car_brand=car_brand, page=page)

@app.route("/vehicle/<int:car_id>")
def car_detail(car_id):
    return render_template("car_detail.html", car=car_id)

def initialize_app():
    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)
    os.environ.pop("http_proxy", None)
    os.environ.pop("https_proxy", None)

    log("Все прокси были отключены.")


    asyncio.run(update_cookies_and_tokens())
    log("Обновления курса")
    rate = get_exchange_rates()
    threading.Thread(target=rates_refresher, daemon=True).start()
    log("Flask запущен")

if __name__ == "__main__":
    initialize_app()
    app.run()