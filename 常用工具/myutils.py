import json
import re
import os

cmt_pat = re.compile("//.*")  # 去掉注释用的
empty_pat = re.compile(",[\s]*}")
# blank_pat = re.compile("[\s]")
fh_pat = re.compile(";")


#  读取JS数据信息 JS文件格式为 XXX = {}
#  可以把字典变量解析为python格式的 只需特殊处理 null false true即可
#  只解析一个
#  但需要注意的是  不能存在依赖 否则无法解析依赖函数 最好全是字符串和基本类型
class JSdata:
    def __init__(self, path, fname=None):
        self.data = None
        self.name = None
        self.path = path
        self.fname = fname
        if fname is not None:
            self.read_from_js(fname)

    def read_from_js(self, fname):
        self.fname = fname
        org_s = ''
        with open(os.path.join(self.path, fname), encoding='utf-8') as f:
            s = f.read()
            org_s = s
            s = cmt_pat.sub("", s)
            s = s.replace('\n', '')
            s = empty_pat.sub("}", s)
            s = fh_pat.sub("", s)
            # s = s.replace("\t", "")
        pos = s.find("=")
        true = True
        false = False
        null = None
        try:
            self.data = eval(s[pos + 1:])
        except Exception as e:
            return False
        self.name = s[:pos]
        return True

    # 把data写进去 然后存文件
    def write_template(self, rep=[], add_floor=False, data=None, ignore=False):  # rep： 模板字典 预设内容
        for k in rep:
            if k in self.data:
                self.data[k] = rep[k]
        if add_floor:
            self.add_floorId()
        self.set_floor(data)
        self.save_to_js(self.data["floorId"], ignore)
        return self.data["floorId"]  # 这个信息要写到data.js里用于更新

    def add_floorId(self):
        last_id = self.data["name"]
        new_id = str(int(last_id) + 1)
        self.data['floorId'] = self.data['floorId'].replace(last_id, new_id)
        self.data['title'] = self.data['title'].replace(last_id, new_id)
        self.data['name'] = new_id
        print(last_id, self.data["floorId"])
        self.name = self.name.replace(last_id, new_id)

    def set_floor(self, data=None):
        for x in range(len(self.data["map"])):
            for y in range(len(self.data["map"][x])):
                it = self.data["map"][x][y]
                if it == 87:  # 上楼梯 改成下楼梯口
                    self.data["map"][x][y] = 88
                else:
                    # 暂时清空 以后决定要不要自动生成墙怪
                    self.data["map"][x][y] = data[x][y]

    def save_to_js(self, fname=None, ignore=True):
        if fname is None:
            fname = self.fname
        s = self.name + ' = \n' + json.dumps(self.data, ensure_ascii=False)
        if fname[-3:] != '.js':
            fname += '.js'
        fname = os.path.join(self.path, fname)
        if os.path.isfile(fname) and not ignore:
            print(fname, '已经存在，是否覆盖？')
            if input() != 'y':
                return
        print('写入', fname)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(s)

    def __getitem__(self, i):
        return self.data[str(i)]

    def __setitem__(self, i, v):
        self.data[str(i)] = v

    def __delitem__(self, i):
        del self.data[i]


# image
from PIL import Image


def print_img(im):
    from matplotlib import pyplot as plt
    plt.imshow(im)
    plt.show()
    input()

