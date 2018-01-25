#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 0025 9:48
# @Author  : Nan.Liu
# @Contact : 153011784@qq.com
# @File    : wjbk.py
# @Software: PyCharm
# @Desc    :
import bs4
import urllib
import time
import requests



'''
根据以下规则，continue_crawl 应该返回 True 或 False： 
如果 search_history 中最近的文章是目标文章，则应停止搜索，函数应返回 False 
如果列表中有 25 个 url，函数应返回 False 
如果列表中有一个循环，函数应返回 False 否则应继续搜索，函数应返回 True。
'''


def continue_crawl(search_history, target_url, max_step=25):
    if search_history[-1] == target_url:
        print("最后一条记录就是" + target_url)
        return False
    elif target_url in search_history[:-1]:
        print("target_url 在之前的列表中")
        return True
    elif len(search_history) > max_step:
        print("search_history 长度大于{}".format(max_step))
        return False
    else:
        return True

def find_first_link(url):
    '''
    发出请求
    :param url:
    :return:
    '''
    response = requests.get(url)
    #解析
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    content_div = soup.find(id='mw-content-text').find(class_='mw-parser-output',recursive=False)
    article_link = None
    for elemenet in content_div.find_all('p',recursive=False):
        if elemenet.find('a',recursive=False):
            article_link= elemenet.find('a',recursive=False).get('href')
            break

    if not article_link:
        return

    first_link= urllib.parse.urljoin('https://en.wikipedia.org/',article_link)

    return first_link;



start_url = "https://en.wikipedia.org/wiki/Special:Random"
# start_url = "https://en.wikipedia.org/wiki/A.J.W._McNeilly"
target_url = "https://en.wikipedia.org/wiki/Philosophy"

article_chain = [start_url]
# find_first_link(article_chain[-1])
while continue_crawl(article_chain, target_url):
    print(article_chain[-1])

    first_link = find_first_link(article_chain[-1])

    if not first_link:
        print("空连接",first_link)
        break;
    article_chain.append(first_link)
    time.sleep(3)
