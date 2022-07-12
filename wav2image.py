from scipy.io.wavfile import read, write
from scipy.fft import fft, fftfreq
import sounddevice as sd
import argparse
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
            TwoDMap[y][x] = c
            c += 1
 
    map = image2wav.Two2OneD(TwoDMap)
    for i, value in enumerate(arr):
        key = map[i]
        out[key // dim][key % dim] = value

    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='audio', dest="audio")
    parser.add_argument('-t', help='record duration', dest="duration", default=1)
    parser.add_argument('-d', help='output image dimensions', dest="dimension", required = True)
    args = parser.parse_args()

    sample_rate = 44100
    duration = float(args.duration)

    if args.audio is None:
        print(f"Recording for {duration} s")
        sound = sd.rec(int(duration * sample_rate), dtype='float64', channels=1)
        sd.wait()

        data = sound.flatten()
    else:
        rate, data = read(args.audio)
        print("Sample rate: {} Hz".format(rate))
        print("Data type: {}".format(data.dtype))
    # write("sound.wav",sample_rate,sound)

    N = int(sample_rate * duration)

    dataFFT = fft(data[0:22050])
    x = fftfreq(N, 1 / sample_rate)[0:2093]

    dataFFTAbs = abs(dataFFT[0:2093])
    plt.figure(figsize=(15, 5))
    plt.plot(x, dataFFTAbs, 'r')
    plt.show()

    dimensions = int(args.dimension)
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
    data = Image.fromarray(array)
    print("Image saved as output.png")
    data.save("output.png")