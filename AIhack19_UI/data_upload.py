#this image will be saved in the current working directory which is to be fed to our network


import librosa
from cv2 import imwrite
import numpy as np
import matplotlib.pyplot as plt


dur=10


def dataprepocess(input):
    audio,fs=librosa.load(input,sr=16000)
    while len(audio)<fs*dur:
        
        audio = np.concatenate((audio,audio), axis=0)
    audio = audio[:fs*dur]
    S = librosa.feature.melspectrogram(audio, sr=fs, n_mels=129, fmax=5000,n_fft=1600, hop_length=320)
    print(np.max(S))
    print(S)
    plt.imshow(S)
    name = input + '.png'
    imwrite(name,S)
