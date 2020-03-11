# 1.安装模块requests
import requests

url = 'http://www.baidu.com'
response = requests.get(url)
# content 返回字节 是 bytes
data = response.content.decode('utf-8')
# text直接就是str
text = response.text
print(text)
with open('05_requests.html', 'w', encoding='utf-8') as f:
    f.write(data)
