from cv2 import imwrite
import os
import librosa
import numpy as np
import glob
loc = "C:/Users/Gowtham Senthil/Desktop/Recorded Good Samples/"
os.chdir(loc)

expDur = 10
sampling = 16000
samples = sampling*expDur
languages = {'Tam': '0','GUJ': '1','Mar': '2','HIN': '3', 'TEL': '4'}
n = 1
dst = 'C:/Users/Gowtham Senthil/Desktop/Recorded Test Data/recTestData.txt'
f = open(dst,'w+')

for file in glob.glob('*.wav'):
    lang = file[0:3]
    langNo = languages[lang]
    audio,sampling = librosa.load(file,sr=sampling)
    noFrames = 0
    
    if len(audio)<samples:
        while len(audio)<samples:
            audio = np.concatenate((audio,audio), axis=0)
        audio = audio[:samples]
        noFrames = 1
        
    elif (len(audio) % samples > samples*0.5):
        noFrames = int(np.ceil(len(audio) / samples))
        audio = np.concatenate((audio,audio), axis=0)
        audio = audio[:noFrames*samples]
        
    elif (len(audio) % samples < samples*0.5):
        noFrames = int(np.floor(len(audio) / samples))
        audio = audio[:noFrames*samples]

    frames = []
    for i in range(int(noFrames)):    
        frames.append(librosa.feature.melspectrogram(
                audio[i*samples:(i+1)*samples], sr = samples, n_mels = 129, 
                fmax = 5000, n_fft = 1600, hop_length = 320))
    
    for frame in frames:
        saveAddr = loc + str(int(n)) + '.png'
        imwrite(saveAddr, frame)
        line = str(int(n)) + ' ' + str(langNo)
        f.write(line + '\n')
        n += 1
        
f.close()