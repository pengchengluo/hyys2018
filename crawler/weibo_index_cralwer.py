from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


browser = webdriver.Chrome()
browser.get('http://data.weibo.com/index')
time.sleep(1)
browser.find_element_by_css_selector('#pl_index_searchMain input').send_keys('海洋'+Keys.ENTER)
time.sleep(3)
browser.find_element_by_css_selector('#datepicker').send_keys('2016-01-01')
browser.find_element_by_css_selector('#datepicker1').send_keys('2017-12-31')
browser.find_element_by_css_selector('#pl_hotkey_contrast > a').click()
time.sleep(3)
browser.execute_script('alert(JSON.stringify(window[w]));}')
# browser.find_element_by_css_selector('#pl_hotkey_contrast li.time-search a[type="start"]').click()
# start = Select(browser.find_element_by_css_selector('#ui-datepicker-div select.ui-datepicker-year'))
# start.select_by_value('2016')
# time.sleep(3)
# browser.find_element_by_css_selector('#pl_hotkey_contrast li.time-search a[type="end"]').click()