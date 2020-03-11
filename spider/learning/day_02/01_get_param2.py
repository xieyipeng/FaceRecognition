import urllib.request
import urllib.parse
import string


def get_params():
    url = "http://www.baidu.com/s?"
    params = {
        "wd": "美女",
        "key": "zhang",
        "value": "san"
    }
    str_params = urllib.parse.urlencode(params)
    final_url = url + str_params
    # 将带有中文的url转译
    end_url = urllib.parse.quote(final_url, safe=string.printable)
    # 发送请求
    print(end_url)
    response = urllib.request.urlopen(end_url)
    data = response.read().decode("utf-8")

    print(data)

    with open("01_test.html", "w", encoding="utf8")as f:
        f.write(data)


get_params()
