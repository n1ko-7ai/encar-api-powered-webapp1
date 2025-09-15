from playwright.sync_api import sync_playwright
import requests

API_URL = "https://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.CarType.Y.)&sr=%7CModifiedDate%7C0%7C20"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True,
                                args=[
                                    "--window-size=1920,1080",
                                    "--disable-blink-features=AutomationControlled"
                                ])
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    # Заходим на страницу, чтобы получить куки и localStorage
    page.goto("https://www.encar.com/dc/dc_carsearchlist.do?carType=kor")
    page.wait_for_timeout(2000)  # небольшая задержка

    # Получаем все куки
    cookies_list = context.cookies()
    cookies = {c['name']: c['value'] for c in cookies_list}
    print("Cookies:")
    for k, v in cookies.items():
        print(f"{k} = {v}")

    # Получаем все значения из localStorage
    local_storage = page.evaluate("() => Object.fromEntries(Object.entries(window.localStorage))")
    print("\nLocal Storage:")
    for k, v in local_storage.items():
        print(f"{k} = {v}")

    browser.close()

# Теперь делаем запрос к API через requests, используя куки
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://www.encar.com/',
    'Origin': 'https://www.encar.com',
}

session = requests.Session()
session.cookies.update(cookies)

# Если API использует данные из localStorage, можно передать их как параметры или заголовки
# Например, если API требует Cognito ID:
# headers['x-local-cognito'] = local_storage.get('aws.cognito.identity-id.ap-northeast-2')

response = session.get(API_URL, headers=headers, timeout=15)

print("\nAPI Status:", response.status_code)
try:
    data = response.json()
    print("JSON keys:", list(data.keys())[:10])
except Exception as e:
    print("Ошибка при разборе JSON:", e)
