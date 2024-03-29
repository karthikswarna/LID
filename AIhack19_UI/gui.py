# # import tkinter as tk
# # import threading

# # class App():
# #     def __init__(self, master):
# #         self.isrecording = False
# #         self.button = tk.Button(text='rec')
# #         self.button.bind("<Button-1>", self.startrecording)
# #         self.button.bind("<ButtonRelease-1>", self.stoprecording)
# #         self.button.pack()

# #     def startrecording(self, event):
# #         self.isrecording = True
# #         t = threading.Thread(target=self._record)
# #         t.start()

# #     def stoprecording(self, event):
# #         self.isrecording = False

# #     def _record(self):
# #         while self.isrecording:
# #             print("Recording")

# # -*- coding: utf-8 -*-
# """
# Created on May 23 2014
# @author: florian
# """
# import sys
# import threading
# import atexit
# import wave
# import pyaudio
# import numpy as np
# import matplotlib
# matplotlib.use("TkAgg")
# from matplotlib import figure
# from PyQt4 import QtGui, QtCore
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

# # class taken from the SciPy 2015 Vispy talk opening example
# # see https://github.com/vispy/vispy/pull/928
# class MicrophoneRecorder(object):
#     def __init__(self, rate=4000, chunksize=1024):
#         self.rate = rate
#         self.chunksize = chunksize
#         self.p = pyaudio.PyAudio()
#         self.stream = self.p.open(format=pyaudio.paInt16,
#                                   channels=1,
#                                   rate=self.rate,
#                                   input=True,
#                                   frames_per_buffer=self.chunksize,
#                                   stream_callback=self.new_frame)
#         self.lock = threading.Lock()
#         self.stop = False
#         self.frames = []
#         atexit.register(self.close)

#     def new_frame(self, data, frame_count, time_info, status):
#         data = np.fromstring(data, 'int16')
#         with self.lock:
#             self.frames.append(data)
#             if self.stop:
#                 return None, pyaudio.paComplete
#         return None, pyaudio.paContinue

#     def get_frames(self):
#         with self.lock:
#             frames = self.frames
#             self.frames = []
#             return frames

#     def start(self):
#         self.stream.start_stream()

#     def close(self):
#         with self.lock:
#             self.stop = True
#         self.stream.close()
#         self.p.terminate()


# class MplFigure(object):
#     def __init__(self, parent):
#         self.figure = figure.Figure(facecolor='white')
#         self.canvas = FigureCanvas(self.figure)
#         self.toolbar = NavigationToolbar(self.canvas, parent)

# class LiveFFTWidget(QtGui.QWidget):
#     def __init__(self):
#         QtGui.QWidget.__init__(self)

#         # customize the UI
#         self.initUI()

#         # init class data
#         self.initData()

#         # connect slots
#         self.connectSlots()

#         # init MPL widget
#         self.initMplWidget()

#     def initUI(self):

#         hbox_gain = QtGui.QHBoxLayout()
#         autoGain = QtGui.QLabel('Auto gain for frequency spectrum')
#         autoGainCheckBox = QtGui.QCheckBox(checked=True)
#         hbox_gain.addWidget(autoGain)
#         hbox_gain.addWidget(autoGainCheckBox)

#         # reference to checkbox
#         self.autoGainCheckBox = autoGainCheckBox

#         hbox_fixedGain = QtGui.QHBoxLayout()
#         fixedGain = QtGui.QLabel('Manual gain level for frequency spectrum')
#         fixedGainSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
#         hbox_fixedGain.addWidget(fixedGain)
#         hbox_fixedGain.addWidget(fixedGainSlider)

#         self.fixedGainSlider = fixedGainSlider

#         vbox = QtGui.QVBoxLayout()

#         vbox.addLayout(hbox_gain)
#         vbox.addLayout(hbox_fixedGain)

#         # mpl figure
#         self.main_figure = MplFigure(self)
#         vbox.addWidget(self.main_figure.toolbar)
#         vbox.addWidget(self.main_figure.canvas)

