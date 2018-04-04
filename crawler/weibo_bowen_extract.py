from bs4 import BeautifulSoup
import os
import csv
import json


def read_str(file, encoding='utf-8', errors='ignore'):
    """从文件中读取数据"""
    file = open(file, 'r', encoding=encoding)
    data = file.read()
    file.close()
    return data


def extract_bowen_2018_from_html_file(file_path):
    """从html文件中提取博文数据"""
    data = read_str(file_path)
    soup = BeautifulSoup(data, 'html.parser')
    weibo_list = []
    element = soup.select('p.noresult_tit')
    if element is not None and len(element) > 0:
        return weibo_list
    for node in soup.select('.WB_cardwrap.S_bg2.clearfix > div[mid]'):
        content_soup = node.select('.feed_content.wbcon > .comment_txt')
        time_soup = node.select('.feed_from.W_textb > .W_textb')
        forward = ''
        comment = ''
        praise = ''
        for feed_soup in node.select('.feed_action_info.feed_action_row4 > li > a'):
            text = feed_soup.get_text().strip()
            if text == "收藏":
                continue
            elif text.startswith("转发"):
                forward = text[2:]
            elif text.startswith("评论"):
                comment = text[2:]
            elif len(text) > 0 and feed_soup['title'] == '赞':
                praise = text
        if len(forward.strip()) == 0:
            forward = '0'
        if len(comment.strip()) == 0:
            comment = '0'
        if len(praise.strip()) == 0:
            praise = '0'
        weibo_list.append((node['mid'], time_soup[0].get_text(), int(forward), int(comment), int(praise),
                           content_soup[0].get_text().strip().replace('\r\n', ' ').replace('\n', ' '), file_path))
                          # content_soup[0].get_text().strip()))
    return weibo_list


def extract_bowen_2016_from_html_file(file_path):
    """从html文件中提取博文数据"""
    if os.path.getsize(file_path) < 2048:
        data = read_str(file_path, encoding='gbk')
    else:
        data = read_str(file_path)
    soup = BeautifulSoup(data, 'html.parser')
    weibo_list = []
    for node in soup.select('script'):
        text = node.get_text()
        if '"pid":"pl_weibo_direct"' in text:
            js = json.loads(text[text.index('(') + 1:text.rindex(')')])
            # print(js['html'])
            html_soup = BeautifulSoup(js['html'], 'html.parser')
            next_page_soup = html_soup.select('a.page.next.S_txt1.S_line1')
            for element in html_soup.select('.WB_cardwrap.S_bg2.clearfix > div[mid]'):
                content_soup = element.select('.feed_content.wbcon > .comment_txt')
                time_soup = element.select('.feed_from.W_textb > .W_textb')
                forward = ''
                comment = ''
                praise = ''
                for feed_soup in element.select('.feed_action_info.feed_action_row4 > li > a'):
                    text = feed_soup.get_text().strip()
                    if text == "收藏":
                        continue
                    elif text.startswith("转发"):
                        forward = text[2:]
                    elif text.startswith("评论"):
                        comment = text[2:]
                    elif len(text) > 0 and feed_soup['title'] == '赞':
                        praise = text
                if len(forward.strip()) == 0:
                    forward = '0'
                if len(comment.strip()) == 0:
                    comment = '0'
                if len(praise.strip()) == 0:
                    praise = '0'
                if len(time_soup) == 0:
                    print(file_path)
                    print(content_soup[0].get_text().strip().replace('\r\n', ' ').replace('\n', ' ')[0:30])
                    continue
                weibo_list.append((element['mid'], time_soup[0].get_text(), int(forward), int(comment), int(praise),
                                   content_soup[0].get_text().strip().replace('\r\n', ' ').replace('\n', ' ')))
    return weibo_list


def extract_bowen_from_directory(dir_path, result_saved_file_path, year):
    """从给定目录下的文件中提取微博博文数据"""
    with open(result_saved_file_path, mode='w', encoding='gbk', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(('keyword', 'mid', 'time', 'forward', 'comment', 'praise', 'file'))
        for sub_dir_name in os.listdir(dir_path):
        # for sub_dir_name in ['波茨坦公告', '开罗宣言', '联合国海洋法公约', '南极条约', '北极理事会', '国际海事组织', '国际海洋法法庭', '东海大陆架', '领海基线', '南海岛礁',
        #                 '南海地图', '专属经济区', '北极', '公海', '南极', '搁置争议', '南海各方行为宣言', '南海宣言', '一带一路', '钓鱼岛', '钓鱼岛国有化', '钓鱼岛争端',
        #                 '黄岩岛事件', '南海仲裁案', '南海', '北海舰队', '东海舰队', '海军', '航空母舰', '护卫舰', '辽宁号', '南海舰队', '潜艇', '驱逐舰', '三大舰队', '巡洋舰', '中国海军',
        #                 '东海军演', '海军演习', '黄海军演', '南海军演', '亚丁湾护航', '港口法', '海岛保护法', '海洋环境保护法', '海域使用管理法', '渔业法', '保护海洋',
        #                 '海砂', '红珊瑚', '国家海洋局', '国家海洋信息中心', '海事局', '海洋局', '海洋环境保护', '海域使用论证', '海域使用权']:
            print(sub_dir_name)
            # one_row = [sub_dir_name]
            for file_name in os.listdir(dir_path+'/'+sub_dir_name):
                if not file_name.endswith('.html'):
                    continue
                if year == 2016:
                    weibo_list = extract_bowen_2016_from_html_file(dir_path+'/'+sub_dir_name+'/'+file_name)
                if year == 2018:
                    weibo_list = extract_bowen_2018_from_html_file(dir_path+'/'+sub_dir_name+'/'+file_name)
                for weibo in weibo_list:
                    one_row = [sub_dir_name]
                    one_row.extend(weibo[0:5])
                    one_row.append(weibo[6])
                    writer.writerow(one_row)
                    # one_row.append('[mid='+str(weibo[0])+',time='+str(weibo[1])+', forward='+str(weibo[2])+', comment='+str(weibo[3])+',praise='+str(weibo[4])+']'+weibo[5])
                    # one_row.append('[' + str(weibo[1])+']'+ weibo[5])
            # writer.writerow(one_row)


if __name__=='__main__':
    dir_path = 'C:/Users/luopc/Desktop/hyys_2016_2018/weibo/2018/热门'
    result_saved_file_path =  'C:/Users/luopc/Desktop/hyys_2016_2018/weibo/2018/2018_热门.csv'
    extract_bowen_from_directory(dir_path, result_saved_file_path, 2018)
