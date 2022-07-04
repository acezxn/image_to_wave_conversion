from scipy.io.wavfile import read
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import image2wav
import sys
import numpy as np
from PIL import Image


def map(arr, MIN, MAX):
    minimum = min(arr.tolist())
    maximum = max(arr.tolist())
    out = []
    for i in arr:
        out.append((i - minimum) / (maximum - minimum) * (MAX - MIN) + MIN)
    
    return out


def One2TwoD(arr, dim):

    TwoDMap = [[0] * dim for i in range(dim)]
    out = [[0] * dim for i in range(dim)]
    c = 0;
    for y in range(dim):
        for x in range(dim):
            print(f"{c} ", end = "")
            TwoDMap[y][x] = c
            c += 1
        print()
    print()

    map = image2wav.Two2OneD(TwoDMap)
    for i, value in enumerate(arr):
        key = map[i]
        out[key // dim][key % dim] = value

    return out




rate, data = read(sys.argv[1])
print("Sample rate: {} Hz".format(rate))
print("Data type: {}".format(data.dtype))

sample_rate = 44100
duration = 0.5
N = int(sample_rate * duration)

dataFFT = fft(data[0:22050])
x = fftfreq(N, 1 / sample_rate)[0:2093]

dataFFTAbs = abs(dataFFT[0:2093])
plt.figure(figsize=(15, 5))
plt.plot(x, dataFFTAbs, 'r')
plt.show()

dimensions = int(sys.argv[2])
freq_resolution = dimensions ** 2
step = 2093 / (freq_resolution-1)

freqs = []
current = 0
count = 0
total = 0
prevGoal = 0;

dataFFTAbs = map(dataFFTAbs, 0, 255)

while current < 2093 and len(freqs) < freq_resolution:
    total += dataFFTAbs[int(current)] ** 40
    count += 1
    goal = int(prevGoal + step)

    if (current == goal):
        
        freqs.append(int((total / count) ** 0.025))
        count = 0
        total = 0
        prevGoal = current
    
    current += 1
        
out = One2TwoD(freqs, dimensions)
array = np.array(out, np.uint8)
print(array)
data = Image.fromarray(array)
data.save("output.png")