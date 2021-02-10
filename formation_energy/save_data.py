from bert_serving.client import BertClient
import numpy as np
bc = BertClient()

element_name1 = np.load('/home/ypd-19-2/BERT/formation_energy/element_name1.npy')
element_name2 = np.load('/home/ypd-19-2/BERT/formation_energy/element_name2.npy')
element_num = np.load('/home/ypd-19-2/BERT/formation_energy/element_num.npy')

x_set = np.zeros((2 * len(element_num), 768))
y_set = np.zeros((2 * len(element_num), 1))
for i in range(len(element_num)):
    temp1 = bc.encode([element_name1[i]])
    temp2 = bc.encode([element_name2[i]])
    x_set[2*i] = temp1
    x_set[2*i+1] = temp2
    y_set[2*i] = element_num[i]
    y_set[2*i+1] = element_num[i]
np.save('x_set.npy', x_set)
np.save('y_set.npy', y_set)
print('bupt')
print('a')