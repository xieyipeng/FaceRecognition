import requests

# ssl认证： TODO: 您的链接不是私密链接
# https有第三方 CA认证
# 但是 12306虽然是https，但不是CA证书，他自己颁布的证书
# 解决方法：我直接告诉web服务器，忽略证书 访问 -> verify=false

url = 'https://www.12306.cn/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

response = requests.get(url, headers=headers, verify=False)
data = response.content.decode('utf-8')
with open('03_ssl.html', 'w', encoding='utf-8')as f:
    f.write(data)
