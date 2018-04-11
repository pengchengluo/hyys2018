import csv

import pandas as pd

from utils import index


def convert_keyword_rate_to_level3_keyword_rate(keyword_growth_rate, level3_keyword_growth_rate):
    """将关键词的增长率转换为三级指标+关键词的增长率"""
    with open(keyword_growth_rate, mode='r', encoding='GBK', newline='') as input_csv, \
            open(level3_keyword_growth_rate, mode='w', encoding='GBK', newline='') as output_csv:
        keyword_rate_map = {}
        reader = csv.DictReader(input_csv)
        for record in reader:
            keyword_rate_map[record['keyword']] = record['rate']
        writer = csv.writer(output_csv)
        writer.writerow(('level3', 'keyword', 'rate'))
        for level1 in index.get_level1():
            for level2 in index.get_level2_by_level1(level1):
                for level3 in index.get_level3_by_level2(level2):
                    for keyword in index.get_keywords_by_level3(level3):
                        writer.writerow((level3, keyword, keyword_rate_map.get(keyword, 0)))


def compute_overall_growth_rate(level3_keyword_growth_rate, weight_file_path):
    """计算整体增长率"""
    weight = pd.read_excel(weight_file_path)
    rate = pd.read_csv(level3_keyword_growth_rate, encoding='GBK')
    rate = rate.groupby(rate['level3']).mean()
    rate = rate.reset_index()
    data_frame = pd.merge(weight, rate[['level3', 'rate']], on='level3')
    data_frame = pd.concat([data_frame, data_frame['rate'] * data_frame['level3_weight']], axis=1)
    data_frame = data_frame.rename(columns={0: 'weight_rate'})
    growth_rate = data_frame['weight_rate'].sum()
    return growth_rate/weight['level3_weight'].sum()

if __name__=='__main__':
    data_dir = 'C:/Users/luopc/Desktop/hyys_2016_2018'
    weight_file_path = 'C:/Users/luopc/Desktop/hyys_2016_2018/compute/index_weight.xlsx'

    # for baidu
    keyword_growth_rate = data_dir+'/baidu/baidu_level3_keyword_growth_rate.csv'
    print('baidu:\t'+str(compute_overall_growth_rate(keyword_growth_rate, weight_file_path)))

    # for toutiao
    keyword_growth_rate = data_dir+'/toutiao/toutiao_keyword_growth_rate.csv'
    level3_keyword_growth_rate = data_dir + '/toutiao/toutiao_level3_keyword_growth_rate.csv'
    convert_keyword_rate_to_level3_keyword_rate(keyword_growth_rate, level3_keyword_growth_rate)
    print('toutiao:\t'+str(compute_overall_growth_rate(level3_keyword_growth_rate, weight_file_path)))

    # for weibo
    keyword_growth_rate = data_dir + '/weibo/weibo_keyword_growth_rate.csv'
    level3_keyword_growth_rate = data_dir + '/weibo/weibo_level3_keyword_growth_rate.csv'
    convert_keyword_rate_to_level3_keyword_rate(keyword_growth_rate, level3_keyword_growth_rate)
    print('weibo:\t' + str(compute_overall_growth_rate(level3_keyword_growth_rate, weight_file_path)))
