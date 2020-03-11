import requests

# url
url = 'https://www.yaozh.com/member/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
# cookies字符串
cookies = 'acw_tc=2f624a0b15826025580545223e648248924af9f78243e14a79d91ee35dca16; _ga=GA1.1.945840169.1582607284; UtzD_f52b_ulastactivity=1582602677%7C0; PHPSESSID=86isrmbn02or9n6ad91cb6c4s2; _gid=GA1.2.1483003831.1582772812; _gat=1; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1582772814; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1582772818; yaozh_logintime=1582772750; yaozh_user=883085%09xieyipeng; yaozh_userId=883085; yaozh_jobstatus=kptta67UcJieW6zKnFSe2JyXnoaZb5hlnZmHnKZxanJT1qeSoMZYoNdzcJtaqszK28rUyc%2Beh3DYnp6bVaOWq6XArZqgxlig13NokXJUlJq91EbF69159e61Bfa47165A08EA2066e9ak5qUmnCVa4ef2JtncVesms6eU27UcJaXc1mSbWqVnJmTm5mRcJ5ph5%2Fi9de84d3031c54824cb020c1746abfc01; db_w_auth=752623%09xieyipeng; UtzD_f52b_saltkey=HydW6M6I; UtzD_f52b_lastvisit=1582769151; UtzD_f52b_lastact=1582772751%09uc.php%09; UtzD_f52b_auth=5354R7zuni9vgIJ8Lt%2FaNl3D2VaIXgbuSf9M3tRcedRbW1iRI8bEODbtFhSK41YI%2BPmjlUDzvHo3CSaD0YTkNWG7z04; yaozh_uidhas=1; yaozh_mylogin=1582772759; acw_tc=2f624a0b15826025580545223e648248924af9f78243e14a79d91ee35dca16; _ga=GA1.1.945840169.1582607284; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1582602978%2C1582607549%2C1582607880%2C1582772812; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1582772818; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1582772820; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1582772858'
# TODO: 1
# 需要字典 vscode
# cook_dict = {
#     "acw_tc": "2f624a0b15826025580545223e648248924af9f78243e14a79d91ee35dca16",
#     "_ga": "GA1.1.945840169.1582607284",
#     "UtzD_f52b_ulastactivity": "1582602677%7C0",
#     "PHPSESSID": "86isrmbn02or9n6ad91cb6c4s2",
#     "_gid": "GA1.2.1483003831.1582772812",
#     "_gat": "1",
#     "Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94": "1582772814",
#     "Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c": "1582772818",
#     "yaozh_logintime": "1582772750",
#     "yaozh_user": "883085%09xieyipeng",
#     "yaozh_userId": "883085",
#     "yaozh_jobstatus": "kptta67UcJieW6zKnFSe2JyXnoaZb5hlnZmHnKZxanJT1qeSoMZYoNdzcJtaqszK28rUyc%2Beh3DYnp6bVaOWq6XArZqgxlig13NokXJUlJq91EbF69159e61Bfa47165A08EA2066e9ak5qUmnCVa4ef2JtncVesms6eU27UcJaXc1mSbWqVnJmTm5mRcJ5ph5%2Fi9de84d3031c54824cb020c1746abfc01",
#     "db_w_auth": "752623%09xieyipeng",
#     "UtzD_f52b_saltkey": "HydW6M6I",
#     "UtzD_f52b_lastvisit": "1582769151",
#     "UtzD_f52b_lastact": "1582772751%09uc.php%09",
#     "UtzD_f52b_auth": "5354R7zuni9vgIJ8Lt%2FaNl3D2VaIXgbuSf9M3tRcedRbW1iRI8bEODbtFhSK41YI%2BPmjlUDzvHo3CSaD0YTkNWG7z04",
#     "yaozh_uidhas": "1",
#     "yaozh_mylogin": "1582772759",
#     "Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94": "1582602978%2C1582607549%2C1582607880%2C1582772812",
#     "Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c": "1582772858",
# }

# TODO: 2
# cookies_list = cookies.split('; ')
#
# cook_dict = {}
# for cookie in cookies_list:
#     cook_dict[cookie.split('=')[0]] = cookie.split('=')[1]

# TODO: 3

# TODO: 3
cook_dict = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies.split('; ')}

response = requests.get(url, headers=headers, cookies=cook_dict)

data = response.content.decode('utf-8')
with open('05_cookies.html', 'w', encoding='utf-8')as f:
    f.write(data)
