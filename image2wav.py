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


def FlipForwardSlash(arr):
    out = [[0]*len(arr) for i in range(len(arr))]
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            out[x][y] = arr[len(arr[y])-1-y][x]
    
    tmp = FlipBackSlash(out)
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            out[len(arr[y])-1-y][x] = tmp[x][y]

    return out

def FlipBackSlash(arr):
    out = [[0]*len(arr) for i in range(len(arr))]
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            out[x][y] = arr[y][x]
    
    return out

def crop(arr, xMin, xMax, yMin, yMax):
    out = [[0]*int(xMax - xMin + 1) for i in range(int(yMax - yMin + 1))]
    for y in range(int(yMax-yMin+1)):
        for x in range(int(xMax - xMin+1)):
            out[y][x] = arr[int(yMin+y)][int(xMin+x)];
    
    return out;

def Two2OneD(arr):
    # print(arr)
    if (len(arr) >= 2):
        out = [0]*(len(arr[0])*len(arr))
        xStart = 0;
        xEnd = len(arr[0])-1;
        yStart = 0;
        yEnd = len(arr)-1;
        xMid = (xStart + xEnd) // 2;
        yMid = (yStart + yEnd) // 2;

        # create four new nodes with each node have four sub-nodes connected in the order: left down -> left up -> right up -> right down
        LD_Piece = Two2OneD(crop(FlipForwardSlash(arr), xStart, xMid, yMid+1, yEnd));
        LU_Piece = Two2OneD(crop(arr, xStart, xMid, yStart, yMid));
        RU_Piece = Two2OneD(crop(arr, xMid+1, xEnd, yStart, yMid));
        RD_Piece = Two2OneD(crop(FlipBackSlash(arr), xMid+1, xEnd, yMid+1, yEnd));

        # concatenate the four pieces of array
        idx = 0;
        for i in LD_Piece:
            out[idx] = i;
            idx += 1
        for i in LU_Piece:
            out[idx] = i;
            idx += 1
        for i in RU_Piece:
            out[idx] = i;
            idx += 1
        for i in RD_Piece:
            out[idx] = i;
            idx += 1

        # print(out)
        return out;
    else:
        return [arr[0][0]];


if __name__ == '__main__':

    arr, dim = convert2arr(sys.argv[1])
    print("Linking pixels... ")

    
    # dimensions = 4
    # arr = [[0]*dimensions for i in range(dimensions)]

    c = 0;
    print("Original array")
    print(arr)

    map = Two2OneD(arr)
    print("New array")
    print(map)

    print("creating wav... ")
    createwav.append_sinewave(volume=1, freq=map)
    print("saving wav... ")
    createwav.save()
    # playsound('output.wav')

    pass
