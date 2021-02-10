import sys
import scipy
import time
import numpy as np
import pickle

periodictable_symbols = np.array([0,'H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co',
                       'Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te',
                       'I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir',
                       'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No',
                       'Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Uut','Uuq','Uup','Uuh','Uus','Uuo'])

def main():
    f = open('./TrainingSet.pkl', 'rb')
    inp = pickle.load(f, encoding='bytes')
    f.close()
    inp[b'T'] = inp[b'T'] / inp[b'N']
    for i in range(len(inp[b'T'])):
        print('---', i, '---')
        print('Formation energy (eV/atom): ', inp[b'T'][i])
        print('Coordinates: ')
        for j in range(len(inp[b'Co'][i])):
            print (inp[b'Co'][i, j, 0], inp[b'Co'][i, j, 1], inp[b'Co'][i, j, 2])
        print('Cell: ')
        for j in range(len(inp[b'Ce'][i])):
            print(inp[b'Ce'][i, j, 0], inp[b'Ce'][i, j, 1], inp[b'Ce'][i, j, 2])
        print('Atoms: ')
        print(" ".join(str(periodictable_symbols[e]) for e in inp[b'Z'][i]))
        print('Representation: ')
        for j in range(len(inp[b'X'][i])):
            print(inp[b'X'][i, j, 0], inp[b'X'][i, j, 1])

if __name__ == "__main__":
	main()
	print ('end')

