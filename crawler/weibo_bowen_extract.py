from bs4 import BeautifulSoup
import os
import csv


def read_str(file, encoding='utf-8', errors='ignore'):
    """从文件中读取数据"""
    file = open(file, 'r', encoding=encoding)
    data = file.read()
    file.close()
    return data


def extract_bowen_from_html_file(file_path):
    """从html文件中提取博文数据"""
    data = read_str(file_path)
    soup = BeautifulSoup(data, 'html.parser')
    weibo_list = []
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
                          content_soup[0].get_text().strip()))
    return weibo_list


def extract_bowen_from_directory(dir_path, result_saved_file_path):
    """从给定目录下的文件中提取微博博文数据"""
    with open(result_saved_file_path, mode='w', encoding='utf-8', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(('mid', 'time', 'forward', 'comment', 'praise', 'content'))
        for file_name in os.listdir(dir_path):
            print(file_name)
            weibo_list = extract_bowen_from_html_file(os.path.join(dir_path, file_name))
            for weibo in weibo_list:
                writer.writerow(weibo)


if __name__=='__main__':
    dir_path = 'C:/Users/luopc/Desktop/crawler_data/crawler_data/南海'
    result_saved_file_path =  'C:/Users/luopc/Desktop/crawler_data/crawler_data/南海.csv'
    extract_bowen_from_directory(dir_path, result_saved_file_path)
