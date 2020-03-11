import requests

# 参数自动转译
# url = 'https://www.baidu.com/s?ie=UTF-8&wd=美女'
url = 'http://www.baidu.com/s'
params = {
    "wd": "美女",
    "ie": "utf-8"
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
# response = requests.get(url, headers=headers)
response = requests.get(url, headers=headers, params=params)
data = response.content.decode('utf-8')
with open('07requests_get.html', 'w', encoding='utf-8')as f:
    f.write(data)

# 发送post请求 添加参数
# requests.post(url,data=(参数{}),json=(参数))
