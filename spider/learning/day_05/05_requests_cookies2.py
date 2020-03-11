import requests

# url
url = 'https://www.yaozh.com/member/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

# 不同于服务器的session，该session类可以自动保存cookies == CookieJar
session = requests.session()
# TODO: 1.代码登陆
login_url = 'https://www.yaozh.com/login/'
member_url = 'https://www.yaozh.com/member/'
login_form_data = {
    "username": "15536839029",
    "pwd": "1793807638xp",
    "formhash": "8D7032B7F6",
    "backurl": "https%253A%252F%252Fwww.yaozh.com%252F"
}
login_response = session.post(login_url, data=login_form_data, headers=headers)
print(login_response.content.decode())
# TODO: 2.登陆成功，带着cookies 访问请求目标数据
data = session.get(member_url, headers=headers).content.decode('utf-8')
with open('05_cookies2.html', 'w', encoding='utf-8')as f:
    f.write(data)
