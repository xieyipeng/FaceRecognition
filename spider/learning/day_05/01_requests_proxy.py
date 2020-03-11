import requests

# 1.请求url

url = 'http://www.baidu.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
free_proxy = {
    # 'http': 'IP:port'
    'http': '163.125.29.23:8118'
}

response = requests.get(url, headers=headers, proxies=free_proxy)

print(response.status_code)
