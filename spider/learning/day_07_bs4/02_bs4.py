from bs4 import BeautifulSoup

# pip install beautifulsoup4

html_doc = """
<html><head><title id="one">The Dormouse's story</title></head>
<body>

<p class="story"><!--gsergszdf--></p>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>


"""

soup = BeautifulSoup(html_doc, features='lxml')

# TODO: find
# 1. 返回符合查询条件的第一个标签
# res = soup.find(name="p")
# 2. 属性
# res = soup.find(attrs={"class": "title"})
# 3.text
# res = soup.find(text="Tillie")

# res = soup.find(
#     name='p',
#     attrs={"class": "story"}
# )

# TODO: find_all -- list(标签对象)
# res = soup.find_all(name="a")
# res = soup.find_all(name="a", limit=1)
# res = soup.find_all(attrs={"class": "sister"})

# TODO: select_one -- css选择器
# res = soup.select_one(selector=".sister")

# TODO: select -- css选择器 -- list
res = soup.select(selector=".sister")
res = soup.select(selector="#one")
# 后代选择器
res = soup.select(selector="head title")
# 组选择器
res = soup.select(selector="title,.title")
# 属性选择器
res = soup.select(selector='a[id="link1"]')

# 标签包裹的内容
# res = soup.select('b')[0].get_text()
# 标签的属性
# res = soup.select('#link1')[0].get('href')


print(res)
