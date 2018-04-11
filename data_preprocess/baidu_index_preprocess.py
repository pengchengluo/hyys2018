import os
import csv
from utils import index
from utils.constant_data import provinces


if __name__=='__main__':
    baidu_index_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/baidu/baidu_converted.csv'
    baidu_index_raw_dir = 'C:/Users/luopc/Desktop/hyys_2016_2018/baidu/all'
    with open(baidu_index_file, mode='w', encoding='GBK', newline='') as output_csv:
        area_keyword_map = {}
        for province in provinces:
            with open(baidu_index_raw_dir+'/'+province+'.csv', mode='r', encoding='GBK', newline='') as input_csv:
                reader = csv.reader(input_csv)
                header = reader.__next__()
                for record in reader:
                    area_keyword_map[province + '_' + record[4]] = record[5:]
        writer = csv.writer(output_csv)
        header = header[2:]
        header.insert(0, 'order')
        writer.writerow(header)
        level3_cnt = 0
        for level1 in index.get_level1():
            for level2 in index.get_level2_by_level1(level1):
                for level3 in index.get_level3_by_level2(level2):
                    level3_cnt += 1
                    for keyword in index.get_keywords_by_level3(level3):
                        for province in provinces:
                            record = [level3_cnt, level3, province, keyword] + area_keyword_map[province + '_' + keyword]
                            writer.writerow(record)