# 图像聚类： 将怪物图片自适应分配类型 并保存索引
from aluxiry import MyDataset
import numpy as np
from PIL import Image

import matplotlib.pyplot as plt


def filter_empty(im):
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    num = 0
    empty_num = 0
    for x in range(width):
        for y in range(height):
            p = pix[x, y]
            num += 1
            if len(p)>2 and p[3] == 0:
                empty_num += 1
    if num - empty_num < 10:
        return True
    else:
        return False

def calcu_avgrgb(im):
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    val = [0 for _ in range(len(pix[0, 0]))]
    num = 0
    # print(pix[0,0])
    for x in range(width):
        for y in range(height):
            num += 1
            p = pix[x, y]
            if len(p)>2 and p[3] == 0:
                continue
            for i in range(len(p)):
                val[i] += p[i]
    for i in range(len(val)):
        val[i] /= num

    return val

def agg_imgs(imgdata, n, labels, width=32, height=32):
    imgs = [None for i in range(n)]
    for i in range(len(labels)):
        t = labels[i]
        y = 0
        if imgs[t] is None:
            imgs[t] = Image.new(imgdata[0].mode, (width, height))
        else:
            newimg = Image.new(imgs[t].mode, (imgs[t].size[0], imgs[t].size[1]+height))
            y = imgs[t].size[1]
            newimg.paste(imgs[t], (0, 0))
            imgs[t] = newimg
        imgs[t].paste(imgdata[i], (0, y))

    for i in range(len(imgs)):
        imgs[i].save('tmp/'+str(i)+'.png')
        # plt.imshow(img)
        # plt.show()
        # input()


config = {
    'alpha': True,
    'width': 64,
    'height': 32,
}
from aluxiry import split_images
# 扩张
def expand_image(img, destW, destH):
    w,h = img.size
    newImg = Image.new(img.mode, (destW, destH))
    for x in range(0, destW, w):
        for y in range(0, destH, h):
            newImg.paste(img, (x, y))
    ##import matplotlib.pyplot as plt
    #plt.imshow(img)
    #plt.show()
   # input()

    return newImg




# 制作GAN所需的原始数据集 大小3*128*128 用单图反复生成 标签用聚类结果生成 共计n个标签种类
def make_data(datapath='tmp/srcdata', outpath='tmp/gandata'):
    import glob
    import pandas as pd
    files = glob.glob(datapath+'/*.png')
    file = files[0]
    idx = 0
    labels_fname = {}
    file_names = []
    for f in files:
        imgs = split_images(fname=f, config=config)
        tmp = []
        for im in imgs:
            name1 = str(idx)+'.png'
            name2 = str(idx+1)+'.png'
            tmp.append(name1)
            tmp.append(name2)
            im = im.resize((im.size[0] * 4, im.size[1] * 4))
            im.crop((0,0,128,128)).save(outpath+'/'+name1)
            im.crop((128,0,256,128)).save(outpath+'/'+name2)
            # expand_image(im.resize((im.size[0] * 2, im.size[1] * 2)), 128, 128)
            idx += 2
        file_names += tmp
        label = f.split('\\')[-1].split('.')[-2]
        labels_fname[label] = tmp

    df = pd.DataFrame(np.zeros((len(file_names), len(labels_fname)), dtype=np.int), columns=list(labels_fname.keys()),
                      index=file_names)  # 创建一个数据表格

    for l in labels_fname:
        for f in labels_fname[l]:
            df[l][f] = 1
    df.to_csv(outpath + '/data.txt', sep=' ')


# 聚类 得到的结果存到tmp
def cluster_images():
    data = MyDataset(imgConfig=config)
    # 如何取特征很关键
    # X = [np.array(i).flatten() for i in data.imgs]
    filt_images = [im for im in data.imgs if not filter_empty(im)]
    filt_rgbdata = [calcu_avgrgb(im) for im in filt_images]

    print('img num:', len(filt_rgbdata))
    from sklearn.cluster import KMeans

    n_cluster = 15
    kmeans_model = KMeans(n_clusters=n_cluster, random_state=1).fit(filt_rgbdata)
    labels = kmeans_model.labels_
    print(labels)
    agg_imgs(filt_images, n_cluster, labels, config['width'], config['height'])



if __name__ == '__main__':
    make_data()
