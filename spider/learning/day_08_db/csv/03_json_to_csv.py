import json
import csv
import sys

# 需求： 将json数据转换成csv文件
# 1. 读，创建文件
# sys.path.append('..')
json_fp = open('../json/02_json_new.json', 'r')
csv_fp = open('02_csv.csv', 'w', encoding='gbk', newline='')
# 2. 提出表头，表内容
data_list = json.load(json_fp)
sheet_title = data_list[0].keys()
sheet_data = []
for data in data_list:
    sheet_data.append(data.values())
# 3. csv写入器
writer = csv.writer(csv_fp)

# 4. 写入表头
writer.writerow(sheet_title)

# 5. 写入内容
writer.writerows(sheet_data)

# 6. 关闭两个文件
json_fp.close()
csv_fp.close()
