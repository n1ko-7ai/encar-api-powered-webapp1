import requests

cookies = {
    'WMONID': 'GJNPd05q7JA',
    '_encar_hostname': 'https://www.encar.com',
    'PCID': '17579323937614380552824',
    '_ga': 'GA1.2.2111845228.1757932394',
    '_gid': 'GA1.2.1668968463.1757932394',
    'JSESSIONID': '06A5C24178AB0BCCF795A868A02ED463.mono-web-prod_202.153',
    '_enlog_lpi': 'd32e.aHR0cHM6Ly93d3cuZW5jYXIuY29tL2luZGV4LmRv.497',
    '_gcl_au': '1.1.1318046605.1758025212',
    '_dsClick': '',
    'X-Auth-Token-Encar': 'a4964ec8-035a-4bf6-aef8-65eff50c7d73',
    'ENID_ACCESS_TOKEN': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsibW9iaWxlX2FwaSIsImVuY2FyX3Jlc291cmNlIl0sImlzc3VlIjoxNzU4MDI1MzUzNjIyLCJ1c2VyX25hbWUiOiJnMDkyNTE2NjBiMmIzIiwic2NvcGUiOlsicmVhZCIsInNpZ24iXSwiZXhwIjoxNzU4MTExNzUzLCJ1c2VyIjp7Im5hbWUiOiLsvZTsubTsvZzrnbwiLCJpZCI6ImcwOTI1MTY2MGIyYjMiLCJ1c2VyVHlwZSI6IklORElWSURVQUwifSwiYXV0aG9yaXRpZXMiOlsiUk9MRV9VU0VSIl0sImp0aSI6Ijc0YjQ4YTNkLTliOTYtNDEwNi04MzMwLTQxZjhkMTA3NzRmOSIsImNsaWVudF9pZCI6IjAwODllMDliLTk2M2QtNDViOC1hYWJhLTZjOTJmNDk0NGY3MyJ9.i9hbDWNRZD5XpP_xou0caDrGbfynqhWoeXC5-wagxM0',
    'USERID': 'g09251660b2b3',
    'USERNAME': '%2525C4%2525DA%2525C4%2525AB%2525C4%2525DD%2525B6%2525F3',
    'USERTYPE': '1',
    'PERSISTENT_USERTYPE': '1',
    'ENID_PLATFORM': 'GOOGLE',
    '_gat_UA-56065139-3': '1',
    '_enlog_native_datatalk_hit': 'gnb',
    '_ga_WY0RWR65ED': 'GS2.2.s1758025186$o3$g1$t1758025377$j39$l0$h0',
    '_enlog_datatalk_hit': '',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,ko;q=0.7,da;q=0.6,fr;q=0.5,zh-CN;q=0.4,zh;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.encar.com/index.do',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0 (Edition Campaign 34)',
    'sec-ch-ua': '"Opera GX";v="121", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'WMONID=GJNPd05q7JA; _encar_hostname=https://www.encar.com; PCID=17579323937614380552824; _ga=GA1.2.2111845228.1757932394; _gid=GA1.2.1668968463.1757932394; JSESSIONID=06A5C24178AB0BCCF795A868A02ED463.mono-web-prod_202.153; _enlog_lpi=d32e.aHR0cHM6Ly93d3cuZW5jYXIuY29tL2luZGV4LmRv.497; _gcl_au=1.1.1318046605.1758025212; _dsClick=; X-Auth-Token-Encar=a4964ec8-035a-4bf6-aef8-65eff50c7d73; ENID_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsibW9iaWxlX2FwaSIsImVuY2FyX3Jlc291cmNlIl0sImlzc3VlIjoxNzU4MDI1MzUzNjIyLCJ1c2VyX25hbWUiOiJnMDkyNTE2NjBiMmIzIiwic2NvcGUiOlsicmVhZCIsInNpZ24iXSwiZXhwIjoxNzU4MTExNzUzLCJ1c2VyIjp7Im5hbWUiOiLsvZTsubTsvZzrnbwiLCJpZCI6ImcwOTI1MTY2MGIyYjMiLCJ1c2VyVHlwZSI6IklORElWSURVQUwifSwiYXV0aG9yaXRpZXMiOlsiUk9MRV9VU0VSIl0sImp0aSI6Ijc0YjQ4YTNkLTliOTYtNDEwNi04MzMwLTQxZjhkMTA3NzRmOSIsImNsaWVudF9pZCI6IjAwODllMDliLTk2M2QtNDViOC1hYWJhLTZjOTJmNDk0NGY3MyJ9.i9hbDWNRZD5XpP_xou0caDrGbfynqhWoeXC5-wagxM0; USERID=g09251660b2b3; USERNAME=%2525C4%2525DA%2525C4%2525AB%2525C4%2525DD%2525B6%2525F3; USERTYPE=1; PERSISTENT_USERTYPE=1; ENID_PLATFORM=GOOGLE; _gat_UA-56065139-3=1; _enlog_native_datatalk_hit=gnb; _ga_WY0RWR65ED=GS2.2.s1758025186$o3$g1$t1758025377$j39$l0$h0; _enlog_datatalk_hit=',
}

params = {
    'carType': 'kor',
}

response = requests.get(
    'https://www.encar.com/dc/dc_carsearchlist.do',
    params=params,
    cookies=cookies,
    headers=headers
)

with open("encar_response.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("✅ HTML сохранён в encar_response.html")

