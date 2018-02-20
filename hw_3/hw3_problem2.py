# -*- coding: utf-8 -*-
"""
Spyder Editor
Nick Cinko
AY250 HW3 Problem 2
Goal: Write a program that identifies musical notes from sound (AIFF) files.
"""

import aifc  #used to open audio files
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.fftpack import fftfreq
import numpy as np

#find frequency of "nth" note, where the 45th note is defined to be 440 Hz (A4); conspiracy theorists prefer 432 Hz
def note_to_freq(n):
    return np.power(2, (n - 45.)/12.)*440

#standard note names of modern (ascending) chromatic scale
notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
         
#dictionary to store note name/frequency pairs         
notedict={}

#loop to fill note dictionary and number relative octaves
for j in range(5):
    for i in range(12):
        notedict[notes[i]+str(j+1)] = note_to_freq(j*12+i)

#loop to remove sharp/flat notes since it appears we have none; not necessary, but it will make the search faster
for key in list(notedict): #dictionary will change size in loop, so get keys list at start of loop
    if "#" in key:
        notedict.pop(key)  

print(notedict)

#open audio files
file = aifc.open('sound_files/5.aif', 'rb')

#get number of audio frames in file & sample rate; playtime = (# frames)/(sample rate)
nframes = file.getnframes()
samplerate = file.getframerate()

#read all audio frames
rawdata = file.readframes(nframes)

#create numpy array from audio data; logic borrowed from https://gist.github.com/arunaugustine/5551446
y = np.fromstring(rawdata, np.short).byteswap()
audiolist = []
audiolist.append(y)
x = np.array(audiolist)

#fast Fourier transform the audio data & generate corresponding frequency values
X = fft(x[0])
freqs = fftfreq(len(x[0]))*samplerate

#frequencies/amplitudes are symmetric about f=0 Hz; split the array and take positive frequencies
sliced = np.split(X,2)
sliced_freqs = np.split(freqs,2)
search_amps = np.abs(sliced[0])/len(x[0])  #fft returns complex values that must be scaled by the length of initial array
search_freqs = sliced_freqs[0]

#create figure/axis from matplotlib
fig, ax = plt.subplots()

#plot fft amplitudes against frequencies
ax.plot(search_freqs, search_amps)
ax.set_xlim(0,100)
ax.set_ylim(0, 50)


    