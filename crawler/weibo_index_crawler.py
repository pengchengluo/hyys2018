from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


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
    browser.find_element_by_css_selector('#datepicker').send_keys('2016-01-01')
    browser.find_element_by_css_selector('#datepicker1').clear()
    browser.find_element_by_css_selector('#datepicker1').send_keys('2017-12-31')
    browser.find_element_by_css_selector('#pl_hotkey_contrast > a').click()
    time.sleep(3)
    print(browser.execute_script('return echart_resources.chart.pc_mobile.origin.component.grid.myChart.component.xAxis.series[0].name;'))
    print(browser.execute_script('return echart_resources.chart.pc_mobile.origin.component.grid.myChart.component.xAxis.series[0].data;'))
    print(browser.execute_script('return echart_resources.chart.pc_mobile.origin.component.grid.myChart.component.xAxis.series[1].name'))
    print(browser.execute_script('return echart_resources.chart.pc_mobile.origin.component.grid.myChart.component.xAxis.series[1].data'))
    print(browser.execute_script('return echart_resources.chart.hotword.origin.chart.line.series[0].name'))
    print(browser.execute_script('return echart_resources.chart.hotword.origin.chart.line.series[0].data'))


if __name__ == '__main__':
    browser = get_browser()
    crawl_index(browser, '南海')
