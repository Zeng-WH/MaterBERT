import numpy as np
import pandas as pd
import tensorflow as tf
import math
data = pd.read_excel('1000_abstracttotal.xls', encoding='utf-8')
data = data.iloc[:,[0,2]]
raw_data = data.to_numpy()
#print(raw_data.shape)
x=raw_data[:,1].reshape(len(raw_data),1)
y=raw_data[:,0].reshape(len(raw_data),1)
#print(x.shape)
x_train_set = x[: math.floor(len(x) * 0.8), 0]
y_train_set = y[: math.floor(len(y) * 0.8), 0]
x_validation = x[math.floor(len(x) * 0.8):, 0]
y_validation = y[math.floor(len(y) * 0.8):, 0]
with open("train.tsv", "w", encoding="utf-8") as train_fh, \
    open("dev.tsv", "w", encoding="utf-8") as dev_fh:
    for i in range(len(x_train_set)):
        train_fh.write("%s\t%s\n" %(y_train_set[i],x_train_set[i]))
    for i in range(len(x_validation)):
        dev_fh.write("%s\t%s\n" %(y_validation[i],x_validation[i]))
