#! /usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from lxml import etree
import os
import pdfkit

ROOT_URL = "http://www.liujiangblog.com"
INDEX_URL = "http://www.liujiangblog.com/course/django/2"


def get_response(url, retry=0):
    s = requests.Session()
    s.headers.update({
        'user-agent':
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36"
    })
    try:
        return s.get(url, timeout=5)
    except requests.exceptions.RequestException:
        if retry < 3:
            return get_response(url, retry=retry + 1)
        raise


def get_tree(url):
    r = get_response(url)
    return etree.HTML(r.text)


def get_content(url):
    options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
    href_tree = get_tree(url)
    a_list = href_tree.xpath("/html/body/div[1]/div/div[1]/div//a/@href")
    htmls = []
    i=0
    for a_href in a_list:
        a_href = ROOT_URL+a_href
        print(a_href)
        content_tree = get_tree(a_href)
        html=content_tree.xpath("/html/body/div[1]/div/div[2]")[0]
        htmlstr = etree.tostring(html,encoding="utf-8")
        f_name = ".".join([str(i), "html"])
        with open(f_name, 'wb') as f:
            f.write(htmlstr)
        htmls.append(f_name)
        i+=1
        print("已经爬取%s页" % i)
    print("开始将网页html合并为PDF")
    pdfkit.from_file(htmls, '刘江的Django博客' + ".pdf", options=options)
    print("PDF保存成功，文件名为:刘江的Django博客.pdf")
    for html in htmls:
        os.remove(html)
    print("移除临时html文件完毕")
if __name__ == '__main__':

    get_content(INDEX_URL)
