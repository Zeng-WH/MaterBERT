import numpy as np
import pandas as pd
from itertools import islice
import pickle

periodictable_symbols = np.array([0,'H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co',
                       'Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te',
                       'I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir',
                       'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No',
                       'Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Uut','Uuq','Uup','Uuh','Uus','Uuo'])
with open('./TrainingSet.pkl', 'rb') as f1:
    raw_data = pickle.load(f1, encoding='bytes')

raw_data[b'T'] = raw_data[b'T']/raw_data[b'N']
element_name1 = []
element_name2 = []
element_num = []
for i in range(len(raw_data[b'T'])):
    temp_name1 = []
    temp_name2 = []
    temp_num = []
    temp_cheele = raw_data[b'Z'][i]
    temp1 = np.zeros((1, 4))
    temp2 = np.zeros((1, 4))
    easyche = np.unique(temp_cheele)
    for pku in easyche:
        if (np.sum(temp_cheele == pku) == 6):  # 将六次的元素放在第四位
            temp1[0][3] = pku
        if (np.sum(temp_cheele == pku) == 2):  # 将两次的元素放在第三位
            temp1[0][2] = pku
        if (np.sum(temp_cheele == pku) == 1):  # 将其中的一个一次元素放在第二位
            temp1[0][1] = pku
    for pku in easyche:
        if(pku!=temp1[0][1] and pku!=temp1[0][2] and pku!=temp1[0][3]):
            temp1[0][0] = pku
    temp2[0][1] = temp1[0][0]
    temp2[0][0] = temp1[0][1]
    temp2[0][2] = temp1[0][2]
    temp2[0][3] = temp1[0][3]
    temp_name1.append(periodictable_symbols[int(temp1[0][0])])
    temp_name1.append(periodictable_symbols[int(temp1[0][1])])
    temp_name1.append(periodictable_symbols[int(temp1[0][2])])
    temp_name1.append('2')
    temp_name1.append(periodictable_symbols[int(temp1[0][3])])
    temp_name1.append('6')
    temp_name2.append(periodictable_symbols[int(temp2[0][0])])
    temp_name2.append(periodictable_symbols[int(temp2[0][1])])
    temp_name2.append(periodictable_symbols[int(temp2[0][2])])
    temp_name2.append('2')
    temp_name2.append(periodictable_symbols[int(temp2[0][3])])
    temp_name2.append('6')
    name1 = "".join(temp_name1)
    name2 = "".join(temp_name2)
    temp_num = raw_data[b'T'][i]
    element_name1.append(name1)
    element_name2.append(name2)
    element_num.append(temp_num)
np.save('element_name1.npy', element_name1)
np.save('element_name2.npy', element_name2)
np.save('element_num.npy', element_num)



print('bupt')