import urllib.request


def create_proxy_handler():
    url = "https://blog.csdn.net/xieyipeng1998/article/details/100053465"

    # 添加代理
    proxy = {
        # 免费的写法
        "http": "http://212.200.27.134:8080"
        # 付费代理
        # "http":"xiaoming":123@115.46.1.1
    }
    # 代理的处理器
    proxy_handler = urllib.request.ProxyHandler(proxy)
    # 创建自己的openner
    openner = urllib.request.build_opener(proxy_handler)
    # 拿着代理ip去发送请求
    data = openner.open(url).read().decode("utf-8")
    print(data)


create_proxy_handler()
