import requests
from lxml import etree

# pip install lxml

url = 'https://news.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
data = requests.get(url, headers=headers).content.decode('utf-8')

# 1.转解析类型
xpath_data = etree.HTML(data)
# 2.调用xpath的方法
# res = xpath_data.xpath('/html/head/body/text()')
# print(res)
# res = xpath_data.xpath('//a/text()')
# print(len(res))
# print(res)
# res = xpath_data.xpath('//a[@mon="ct=1&a=2&c=top&pn=27"]/text()')
# res = xpath_data.xpath('//a[@mon="ct=1&a=2&c=top&pn=27"]/@href')
# print(res)

res = xpath_data.xpath('//li/a/text()')
print(res)

# with open('02_news_re.html', 'w', encoding='utf-8') as f:
#     f.write(data)


# xpath语法
# 1. 节点： /
# 2. 跨界点： //
# 3. 精确标签： //a[@属性="..."]    **标签必须唯一**
# 4. 标签包裹内容 text()
# 5. 属性： @href
# 6. xpath返回类型是 -- list
# 7. xpath下表从1开始
# 8. 模糊查询： //div[contains(@id,"normal thread")]    normal thread->值
# 9. 取下一个节点（平级关系） following-sibling::*
