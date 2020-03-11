import urllib.request


def handler_openner():
    # 系统的urlopen并没有添加代理功能,需要我们自定义
    # 安全 套阶层 ssl：第三方CA数字证书
    # http 80端口 - https443端口
    # urlopen为什么可以请求数据 handler处理器
    # 自己的openner请求数据

    # urllib.request.urlopen()
    url = "https://blog.csdn.net/xieyipeng1998/article/details/100053465"
    # 创建自己的处理器
    handler = urllib.request.HTTPHandler()
    # 创建自己的openner
    openner = urllib.request.build_opener(handler)
    # 用自己创建的openner请求数据
    response = openner.open(url)
    print(response)
    data = response.read().decode("utf-8")
    print(data)
    # with open("05_openner.html", "w", encoding="utf-8")as f:
    #     f.write(data)


handler_openner()
