from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import quote
import logging
import json
import os
import csv
import datetime
import time
import crawler.common as common


def crawl_keyword_index(keyword, start_date, end_date):
    """爬取指定搜狗微信指数"""
    url = 'http://index.sogou.com/getDateData?kwdNamesStr='+quote(keyword)+\
          '&startDate='+start_date+'&endDate='+end_date+'&dataType=MEDIA_WECHAT&queryType=INPUT'
    logging.info('crawl url:'+url)
    request = Request(url)
    response = urlopen(request)
    data = response.read()
    json_data = json.loads(data)
    time.sleep(2)
    return json_data
    # print(json_data['success'])
    # for element in json_data['data']['pvList'][0]:
    #     print(str(element['date'])+'\t'+str(element['pv']))


def add_date_header(start_date, end_date, header):
    start = datetime.datetime.strptime(start_date, '%Y%m%d')
    end = datetime.datetime.strptime(end_date, '%Y%m%d')
    one_day = datetime.timedelta(days=1)
    while start <= end:
        header.append(datetime.datetime.strftime(start, '%Y%m%d'))
        start += one_day


def crawl_and_save_weixin_index(keywords, saved_file_path):
    if os.path.exists(saved_file_path):
        mode = 'a'
    else:
        mode = 'w'
    with open(saved_file_path, mode=mode, encoding='GBK', newline='') as output_csv:
        writer = csv.writer(output_csv)
        header = ['地区', '关键词']
        add_date_header('20160101', '20171231', header)
        if mode == 'w':
            writer.writerow(header)
        index = 0
        for keyword in keywords:
            index += 1
            row = ['全国', keyword]
            json_data_1 = crawl_keyword_index(keyword, '20160101', '20161231')
            json_data_2 = crawl_keyword_index(keyword, '20170101', '20171231')
            if json_data_1['success'] and json_data_2['success']:
                logging.info(str(index) + '[全国,' + keyword + ']:' + 'success finally')
                for element in json_data_1['data']['pvList'][0]:
                    row.append(str(element['pv']))
                for element in json_data_2['data']['pvList'][0]:
                    row.append(str(element['pv']))
            writer.writerow(row)
            output_csv.flush()
            time.sleep(5)


if __name__ == '__main__':
    logging.basicConfig(filename='weixin_index.log',
                        format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %p',
                        level=logging.INFO)
    saved_file_path = 'weixin_index.csv'
    crawl_and_save_weixin_index(common.keywords, saved_file_path)

