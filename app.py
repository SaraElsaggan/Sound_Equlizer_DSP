from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pydub.playback import play
import librosa as librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import librosa.display
from IPython.display import Audio
import sys, os, shutil

from librosa.core.spectrum import _spectrogram
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from datetime import datetime
import matplotlib.pyplot as plt
import librosa.display
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pyqtgraph as pg
from scipy import fftpack
from scipy.signal import spectrogram
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
from PyQt5.QtWidgets import QApplication, QMainWindow , QStackedWidget ,QFrame , QComboBox
from mainwindow import Ui_MainWindow
import numpy as np
from PyQt5.QtWidgets import QInputDialog, QFileDialog
from scipy.io import wavfile
import os
import pyqtgraph as pg
import numpy as np
from scipy.fftpack import rfft, rfftfreq, irfft , fft , fftfreq
from random import randint
from pyqtgraph import PlotWidget, plot, QtCore
from PyQt5.QtCore import pyqtSlot
from cmath import rect
import sys
import sounddevice as sd
from numba import jit


class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=5, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
    


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

      
   
        
        
      
        
        
        
        self.timer_input = QTimer(self)
        
        self.ui.chek_bx_show_spect_input.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_input.isChecked(), self.spectrogram_canvas_input))
        self.ui.chek_bx_show_spect_output.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_output.isChecked(), self.spectrogram_canvas_output))
        
        self.ui.combo_bx_mode.currentIndexChanged.connect(self.handleComboBox)
        self.spectrogram_canvas_input = MplCanvas(self)
        self.spectrogram_canvas_output = MplCanvas(self)
        
        
        self.ui.verticalLayout_7.addWidget(self.spectrogram_canvas_input)
        self.ui.verticalLayout_8.addWidget(self.spectrogram_canvas_output)
        
        
        
        self.ui.btn_zoom_in_input.clicked.connect(lambda: self.zoom(self.ui.grph_input_sig , 1))
        self.ui.btn_zoom_out_input.clicked.connect(lambda: self.zoom(self.ui.grph_input_sig , 0))

        self.ui.btn_zoom_in_output.clicked.connect(lambda: self.zoom(self.ui.grph_output_sig , 1))
        self.ui.btn_zoom_out_output.clicked.connect(lambda: self.zoom(self.ui.grph_output_sig , 0))

        self.ui.actionUpload_file.triggered.connect(self.upload_signal_file)
        self.ui.btn_play_pause_input.clicked.connect(lambda: self.play_audio(self.original_sig)) #this is for the input signal

        

        QShortcut(QKeySequence("Ctrl+o"), self).activated.connect(self.upload_signal_file)
        
        ##orignal_sig --------> input signal(loaded)

    def handleComboBox(self, index):
        # Hide or show controls in the stacked widget based on the index
        self.ui.stackedWidget.setCurrentIndex(index)
    
    
    
   
    def min_max(self):
        '''
        this funcrion is to cala the min and max of graph to set it limits
        '''

        x_min, x_max = self.ui.grph_input_sig.getViewBox().viewRange()[0]
        y_min, y_max = self.ui.grph_input_sig.getViewBox().viewRange()[1]

        return x_min  , x_max , y_min , y_max
        
        
    def upload_signal_file(self):
    
        file_path = QFileDialog.getOpenFileName(self, "Open Song", "~", "Sound Files ( *.wav )")
        if file_path[0] == "":
            pass
        else:
            self.sample_rate, self.original_sig = wavfile.read(file_path[0])
           
            self.is_loaded = True
        # self.ui.grph_input_sig.clear()
        # self.plot_input = self.ui.grph_input_sig.plot(self.original_sig , pen= "b")
        # self.ui.grph_input_sig.autoRange()
        self.plot_audio_signal(self.original_sig , self.sample_rate , self.ui.grph_input_sig)
        self.fourier(self.original_sig)
        # # self.edit_graphs()
        
    def plot_audio_signal(self , samples , sampling_rate , widget):
        peak_value = np.amax(samples)
        normalized_data = samples / peak_value
        print(f"shape :  {samples.shape}")
        # time = list(np.linspace(0, length, samples.shape[0]))
        time = np.array(range(0 , len(samples) )) / sampling_rate
        print(f"time {len(time)}")
        drawing_pen = pg.mkPen(color=(255, 0, 0), width=0.5)
        widget.clear()
        widget.plot(time, samples, pen=drawing_pen)
        # widget.plot(time, normalized_data, pen=drawing_pen)
        
        # widget.plotItem.getViewBox().setLimits(xMin=0, xMax=np.max(time), yMin=-1.1, yMax=1.1)
  
        
        
    
    def fourier(self , signal): 
        self.fourier_transform = np.fft.fft(self.original_sig)
        self.magnitude_spectrum = 2 * np.abs(self.fourier_transform / len(self.original_sig))
        freqs = np.fft.fftfreq(len(self.original_sig), 1 / self.sample_rate)
        
        self.ui.signal_view.plot(freqs[:len(freqs)//2] , self.magnitude_spectrum[:len(freqs)//2])
        self.spectogram(self.original_sig  , self.sample_rate)
    

    
    def play_audio(self, signal):
    
        sd.play(signal , self.sample_rate)
        '''need edits'''
        self.vertical_line = pg.InfiniteLine(angle=90, movable=False, pen='r')
        self.ui.grph_input_sig.addItem(self.vertical_line)
        self.x_position = 0
        self.timer_input.timeout.connect(self.update_plot)
        self.timer_input.start(100)  # Update every 100 milliseconds



    def update_plot(self):
        # Update the position of the vertical line
        self.vertical_line.setValue(self.x_position)
        
        # Update x-axis position for the next iteration
        self.x_position += 0.1
        
        
    def spectogram(self  ,signal , sample_rate):
        self.spectrogram_canvas_input.axes.clear()
        self.spectrogram_canvas_input.axes.specgram(signal , Fs = sample_rate)
        self.spectrogram_canvas_input.draw()
        
        

    
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
        
          
      
    

def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
