import cv2
import numpy
import pytesseract
import Mod as mod
from PIL import Image
def main1():

    img = cv2.imread('2.jpg', cv2.COLOR_BGR2GRAY)
    height, width = img.shape[:2]
    # resized = cv2.resize(img, (3*width,3*height), interpolation=cv2.INTER_CUBIC)
    #二值化
    (_, thresh) = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    #cv2.imshow('thresh', thresh)
    #扩大黑色面积，使效果更明显
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))#形态学处理，定义矩形结构
    closed = cv2.erode(thresh, None, iterations = 5)
    # cv2.imshow('erode',closed)
    height, width = closed.shape[:2]
    v = [0]*width
    z = [0]*height

    #水平投影
    #统计每一行的黑点数
    a = 0
    emptyImage1 = numpy.zeros((height, width, 3), numpy.uint8)
    for y in range(0, height):
        for x in range(0, width):
            if closed[y,x][0] == 0:
                a = a + 1
            else :
                continue
        z[y] = a
        a = 0
    l = len(z)
    #绘制水平投影图

    listY = []
    for y in range(0,height):
        for x in range(0, z[y]):
            listY.append(y)


    listY = mod.Duplicate_removal(listY)
    listY = mod.continuity(listY)
    listY = mod.lxyz(listY,75)

    cropImg = img[0:45, 1080:87]

    listXY = []

    for i in listY:
        # 画一个绿色边框的矩形，参数2：左上角坐标，参数3：右下角坐标
        cv2.rectangle(img, (0, int(i.split('-')[0])), (width, int(i.split('-')[1])), (0, 255, 0), 3)
        listXY.append([(0, int(i.split('-')[0])), (width, int(i.split('-')[1]))])


    cv2.namedWindow('shuipin',cv2.WINDOW_NORMAL)
    cv2.imshow('shuipin', img)
    cv2.waitKey(0)
    return listXY



list = main1()

import matplotlib.pyplot as plt

img = Image.open('3.jpg')

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

for i in range(len(list)):
    region = img.crop((list[i][0][0], list[i][0][1], list[i][1][0], list[i][1][1]))
    # region.save('baidu\\'+str(i)+'.jpg')
    # print(mod.img_to_str('baidu\\' + str(i) + '.jpg'))
    print(i,'-------------------------------')
    try:
        text = pytesseract.image_to_string((region), lang='chi_sim')
        print(text)
    except:
        print('')

    plt.figure(str(i))
    plt.imshow(region)
    plt.show()