import json

# TODO: 1.字符串 和 dic list 转换 -- +s
# json -> dict list
data = '[{"name": "张三", "age": "23"}, {"name": "李四", "age": "18"}]'
list_data = json.loads(data)
print('1 -> ' + format(type(data)))
print('2 -> ' + format(type(list_data)))
# json <- dict list
list2 = '[{"name": "张三", "age": "23"}, {"name": "李四", "age": "18"}]'
data_json = json.dumps(list2)
print('3 -> ' + format(type(data_json)))

# TODO: 2.文件对象 和 dict list 转换
# dict list 写入文件
list2 = [{"name": "张三", "age": "23"}, {"name": "李四", "age": "18"}]
# str_data = json.dumps(list2)
# with open('01_json.json', 'w', encoding='utf-8')as f:
#     f.write(str_data)
json.dump(list2, open('02_json_new.json', 'w', encoding='utf-8'))

# 读取文件 -> dict list  E:\Graduation-design\spider\learning\day_08_db\02_new_.json
res = json.load(open('02_json_new.json', 'r'))
print(res)