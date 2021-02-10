import os
import numpy as np
import torch
import torch.nn as nn

'''搭建模型'''

class Formation_Prediction(nn.Module):
    def __init__(self):
        super(Formation_Prediction, self).__init__()

        self.fnn = nn.Sequential(
            nn.Linear(768, 10),
            nn.ReLU(),
            nn.Linear(10, 1)
        )

    def forward(self, x):
        return self.fnn(x)

