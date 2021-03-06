# Copyright (c) 2022 Raven Stock. email:cquptriven@qq.com

from torch import nn
from abc import abstractmethod


__all__ = ['BaseModel']


class BaseModel(nn.Module):
    def __init__(self, num_classes: int=4, **kwargs):
        super().__init__()
        self.num_classes = num_classes
        
        self._fdim = None

    def build_head(self):
        '''
        Build classification head
        '''
        # self.fc = nn.Sequential(
        #     nn.Flatten(),
        #     nn.Linear(self.fdim, self.num_classes)
        # )
        self.fc = nn.Linear(self.fdim, self.num_classes)
        nn.init.kaiming_normal_(self.fc.weight)
        nn.init.zeros_(self.fc.bias)

    @property
    def fdim(self) -> int:
        return self._fdim

    @abstractmethod
    def get_backbone_parameters(self) -> list:
        return []

    def get_parameters(self):
        parameter_list = self.get_backbone_parameters()
        parameter_list.append({'params': self.fc.parameters(), 'lr_mult':10})
        return parameter_list

    @abstractmethod
    def forward_backbone(self, x):
        return x

    def forward(self, x) -> tuple:
        '''
        return: tuple like (feature, y_pred)
        '''
        feature = self.forward_backbone(x)

        y = self.fc(feature)

        return feature, y