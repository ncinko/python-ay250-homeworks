# -*- coding: utf-8 -*-
"""
Spyder Editor
Nick Cinko
AY250 HW3 Problem 2
Goal: Write a program that identifies musical notes from sound (AIFF) files.
"""
from os import listdir
import aifc  #used to open audio files
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.fftpack import fftfreq
import numpy as np

#find frequency of "nth" note, where the 45th note is defined to be 440 Hz (A4); conspiracy theorists prefer 432 Hz
def note_to_freq(n):
    return np.power(2, (n - 33.)/12.)*440

#standard note names of modern (ascending) chromatic scale
notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
         
#dictionary to store note name/frequency pairs         
notedict={}

#loop to fill note dictionary and number relative octaves
for j in range(4):
    for i in range(12):
        notedict[notes[i]+str(j+2)] = note_to_freq(j*12+i)

#loop to remove sharp/flat notes since it appears we have none; not necessary, but it will make the search faster
for key in list(notedict): #dictionary will change size in loop, so get keys list at start of loop
    if "#" in key:
        notedict.pop(key)  


def AnalyzeFile(filename):
    
    #open audio files
    file = aifc.open(directory + '/' + filename, 'rb')
    
    #get number of audio frames in file & sample rate; playtime = (# frames)/(sample rate)
    nframes = file.getnframes()
    samplerate = 2*file.getframerate()  #not sure why I need to double this, but my frequencies were all 50% their normal value
    
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
    freq_spacing = samplerate/len(x[0])
    
    #frequencies/amplitudes are symmetric about f=0 Hz; split the array and take positive frequencies
    sliced = np.split(X,2)
    sliced_freqs = np.split(freqs,2)
    search_amps = np.abs(sliced[0])/len(x[0])  #fft returns complex values that must be scaled by the length of initial array
    search_freqs = sliced_freqs[0]
    
    #uncomment for plots
    """#create figure/axis from matplotlib
    fig, ax = plt.subplots()
    fig.suptitle(filename + ' Power Spectrum', fontsize=14, fontweight='bold')
    #plot fft amplitudes against frequencies
    ax.plot(search_freqs, search_amps)
    ax.set_xlabel('frequency (Hz)')
    ax.set_ylabel('power')
    ax.set_xlim(0,2400)
    ax.set_ylim(0, np.amax(search_amps))"""
    
    possiblenotes = []  #this will store the note names & amplitudes of peaks found in the power spectrum plots
    windowsize = 100  #roughly 6 Hz wide with given frequency spacing
    #the 'instruments' appear to produce harmonics of the form f, 2f, 3f, etc. where f is the fundamental frequency
    #we will search for peaks in a frequency window around each fundamental note frequency
    for note in notedict:
        frequency = notedict[note]
        freq_bin = int(frequency/freq_spacing)  #convert desired frequency to an index (bin) of our numpy array
        avg_amp = np.amax(search_amps[int(freq_bin - windowsize/2):int(freq_bin + windowsize/2)])  #get max amplitude in the frequency window
        #print(note, avg_amp)
        if avg_amp > 50:
            possiblenotes.append([note,avg_amp])  #append note name & amplitude if there's a peak
    
    #Attempt to eliminate redundant overtones below
    newnote_truth = [1]*len(possiblenotes)  #Boolean list (True will mean a possible note is unique and not a harmonic)
    threshold = .08  #somewhat arbitrary threshold for harmonic search
    harmonics = []
    for j in range(20):
        harmonics.append(2 + j)
    
    
    for i in range(len(possiblenotes)):  #loop through all possible notes
        note1 = notedict[possiblenotes[i][0]]
        for j in range(i+1, len(possiblenotes)):  #loop through possible notes higher (in frequency) than outer loop note
            note2 = notedict[possiblenotes[j][0]]
            for ratio in harmonics:  #check if note 2 is a multiple of note 1
                if np.abs(note2/note1 - ratio) < threshold and possiblenotes[i][1] > possiblenotes[j][1] :  #amplitude comparison as well to attempt to allow octaves
                    newnote_truth[j] = 0  #note 2 is probably an overtone
                    
    #print(possiblenotes)
    #print out results
    print('Notes found in '+ filename + ':')
    for i in range(len(newnote_truth)):
        if newnote_truth[i] == True:
            print(possiblenotes[i][0])
    print('=====================')       

    
    
directory = 'sound_files'

for file in listdir(directory):
    if 'aif' in file:
        AnalyzeFile(file)
               

    #print(search_freqs[int(frequency/freq_spacing)], frequency)


    