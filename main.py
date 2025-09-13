import requests
from flask import Flask, render_template

app = Flask(__name__)

cookies = {
    '_encar_hostname': 'https://www.encar.com',
    'PCID': '17577416528492457772199',
    '_ga': 'GA1.2.400926650.1757741653',
    '_gid': 'GA1.2.1340211684.1757741653',
    '_enlog_datatalk_hit': '',
    '_enlog_lpi': '2eb6.aHR0cHM6Ly93d3cuZW5jYXIuY29tL2RjL2RjX2NhcnNlYXJjaGxpc3QuZG8%2FY2FyVHlwZT1rb3IjISU3QiUyMmFjdGlvbiUyMiUzQSUyMihBbmQuSGlkZGVuLk4uXy5DYXJUeXBlLlkuKSUyMiUyQyUyMnRvZ2dsZSUyMiUzQSU3QiU3RCUyQyUyMmxheWVyJTIyJTNBJTIyJTIyJTJDJTIyc29ydCUyMiUzQSUyMk1vZGlmaWVkRGF0ZSUyMiUyQyUyMnBhZ2UlMjIlM0ExJTJDJTIybGltaXQlMjIlM0EyMCUyQyUyMnNlYXJjaEtleSUyMiUzQSUyMiUyMiUyQyUyMmxvZ2luQ2hlY2slMjIlM0FmYWxzZSU3RA%3D%3D.edd',
    '_gat_UA-56065139-3': '1',
    '_ga_WY0RWR65ED': 'GS2.2.s1757752490$o3$g1$t1757752490$j60$l0$h0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ko;q=0.7,da;q=0.6,fr;q=0.5',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Opera GX";v="121", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0 (Edition Campaign 34)',
    'cookie': '_encar_hostname=https://www.encar.com; PCID=17577416528492457772199; _ga=GA1.2.400926650.1757741653; _gid=GA1.2.1340211684.1757741653; _enlog_datatalk_hit=; _enlog_lpi=2eb6.aHR0cHM6Ly93d3cuZW5jYXIuY29tL2RjL2RjX2NhcnNlYXJjaGxpc3QuZG8%2FY2FyVHlwZT1rb3IjISU3QiUyMmFjdGlvbiUyMiUzQSUyMihBbmQuSGlkZGVuLk4uXy5DYXJUeXBlLlkuKSUyMiUyQyUyMnRvZ2dsZSUyMiUzQSU3QiU3RCUyQyUyMmxheWVyJTIyJTNBJTIyJTIyJTJDJTIyc29ydCUyMiUzQSUyMk1vZGlmaWVkRGF0ZSUyMiUyQyUyMnBhZ2UlMjIlM0ExJTJDJTIybGltaXQlMjIlM0EyMCUyQyUyMnNlYXJjaEtleSUyMiUzQSUyMiUyMiUyQyUyMmxvZ2luQ2hlY2slMjIlM0FmYWxzZSU3RA%3D%3D.edd; _gat_UA-56065139-3=1; _ga_WY0RWR65ED=GS2.2.s1757752490$o3$g1$t1757752490$j60$l0$h0',
}

@app.route('/')
def index():
    response = requests.get(
        'https://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.CarType.Y.)&sr=%7CModifiedDate%7C0%7C20',
        cookies=cookies,
        headers=headers,
    )
    return response.text

if __name__ == "__main__":
    app.run(debug=False)



print(response.text)