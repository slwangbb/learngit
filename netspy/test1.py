import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BaiDuwenku:
    def __init__(self,url):
        self.options = self.set_options()
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver,10)
        self.url = url


    def set_options(self):
        options = Options()
        options.add_argument('Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')
        #手机端,用电脑端爬不到不懂是什么鬼
        options.add_argument('--headless')
        #无界面模式
        return options


    def find_content(self):
        self.driver.get(self.url)
        target = self.wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="html-reader-go-more"]'
        ))) #继续阅读按钮所在区域
        time.sleep(2)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)#滑动滚动条到按钮所在位置

        Butt = self.wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="html-reader-go-more"]/div[2]/span/span[2]'
        )))
        Butt.click() #点击继续阅读
        time.sleep(1)

        html = self.driver.page_source #得到网页源码
        return html


    def get_content(self,html): #爬内容
        htmls = etree.HTML(html)
        contents = htmls.xpath('//div[@class="ie-fix"]/p') #P标签下面的文章
        content= '>>>>'
        for i in range(len(contents)):
            for j in contents[i].text:
                content = content + j #拼接内容
        self.save_content(content) #保存内容
        time.sleep(2)
        self.driver.quit() #driver关闭

    def save_content(self,fincontent):
        with open('G:/paphotos/单片机.txt','w',encoding='utf-8') as f:
            f.write(fincontent)

if __name__ == '__main__':
    pa = BaiDuwenku('https://wenku.baidu.com/view/be5ba864804d2b160b4ec0aa.html?sxts=1535076562903')
    html = pa.find_content()
    pa.get_content(html)
