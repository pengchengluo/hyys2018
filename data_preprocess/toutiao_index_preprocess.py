import csv

from utils import index
from utils.constant_data import provinces


if __name__=='__main__':
    toutiao_index_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/toutiao/toutiao_converted.csv'
    toutiao_index_raw_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/toutiao/toutiao_index_province_2017.csv'
    with open(toutiao_index_file, mode='w', encoding='GBK', newline='') as output_csv, \
            open(toutiao_index_raw_file, mode='r', encoding='GBK', newline='') as input_csv:
        writer = csv.writer(output_csv)
        reader = csv.reader(input_csv)
        header = reader.__next__()
        area_keyword_map = {}
        for record in reader:
            area_keyword_map[record[0] + '_' + record[1]] = record[2:]
        writer.writerow(['order', '类别', '地域', '搜索词'] + header[2:])
        level3_cnt = 0
        for level1 in index.get_level1():
            for level2 in index.get_level2_by_level1(level1):
                for level3 in index.get_level3_by_level2(level2):
                    level3_cnt += 1
                    for keyword in index.get_keywords_by_level3(level3):
                        for province in provinces:
                            record = [level3_cnt, level3, province, keyword] + area_keyword_map[
                                province + '_' + (keyword if keyword != '海水的密度' else '海水密度')]
                            if str(record[4]).strip() == '':
                                for i in range(4, len(record)):
                                    record[i] = 0
                            writer.writerow(record)