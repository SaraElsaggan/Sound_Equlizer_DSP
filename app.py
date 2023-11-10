# from pydub import AudioSegment
# from pydub.playback import play
from PyQt5.QtCore import QBuffer, QIODevice, QByteArray  # Add these import statements
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QBuffer, QIODevice 
from scipy.signal import spectrogram
import winsound
import pyaudio
from scipy.io import wavfile
from scipy.interpolate import interp1d
from scipy.signal import resample
from scipy.interpolate import interp1d
from PyQt5 import QtCore, QtGui
import os
import pandas as pd
import sys
from PyQt5.QtWidgets import QInputDialog  ,  QApplication, QMainWindow, QShortcut, QFileDialog , QSplitter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
import numpy as np
from PyQt5.QtWidgets import QFileDialog
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow , QStackedWidget ,QFrame , QComboBox
from mainwindow import Ui_MainWindow
import numpy as np
from PyQt5 import QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QInputDialog, QFileDialog
from scipy.io import wavfile
import os
import pyqtgraph as pg
import numpy as np
from scipy.fftpack import rfft, rfftfreq, irfft
from random import randint
from pyqtgraph import PlotWidget, plot, QtCore
# import simpleaudio as sa
from PyQt5.QtCore import pyqtSlot
from cmath import rect
import sys
import sounddevice as sd
from numba import jit



