"""
直接获取个人中心的页面
手动粘贴 复制 pc 抓取的 cookies
放在 request对象的请求头里

登录后进入个人中心，检查cookie，粘贴到代码

"""

import urllib.request

url = "https://www.yaozh.com/member/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Cookie': '_ga=GA1.2.1282875296.1579327835; acw_tc=2f624a0b15826025580545223e648248924af9f78243e14a79d91ee35dca16; PHPSESSID=rj1b604r0bha2gs0b1ako8e9j3; _gid=GA1.2.1958442999.1582602640; yaozh_logintime=1582602677; yaozh_user=883085%09xieyipeng; yaozh_userId=883085; yaozh_jobstatus=kptta67UcJieW6zKnFSe2JyXnoaZb5hlnZmHnKZxanJT1qeSoMZYoNdzcJtaqszK28rUyc%2Beh3DYnp6bVaOWq6XArZqgxlig13NokXJUlJq77eE154F261086C7ca00f910120A87b7ak5qUk22cbIef2JtncVesms6eU27UcJaXc1mSbWqVm5KTmpuabZdrh5%2Fi7f0c99310ac314e0a7f7d891a8861db5; _gat=1; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1582602760; yaozh_uidhas=1; yaozh_mylogin=1582602683; acw_tc=2f624a0b15826025580545223e648248924af9f78243e14a79d91ee35dca16; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1582602640%2C1582602656'
}

# TODO: 1431

# 构建请求对象
request = urllib.request.Request(url, headers=headers)
# 发送请求对象
response = urllib.request.urlopen(request)
# 读取数据
data = response.read().decode("utf-8")

with open("02_cookies.html", "w", encoding='utf-8')as f:
    f.write(data)
