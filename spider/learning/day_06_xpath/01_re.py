import re
# 数据解析
# TODO: 1.拆分字符串
one = 'asihoesrfhhs'
# 标准：以s为拆分
# pattern = re.compile('s')
# res = pattern.split(one)
# print(res)

# TODO: 2.匹配中文
two = '<a href="http://job.csdn.net" title="招聘">招聘的是最好的，适配移动端</a>'
# python中 匹配中间[a-z] unicode unicode的范围       * + ?
pattern = re.compile('[\u4e00-\u9fa5]+')
res = pattern.findall(two)
print(res)
