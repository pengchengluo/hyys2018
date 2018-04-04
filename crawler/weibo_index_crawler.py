from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time, datetime
import csv
from crawler.common import keywords


def add_date_header(start_date, end_date, header):
    start = datetime.datetime.strptime(start_date, '%Y%m%d')
    end = datetime.datetime.strptime(end_date, '%Y%m%d')
    one_day = datetime.timedelta(days=1)
    while start <= end:
        header.append(datetime.datetime.strftime(start, '%Y%m%d'))
        start += one_day

def get_browser():
    browser = webdriver.Chrome()
    browser.get('http://data.weibo.com/index')
    time.sleep(1)
    browser.find_element_by_css_selector('#pl_index_searchMain input').send_keys('海洋'+Keys.ENTER)
    time.sleep(3)
    return browser


def crawl_index(browser, keyword):
    browser.find_element_by_css_selector('#pl_hotkey_contrast li.long-search > input').clear()
    browser.find_element_by_css_selector('#pl_hotkey_contrast li.long-search > input').send_keys(keyword)
    browser.find_element_by_css_selector('#datepicker').clear()
    browser.find_element_by_css_selector('#datepicker').send_keys('2015-01-01')
    browser.find_element_by_css_selector('#datepicker1').clear()
    browser.find_element_by_css_selector('#datepicker1').send_keys('2017-12-31')
    browser.find_element_by_css_selector('#pl_hotkey_contrast > a').click()
    time.sleep(5)
    if '找不到此热词' in browser.find_element_by_css_selector('#pl_hotkey_contrast li.long-search > input').get_attribute('value'):
        return None
    data = []
    name =  browser.execute_script('return echart_resources.chart.pc_mobile.origin.component.grid.myChart.component.xAxis.series[0].name;')
    value = browser.execute_script('return echart_resources.chart.pc_mobile.origin.component.grid.myChart.component.xAxis.series[0].data;')
    data.append((name, value))
    name =  browser.execute_script('return echart_resources.chart.pc_mobile.origin.component.grid.myChart.component.xAxis.series[1].name')
    value = browser.execute_script('return echart_resources.chart.pc_mobile.origin.component.grid.myChart.component.xAxis.series[1].data')
    data.append((name, value))
    name = browser.execute_script('return echart_resources.chart.hotword.origin.chart.line.series[0].name')
    value = browser.execute_script('return echart_resources.chart.hotword.origin.chart.line.series[0].data')
    data.append((name, value))
    return data


if __name__ == '__main__':
    result_saved_file_path = 'C:/Users/luopc/Desktop/hyys_2016_2018/weibo/weibo_index_2015-2017.csv'
    browser = get_browser()
    with open(result_saved_file_path, mode='a', encoding='gbk', newline='') as output_csv:
        writer = csv.writer(output_csv)
        header = ['keyword', 'type']
        add_date_header('20150101', '20171231', header)
        writer.writerow(header)
        cnt = 0
        for keyword in keywords:
            cnt += 1
            if cnt < 13:
                continue
            print(str(cnt)+'\t'+keyword)
            data = crawl_index(browser, keyword)
            if data is None:
                row = [keyword, '找不到此热词']
                writer.writerow(row)
                output_csv.flush()
            else:
                for element in data:
                    row = [keyword]
                    row.append(element[0])
                    row.extend(element[1])
                    writer.writerow(row)
                    output_csv.flush()
            time.sleep(10)
    browser.close()
