import re

# 贪婪模式，从开头到结尾
one = 'muherfuihaiuniuwhgefuihcn'
pattern = re.compile('m(.*)n')
res = pattern.findall(one)
print(res)

# 非贪婪模式
pattern = re.compile('m(.*?)n')
res = pattern.findall(one)
print(res)

# match 从头开始匹配一次
# search 任意位置开始，匹配一次
# findall 查找符合正则的内容
# sub 替换字符串
# split 拆分
