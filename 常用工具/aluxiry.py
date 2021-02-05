#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/3 20:47
# @Author  : hw
# @Site    :
# @File    : towerInfo.py
# @Software: PyCharm
"""
function:
"""


from PIL import Image
import os
from myutils import JSdata
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms

enemyData = JSdata('../project')
iconData = JSdata('../project')
enemyData.read_from_js('enemys.js')
iconData.read_from_js('icons.js')
import matplotlib.pyplot as plt


def split_images(fname, config=None):
    config = config or {}
    ret = []
    img = Image.open(fname)
    if 'alpha' not in config or not config['alpha']:
        img = img.convert("RGB")
    w, h = img.size
    dw = 32
    dh = 32
    if 'width' in config:
        dw = config['width']
    if 'height' in config:
        dh = config['height']

    for ch in range(0, h, dh):
        new_image = Image.new(img.mode, (dw, dh))
        new_image.paste(img.crop((0, ch, dw, dh+ch)), (0, 0))
        #plt.imshow(new_image)
        #plt.show()
        #input()
        ret.append(new_image)

    return ret


labelName = []
blockInfo = []

# 返回有label的下标与标签编号0~n
def get_labels():
    global blockInfo
    ids = ['' for _ in range(len(iconData.data['enemys']))]
    for i in iconData.data['enemys']:
        ids[iconData.data['enemys'][i]] = i
    blockInfo = ids
    index = []
    ret = []
    for i in range(len(ids)):
        eid = ids[i]
        if 'race' in enemyData.data[eid] and enemyData.data[eid]['name'] != '新敌人':
            race = enemyData.data[eid]['race']
            if race not in labelName:
                labelName.append(enemyData.data[eid]['race'])
            index.append(i)
            ret.append(labelName.index(race))
    return index, ret


# enemys.png
class MyDataset(Dataset):  # 创建自己的类：MyDataset,这个类是继承的torch.utils.data.Dataset
    def __init__(self, mode='train', transform=None, target_transform=None, imgConfig=None):  # 初始化一些需要传入的参数
        self.mode = mode
        self.imgs = split_images('../project/images/enemys.png', config=imgConfig)
        self.train_index, self.label = get_labels()
        self.test_index = [i for i in range(len(self.imgs)) if i not in self.train_index]
        self.transform = transform
        self.target_transform = target_transform
        #if mode == 'test':
        #    while True:
        #        try:
        #            print(eval(input()))
        #        except:
        #            pass

    def __getitem__(self, index):
        t_idx = self.train_index if self.mode == 'train' else self.test_index
        img = self.imgs[t_idx[index]]  # fn是图片path #fn和label分别获得imgs[index]也即是刚才每行中word[0]和word[1]的信息
        label = self.label[index] if self.mode == 'train' else index
        # img = Image.open(root + fn).convert('RGB')  # 按照path读入图片from PIL import Image # 按照路径读取图片
        # img = Image.open(fn)#read_floor_data(fn)
        if self.transform is not None:
            img = self.transform(img)  # 是否进行transform

        return img, label  # return很关键，return回哪些内容，那么我们在训练时循环读取每个batch时，就能获得哪些内容

    def __len__(self):  # 这个函数也必须要写，它返回的是数据集的长度，也就是多少张图片，要和loader的长度作区分
        if self.mode == 'train':
            return len(self.train_index)
        else:
            return len(self.test_index)


transform = transforms.Compose(
    [transforms.ToTensor(),  # [0,256]-[0-1]
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
train_data = MyDataset('train', transform=transform)
trainloader = torch.utils.data.DataLoader(train_data, batch_size=4,
                                          shuffle=True, num_workers=0)
test_data = MyDataset('test', transform=transform)
testloader = torch.utils.data.DataLoader(test_data, batch_size=4,
                                         shuffle=True, num_workers=0)

from cnn import Net, train, test
import numpy as np

def test_fn(label, predict):
    label = np.array(test_data.test_index)[label.numpy()]
    predict = predict.numpy()
    for i in range(len(label)):
        enemyData.data[blockInfo[label[i]]]['race'] = labelName[predict[i]]
    print(label, predict)


if __name__ == '__main__':
    net = Net(10)
    train(net, trainloader, 50)
    test(net, testloader, test_fn)
    # torch.save(net.state_dict(), 'model.pt')
    enemyData.save_to_js()
