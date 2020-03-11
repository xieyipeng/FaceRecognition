import urllib.request


def auth_neiwang():
    # 哟ing户名密码
    user = "admin"
    pwd = "123456"
    nei_url = "http://192.168.179.66"

    # 创建密码管理器
    pwd_manger = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    pwd_manger.add_password(None, nei_url, user, pwd)
    auth_handler = urllib.request.HTTPBasicAuthHandler(pwd_manger)
    opener = urllib.request.build_opener(auth_handler)
    response = opener.open(nei_url)
    print(response.read())


auth_neiwang()
