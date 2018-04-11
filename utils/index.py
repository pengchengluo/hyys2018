import csv
import os
from collections import OrderedDict

level1_to_level2 = OrderedDict()
level2_to_level3 = OrderedDict()
level3_to_weight = OrderedDict()
level3_to_keywords = OrderedDict()


def insert_into_dict(dict_obj, key, value):
    s = dict_obj.get(key, [])
    if len(s) == 0:
        dict_obj[key] = s
    if value not in s:
        s.append(value)

package_dir = os.path.dirname(os.path.abspath(__file__))
with open(package_dir+'/index.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        insert_into_dict(level1_to_level2, row['level1'], row['level2'])
        insert_into_dict(level2_to_level3, row['level2'], row['level3'])
        level3_to_weight[row['level3']] = row['level3_weight']
        level3_to_keywords[row['level3']] = row['keywords'].split('、')


def get_level1():
    """获得一级指标集合"""
    return level1_to_level2.keys()


def get_level2_by_level1(level1):
    """通过一级指标获得二级指标集合"""
    return level1_to_level2[level1]


def get_level3_by_level2(level2):
    """通过二级指标获得三级指标集合"""
    return level2_to_level3[level2]


def get_weight_by_level3(level3):
    """通过三级指标获得三级指标权重"""
    return level3_to_weight[level3]


def get_keywords_by_level3(level3):
    """通过三级指标获得三级指标对应的关键词集合"""
    return level3_to_keywords[level3]


if __name__ == '__main__':
    for level1 in get_level1():
        for level2 in get_level2_by_level1(level1):
            for level3 in get_level3_by_level2(level2):
                data = (level1, level2, level3, get_weight_by_level3(level3), '、'.join(get_keywords_by_level3(level3)))
                print('\t\t'.join(data))