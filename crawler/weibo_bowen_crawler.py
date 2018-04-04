from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from utils.file_utils import save
import pickle
import os
import time
import random
from bs4 import BeautifulSoup


def read_str(file, encoding='utf-8', errors='ignore'):
    """从文件中读取数据"""
    file = open(file, 'r', encoding=encoding)
    data = file.read()
    file.close()
    return data


def has_retrivaled_result(file_path):
    """从html文件判断是否有检索结果"""
    data = read_str(file_path)
    soup = BeautifulSoup(data, 'html.parser')
    try:
        element = soup.select('p.noresult_tit')
        if element is not None and len(element) > 0:
            return False
        else:
            return True
    except NoSuchElementException:
        return True


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
    browser = webdriver.Chrome()
    # browser = webdriver.Chrome()chrome_options=options
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
        login = browser.find_element_by_css_selector('ul.gn_login_list a[node-type="loginBtn"]')
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
    browser.execute_script('window.scrollTo(0,0);')
    browser.find_element_by_css_selector('#pl_common_searchTop a[node-type="advsearch"]').click()
    time.sleep(2)
    input_keyword = browser.find_element_by_css_selector('input[name="keyword"]')
    input_keyword.clear()
    input_keyword.send_keys(keyword)
    # browser.find_element_by_id('radio02').click()
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
        if os.path.exists(save_dir +'/'+ keyword+'_'+start_time+'_'+end_time+"_"+str(i)+".html"):
            continue
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(6 + random.randint(10, 15))
        save(browser.page_source.encode('utf-8'), save_dir, keyword+'_'+start_time+'_'+end_time+"_"+str(i)+".html")
        for refresh_time in range(0,3):
            if has_retrivaled_result(os.path.join(save_dir, keyword+'_'+start_time+'_'+end_time+"_"+str(i)+".html")):
                break
            else:
                print(keyword+'\trefresh')
                time.sleep(10*(refresh_time+1))
                browser.refresh()
        try:
            next_page = browser.find_element_by_css_selector('div.W_pages a.page.next.S_txt1.S_line1')
            if next_page is not None:
                current_url = browser.current_url
                browser.get(current_url[0:current_url.rindex('&')]+'&page='+str(i))
                # browser.get(next_page.get_attribute('href'))
        except NoSuchElementException:
            print("no more page")
            break
    return i


