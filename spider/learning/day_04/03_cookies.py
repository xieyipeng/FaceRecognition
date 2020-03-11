"""
直接获取个人中心的页面
手动粘贴 复制 pc 抓取的 cookies
放在 request对象的请求头里

代码登陆
自动带着cookie，请求个人中心

"""

import urllib.request
# 自动保存cookie
from http import cookiejar
from urllib import parse

# TODO: 1.代码登陆
# 1.1 登陆网址 登陆页网址，找参数

# 后台：若你是get（登陆页面），若你是post（登陆结果）

login_url = 'https://www.yaozh.com/login/'
# 1.2 登陆参数
login_form_data = {
    "username": "15536839029",
    "pwd": "1793807638xp",
    "formhash": "8D7032B7F6",
    "backurl": "https%253A%252F%252Fwww.yaozh.com%252F"

}
# 参数，转码，转译；post请求，data，要求bytes
login_str = parse.urlencode(login_form_data).encode('utf-8')
print(login_str)
# 1.3 发送post登录请求
cook_jar = cookiejar.CookieJar()
# 定义有添加cookie功能的处理器
cook_handler = urllib.request.HTTPCookieProcessor(cook_jar)
# 根据处理器生成opener
opener = urllib.request.build_opener(cook_handler)
# 带着参数 发送post请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
}

login_request = urllib.request.Request(login_url, headers=headers, data=login_str)
# 如果登陆成功，cookiejar自动保存cookie
opener.open(login_request)

# TODO: 2.带着cookie访问个人中心
center = "https://www.yaozh.com/member/"
center_request = urllib.request.Request(center, headers=headers)
response = opener.open(center)
data = response.read().decode('utf-8')
with open("03cookies.html", 'w', encoding='utf-8')as f:
    f.write(data)