class MyWindow(QMainWindow):   
    
    def __init__(self ):
        super(MyWindow , self).__init__()
      
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  
        # Set the checkbox to be checked by default
        self.ui.chek_bx_show_spect_input.setChecked(True)
        self.ui.chek_bx_show_spect_output.setChecked(True)
        # Set the default page to index 0
        self.ui.stackedWidget.setCurrentIndex(0)
       
        self.ui.stackedWidget.setFrameShape(QFrame.NoFrame)
        self.ui.stackedWidget.setFrameShadow(QFrame.Plain)
        self.ui.combo_bx_mode.currentIndexChanged.connect(self.handleComboBox)
        
        
        
        #----me---
        # self.file_path = None;
        self.timer = None
        self.playing_audio = None 
        self.plt_input_signal = None 
        self.plt_output_signal = None
        
        self.input_time = None
        self.input_signal = None
        
        self.output_time = None
        self.input_time = None
        
        self.is_loaded = None
        
        self.is_play = False
        
        self.ui.chek_bx_show_spect_input.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_input.isChecked(), self.ui.spect_input))
        self.ui.chek_bx_show_spect_output.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_output.isChecked(), self.ui.spect_output))
        
        self.ui.btn_zoom_in_input.clicked.connect(lambda: self.zoom(self.ui.grph_input_sig , 1))
        self.ui.btn_zoom_out_input.clicked.connect(lambda: self.zoom(self.ui.grph_input_sig , 0))

        self.ui.btn_zoom_in_output.clicked.connect(lambda: self.zoom(self.ui.grph_output_sig , 1))
        self.ui.btn_zoom_out_output.clicked.connect(lambda: self.zoom(self.ui.grph_output_sig , 0))

        self.ui.actionUpload_file.triggered.connect(self.upload_signal_file)
        # self.ui.btn_play_pasuse.clicked.connect(lambda: self.play_pause(self.original_sig)) #this is for the input signal
        QShortcut(QKeySequence("Ctrl+o"), self).activated.connect(self.upload_signal_file)
        
        ##orignal_sig --------> input signal(loaded)

    def handleComboBox(self, index):
        # Hide or show controls in the stacked widget based on the index
        self.ui.stackedWidget.setCurrentIndex(index)
    
    
    
   
    def min_max(self):
        '''
        this funcrion is to cala the min and max of graph to set it limits
        '''

        # min_x =  min(self.plot_input.getData()[0])
        # max_x =  max(self.plot_input.getData()[0])


        # min_y =  min(self.plot_input.getData()[1])
        # max_y =  max(self.plot_input.getData()[1])
        
        # return min_x  , max_x , min_y , max_y
        x_min, x_max = self.ui.grph_input_sig.getViewBox().viewRange()[0]
        y_min, y_max = self.ui.grph_input_sig.getViewBox().viewRange()[1]

        return x_min  , x_max , y_min , y_max
        
        
    def upload_signal_file(self):
        '''this function read the sound signal file 
            plot it in the input graph
            this code is from the sound equlizer repo
        '''
        file_path = QFileDialog.getOpenFileName(self, "Open Song", "~", "Sound Files ( *.wav )")
        if file_path[0] == "":
            pass
        else:
            self.sample_rate, self.original_sig = wavfile.read(file_path[0])
            # if self.original_sig.ndim == 2:
            #     self.original_sig = np.mean(self.original_sig, axis=1)
            # else:
            #     pass
            self.is_loaded = True
        self.ui.grph_input_sig.clear()
        self.plot_input = self.ui.grph_input_sig.plot(self.original_sig , pen= "b")
        self.ui.grph_input_sig.autoRange()
        self.edit_graphs()
        self.freq_domain_convert(self.original_sig)

        '''just was trying somthing
        t = np.linspace(0  , 5 , 1000)
        self.ui.input_signal.clear()
        self.original_sig = (np.sin(2*t*np.pi* 5 )+3* np.sin(2*t*np.pi* 10 ) + 5* np.sin(t*np.pi* 40 ))
        self.sample_rate = 1/1000
        self.ui.input_signal.plot(self.original_sig , pen= "b")
        '''
        
        
    def freq_domain_convert(self , signal):
        '''this function takes the input signal and convert it into freq domain and plot it'''
        '''this code is from chatgpt 
        # n = len(self.original_sig)
        # k = np.arange(n)
        # T = n / self.sample_rate
        # frq = k / T
        # frq = frq[range(n // 2)]
        # fft_vals = np.fft.fft(self.original_sig)
        # fft_vals = fft_vals[range(n // 2)]

        # Plot the frequency-domain signal
        # self.ui.signal_view.clear()
        # self.ui.signal_view.plot(frq, abs(fft_vals), pen='r')
        '''
        
        '''this code is from sound_equlizer repo'''
        self.original_complex = rfft(signal)
        self.modified_complex= np.copy(self.original_complex)
        self.freq = (rfftfreq(len(self.original_complex) + 1, 1 / self.sample_rate))
        self.freq = self.freq[self.freq > 0]
        print(self.freq[len(self.freq)-1])
        self.ui.signal_view.clear()
        self.ui.signal_view.plot(self.freq, np.abs(self.modified_complex), pen='g')
        
        
        # self.file_path  , _ = QFileDialog.getOpenFileName( self , "open file", "" ,"(*.wav) ")
        # sampling_rate, self.original_sig = wavfile.read(self.file_path)
        # self.input_time = np.arange(len(self.original_sig))
        # self.ui.original_sig.clear()
        # self.plt_original_sig = self.ui.original_sig.plot(self.input_time , self.original_sig)
        # self.edit_graphs( self.ui.original_sig)
    
    def show_hide_specto_grph(self  , state  , specto_grph_widget ):
        if state:
            specto_grph_widget.show()
        else:
            specto_grph_widget.hide()
      
    def zoom(self , graph , state): # it state = 0 zoom out , 1 zoom in
        if state:
            graph.getViewBox().scaleBy((1 / 1.2, 1 / 1.2))
        else:
            graph.getViewBox().scaleBy((1.2, 1.2))
        
          
      
    # def play_pause(self , signal):
    #     # if self.playing_audio is not None:
    #     #     # Stop the currently playing audio
    #     #     self.playing_audio.stop()
    #     #     self.playing_audio = None
    #     icon = QtGui.QPixmap("play.png")
    #     self.ui.btn_play_pasuse.setToolTip("paly")
    #     self.ui.btn_play_pasuse.setIcon(QtGui.QIcon(icon))

    #     audio_segment = AudioSegment(
    #             data=signal.tobytes(),
    #             sample_width=signal.dtype.itemsize,
    #             frame_rate=self.sample_rate,
    #             channels=1 if signal.ndim == 1 else signal.shape[1]
    #         )   

    #         # Play the audio
    #     self.playing_audio = play(audio_segment)
         
         
            



 
 
    

  
    

def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
