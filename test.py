import scrapy
import json

class EncarSpider(scrapy.Spider):
    name = "encar"
    start_urls = [
        "https://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.Y._.Manufacturer.현대.)_.Year.range(202012..202210).)&sr=%7CModifiedDate%7C0%7C8"
    ]

    def parse(self, response):
        try:
            data = json.loads(response.text)
            print("\n=== Результаты Encar ===")
            for car in data.get("SearchResult", {}).get("Vehicles", []):
                print(f"{car.get('ModelName')} | {car.get('Price')}만원 | {car.get('Year')} | {car.get('Mileage')}km")
        except Exception as e:
            self.logger.error(f"Ошибка при обработке JSON: {e}")
