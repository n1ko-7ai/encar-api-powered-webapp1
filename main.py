import requests, json

API_URL = "https://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.Y._.Manufacturer.현대.)_.Year.range(202012..202210).)&sr=%7CModifiedDate%7C0%7C20"

# cookies, которые ты получил
cookies = {
    'JSESSIONID': '514DD59E5C84AC7A1FFBC75CC63A82B2.mono-web-prod_202.38',
    'WMONID': 'mgohRjT3ChQ',
}

# рекомендуемые заголовки — используй те, что у тебя в рабочем браузере
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://www.encar.com/',
    'Origin': 'https://www.encar.com',
}

s = requests.Session()
s.cookies.update(cookies)
r = s.get(API_URL, headers=headers, timeout=15)

print("Status:", r.status_code)
print("Response length:", len(r.text))
print("Response preview:\n", r.text[:800])
print("Response headers:\n", r.headers)
print("Set-Cookie in response:", r.headers.get('set-cookie'))
print("Session cookies now:", s.cookies.get_dict())

# попытка распарсить JSON (если сервер его вернёт)
try:
    data = r.json()
    print("JSON keys:", list(data.keys())[:10])
except Exception as e:
    print("Не JSON или ошибка парсинга:", e)