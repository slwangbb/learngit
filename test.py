#在https://wkhtmltopdf.org/downloads.html下载wkhtmltopdf 进行安装
#安装完成之后把该程序的执行路径加入到系统环境 $PATH 变量中

# coding=utf-8
from __future__ import unicode_literals
import logging
import os
import time
import re

try:
    from urllib.parse import urlparse  #py3
except:
    from urlparse import urlparse #py2

import pdfkit
import requests
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""


"""
爬虫基类，所有的爬虫都应该继承此类
"""
class Crawler(object):
    name = None
    """
    初始化
    :param name:保存的PDF文件名，不需要后缀名
    :param  start_url:爬虫入口URL
    """
    def __init__(self, name, start_url):
        self.name = name
        self.start_url = start_url
        self.domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.start_url))
        """
        urlparse(self.start_url)会返回scheme、netloc、path、params、query、fragment六个参数
        self.domain得到网址的域名
        """
    def crawl(self, url):
        print(url)
        response = requests.get(url)
        return response

    """
    解析目录结构，获取所有URL目录列表，由子类实现
    ：param response 爬虫返回的response对象
    ：return url 可迭代对象（iterable）列表，生成器，元组都可以
    """
    def parse_menu(self, response):
        raise NotImplementedError

    """
    解析正文，由子类实现
    ：param response：爬虫返回的response对象
    ：return 返回经过处理的html文本
    """
    def parse_body(self, response):
        raise NotImplementedError

    def run(self):
        start = time.time()
        # options 设置PDF格式
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
        #将menu对应的html解析出来，保存为html文件
        htmls = []
        for index,url in enumerate(self.parse_menu(self.crawl(self.start_url))):
            html = self.parse_body(self.crawl(url))
            f_name = ".".join([str(index),"html"])
            with open(f_name,'wb') as f:
                f.write(html)
            htmls.append(f_name)

        pdfkit.from_file(htmls, self.name+".pdf", options=options)
        for html in htmls:
            os.remove(html)
        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time)
"""
子类：爬虫廖雪峰的Python3教程
"""
class LiaoXueFengPythonCrawler(Crawler): #括号，表示继承
    """
    完善目录解析函数,获取所有URL目录列表
    ：param response 爬虫返回的response对象
    ：return url生成器

    """
    def parse_menu(self, response):
        soup = BeautifulSoup(response.content, "html.parser")
        menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
        for li in menu_tag.find_all("li"):
            url = li.a.get("href")
            if not url.startswith("http"):
                url = "".join([self.domain, url])    #补全为全路径
            yield url

    """
    完善正文解析函数，
    ：param response：爬虫返回的response对象
    ：return 返回处理后的html文本
    """
    def parse_body(self, response):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.find_all(class_="x-wiki-content")[0]

            #加入标题，居中显示
            title = soup.find('h4').get_text()
            center_tag = soup.new_tag("center")
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1,title_tag)
            body.insert(1,center_tag)

            html = str(body)

            #body中的img标签的src相对路径改成绝对路径
            pattern = "(<img .*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(3).startswith("http"):
                    rtn = "".join([m.group(1), self.domain, m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])
            html = re.compile(pattern).sub(func, html)
            html = html_template.format(content=html)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)

if __name__ == '__main__':
    start_url = "http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000"
    crawler = LiaoXueFengPythonCrawler("廖雪峰blogs", start_url)
    crawler.run()