class Imagedata:
    def __init__(self, path, size):
        """
        :param path: 图片路径
        :param size: 图元尺寸
        """
        self.path = path
        self.size = size
        self.img = Image.open(path)
        self.isVertical = True  # 适用于纵向图片

    def swap(self, idx1, idx2):
        """
        交换两个图元的位置
        :return:
        """
        if idx2 > idx1: idx1, idx2 = idx2, idx1
        img = self.img
        toImage = Image.new(self.img.mode, (self.img.width, self.img.height))
        num = self.size[1]
        pos1 = idx1 * num
        pos2 = idx2 * num
        if pos1 != 0:
            toImage.paste(img.crop((0, 0, img.width, pos1)), (0, 0))
        toImage.paste(img.crop((0, pos1 + num, img.width, pos2)), (0, pos1 + num))
        toImage.paste(img.crop((0, pos2 + num, img.width, img.height)), (0, pos2 + num))
        toImage.paste(img.crop((0, pos1, img.width, pos1 + num)), (0, pos2))
        toImage.paste(img.crop((0, pos2, img.width, pos2 + num)), (0, pos1))
        self.img = toImage
        return toImage

    def split_images(self, config=None):
        """
        分割图片
        :param config:
        :return:
        """
        config = config or {}
        ret = []
        img = self.img
        w, h = img.size
        dw, dh = self.size
        if 'width' in config:
            dw = config['width']
        if 'height' in config:
            dh = config['height']

        for ch in range(0, h, dh):
            new_image = Image.new(img.mode, (dw, dh))
            new_image.paste(img.crop((0, ch, dw, dh + ch)), (0, 0))
            ret.append(new_image)
        return ret

    def fill_blank(self, idx):
        pos = idx * self.size[1]
        num = self.size[1]
        toImage = Image.new(self.img.mode, (self.img.width, self.img.height))
        img = self.img
        if idx != 0:
            toImage.paste(img.crop((0, 0, img.width, pos)), (0, 0))
        toImage.paste(img.crop((0, pos + num, img.width, img.height)), (0, pos + num))
        self.img = toImage

    def is_blank(self, idx):
        img = self.img.crop((0, self.size[1]*idx, self.size[0], self.size[1]*(idx+1)))
        img = img.convert('RGB')
        clrs = img.getcolors(img.size[0]*img.size[1])
        if clrs is None or len(clrs) <= 1:
            return False
        return True

    # 去重 返回重复的下标
    def filter_same(self):
        from hashlib import md5
        import numpy as np
        imgs = self.split_images()
        hash_list = [md5(np.array(imgs[i])).hexdigest() for i in range(len(imgs))]
        hash_table = {}
        ret = []
        for idx in range(len(hash_list)):
            h = hash_list[idx]
            if h in hash_table:
                self.fill_blank(idx)
                ret.append(idx)
                continue
            hash_table[h] = idx
        return ret

    # 去除空白的图
    def filter_blank(self):
        idx = [i for i in range(int(self.img.size[1] / self.size[1])) if not self.is_blank(i)]
        return idx



    def save(self, fname=None):
        fname = fname or self.path
        self.img.save(fname)



from torch.utils.data import Dataset
import torchvision.transforms as transforms

labelName = []
blockInfo = []

# 返回有label的下标与标签编号0~n
def get_labels(iconData, enemyData):
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
    def __init__(self, imgs, labels, index, mode='train', transform=None):  # 初始化一些需要传入的参数
        self.mode = mode
        self.imgs = imgs
        self.train_index = index
        self.label = labels
        self.transform = transform
        self.test_index = [i for i in range(len(self.imgs)) if i not in self.train_index]
        print(len(self.train_index), self.train_index)


    def __getitem__(self, index):
        t_idx = self.train_index if self.mode == 'train' else self.test_index
        img = self.imgs[t_idx[index]].convert('RGB')  # fn是图片path #fn和label分别获得imgs[index]也即是刚才每行中word[0]和word[1]的信息
        label = self.label[index] if self.mode == 'train' else index

        if self.transform:
            img = self.transform(img)
        return img, label  # return很关键，return回哪些内容，那么我们在训练时循环读取每个batch时，就能获得哪些内容

        from matplotlib import pyplot as plt
        plt.imshow(img)
        plt.show()
        print(img, label)
        q = ''
        while q != 'q':
            q = input()
            try:
                print(eval(q))
            except:
                pass

    def __len__(self):  # 这个函数也必须要写，它返回的是数据集的长度，也就是多少张图片，要和loader的长度作区分
        if self.mode == 'train':
            return len(self.train_index)
        else:
            return len(self.test_index)


if __name__ == '__main__':
    im = Imagedata('../project/images/enemys.png', (64, 32))
    import matplotlib.pyplot as plt
    print(im.filter_blank())