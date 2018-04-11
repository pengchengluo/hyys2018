import json
import os
import csv
from utils.constant_data import provinces
from utils import index


def parser(file_path):
    """读取并解析json文件"""
    file = open(file_path, 'r', errors='ignore')
    data = json.load(file)
    file.close()
    return data


def get_comment_region(dir_path):
    """读取目录下所有json文件，计算各个省份各自评论数量"""
    if not os.path.exists(dir_path):
        return {}
    file_names = os.listdir(dir_path)
    file_names = sorted(file_names, key=lambda x: int(x[:x.index('.')]))
    region_cnt_map = {}
    for file_name in file_names:
        data = parser(dir_path+'/'+file_name)
        for comment in data['comments']:
            location = comment['user']['location'].strip()
            idx = location.find(' ')
            if idx > 0:
                location = location[:idx]
            if location in provinces:
                region_cnt_map[location] = region_cnt_map.get(location, 0)+1
    return region_cnt_map


def get_keyword_to_mids(file_path):
    """读取关键词到mid映射文件"""
    keyword_to_mids = {}
    with open(file_path, mode='r', encoding='utf-8') as input_file:
        for line in input_file.readlines():
            array = line.split('\t')
            s = keyword_to_mids.get(array[0], [])
            if len(s) == 0:
                keyword_to_mids[array[0]] = s
            s.append(array[1])
    return keyword_to_mids


if __name__ == '__main__':
    # 关键词到评论数量最多TOP20微博mid映射列表
    mids_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/weibo/2018/2018_remen_comment/top20_mids.txt'
    # 微博评论存放目录
    comment_dir = 'C:/Users/luopc/Desktop/hyys_2016_2018/weibo/2018/2018_remen_comment/comments'
    # 微博评论统计结果保存路径
    weibo_comment_cnt_file = 'C:/Users/luopc/Desktop/hyys_2016_2018/weibo/2018/weibo_comment_cnts.csv'

    keyword_to_mids = get_keyword_to_mids(mids_file)
    with open(weibo_comment_cnt_file, mode='w', encoding='GBK', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(('order', 'level3', 'area', 'keyword', 'score'))
        level3_cnt = 0
        for level1 in index.get_level1():
            for level2 in index.get_level2_by_level1(level1):
                for level3 in index.get_level3_by_level2(level2):
                    print(level3)
                    level3_cnt += 1
                    for keyword in index.get_keywords_by_level3(level3):
                        cnt_map = {}
                        for mid in keyword_to_mids.get(keyword, []):
                            region_cnt_map = get_comment_region(comment_dir+'/'+mid)
                            for province, cnt in region_cnt_map.items():
                                cnt_map[province] = cnt_map.get(province, 0) + cnt
                        for province in provinces:
                            writer.writerow((level3_cnt, level3, province, keyword, cnt_map.get(province, 0)))