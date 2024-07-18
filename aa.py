import csv
import time
from random import randint

# CSV文件名
csv_filename = 'positions.csv'

# 生成示例数据
def generate_sample_data(num_entries):
    data = []
    for i in range(num_entries):
        timestamp = int(time.time())
        longitude = randint(-180, 180)
        latitude = randint(-90, 90)
        label = '位置' + str(i)  # 生成一个简单的标签
        data.append([timestamp, longitude, latitude, label])
    return data

# 写入CSV文件
def write_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入列名
        writer.writerow(['time', 'longitude', 'latitude', 'label'])
        # 写入数据
        for row in data:
            writer.writerow(row)

# 生成数据并写入CSV
sample_data = generate_sample_data(10)  # 生成10条数据作为示例
write_to_csv(sample_data, csv_filename)

print(f"CSV文件'{csv_filename}'已生成。")
