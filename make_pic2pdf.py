#导入外部函数库
#注意PIL在安装时是pip install pillow
import os 
import string
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import sys
 
def file_name(file_dir, suffix = ".jpg"):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == suffix:
                L.append(os.path.join(root, file))
    #os.path.split分离路径和文件名，splitext分离文件名前后缀内容
    #用key=lambda定义排序函数
    L.sort(key=lambda x:int(os.path.splitext(os.path.split(x)[1])[0]))
    return L
 
def conpdf(f_pdf , filedir, suffix):
    (w, h) = landscape(A4)
    c = canvas.Canvas(f_pdf, pagesize = landscape(A4))
    fileList = file_name(filedir, suffix)

    for f in fileList:
        (xsize, ysize) = Image.open(f).size

        ratx = xsize / w
        raty = ysize / h
        ratxy = xsize / (1.0 * ysize)
        if ratx > 1:
            ratx = 0.99
        if raty > 1:
            raty = 0.99
        rat = ratx
        if ratx < raty:
            rat = raty

        widthx = w * rat
        widthy = h * rat
        widthx = widthy * ratxy
        posx = (w - widthx) / 2
        if posx < 0:
            posx = 0
        posy = (h - widthy) / 2
        if posy < 0:
            pos = 0 

        c.drawImage(f, posx, posy, widthx, widthy)
        c.showPage()
        print(f)
                
    c.save()
    print('Image to pdf success!')

if __name__ == '__main__':
    conpdf("E:\\汪圣利\\python\\ppt\\test.pdf", "E:\\汪圣利\\python\\ppt", ".jpg")
