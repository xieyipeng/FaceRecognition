import re
import requests

url = 'https://news.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
data = requests.get(url, headers=headers).content.decode('utf-8')
# 正则解析数据
# 每个新闻的标题和url
# re.S -> 匹配\n换行符

# pattern = re.compile('<a href="(.*?)" target="_blank" mon="(.*?)">(.*?)</a>')
pattern = re.compile('<a(.*?)</a>')

res = pattern.findall(data)
print(res)

# with open('02_news_re.html', 'w', encoding='utf-8') as f:
#     f.write(data)
