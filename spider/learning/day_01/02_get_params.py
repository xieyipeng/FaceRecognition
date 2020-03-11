import urllib.request
import urllib.parse
import string


def get_method_params():
    url = "http://www.baidu.com/s?"

    params = {
        "wd": "美女",
        "key": "zhang",
        "value": "san"
    }
    str_params = urllib.parse.urlencode(params)
    final_url = url + str_params
    print(final_url)
    # 代码发送请求，网址内含汉字，但ascii不含有汉字，url转译
    # 将包含汉字网址进行转译
    encode_new_url = urllib.parse.quote(final_url, safe=string.printable)
    # 发送网络请求
    response = urllib.request.urlopen(encode_new_url)
    # 读取内容
    new_data = response.read().decode("utf-8")
    print(new_data)
    # 保存到本地
    with open("02-encode.html", "w", encoding="utf8")as f:
        f.write(new_data)


get_method_params()
