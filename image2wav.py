import itertools
from PIL import Image
import numpy as np
import createwav
import sys
from playsound import playsound
import math
import matplotlib.pyplot as plt
#import pyaudio


arr = [
[1, 2, 3, 4],
[11, 12, 13, 14],
[21, 22, 23, 24],
[31, 32, 33, 34]
]

audio = []

def convert2arr(file):
    img = Image.open(file)
    dim = img.size[0]
    print(dim, img.size[1])
    img = img.crop((0, 0, dim, dim))
    img.convert("L")

    data = img.getdata()
    idx = 0
    array = []
    sublist = []
    for e in data:
        if idx + 1 <= dim:
            sum = 0
            for i in e:
                sum += i
            sublist.append(sum/3)
        else:
            array.append(sublist)
            sublist = []
            sum = 0
            for i in e:
                sum += i
            sublist.append(sum/3)
            idx = 0
        idx += 1
    array.append(sublist)


    return array, dim

def devide(arr, dir): # recursive formula to chain 2D data with the Hilbert's curve
    x = len(arr[0])
    y = len(arr)


    if x % 2 == 0 and y % 2 == 0:
        LU_block = arr[0:((y//2))]
        o = []
        for e in LU_block:
            o.append(e[0:((x//2))])
        LU = devide(o, 'LU')

        RU_block = arr[0:((y//2))]
        o2 = []
        for e in RU_block:
            o2.append(e[((x//2)):x])
        RU = devide(o2, 'RU')

        LD_block = arr[((y//2)):y]
        o3 = []
        for e in LD_block:
            o3.append(e[0:((x//2))])
        LD = devide(o3, 'LD')

        RD_block = arr[((y//2)):y]
        o4 = []
        for e in RD_block:
            o4.append(e[((x//2)):x])
        RD = devide(o4, 'RD')

        if dir == 'LU' or dir == 'RU':
            connection = LD+LU+RU+RD
        elif dir == 'LD':
            connection = LD+RD+RU+LU
        elif dir == 'RD':
            connection = RU+LU+LD+RD
        else:
            connection = LD+LU+RU+RD



        return connection



    else:
        return arr

if __name__ == '__main__':

    arr, dim = convert2arr(sys.argv[1])
    print("Linking pixels... ")

    map = devide(arr, 'w')
    chain = [element for sublist in map for element in sublist] # flatten list
    print(chain)
    print(len(chain))
    print("creating wav... ")
    createwav.append_sinewave(volume=1, freq=chain)
    createwav.save()
    playsound('output.wav')

    pass
