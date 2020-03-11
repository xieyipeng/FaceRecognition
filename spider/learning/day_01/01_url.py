import urllib.request
# 学习网址 https://www.bilibili.com/video/av68030937?p=26

def load_data():
    url = "http://www.baidu.com/"
    # get请求
    # http请求
    # response：http相应对象
    response = urllib.request.urlopen(url)
    print(response)
    # 读取内容 byte类型
    data = response.read()
    print(data)
    # 将文件获取的内容转换成字符串
    str_data = data.decode("utf-8")
    print(str_data)
    # 将数据写入文件
    with open("01-baidu.html", "w", encoding="utf-8")as f:
        f.write(str_data)
    # 将字符串类型转换为bytes
    str_name="baidu"
    byte_name=str_name.encode("utf-8")
    print(byte_name)

    # 如果爬取bytes，类型，要写入str： decode
    # 如果爬取str，类型，要写入bytes： encode


load_data()
