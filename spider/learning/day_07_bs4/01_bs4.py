from bs4 import BeautifulSoup

# pip install beautifulsoup4

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>

<p class="story"><!--gsergszdf--></p>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>


"""

# TODO: 1.转类型 -- BeautifulSoup
# 默认bs4会调用系统中lxml的解析库，会有警告提示
soup = BeautifulSoup(html_doc, features='lxml')

# TODO: 2.格式化输出 补全
# res = soup.prettify()
# print(res)

# TODO: 3.解析数据 -- Tag 标签对象
# res = soup.p
# print(res)

# TODO: 4.内容 -- NavigableString
# res = soup.a.string
# print(res)

# TODO: 5.属性 -- str
# res = soup.a['href']
# print(type(res))

# TODO: 6.取注释 -- Comment
res = soup.p.string
print(res)


