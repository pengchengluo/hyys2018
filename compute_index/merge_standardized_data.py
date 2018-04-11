"""
将标准化后的数据合并，以便求整体得分
"""


import csv
from utils import index
from utils.constant_data import provinces


def read_standardized_data(file_path):
    data = {}
    with open(file_path, mode='r', encoding='GBK') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            data[row['level3']+'_'+row['area']] = row
    return data


def get_rows(baidu_std_data, news_std_data, weibo_std_data, survey_std_data, level3, province):
    rows = {}
    baidu_row = baidu_std_data.get(level3+'_'+province)
    if baidu_row is not None:
        rows['baidu'] = baidu_row
    news_row = news_std_data.get(level3+'_'+province)
    if news_row is not None:
        rows['news'] = news_row
    weibo_row = weibo_std_data.get(level3+'_'+province)
    if weibo_row is not None:
        rows['weibo'] = weibo_row
    survey_row = survey_std_data.get(level3+'_'+province)
    if survey_row is not None:
        rows['survey'] = survey_row
    return rows


def get_avg(rows, field):
    score = 0
    total_weight = 0
    for key, value in rows.items():
        total_weight += weights[key]
    for key, value in rows.items():
        score += float(value[field])*weights[key]/total_weight
    return score


if __name__=='__main__':
    baidu_standardized_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/compute_growth/2_baidu_cnts_standardized_mean.csv'
    news_standardized_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/compute_growth/2_toutiao_cnts_standardized_mean.csv'
    weibo_standardized_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/compute_growth/2_weibo_cnts_standardized_mean.csv'
    survey_standardized_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/compute_growth/2_survey_converted.csv'
    all_merged_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/compute_growth/3_merged.csv'

    baidu_std_data = read_standardized_data(baidu_standardized_file)
    news_std_data = read_standardized_data(news_standardized_file)
    weibo_std_data = read_standardized_data(weibo_standardized_file)
    survey_std_data = read_standardized_data(survey_standardized_file)
    weights = {'baidu': 0.25, 'weibo': 0.25, 'news': 0.25, 'survey': 0.25}

    with open(all_merged_file, mode='w', encoding='GBK', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(('order', 'level3', 'area', 'score_std', 'score_avg_std', 'score_weight'))
        level3_cnt = 0
        for level1 in index.get_level1():
            for level2 in index.get_level2_by_level1(level1):
                for level3 in index.get_level3_by_level2(level2):
                    level3_cnt += 1
                    for province in provinces:
                            rows = get_rows(baidu_std_data, news_std_data, weibo_std_data, survey_std_data, level3, province)
                            writer.writerow((level3_cnt, level3, province,
                                             get_avg(rows, 'score_std'),
                                             get_avg(rows, 'score_avg_std'),
                                             get_avg(rows, 'score_weight')))