if __name__ == '__main__':
    save_dir = 'C:/Users/luopc/Desktop/hyys_2016_2018/weibo/2018/非热门'
    browser = get_browser()
    date_ranges = [('2017-01-01', '2017-12-31'),
        # ('2017-01-01', '2017-01-15'), ('2017-01-16', '2017-01-31'),
        # ('2017-02-01', '2017-02-15'), ('2017-02-16', '2017-02-28'),
        # ('2017-03-01', '2017-03-15'), ('2017-03-16', '2017-03-31'),
        # ('2017-04-01', '2017-04-15'), ('2017-04-16', '2017-04-30'),
        # ('2017-05-01', '2017-05-15'), ('2017-05-16', '2017-05-31'),
        # ('2017-06-01', '2017-06-15'), ('2017-06-16', '2017-06-30'),
        # ('2017-07-01', '2017-07-15'), ('2017-07-16', '2017-07-31'),
        # ('2017-08-01', '2017-08-15'), ('2017-08-16', '2017-08-31'),
        # ('2017-09-01', '2017-09-15'), ('2017-09-16', '2017-09-30'),
        # ('2017-10-01', '2017-10-15'), ('2017-10-16', '2017-10-31'),
        # ('2017-11-01', '2017-11-15'), ('2017-11-16', '2017-11-30'),
        # ('2017-12-01', '2017-12-15'), ('2017-12-16', '2017-12-31'),
    ]
    # '海苔',#未抓好
    keywords1 = ['波茨坦公告', '开罗宣言', '联合国海洋法公约', '南极条约', '北极理事会', '国际海事组织', '国际海洋法法庭', '东海大陆架', '领海基线', '南海岛礁', '南海地图', '专属经济区', '北极', '公海', '南极', '搁置争议', '南海各方行为宣言', '南海宣言', '一带一路', '钓鱼岛', '钓鱼岛国有化', '钓鱼岛争端', '黄岩岛事件', '南海仲裁案','南海', '北海舰队', '东海舰队', '海军', '航空母舰', '护卫舰', '辽宁号', '南海舰队',]
    keywords2 = [ '驱逐舰', '三大舰队', '巡洋舰', '中国海军', '东海军演', '海军演习', '黄海军演', '南海军演', '亚丁湾护航', '港口法', '海岛保护法', '海洋环境保护法', '海域使用管理法', '渔业法', '保护海洋', '海砂', '红珊瑚', '国家海洋局', '国家海洋信息中心', '海事局', '海洋局', '海洋环境保护', '海域使用论证', '海域使用权']
    keywords3 = []
    keywords4 = ['达伽马','发现新大陆','哥伦布','好望角','麦哲伦','南极探险','甲午海战','罗盘','下南洋','徐福','郑和','郑和下西洋','指南针','瓷器','海上丝绸之路','泉州', '丝绸','波塞冬','海神','龙王庙','妈祖','水阙仙班','四海龙王','开渔节','青岛海洋节','世界海洋日','中国航海日','观沧海','海底两万里','精卫填海','浪淘沙 北戴河','鲁滨逊漂流记',]
    keywords5 = ['大海啊故乡','海贼王','南海风云','外婆的澎湖湾','我爱这蓝色的海洋','悉尼歌剧院','海洋传说','龙的传说','哪吒闹海','大沽口炮台','南澳一号','南海一号','致远舰','中山舰','大连海事大学','海洋大学','海洋知识竞赛','中国海洋大学','海洋公园','海洋馆','海洋世界','文化馆','开渔节','游艇展']
    keywords6 = ['巴拿马运河','北冰洋','波斯湾','渤海','大陆漂移','大西洋','黄海','马六甲海峡','南海','南沙群岛','太平洋','西沙群岛','印度洋','潮汐','厄尔尼诺','海浪','海水的密度','拉尼娜','洋流','反渗透技术','海水淡化', '可燃冰','锰结核','溴','大洋一号','海龙号','蛟龙号','南极泰山站','雪龙号','远望号','长城站','反渗透法','海洋大学','遥感技术','赤潮','海水污染','海洋污染','红树林','人工鱼礁','珊瑚礁','休渔','风暴潮','海啸','寒潮','飓风','离岸流','台风','海平面上升','印度尼西亚海啸','沉没','触礁','东方之星','搁浅','古斯特洛夫号', '救生舱','救生船','救生筏','救生衣','滨海旅游','海洋经济','渔业','造船业','滨海旅游区','海水淡化','海洋工程','盐业','海产品','海水珍珠','海鲜','海鲜大排档','海岛旅游','海南旅游','青岛旅游','三亚旅游','厦门旅游','舟山旅游','海岸线','海岛','海湾','海域','湿地','带鱼','海带','南极磷虾','鱿鱼','紫菜','海洋石油','可燃冰','锰结核','波浪','潮汐能','海浪','可再生能源','迪拜人工岛','人工岛','棕榈岛','海参','乌贼骨','鱼肝油','港口','海底隧道','海上钻井平台','跨海大桥','中海油','海洋工程','海水淡化设备','海水稻','海水晶','海水淡化']
    keywords = ['潜艇','八仙过海','面朝大海','东海','海盐','泰坦尼克号',]#未抓好

    #'巴拿马运河', '北冰洋', '大陆漂移', '大西洋', '东海', '马六甲海峡', '南海','西沙群岛', '印度洋', '潮汐','厄尔尼诺', '海浪', '海水密度', '拉尼娜', '洋流', '反渗透技术', '海水淡化', '海盐', '可燃冰', '锰结核', '溴', '大洋一号', '海龙号', '蛟龙号', '南极泰山站','雪龙号', '远望号','长城站', '反渗透法', '遥感技术','赤潮','海水污染','海洋污染',
    #'波斯湾','渤海', '黄海','南沙群岛', '太平洋','海洋大学','红树林','人工鱼礁', '珊瑚礁', '休渔', '风暴潮',
    keywords = [
             '海啸',]
    for keyword in keywords:
        # if keyword in keywords1 or keyword in keywords2 or keyword in keywords3 or keyword in keywords4 or keyword in keywords5 or keyword in keywords6:
        #     continue
        sub_dir = os.path.join(save_dir,keyword)
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
        for date_range in date_ranges:
            cnt = search_keyword(browser, keyword, date_range[0], date_range[1], sub_dir)
            time.sleep(60+cnt*2)
    browser.close()
