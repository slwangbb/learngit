#导入外部函数库
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urlparse

#定义要处理网页、浏览器位置、存储路径
url =  'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
chrome_path = 'E:\汪圣利\python\chromedriver.exe'

#打开浏览器，浏览网页
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=chrome_path)
driver.get(url)
sleep(5)

#读取网页和域名
domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
html = driver.page_source
bf = BeautifulSoup(html,'lxml')

#把目录链接存储到指定List中
result = bf.find_all('ul',class_='uk-nav uk-nav-side')
bf_tmp = BeautifulSoup(str(result[1]),'html.parser')
link = bf_tmp.find_all(class_='x-wiki-index-item')
x=1
L=[]
for each_link in link:
    print(x)
    url_tmp = each_link.get('href')
    L.append(''.join([domain, url_tmp]))
    x=x+1