#         self.setLayout(vbox)

#         self.setGeometry(300, 300, 350, 300)
#         self.setWindowTitle('LiveFFT')
#         self.show()
#         # timer for calls, taken from:
#         # http://ralsina.me/weblog/posts/BB974.html
#         timer = QtCore.QTimer()
#         timer.timeout.connect(self.handleNewData)
#         timer.start(50)
#         # keep reference to timer
#         self.timer = timer


#     def initData(self):
#         mic = MicrophoneRecorder()
#         mic.start()

#         # keeps reference to mic
#         self.mic = mic

#         # computes the parameters that will be used during plotting
#         self.freq_vect = np.fft.rfftfreq(mic.chunksize,
#                                          1./mic.rate)
#         self.time_vect = np.arange(mic.chunksize, dtype=np.float32) / mic.rate * 1000

#     def connectSlots(self):
#         pass

#     def initMplWidget(self):
#         """creates initial matplotlib plots in the main window and keeps
#         references for further use"""
#         # top plot
#         self.ax_top = self.main_figure.figure.add_subplot(211)
#         self.ax_top.set_ylim(-32768, 32768)
#         self.ax_top.set_xlim(0, self.time_vect.max())
#         self.ax_top.set_xlabel(u'time (ms)', fontsize=6)

#         # bottom plot
#         self.ax_bottom = self.main_figure.figure.add_subplot(212)
#         self.ax_bottom.set_ylim(0, 1)
#         self.ax_bottom.set_xlim(0, self.freq_vect.max())
#         self.ax_bottom.set_xlabel(u'frequency (Hz)', fontsize=6)
#         # line objects
#         self.line_top, = self.ax_top.plot(self.time_vect,
#                                          np.ones_like(self.time_vect))

#         self.line_bottom, = self.ax_bottom.plot(self.freq_vect,
#                                                np.ones_like(self.freq_vect))


#         # tight layout
#         #plt.tight_layout()

#     def handleNewData(self):
#         """ handles the asynchroneously collected sound chunks """
#         # gets the latest frames
#         frames = self.mic.get_frames()

#         if len(frames) > 0:
#             # keeps only the last frame
#             current_frame = frames[-1]
#             # plots the time signal
#             self.line_top.set_data(self.time_vect, current_frame)
#             # computes and plots the fft signal
#             fft_frame = np.fft.rfft(current_frame)
#             if self.autoGainCheckBox.checkState() == QtCore.Qt.Checked:
#                 fft_frame /= np.abs(fft_frame).max()
#             else:
#                 fft_frame *= (1 + self.fixedGainSlider.value()) / 5000000.
#                 #print(np.abs(fft_frame).max())
#             self.line_bottom.set_data(self.freq_vect, np.abs(fft_frame))

#             # refreshes the plots
#             self.main_figure.canvas.draw()




# def main():
#     app = QtGui.QApplication(sys.argv)
#     window = LiveFFTWidget()
#     sys.exit(app.exec_())


############################################


import tkinter as tk
import pyaudio
import wave
from data_upload import dataprepocess
from tkinter import *


def main():
    m=tk.Tk()
    m.title('Counting Seconds') 
    button = tk.Button(m, text='record', width=25, command=record)
    button.pack()
    w = Label(m, text='GeeksForGeeks.org!')
    w.pack() 
    m.mainloop()

def record():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    for k in range(5):
        frames = []  # Initialize array to store frames
        filename = str(k)+"output.wav" 
        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        imgs = dataprepocess(filename)
		noFrames = imgs.shape[0]
		imgs = torch.from_numpy(imgs)
		prob = model(imgs)
		prob = prob.tolist()
		if noFrames == 1:
            ans = prob
        else:
            ans = np.array(prob[0])
            for i in range(1,noFrames):
                ans = np.multiply(ans,np.array(prob[i]))
            ans = list(ans)
		probabilites = [float(i)/sum(ans) for i in ans]
        print(probabilities)
        print(imgs.shape)
    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
