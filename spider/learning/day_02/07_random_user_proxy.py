import urllib.request


def proxy_user():
    proxy_list = [
        {"http": "212.200.27.134:8080"},
        {"http": "43.254.168.56:53281"},
        {"http": "217.150.77.31:53281"},
        {"http": "87.228.103.111:8080"},
        {"http": "212.117.19.215:55555"}
    ]
    for proxy in proxy_list:
        # print(proxy)
        # 创建处理器
        proxy_handler = urllib.request.ProxyHandler(proxy)
        # 创建openner
        openner = urllib.request.build_opener(proxy_handler)

        try:
            openner.open("http://www.baidu.com", timeout=1)
            print("ok")
        except Exception as e:
            print(e)


proxy_user()
