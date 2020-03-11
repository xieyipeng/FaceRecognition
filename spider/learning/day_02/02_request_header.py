import urllib.request


def load_baidu():
    url = "http://www.baidu.com"

    # 创建请求对象
    request = urllib.request.Request(url)

    # 请求网络数据
    response = urllib.request.urlopen(request)
    print(response)

    data = response.read().decode("utf-8")
    print(data)

    # 响应头
    print(response.headers)

    # 获取请求头信息
    print(request.headers)

    # 保存
    with open("02_header.html", "w",encoding="utf-8")as f:
        f.write(data)

load_baidu()
