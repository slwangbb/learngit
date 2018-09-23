#导入外部函数库
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pdfkit
import os

#定义要处理网页、浏览器位置、存储路径
url =  'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
chrome_path = 'C:\常用软件\chromedriver.exe'

#打开浏览器，浏览网页
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=chrome_path)
driver.get(url)
sleep(5)

#读取网页和域名
domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
html = driver.page_source
bf = BeautifulSoup(html,'lxml')
pdf_name = bf.title.string+'.pdf'

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

#定义html模板
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

#读取每个链接的内容，并保存相应网页
htmls = []
h_idx = 0
for webpage in L:
    h_idx = h_idx+1
    url = webpage
    driver.get(url)
    html = driver.page_source
    bf = BeautifulSoup(html,'lxml')
    result = bf.find_all(class_='x-wiki-content x-main-content')
    body = result[0]
    
#修改网页的正文部分，加入标题，居中显示
    title = bf.find('h4').get_text()
    center_tag = bf.new_tag("center")
    title_tag = bf.new_tag('h1')
    title_tag.string = title
    center_tag.insert(1,title_tag)
    body.insert(1,center_tag)
    bf_tmp = BeautifulSoup(str(body),'html.parser')
    images = bf_tmp.find_all('img')
    for each_image in images:
        each_image['src']=each_image['data-src']
    html = str(bf_tmp)

#将修改后正文部分变成完整网页
    html = html_template.format(content=html)

#将修改后的网页保存为html文件
    f_name = ".".join([str(h_idx),"html"])
    f=open(f_name,'wb')
    f.write(html.encode())
    f.close()
    print('save %s successfully !'%f_name)
    htmls.append(f_name)
    
#将html文件存储为PDF文件
path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
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
config = pdfkit.configuration(wkhtmltopdf = path_wk)
pdfkit.from_file(htmls, pdf_name, options=options,configuration = config)
print('%s generated successfully !'%pdf_name)
for each_html in htmls:
    os.remove(each_html)
