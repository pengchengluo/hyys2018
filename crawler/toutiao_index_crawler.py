
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import quote
import json
import datetime
import csv
import time
import logging
import crawler.common as common
import os


region_id_map = {
    '全国': '0',
    '北京': '11', '天津': '12', '河北': '13', '山西': '14', '内蒙古': '15',
    '辽宁': '21', '吉林': '22', '黑龙江': '23',
    '上海': '31', '江苏': '32', '浙江': '33', '安徽': '34', '福建': '35', '江西': '36', '山东': '37',
    '河南': '41', '湖北': '42', '湖南': '43', '广东': '44', '广西': '45', '海南': '46',
    '重庆': '50', '四川': '51', '贵州': '52', '云南': '53', '西藏': '54',
    '陕西': '61', '甘肃': '62', '青海': '63', '宁夏': '64', '新疆': '65',
    '香港': '81',
}


def is_keyword_included(keyword):
    url = 'https://index.toutiao.com/keyword/trends?keywords%5B%5D='+quote(keyword)
    request = Request(url)
    response = urlopen(request)
    data = response.read()
    html = data.decode('utf-8')
    if 'active-keyword-empty-90ad68d91f759751ad40' in html:
        return False
    return True

def crawl_keyword_index(region, keyword, start_date, end_date):
    """爬取指定头条指数，并以name命名保存在result_saved_dir目录中"""
    url = 'https://index.toutiao.com/api/keyword/trends?region='+region_id_map[region] +\
          '&category=0&keyword='+quote(keyword)+'&start='+start_date+'&end='+end_date+'&is_hourly=0'
    logging.info('crawl url:'+url)
    request = Request(url)
    response = urlopen(request)
    data = response.read()
    if data.decode().startswith('<script id="script-injected">'):
        return []
    json_data = json.loads(data)
    return json_data['trends'][keyword]


def add_date_header(start_date, end_date, header):
    start = datetime.datetime.strptime(start_date, '%Y%m%d')
    end = datetime.datetime.strptime(end_date, '%Y%m%d')
    one_day = datetime.timedelta(days=1)
    while start <= end:
        header.append(datetime.datetime.strftime(start, '%Y%m%d'))
        start += one_day


def crawl_and_save_toutiao_index(regions, keywords, start_date, end_date, saved_file_path, start_row):
    if os.path.exists(saved_file_path):
        mode = 'a'
    else:
        mode = 'w'
    with open(saved_file_path, mode=mode, encoding='GBK', newline='') as output_csv:
        writer = csv.writer(output_csv)
        header = ['地区', '关键词']
        add_date_header(start_date, end_date, header)
        if mode == 'w':
            writer.writerow(header)
        index = 0
        for region in regions:
            for keyword in keywords:
                index += 1
                if index < start_row:
                    continue
                if not is_keyword_included(keyword):
                    continue
                row = [region, keyword]
                try_time = 0
                while try_time < 10:
                    try:
                        try_time += 1
                        data = crawl_keyword_index(region, keyword, start_date, end_date)
                        break
                    except Exception as e:
                        print(e)
                        logging.warning(str(index)+'['+region+','+keyword+']:'+'try '+str(try_time)+' times failed:')
                        time.sleep(10 * (try_time * try_time))
                if try_time >= 10:
                    logging.error(str(index)+'['+region+','+keyword+']:'+'failed finally')
                else:
                    logging.info(str(index)+'['+region+','+keyword+']:'+'success finally')
                    row.extend(data)
                    writer.writerow(row)
                    output_csv.flush()
                    time.sleep(10)


if __name__ == '__main__':
    logging.basicConfig(filename='toutiao_index.log',
                        format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %p',
                        level=logging.INFO)
    saved_file_path = 'toutiao_index.csv'
    crawl_and_save_toutiao_index(common.regions, common.keywords, common.start_date, common.end_date, saved_file_path,
                                 1)
