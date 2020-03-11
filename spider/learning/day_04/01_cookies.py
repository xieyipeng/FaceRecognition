import urllib.request

url = "https://www.yaozh.com/member/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

# 构建请求对象
request = urllib.request.Request(url, headers=headers)
# 发送请求对象
response = urllib.request.urlopen(request)
# 读取数据
data = response.read().decode("utf-8")

with open("01_cookies.html", "w", encoding='utf-8')as f:
    f.write(data)
