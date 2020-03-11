import requests


class RequestSpider(object):
    def __init__(self):
        url = 'http://www.baidu.com'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }
        self.response = requests.get(url, headers=headers)

    def run(self):
        data = self.response.content
        # 1、获取请求头
        request_headers = self.response.request.headers
        # 2、获取响应头
        response_headers = self.response.headers
        # 3、获取响应状态码
        code = self.response.status_code
        # 4、获取请求cookie
        request_cookie = self.response.request._cookies
        # 5、获取响应cookie
        response_cookie = self.response.cookies
        print(response_cookie)


RequestSpider().run()
