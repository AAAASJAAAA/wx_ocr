from itertools import groupby
import matplotlib.pylab as plt
def plti(im, **kwargs):

  """
  画图的辅助函数
  """
  plt.imshow(im, interpolation="none", **kwargs)
  plt.axis('off') # 去掉坐标轴
  plt.show() # 弹窗显示图像

def GetCol(im,y):
    im_size = im.size
    pix = im.load()
    list = []
    for x in range(im_size[0]):
        list.append(pix[y, x])
    return list


def Duplicate_removal(listY):
    listY1 = []
    for i in listY:
        if i not in listY1:
            listY1.append(i)
    return listY1

def continuity(lst):
    list = []
    fun = lambda x: x[1]-x[0]
    for k, g in groupby(enumerate(lst), fun):
        l1 = [j for i, j in g]    # 连续数字的列表
        if len(l1) > 1:
            scop = str(min(l1)) + '-' + str(max(l1))    # 将连续数字范围用"-"连接
        else:
            scop = l1[0]
        list.append(scop)
    return list


def lxyz(list,yz):
    list2 = []
    for i in range(len(list)):
        if(len(list) > i+1):
            i0 = int(list[i].split('-')[1])
            i1 = int(list[i+1].split('-')[0])
            i3 = i1 - i0
            if i3 < yz:
                list2.append(list[i].split('-')[0] + '-' + list[i+1].split('-')[1])
                list.remove(list[i])
                list.remove(list[i])
    for i in list2:
        list.append(i)

    return list

from aip import AipOcr

# 新建一个AipOcr对象
config = {
    'appId': '14619918',
    'apiKey': '8oRSd83vxAK59FcSSVSLPXth',
    'secretKey': '6SEPeaLPXbTL7aetN1kg9hr3ZeCpfSrm'
}
client = AipOcr(**config)


# 读取图片
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()

# 识别图片里的文字
def img_to_str(image_path):
    image = get_file_content(image_path)
    # 调用通用文字识别, 图片参数为本地图片
    result = client.basicGeneral(image)
    # 结果拼接返回
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])