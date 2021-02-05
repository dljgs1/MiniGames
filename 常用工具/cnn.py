import torch
import torch.nn as nn
import torch.nn.functional as F
class Net(nn.Module):
    def __init__(self, num):
        super(Net, self).__init__()  # 调用Net父类（nn.Module）的__init__()方法
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(3, 6, 5)  # 表
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

def train(net, dataset, n_epoch=10):
    trainloader = dataset
    import torch.optim as optim
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(n_epoch):  # 一个epoch说明用所用数据进行训练一次
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            #特征向量和标签
            # 由于batch是4，因此input是4*C*W*H的tensor
            # label是一个1*4的tensor
            inputs, labels = data
            # print('input', inputs, labels)
            # zero the parameter gradients
            optimizer.zero_grad()
            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
        #   if i % 2000 == 1999:    # print every 2000 mini-batches
        # 每个mini-batch的大小之前在trainloader里面有设置过
        print('[%d, %5d] loss: %.3f' %
              (epoch + 1, i + 1, running_loss / 2000))
        running_loss = 0.0

    print('Finished Training')

def test(net, testloader, fn=None):
    correct = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data  # label指的是在类里面的下标
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            if fn is not None:
                fn(labels, predicted)
            # 找出第一维的最大值，predicted里面保存的是下标
            #total += labels.size(0) # 因为是minibatch，所以一组里面有很多个数据
            #correct += (predicted == labels).sum().item()

    #print('Accuracy of the network on the 10000 test images: %d %%' % (
     #       100 * correct / total))



from torch.utils.data import Dataset
import torchvision.transforms as transforms

def get_transform():
    return transforms.Compose(
        [transforms.ToTensor(),  # [0,256]-[0-1]
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

def train_with_default(net, train_data, n_epoch=10):
    trainloader = torch.utils.data.DataLoader(train_data, batch_size=4,
                                              shuffle=True, num_workers=0)
    import torch.optim as optim
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    for epoch in range(n_epoch):  # 一个epoch说明用所用数据进行训练一次
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            #特征向量和标签
            # 由于batch是4，因此input是4*C*W*H的tensor
            # label是一个1*4的tensor
            inputs, labels = data
            # print('input', inputs, labels)
            # zero the parameter gradients
            optimizer.zero_grad()
            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
        print('[%d, %5d] loss: %.3f' %
              (epoch + 1, i + 1, running_loss / 2000))

    print('Finished Training')

def test_with_default(net, test_dataset, fn=None):
    testloader = torch.utils.data.DataLoader(test_dataset, batch_size=4,
                                              shuffle=True, num_workers=0)
    with torch.no_grad():
        for data in testloader:
            images, labels = data  # label指的是在类里面的下标
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            if fn is not None:
                fn(labels, predicted)