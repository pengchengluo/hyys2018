from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from utils.file_utils import save
import pickle
import os
import time
import random


def save_cookies(cookies):
    output = open('data/cookies', 'wb')
    pickle.dump(cookies, output)
    output.close()


def load_cookies():
    if not os.path.exists('data/cookies'):
        return None
    input = open('data/cookies', 'rb')
    cookies = pickle.load(input)
    input.close()
    return cookies


def load_account():
    if not os.path.exists('data/account'):
        return None
    input = open('data/account', 'r')
    lines = input.readlines()
    input.close()
    return lines

def get_browser():
    weibo_search_url = 'https://s.weibo.com/'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1600x900')
    browser = webdriver.Chrome(chrome_options=options)
    # browser = webdriver.Chrome()
    # browser = webdriver.Edge()
    # browser = webdriver.Firefox()
    cookies = load_cookies()
    browser.get(weibo_search_url)
    browser.maximize_window()
    time.sleep(1)
    if cookies is not None:
        for cookie in cookies:
            browser.add_cookie(cookie)
    browser.get(weibo_search_url)
    time.sleep(1)
    login = None
    try:
        login = browser.find_element_by_link_text('登录')
    except:
        print("Can't find login button. Maybe it already login.")
    if login is not None:
        login.click()
        time.sleep(2)
        account = load_account()
        browser.find_element_by_css_selector('input[name="username"]').send_keys(account[0])
        browser.find_element_by_css_selector('input[name="password"]').send_keys(account[1])
        browser.find_element_by_css_selector('div.item_btn a.W_btn_a').click()
        time.sleep(5)
        cookies = browser.get_cookies()
        save_cookies(cookies)
    browser.find_element_by_css_selector('input.searchInp_form').send_keys('海洋' + Keys.ENTER)
    time.sleep(3)
    return browser


def search_keyword(browser, keyword, start_time, end_time, save_dir):
    browser.find_element_by_link_text('高级搜索').click()
    time.sleep(2)
    input_keyword = browser.find_element_by_css_selector('input[name="keyword"]')
    input_keyword.clear()
    input_keyword.send_keys(keyword)
    browser.find_element_by_id('radio02').click()
    browser.execute_script('document.querySelector("input[name=\'stime\']").removeAttribute("readonly")')
    browser.execute_script('document.querySelector("input[name=\'etime\']").removeAttribute("readonly")')
    stime = browser.find_element_by_css_selector('input[name="stime"]')
    stime.clear()
    stime.send_keys(start_time)
    etime = browser.find_element_by_css_selector('input[name="etime"]')
    etime.clear()
    etime.send_keys(end_time)
    browser.find_element_by_css_selector('div.adv_btn a.W_btn_cb').click()
    i = 0
    while True:
        i += 1
        time.sleep(5)
        save(browser.page_source.encode('utf-8'), save_dir, keyword+'_'+start_time+'_'+end_time+"_"+str(i)+".html")
        next_page = browser.find_element_by_link_text('下一页')
        if next_page is not None:
            next_page.click()
            time.sleep(5+random.randint(2,6))


if __name__ == '__main__':
    save_dir = 'C:/Users/luopc/Desktop/crawler_data'
    browser = get_browser()
    date_ranges = [
        ('2017-01-01', '2017-01-15'), ('2017-01-16', '2017-01-31'),
        ('2017-02-01', '2017-02-15'), ('2017-02-16', '2017-02-28'),
        ('2017-03-01', '2017-03-15'), ('2017-03-16', '2017-03-31'),
        ('2017-04-01', '2017-04-15'), ('2017-04-16', '2017-04-30'),
        ('2017-05-01', '2017-05-15'), ('2017-05-16', '2017-05-31'),
        ('2017-06-01', '2017-06-15'), ('2017-06-16', '2017-06-30'),
        ('2017-07-01', '2017-07-15'), ('2017-07-16', '2017-07-31'),
        ('2017-08-01', '2017-08-15'), ('2017-08-16', '2017-08-31'),
        ('2017-09-01', '2017-09-15'), ('2017-09-16', '2017-09-30'),
        ('2017-10-01', '2017-10-15'), ('2017-10-16', '2017-10-31'),
        ('2017-11-01', '2017-11-15'), ('2017-11-16', '2017-11-30'),
        ('2017-12-01', '2017-12-15'), ('2017-12-16', '2017-12-31'),
    ]
    keywords = ['南海']
    for keyword in keywords:
        sub_dir = os.path.join(save_dir,keyword)
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
        for date_range in date_ranges:
            search_keyword(browser, keyword, date_range[0], date_range[1], sub_dir)
    browser.close()
