#!/usr/bin/python
# based on : www.daniweb.com/code/snippet263775.html
import math
import wave
import struct

# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in
# memory.
audio = []
sample_rate = 44100.0

def append_sinewave(
        freq,
        duration_milliseconds=500,
        volume=1.0):

    global audio

    num_freqs = len(freq)
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    freq_range = [130, 4186]
    step = (freq_range[1]-freq_range[0]) / (num_freqs-1)
    for x in range(int(num_samples)):
        current = freq_range[0]
        sum = 0

        for f in freq:
            sum += (f/255) * volume * math.sin(2 * math.pi * current * ( x / sample_rate ))
            current += step
        audio.append(sum/num_freqs)

    return



def save_wav(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return


def save():
    save_wav("output.wav")
