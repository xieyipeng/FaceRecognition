import urllib.request
import random


def load_baidu():
    url = "http://www.baidu.com"
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    ]
    # 每次选择不一样的浏览器
    random_user_agent = random.choice(user_agent_list)
    request = urllib.request.Request(url)
    # 增加请求头信息
    request.add_header("User-Agent", random_user_agent)
    # 请求数据
    response = urllib.request.urlopen(request)

    # 请求头信息
    print(request.get_header("User-agent"))


load_baidu()
