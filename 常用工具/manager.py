from myutils import JSdata
from myutils import Imagedata


# .convert('RGB')


class Manager:
    def __init__(self):
        self.enemys = JSdata('../project', 'enemys.js')
        self.icons = JSdata('../project', 'icons.js')
        self.maps = JSdata('../project', 'maps.js')
        self.items = JSdata('../project', 'items.js')
        self.enemyImg = Imagedata('../project/images/enemys.png', (32, 32))

    # 批量重命名 比如x宝石之类的
    def rename(self):
        pass

    # 交换两个数据 icons maps ok
    def swap_data(self, cls, id1, id2):
        self.icons[cls][id1], self.icons[cls][id2] = self.icons[cls][id2], self.icons[cls][id1]
        if cls == 'enemys':
            self.enemyImg.swap(self.icons[cls][id2], self.icons[cls][id1])
        # TODO: 物品？

    # !删除某条数据？
    def del_data(self, cls, idx):
        return '地图图块可能混乱 暂时不做'
        idx2id = {str(self.icons[cls][eid]): eid for eid in self.icons[cls]}
        eid = idx2id[str(idx)]
        if cls == 'enemys':
            del self.enemys.data[eid]
        pass

    # 整理敌人数据、把大量不用的(name=新敌人)放到后面 仅限enemys 不含enemy48 ok
    # TODO： 根据已使用的分类训练模型 重新预测新敌人的分类
    def shuffle_enemys(self):
        self.enemyImg.filter_same()
        del_list = self.enemyImg.filter_blank()
        import random
        race_list = ['莱姆', '妖', '魔', '人', '亡灵']
        dels = [eid for eid in self.icons['enemys'] if self.icons['enemys'][eid] in del_list]
        used = [eid for eid in self.icons.data['enemys'] if self.enemys.data[eid]['name'] != '新敌人' and eid not in dels]
        unused = [eid for eid in self.icons.data['enemys'] if eid not in used and eid not in dels]
        for eid in self.enemys.data:
            if 'race' not in self.enemys.data[eid]:
                self.enemys.data[eid]['race'] = race_list[random.randint(0, len(race_list) - 1)]
        used.sort(key=lambda u: race_list.index(self.enemys.data[u]['race']))
        unused.sort(key=lambda u: race_list.index(self.enemys.data[u]['race']))
        sorted_list = used + unused + dels
        org_list = list(self.icons['enemys'].keys())
        org_list.sort(key=lambda u: self.icons.data['enemys'][u])
        print(org_list)
        print(sorted_list)
        for i in range(len(org_list)):
            oid = org_list[i]
            eid = sorted_list[i]
            if eid == oid: continue
            idx = org_list.index(eid)
            org_list[i], org_list[idx] = org_list[idx], org_list[i]
            self.swap_data('enemys', eid, oid)
        self.enemyImg.save()
        self.icons.save_to_js()

    # 宝石图块 连续四个 模板如下
    def create_Jewels(self, idrange):
        levels = ["圆角", "四芒", "大", "五芒", "巨", "宝钻", "宝_晶", "石_环", "宝石_色月华", "残缺", "完美"]
        ratio = [2, 3, 5, 8, 10, 16, 20, 30, 40, 25, 64]
        templates = [
            {"name": "红宝石", "text": '，攻击+${core.values.redJewel*%d}',
             "itemEffect": "core.status.hero.atk += core.values.redJewel * %d",
             "itemEffectTip": "'，攻击+'+core.values.redJewel * %d",
             },
            {"name": "蓝宝石", "text": '，防御+${core.values.redJewel*%d}',
             "itemEffect": "core.status.hero.def += core.values.redJewel * %d",
             "itemEffectTip": "'，防御+'+core.values.blueJewel * %d",
             },
            {"name": "绿宝石", "text": '，魔防+${core.values.redJewel*%d}',
             "itemEffect": "core.status.hero.mdef += core.values.redJewel * %d",
             "itemEffectTip": "'，魔防+'+core.values.greenJewel * %d",
             },
            {"name": "黄宝石", "text": "'，全属性提升'",
             "itemEffect": "var tmp = %d;core.status.hero.hpmax += 10*tmp;core.status.hero.hp += 100*tmp;core.status.hero.atk += core.values.redJewel * tmp;core.status.hero.def +=  core.values.blueJewel * tmp;core.status.hero.mdef += core.values.greenJewel * tmp;",
             "itemEffectTip": "'，全属性提升'",
             },
        ]
        idx = 0
        for itemid in idrange:
            level = levels[idx]
            name = templates[idx % 4]["name"]
            splt = level.split('_')
            if len(splt) > 1:
                name = name.replace(splt[0], splt[1])
            else:
                name = level+name
            self.items["items"][itemid]["name"] = name
            self.items["itemEffect"][itemid] = templates[idx % 4]["itemEffect"] % (idx + 2)
            self.items["itemEffectTip"][itemid] = templates[idx % 4]["itemEffectTip"] % (idx + 2)

            idx += 1
        self.items.save_to_js()

    # 训练模型并进行预测(枚举类型）
    def train_test_model(self, dtype='enemys', tag='race'):
        from myutils import MyDataset
        imgs = self.enemyImg.split_images(config={'width': 32})  # TODO: 自定义图片
        label_id = {}  # 标签对应的数字
        label_name = []  # 标签数字对应的原始
        labels = []
        train_idx = []
        for eid in self.icons[dtype]:
            idx = self.icons[dtype][eid]
            if self.enemys[eid]['name'] != '新敌人':
                train_idx.append(idx)

            if self.enemys[eid][tag] not in label_id:
                label_id[self.enemys[eid][tag]] = len(label_id)
                label_name.append(self.enemys[eid][tag])
            labels.append(label_id[self.enemys[eid][tag]])

        from cnn import Net, train_with_default, test_with_default, get_transform
        trainData = MyDataset(imgs, labels, train_idx, mode='train', transform=get_transform())
        testData = MyDataset(imgs, labels, train_idx, mode='test', transform=get_transform())
        net = Net(len(label_name))

        train_with_default(net, trainData, n_epoch=10)

        import numpy as np
        id_info_list = sorted(list(self.icons[dtype].keys()), key=lambda k: self.icons[dtype][k])

        data = self.enemys

        def test_fn(index, predict):
            index = np.array(testData.test_index)[index.numpy()]
            predict = predict.numpy()
            for i in range(len(index)):
                data[id_info_list[index[i]]]['race'] = label_name[predict[i]]

        test_with_default(net, testData, test_fn)

        count = {l: 0 for l in label_name}
        for k in self.icons[dtype]:
            count[data[k]['race']] += 1
        print(count)

    def test(self):
        pass


m = Manager()
# for i in m.enemys.data:
#    pass

# m.train_test_model()
# m.shuffle_enemys()
rgs = ["I" + str(i) for i in range(1089, 1133)]
# m.create_Jewels(rgs)
print(rgs)

