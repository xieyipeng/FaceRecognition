import requests
import json

# 返回内容是json
url = 'https://api.github.com/user'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
response = requests.get(url, headers=headers)
data = response.content.decode('utf-8')
data_json = response.json()
# TODO:
# print(data)
response.close()
# TODO: str->dict
data_dict = json.loads(data)

# print(data_dict)
# print(data_dict['message'])
# TODO: json 自动将json字符转转换成dict或list
print(data_json)
