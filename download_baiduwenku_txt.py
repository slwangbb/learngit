#本函数用于从百度文库下载text文档
#作者：WANG Shengli
#时间：2018年9月16日
#版本：Ver1.0

#导入外部函数库
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import re


#定义要处理网页和搜索的关键字
url =  'https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html'
chrome_path = 'C:\常用软件\chromedriver.exe'
search_key1 = 'foldpagewg-root'
search_key11 = 'foldpagewg-text'
search_key2 = 'pagerwg-root'
search_key21 = 'pagerwg-button'
search_key3 = 'content singlePage wk-container'


options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
driver = webdriver.Chrome(executable_path=chrome_path ,options=options )
driver.get(url)
sleep(5)
openflag = 1

while openflag!= 0:
    try:
        page = driver.find_element_by_xpath("//div[@class='%s']"%search_key1)
        driver.execute_script('arguments[0].scrollIntoView();', page)
        page = driver.find_element_by_xpath("//div[@class='%s']"%search_key11)
        page.click()
        print(openflag)
        openflag=openflag+1
        sleep(2)
    except:
        try:
           page = driver.find_element_by_xpath("//div[@class='%s']"%search_key2)
           driver.execute_script('arguments[0].scrollIntoView();', page)
           page = driver.find_element_by_xpath("//div[@class='%s']"%search_key21)
           page.click()
           print(openflag)
           openflag=openflag+1
           sleep(2)
        except:
            print('Search2 failed !')
            print('Search1 Failed')
            openflag=0
    
#将网页转换为可解析的结构
html = driver.page_source        
bf = BeautifulSoup(html,'lxml')
#获得网页的题目
title = bf.title.string
filename = title+'.txt'
#获得网页的文本
texts_list = []
result = bf.find_all('div',class_='%s'%search_key3)
for each_result in result:
    bf_tmp = BeautifulSoup(str(each_result),'html.parser')
    texts_list.append(bf_tmp.get_text())

#用正则表达式将列表用空格合转换成换行符
#用len(texts_list)看list的大小,用join函数可以将list转换为字符串
texts_list = re.sub(r'\s+','\r\n',' '.join(texts_list))
try:
    f = open(filename,'w',encoding='utf-8')
    f.writelines(texts_list)
    f.write('\n\n')
    f.close()
    print('write %s successfully'%filename)
except:
    print('Open file failed!')


        
