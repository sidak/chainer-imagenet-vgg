#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chainer import Variable, FunctionSet
import chainer.functions as F


class VGGNet(FunctionSet):

    """
    VGGNet
    - It takes (224, 224, 3) sized image as imput
    """

    def __init__(self):
        super(VGGNet, self).__init__(
            conv1_1=F.Convolution2D(3, 64, 3, stride=1, pad=1),
            conv1_2=F.Convolution2D(64, 64, 3, stride=1, pad=1),

            conv2_1=F.Convolution2D(64, 128, 3, stride=1, pad=1),
            conv2_2=F.Convolution2D(128, 128, 3, stride=1, pad=1),

            conv3_1=F.Convolution2D(128, 256, 3, stride=1, pad=1),
            conv3_2=F.Convolution2D(256, 256, 3, stride=1, pad=1),
            conv3_3=F.Convolution2D(256, 256, 3, stride=1, pad=1),

            conv4_1=F.Convolution2D(256, 512, 3, stride=1, pad=1),
            conv4_2=F.Convolution2D(512, 512, 3, stride=1, pad=1),
            conv4_3=F.Convolution2D(512, 512, 3, stride=1, pad=1),

            conv5_1=F.Convolution2D(512, 512, 3, stride=1, pad=1),
            conv5_2=F.Convolution2D(512, 512, 3, stride=1, pad=1),
            conv5_3=F.Convolution2D(512, 512, 3, stride=1, pad=1),

            fc6=F.Linear(25088, 4096),
            fc7=F.Linear(4096, 4096),
            fc8=F.Linear(4096, 1000)
        )

    def forward(self, x_data, y_data, train=True):
        x = Variable(x_data, volatile=not train)
        t = Variable(y_data, volatile=not train)

        h = F.relu(self.conv1_1(x))
        h = F.relu(self.conv1_2(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv2_1(h))
        h = F.relu(self.conv2_2(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv3_1(h))
        h = F.relu(self.conv3_2(h))
        h = F.relu(self.conv3_3(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv4_1(h))
        h = F.relu(self.conv4_2(h))
        h = F.relu(self.conv4_3(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv5_1(h))
        h = F.relu(self.conv5_2(h))
        h = F.relu(self.conv5_3(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.dropout(F.relu(self.fc6(h)), train=train, ratio=0.5)
        h = F.dropout(F.relu(self.fc7(h)), train=train, ratio=0.5)
        h = self.fc8(h)
        h = F.softmax(h)

        if train:
            return F.softmax_cross_entropy(h, t), F.accuracy(h, t), h
        else:
            return h
