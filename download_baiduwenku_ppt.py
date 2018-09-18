#导入外部函数库
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import urllib.request
import os
#导入自建函数库
from make_pic2pdf import conpdf

#定义要处理网页、浏览器位置、存储路径
url =  'https://wenku.baidu.com/view/6e329617580102020740be1e650e52ea5418ce76.html?sxts=1537239654915'
chrome_path = 'E:\汪圣利\python\chromedriver.exe'
path = 'E:\\汪圣利\\python\\'

#打开浏览器，浏览网页
options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
driver = webdriver.Chrome(executable_path=chrome_path ,options=options )
driver.get(url)
sleep(5)

   
#读取网页
html = driver.page_source
bf = BeautifulSoup(html,'lxml')

#建存储网页的目录
path = path+bf.title.string+'\\'
isExists=os.path.exists(path)
if not isExists:
    os.makedirs(path)
    print('make %s successfully !'%path)
else:
    print('%s already exists'%path)
    
#把PPT图片存储到指定目录下
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

#从图片创建成PDF文件，便于浏览和存储   
conpdf(path+bf.title.string+'.pdf',path,'.jpg')        
