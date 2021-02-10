import data_process
import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import math
import time
import modeling
import numpy as np

def main():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    torch.set_num_threads(1)
    print('----------------------------------Read Data---------------------------------------')
    x_set = np.load('x_set.npy')
    y_set = np.load('y_set.npy')
    seed_1 = np.arange(len(x_set))
    np.random.shuffle(seed_1)
    x_train_set = x_set[seed_1[0: math.floor(0.8 * len(x_set))]]
    y_train_set = y_set[seed_1[0: math.floor(0.8 * len(x_set))]]
    x_val_set = x_set[seed_1[math.floor(0.8 * len(x_set)): len(x_set)]]
    y_val_set = y_set[seed_1[math.floor(0.8 * len(x_set)): len(x_set)]]
    x_train_set = torch.tensor(x_train_set,dtype=torch.float32).cuda()
    y_train_set = torch.tensor(y_train_set,dtype=torch.float32).cuda()
    x_val_set = torch.tensor(x_val_set,dtype=torch.float32).cuda()
    y_val_set = torch.tensor(y_val_set,dtype=torch.float32).cuda()
    batch_size = 512
    train_set = data_process.Formation_Dataset(x_train_set, y_train_set)
    val_set = data_process.Formation_Dataset(x_val_set, y_val_set)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=True)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    model = modeling.Formation_Prediction().cuda()
    loss = nn.L1Loss().cuda()

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    num_epoch = 1000

    print('--------------------------------Run Training----------------------------------')
    for epoch in range(num_epoch):
        epoch_start_time = time.time()
        train_loss = torch.tensor(0.0).cuda()
        val_loss = torch.tensor(0.0).cuda()

        model.train()
        for i, data in enumerate(train_loader):
            optimizer.zero_grad()
            train_pred = model(data[0].cuda())
            batch_loss = loss(train_pred, data[1].cuda())
            batch_loss.backward()
            optimizer.step()

            train_loss += batch_loss

        model.eval()
        with torch.no_grad():
            for i, data in enumerate(val_loader):
                val_pred = model(data[0].cuda())
                batch_loss = loss(val_pred, data[1].cuda())
                val_loss += batch_loss
            # 将结果print出来
            print('[%03d/%03d] %2.2f sec(s)  Train Loss: %3.6f | Val Loss: %3.6f' % \
                  (epoch + 1, num_epoch, time.time() - epoch_start_time, train_loss / len(train_loader),
                   val_loss / len(val_loader)))


if __name__ == '__main__':
    main()

