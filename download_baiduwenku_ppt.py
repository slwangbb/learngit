#导入外部函数库
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import urllib.request


#定义要处理网页和搜索的关键字
url =  'https://wenku.baidu.com/view/d9bb18d181c758f5f61f67ac.html?from=search'
chrome_path = 'E:\汪圣利\python\chromedriver.exe'
path = 'E:\\汪圣利\\python\\ppt\\'


options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
driver = webdriver.Chrome(executable_path=chrome_path ,options=options )
driver.get(url)
sleep(5)

html = driver.page_source
bf = BeautifulSoup(html,'lxml')
result = bf.find_all('div',class_='ppt-image-wrap')
x=1
for each_result in result:
    bf_tmp = BeautifulSoup(str(each_result),'html.parser')
    image = bf_tmp.find_all('img')
    for each_image in image:
        print(x)
        try:
            urllib.request.urlretrieve(each_image['src'], path+'%s.jpg'%(x))
        except:
            urllib.request.urlretrieve(each_image['data-src'], path+'%s.jpg'%(x))
        x=x+1
         
         
