import pandas as pd
import numpy as np
from pandas import Series
from pandas import ExcelWriter

"""
在标准化后数据的基础上求指标得分
"""


def compute_index_score(data_frame, weight_frame, score_column):
    data_frame = pd.merge(weight_frame, data_frame[['level3','area',score_column]], on='level3')
    data_frame = pd.concat([data_frame, data_frame[score_column]*data_frame['level3_weight']], axis=1)
    data_frame = data_frame.rename(columns={0: 'new_score'})
    return data_frame


def compute_index_one_time(data_frame, column_name):
    return data_frame[column_name].groupby([data_frame['area'],data_frame['level3']]).mean().sum(level='area')


def compute_index(data_frame, level=None):
    if level is None:
        return data_frame['new_score'].groupby(data_frame['area']).sum()
    else:
        return data_frame['new_score'].groupby([data_frame['area'], data_frame[level]]).sum()


if __name__ == '__main__':
    data_file_path = 'C:/Users/luopc/Desktop/hyys_2016_2018/compute_growth/3_merged.csv'
    weight_file_path = 'C:/Users/luopc/Desktop/hyys_2016_2018/compute_growth/index_weight.xlsx'

    weight = pd.read_excel(weight_file_path)
    data_all = pd.read_csv(data_file_path, encoding='GBK')

    # compute index basically
    # index_total = compute_index_one_time(data_all, 'score_std')
    # index_avg = compute_index_one_time(data_all, 'score_avg_std')
    # index_weight = compute_index_one_time(data_all, 'score_weight')

    # compute index with the weight file
    score_data_level3 = compute_index_score(data_all, weight, 'score_std')
    score_data_level2 = compute_index(score_data_level3, 'level2')
    score_data_level1 = compute_index(score_data_level3, 'level1')
    score_data_level0 = compute_index(score_data_level3)

    score_avg_data_level3 = compute_index_score(data_all, weight, 'score_avg_std')
    score_avg_data_level2 = compute_index(score_avg_data_level3, 'level2')
    score_avg_data_level1 = compute_index(score_avg_data_level3, 'level1')
    score_avg_data_level0 = compute_index(score_avg_data_level3)

    score_weight_data_level3 = compute_index_score(data_all, weight, 'score_weight')
    score_weight_data_level2 = compute_index(score_weight_data_level3, 'level2')
    score_weight_data_level1 = compute_index(score_weight_data_level3, 'level1')
    score_weight_data_level0 = compute_index(score_weight_data_level3)

    writer = ExcelWriter('C:/Users/luopc/Desktop/hyys_2016_2018/compute_growth/计算结果.xlsx')
    score_data_level3.to_excel(writer, '总量')
    score_avg_data_level3.to_excel(writer, '人均')
    score_weight_data_level3.to_excel(writer, '加权')
    pd.DataFrame.from_items([('总量', score_data_level2),
                             ('人均', score_avg_data_level2),
                             ('加权', score_weight_data_level2)],
                            orient='columns').to_excel(writer, 'level2', merge_cells=False)
    pd.DataFrame.from_items([('总量', score_data_level1),
                             ('人均', score_avg_data_level1),
                             ('加权', score_weight_data_level1)],
                            orient='columns').to_excel(writer, 'level1', merge_cells=False)
    pd.DataFrame.from_items([('总量', score_data_level0),
                             ('人均', score_avg_data_level0),
                             ('加权', score_weight_data_level0)],
                            orient='columns').to_excel(writer, 'level0', merge_cells=False)
    writer.save()