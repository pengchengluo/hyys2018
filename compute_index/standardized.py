import pandas as pd
import numpy as np
from pandas import Series

"""
将原始数据标准化（包括求网民人均值）
"""

def add_divided_by_cybercitizen(data_frame, cybercitizen_frame):
    data_avg_frame = pd.merge(data_frame, cybercitizen_frame, on='area')
    data_avg_frame = pd.concat([data_avg_frame, data_avg_frame['score']/data_avg_frame['population']], axis=1)
    data_avg_frame.columns = ['order', 'level3', 'area', 'keyword', 'score', 'population', 'score_avg']
    return data_avg_frame


def std_array(x):
    avg = x.mean()
    std = x.std(ddof=0)
    if std == 0:
        return x*0+0.6+grow_score
    else:
        return ((x-avg)/std)*((0.4-grow_score/100)/3)+0.6+grow_score


def add_standardized(data_frame, column_name, new_column_name, std_method=None, std_param1=None):
    if std_method == 'mean_var':
        # 六级计算方法
        # standardized = data_frame[column_name].groupby([data_frame['level3'], data_frame['keyword']])\
        #     .apply(lambda x: ((x-x.mean())/x.std())*7/71+50/71)
        standardized = data_frame[column_name].groupby([data_frame['level3'], data_frame['keyword']])\
            .apply(std_array)
        standardized[standardized > 1] = 1
        standardized[standardized < 0] = 0
        # 3/7 for 0.7, 7/13 for 0.65, 2/3 for 0.6
        # standardized = data_frame[column_name].groupby([data_frame['level3'], data_frame['keyword']])\
        #     .apply(lambda x: 1/(1+np.exp(-(x-x.mean())/x.std()+np.log(7/13))))
        # standardized = data_frame[column_name].groupby([data_frame['level3'], data_frame['keyword']])\
        #     .apply(lambda x: (x-x.mean())/x.std())
    elif std_method == 'ln':
        standardized = data_frame[column_name].groupby([data_frame['level3'], data_frame['keyword']])\
            .apply(lambda x: np.log(x+1)/np.log(x.max()+1))
    elif std_method == 'n_max':
        standardized = data_frame[column_name].groupby([data_frame['level3'], data_frame['keyword']])\
            .apply(lambda x: x/np.partition(x, std_param1)[std_param1])
        standardized[standardized > 1] = 1
    else:
        standardized = data_frame[column_name].groupby([data_frame['level3'], data_frame['keyword']])\
            .apply(lambda x: x/np.max(x))
    standardized.name = new_column_name
    data_frame = pd.concat([data_frame, standardized], axis=1)
    return data_frame


def add_weight_score(data_frame):
    weight_score = 0.3*data_frame['score_std']+0.7*data_frame['score_avg_std']
    weight_score.name = 'score_weight'
    data_frame = pd.concat([data_frame, weight_score], axis=1)
    return data_frame


def standardized(file_path):
    data = pd.read_csv(file_path, encoding='GBK')
    # add average data
    data = add_divided_by_cybercitizen(data, cybercitizen)
    # standardized
    data = add_standardized(data, 'score', 'score_std', std_method='mean_var')
    data = add_standardized(data, 'score_avg', 'score_avg_std', std_method='mean_var')
    data = add_weight_score(data)
    return data


if __name__ == '__main__':
    data_dir = 'C:/Users/luopc/Desktop/hyys_2016_2018/compute_growth'
    data_filename = 'baidu_cnts'
    grow_score = 2.098/100
    cybercitizen_file = 'cybercitizen.xlsx'

    cybercitizen = pd.read_excel(data_dir+'/'+cybercitizen_file)
    data = standardized(data_dir+'/0_'+data_filename+'.csv')
    data.to_csv(data_dir+'/1_'+data_filename+'_standardized.csv', encoding='GBK')

    data_mean = data.groupby([data['level3'], data['area']]).mean()
    data_mean.reset_index(level=['level3', 'area'], inplace=True)
    data_mean.sort_values(['order', 'area'], inplace=True)
    data_mean.to_csv(data_dir+'/2_'+data_filename+'_standardized_mean.csv',
                     columns=['order', 'level3', 'area', 'score', 'population',
                              'score_avg', 'score_std', 'score_avg_std', 'score_weight'], encoding='GBK')