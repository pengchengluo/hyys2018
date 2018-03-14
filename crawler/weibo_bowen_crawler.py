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
    browser = webdriver.Chrome()
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
        time.sleep(1)
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


def search_keyword(browser, keyword):
    browser.find_element_by_link_text('高级搜索').click()
    time.sleep(2)
    input_keyword = browser.find_element_by_css_selector('input[name="keyword"]')
    input_keyword.clear()
    input_keyword.send_keys(keyword)
    browser.find_element_by_id('radio02').click()
    browser.execute_script('document.querySelector("input[name=\'stime\']").removeAttribute("readonly")')
    browser.execute_script('document.querySelector("input[name=\'etime\']").removeAttribute("readonly")')
    # browser.execute_script('document.querySelector("select[name=\'startHour\']").removeAttribute("disabled")')
    # browser.execute_script('document.querySelector("select[name=\'endHour\']").removeAttribute("disabled")')
    stime = browser.find_element_by_css_selector('input[name="stime"]')
    stime.clear()
    stime.send_keys('2017-01-01')
    etime = browser.find_element_by_css_selector('input[name="etime"]')
    etime.clear()
    etime.send_keys('2017-01-15')
    # browser.find_element_by_css_selector('select[name="startHour"]').select_by_value('0')
    # browser.find_element_by_css_selector('select[name="endHour"]').select_by_value('23')
    browser.find_element_by_css_selector('div.adv_btn a.W_btn_cb').click()
    i = 0
    while True:
        i += 1
        time.sleep(5)
        save(browser.page_source.encode('utf-8'), 'C:/Users/luopc/Desktop/crawler_data', keyword+"_"+str(i)+".html")
        next_page = browser.find_element_by_link_text('下一页')
        if next_page is not None:
            next_page.click()
            time.sleep(5+random.randint(2,6))


if __name__ == '__main__':
    browser = get_browser()
    search_keyword(browser, '南海')
