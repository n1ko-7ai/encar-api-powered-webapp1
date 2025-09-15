from playwright.sync_api import sync_playwright

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

    # Эмуляция движений мыши и задержек может помочь
    page.goto("https://www.encar.com/dc/dc_carsearchlist.do?carType=kor")

    cookies = context.cookies()
    for cookie in cookies:
        print(f"{cookie['name']} : {cookie['value']}")

    browser.close()


