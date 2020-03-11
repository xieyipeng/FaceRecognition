import urllib.request


def load_baidu():
    url = "https://www.baidu.com"

    # 添加请求头信息
    header = {
        # 浏览器版本
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        # "haha": "hehe"
    }

    # 创建请求对象
    request = urllib.request.Request(url, headers=header)

    # 动态添加header信息
    # request.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36")

    # 请求网络数据(不在此处添加请求头信息)
    response = urllib.request.urlopen(request)
    # print(response)

    data = response.read().decode("utf-8")

    # 获取完整的url
    final_url=request.get_full_url()
    print(final_url)
    # TODO: 46:53

    # 响应头
    # print(response.headers)
    # print(data)

    # 获取请求头信息(打印所有头信息)
    # print(request.headers)
    # 第二种方式(首字母大写，其他字母小写)
    user_agent = request.get_header("User-agent")
    # print(user_agent)

    # 保存
    with open("02_header.html", "w", encoding="utf-8")as f:
        f.write(data)


load_baidu()
