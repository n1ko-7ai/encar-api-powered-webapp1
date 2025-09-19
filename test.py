import requests

url = "https://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.CarType.Y.)&sr=%7CModifiedDate%7C0%7C20"

encar_cookies = {
    "_enlog_datatalk_hit": "",
    "_enlog_lpi": "0d48.aHR0cHM6Ly93d3cuZW5jYXIuY29tL2luZGV4LmRv.a53",
    "_ga": "GA1.2.2111845228.1757932394",
    "_ga_WY0RWR65ED": "GS2.2.s1758193272$o4$g1$t1758194645$j26$l0$h0",
    "_gcl_au": "1.1.1318046605.1758025212",
    "_gid": "GA1.2.32251106.1758193272",
    "AEC": "AaJma5tz9C4Y3lm16Jc6iyaIeJW3HqVWTvdNpM33g_Vm7bre7tqqjXuIAA",
    "APISID": "PT6hW874qUSd14qw/AUbzFFlYnA5O7HWxH",
    "DV": "EwXRP1JGe4gvUAuW96t36_5eimTJlZn-BnbWayEtSgAAAAA",
    "HSID": "ASDYO8Tp2fkCjxr0f",
    "IDE": "AHWqTUkXcngHmYvrJfjIW2BJ5z3n3Ngk9Zor6dIUYSbJm2n7dwBpn85yMuhz8l4UsMg",
    "JSESSIONID": "460FFFB6CF93B8802722DF75F087D99E.mono-web-prod_199.37",
    "NID": "525=c99gXSFkPvL0EWpaAYnYrlH9BKJ6AyY4fjHdYWpShMylfMVFL0eDMgw7J1h-vPzLKtMR6MfLgMnB-ei_al_Zq9mtwOwvodu2014juk-E5VqOOtfU7QJC0MhC2xz7XdXpzNPfDvqNjs4T1iH6kqDFCGwB0jxqXqoWY2jyA3M2phFhu7fENnU5wXrYWmB1pR_G0m-lyPeVpoMJ8hdXV_k3dbATmpEeBQQ4JglcIAcIo29UMUt_orSMQPSEXl3AAU4xKBpIwV8jbZhz5LmRwf1X-uv9qOVYleuM9afuVPRgVA8sivlMcUfzyVr_L5jHYFqjxhD54nigmkYcOf_dZ-cS5YEY3pqfAUyrd5KQWNH-ciklJCmEDFUHGNZ7GDszDrEAiPHuDVXQg1RAuaM822p34KbgxE1yz1uzbwdOCYWL-bcBksmEBHGQlBPvVJV2AzMOdwXLE9bYI4v3ZhOy62PcarvRXM8rz-I4znI63FTC5UtljoZx_1Ijv1uznjrHid_9t0TbL9v3P-olX7LY9vyY5C_dQEV1qigd7p_Lbh2holZo7YeGZxWHDKybbN0G6cU6Ha7uKMOyPziZ8aw4ZBt7Oma0xEszwl9Wcx31HsS_ZtfdNiYnd1c4RVccGRgRXUqWdYJTnm-vq3G37J-464bjBo2LrvQr3wHDU4i_248nnisF0hSm1RPU-Ul3jjfEITGy4w1NLRIULbe_n1l3b0BBsxmXiI5OfDJe9iWEdY8m80va3XG86ZuCwHs_IaKSAFMGWx0OTk5zYTEBOVqi4zrwhqjKRe1H_D614is1_WKMAUZ8a6IoSpoancgR6XmQMRKBLIjeywFtqHWDgLVk7pGM_9WymXcNPJ1-njCHVwZEae-OoCFle_NZ9k8zPRl_uGfBRJyX8E_KQCoyMW75ecJG-iQ6KGEmE5R3BfUPkCGceevi-c0NAaxG1fmsh87dJKzjv2H7RC-VKQUhuDugEftS0uC0TARnb029lsjj81rlnjyRbBfhBFdeD8XN4sRs9Jfo3IJrXPVk8JyjROZHuKLqnxSuPHRRUJKpFShZO-knmKhlP6QsWErNTIT7uAtxgDeR2hwhiRkaRXyf3l6wQe22RO-01MgYagnaaoO_DDeeKAXr_xHOnWWzzf11f5Mwm70",
    "PCID": "17579323937614380552824",
    "PERSISTENT_USERTYPE": "1",
    "SAPISID": "ljK395KBd_a4UtKa/A-xu7u7X1SQtcbsEP",
    "SID": "g.a0001ghKazKULubq9y-VJMwUnNFrBDu0nwkUpCMuvwPN_5V_7wqgQKksnuxAISY8yTHMWY8dpwACgYKAUUSARQSFQHGX2Mi575W1EiFgWxsG32z_NJFUhoVAUF8yKrx5reRzdSa9z_axqfl_Z9b0076",
    "SIDCC": "AKEyXzWGjavCiKWa-FnC6tztB6r3zlxXMuOibX7cTtEHH9A0jZ62n-dHCOJa5BPJ5Erko_lCp9I",
    "SSID": "AtsrjxkR3orx4VOjj",
    "WMONID": "GJNPd05q7JA"
}

headers = {
    "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.encar.com",
    "Referer": "https://www.encar.com/dc/dc_carsearchlist.do?carType=kor",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "X-Requested-With": "XMLHttpRequest"
}

response = requests.post(url, headers=headers, cookies=encar_cookies)

print(response.status_code)  # или .json(), если это JSON
