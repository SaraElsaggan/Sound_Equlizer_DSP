from scipy.signal import gaussian
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import  QApplication, QMainWindow, QShortcut, QFileDialog , QSplitter , QFrame
from scipy.signal import spectrogram
from scipy.signal import resample
import sys
from PyQt5.QtGui import QIcon, QKeySequence
from mainwindow import Ui_MainWindow
import numpy as np
import pandas as pd
from scipy.io import wavfile
import pyqtgraph as pg
from scipy.fftpack import rfft, rfftfreq, irfft , fft , fftfreq
from PyQt5.QtCore import pyqtSlot
import sounddevice as sd


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
        self.ui.combo_bx_mode.currentIndexChanged.connect(self.handleComboBox)
        # add canvas to plot spectogram
        self.spectrogram_canvas_input = MplCanvas(self)
        self.spectrogram_canvas_output = MplCanvas(self)
        self.ui.verticalLayout_7.addWidget(self.spectrogram_canvas_input)
        self.ui.verticalLayout_8.addWidget(self.spectrogram_canvas_output)
        
        self.timer_1 = QTimer(self)
        self.timer_1.timeout.connect(lambda :self.update_slider( self.ui.horizontalSlider))
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setValue(0)
        
        self.timer_2 = QTimer(self)
        self.timer_2.timeout.connect(lambda :self.update_slider( self.ui.horizontalSlider_2))
        self.ui.horizontalSlider_2.setMinimum(0)
        self.ui.horizontalSlider_2.setValue(0)
        
        self.ui.chek_bx_show_spect_input.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_input.isChecked(), self.spectrogram_canvas_input))
        self.ui.chek_bx_show_spect_output.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_output.isChecked(), self.spectrogram_canvas_output))

        self.ui.btn_zoom_in_input.clicked.connect(lambda: self.zoom(self.ui.grph_input_sig , 1))
        self.ui.btn_zoom_out_input.clicked.connect(lambda: self.zoom(self.ui.grph_input_sig , 0))

        self.ui.btn_zoom_in_output.clicked.connect(lambda: self.zoom(self.ui.grph_output_sig , 1))
        self.ui.btn_zoom_out_output.clicked.connect(lambda: self.zoom(self.ui.grph_output_sig , 0))

        self.ui.actionUpload_file.triggered.connect(self.upload_signal_file)
        
        self.ui.btn_play_pause_input.clicked.connect(lambda: self.play_audio(self.original_sig , 1 , self.ui.horizontalSlider , self.timer_1)) #this is for the input signal
        self.ui.btn_play_pasuse_output.clicked.connect(lambda: self.play_audio(self.modified_signal , 5 , self.ui.horizontalSlider_2 , self.timer_2)) #this is for the input signal

        self.ui.btn_fast_input.clicked.connect(lambda: self.playpack_speed(1))
        self.ui.btn_slow_input.clicked.connect(lambda: self.playpack_speed(0))
        
        self.ui.windows_tabs.currentChanged.connect(self.plot_window)
        
        # self.ui.btn_srt_begin_input.clicked.connect(lambda :self.pause(self.timer_1))
        self.ui.btn_srt_begin_input.clicked.connect(lambda :self.play_audio(self.original_sig , 1 , self.ui.horizontalSlider , self.timer_1))
        self.ui.btn_srt_begin_output.clicked.connect(lambda :self.play_audio(self.modified_signal , 1 , self.ui.horizontalSlider_2 , self.timer_2))
        
        self.ui.verticalSlider_23.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["cat"] ,self.ui.verticalSlider_23.value() )) #this is for the input signal
        self.ui.verticalSlider_28.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["dog"] ,self.ui.verticalSlider_28.value() )) #this is for the input signal
        self.ui.verticalSlider_30.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["duck"] ,self.ui.verticalSlider_30.value() )) #this is for the input signal
        # self.ui.verticalSlider_33.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["elephant"] ,self.ui.verticalSlider_33.value() )) #this is for the input signal
        self.ui.verticalSlider_33.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["cow"] ,self.ui.verticalSlider_33.value() )) #this is for the input signal

        self.ui.verticalSlider_21.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["bass"] ,self.ui.verticalSlider_21.value() )) #this is for the input signal
        self.ui.verticalSlider_25.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["Voil_c5"] ,self.ui.verticalSlider_25.value() )) #this is for the input signal
        self.ui.verticalSlider_26.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["p"] ,self.ui.verticalSlider_26.value() )) #this is for the input signal
        self.ui.verticalSlider_29.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["drum"] ,self.ui.verticalSlider_29.value() )) #this is for the input signal

        # self.ui.verticalSlider_15.valueChanged.connect(self.uniform_ranges) #this is for the input signal
        self.ui.verticalSlider_15.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[0] ,self.ui.verticalSlider_15.value() )) #this is for the input signal
        self.ui.verticalSlider_17.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[1] ,self.ui.verticalSlider_17.value() )) #this is for the input signal
        self.ui.verticalSlider_16.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[2] ,self.ui.verticalSlider_16.value() )) #this is for the input signal
        self.ui.verticalSlider_14.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[3] ,self.ui.verticalSlider_14.value() )) #this is for the input signal
        self.ui.verticalSlider.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[4] ,self.ui.verticalSlider.value() )) #this is for the input signal
        self.ui.verticalSlider_11.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[5] ,self.ui.verticalSlider_11.value() )) #this is for the input signal
        self.ui.verticalSlider_24.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[6] ,self.ui.verticalSlider_24.value() )) #this is for the input signal
        self.ui.verticalSlider_13.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[7] ,self.ui.verticalSlider_13.value() )) #this is for the input signal
        self.ui.verticalSlider_12.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[8] ,self.ui.verticalSlider_12.value() )) #this is for the input signal
        self.ui.verticalSlider_20.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[9] ,self.ui.verticalSlider_20.value() )) #this is for the input signal

        self.freq_ranges = {
            "cat" : [(2200 , 2400)  , (550 , 600) , (1700 , 1800) , (2800 , 3000)],
            "dog" : [(220 , 300 ) , (520 , 680) , (800 , 850) , (900,  1000) , (1060 , 110) , (1040 , 1220)],
            "duck" :[ (800, 2500)],
            "cow" : [(250, 400)],
            "elephant" : [(100 , 300) ]  , 
            "bass" : [(0 , 400)] , 
            "glock" : [(650 , 400) , (690 , 710) , (785 , 790) , (833 , 836),  (936 , 942) , (992 , 996) , (1070 , 1090) , (1315 , 1340) , (1400 , 1415)] , 
            "voil" : [(485 ,500) , (515 ,530) , (770 , 790) , (980 , 1000),  (1030 , 1065) , (1480 , 1490) , (1560 , 1580) , (1970 , 1985) , (2085 , 2110) , (2460 , 2480) , (2600 , 2630) , (2970 , 2980) , (3130 , 3155) , (3454 , 3477) , (3654 , 3680)] , 
            "Voil_c5" : [(510 , 540 ) , (1020 , 1060) ,  (1530 , 1590) , (2060 , 2120) , (2570 , 640)],
            "T" : [(775 , 795 ) , (1560 , 1580) ,  (2345 , 2365) ],
            "f" : [(1540 , 1610 ) ],
            "p" : [(260 , 264 ) , (520 , 532) ,  (780 , 790) , (1045 , 1052) , (1574 , 1584) , (1840 , 1850)],
            # "p" : [(255 , 267 ) , (218 , 532) ,  (780 , 790) , (1045 , 1052) , (1574 , 1584) , (1840 , 1850)],
            "drum" : [(0 , 250)],
            # "uniform":[(0 , 2000) , (2000 , 4000) , (4000 , 6000) , (6000 , 8000) , (8000 , 10000) (10000 , 12000), (12000 , 14000) , (14000 , 16000) , (16000 , 18000) , (18000, 20000)]

            
        }

        QShortcut(QKeySequence("Ctrl+o"), self).activated.connect(self.upload_signal_file)
        

    def handleComboBox(self, index):
        # Hide or show controls in the stacked widget based on the index
        self.ui.stackedWidget.setCurrentIndex(index)
    
    def update_slider(self , slider):
        current_value = slider.value()
        if current_value < slider.maximum():
            slider.setValue(current_value + 100)  # Increment by 100 milliseconds
   
    def uniform_ranges(self ):
        _ , __  , freq = self.fourier_function()
        freq_batches = np.array_split(freq, 20)
        freq_ranges = [[(batch[0], batch[-1])] for batch in freq_batches]
        return(freq_ranges)    
    
   
    def min_max(self):
        '''
        this funcrion is to cala the min and max of graph to set it limits
        '''

        x_min, x_max = self.ui.grph_input_sig.getViewBox().viewRange()[0]
        y_min, y_max = self.ui.grph_input_sig.getViewBox().viewRange()[1]

        return x_min  , x_max , y_min , y_max
        
        
    def upload_signal_file(self):
        
        file_path , _ = QFileDialog.getOpenFileName(self, "Open Song", "~")
        
            
        if file_path[-3:]== "csv":
            self.is_ecg = True
            print("csvvv")
            df = pd.read_csv(file_path)
            t = df.iloc[:, 0].values
            self.original_sig = df.iloc[:, 1].values
            self.ui.grph_input_sig.clear()
            self.ui.grph_input_sig.plot(t , self.original_sig)
            self.sample_rate = 125
            self.spectogram(self.original_sig , 125 , self.spectrogram_canvas_input)
            # self.play_audio(self.original_sig , 1 ,self.ui.horizontalSlider , self.timer_1 )
            
        elif file_path[-3:]== "wav":
            print("wavvv")
            self.sample_rate, self.original_sig = wavfile.read(file_path)
            self.is_loaded = True
            self.plot_audio_signal(self.original_sig , self.sample_rate , self.ui.grph_input_sig)

        else :
            pass

            
            
        self.fourier_function()
        
    def plot_audio_signal(self , samples , sampling_rate , widget):
        peak_value = np.amax(samples)
        samples = samples / peak_value
        self.length = samples.shape[0] / sampling_rate
        print(f"self.length :  {self.length}")
        print(f"shape :  {samples.shape}")
        time = np.array(range(0 , len(samples) )) / sampling_rate
        print(f"time {len(time)}")
        drawing_pen = pg.mkPen(color=(255, 0, 0), width=0.5)
        widget.clear()
        widget.plot(time, samples, pen=drawing_pen)
        self.spectogram(self.original_sig , self.sample_rate , self.spectrogram_canvas_input)
  
    def fourier_function(self):
        complex_fft = np.fft.rfft(self.original_sig)
        # magnitude = np.abs(complex_fft)
        magnitude = np.abs(complex_fft / len(self.original_sig))
        phase = np.angle(complex_fft)
        frequency = np.fft.rfftfreq(len(self.original_sig), 1 / self.sample_rate)
        
        self.ui.signal_view.plot(frequency[:len(frequency)//2] , magnitude[:len(frequency)//2])

        return magnitude, phase, frequency

    def window_function(self   , length  ,  window_type  , range ):
        print(f"here{window_type}")
        if window_type == 0 :
            window = np.ones(length) 
            print(0)
        elif window_type == 1:
            window = np.hamming(length)
            print(1)
        elif window_type == 2:
            window = np.hanning(length)
            print(2)
        elif window_type == 3:
            window = gaussian(length , length/2)
        
        return window
            
    def playpack_speed(self , speed):
        if speed == 1:
            self.sample_rate += self.sample_rate*.25
        else :
            self.sample_rate -= self.sample_rate*.25
        self.length = self.original_sig.shape[0] / self.sample_rate
        
        
    def modfy_frq_component(self, freq_range , slider_gain ):
        print(freq_range)
        print("please")
        windows = []
        magnitude, phase, frequency = self.fourier_function()
        for range in freq_range:
            indices_to_modify = np.where((frequency >= range[0]) & (frequency <= range[1]))[0]
            
            window = self.window_function( len(magnitude[indices_to_modify])  , self.ui.windows_tabs.currentIndex() , range) 
            magnitude[indices_to_modify] *= slider_gain *window
            windows.append((window * max(magnitude[indices_to_modify]) ,frequency[indices_to_modify]))
        complex_signal = magnitude * np.exp(1j * phase)
        self.modified_signal = np. fft.irfft(complex_signal)
        self.spectogram(self.modified_signal , self.sample_rate , self.spectrogram_canvas_output)

        
        self.ui.signal_view.clear()
        self.ui.signal_view.plot(frequency[:len(frequency)//2] , magnitude[:len(frequency)//2])

        self.plot_audio_signal(self.modified_signal , self.sample_rate , self.ui.grph_output_sig )
        self.ui.graphicsView_rectangle.clear()
        for (window , range) in windows:
            self.ui.signal_view.plot(frequency[indices_to_modify] , magnitude[indices_to_modify])
            # self.ui.graphicsView_rectangle.plot(frequency[indices_to_modify] , magnitude[indices_to_modify])
            # self.ui.graphicsView_rectangle.plot( window , pen ="r")
            print(range)
            self.ui.signal_view.plot(range , window , pen = pg.mkPen(color=(255, 0, 0), width=0.5))

    def plot_window(self  ):
        # window = self.window_function()
        print("dd")
        window = self.window_function(50000 ,  self.ui.windows_tabs.currentIndex() , 2500)
        if self.ui.windows_tabs.currentIndex() ==0:
            print("0")
            # self.ui.graphicsView_rectangle.plot( , pen ="r")

            self.ui.graphicsView_rectangle.plot(window)
        elif self.ui.windows_tabs.currentIndex() ==1:
            print("1")
            self.ui.graphicsView_hamming.plot(window)
        elif self.ui.windows_tabs.currentIndex() ==2:
            print("2")
            self.ui.graphicsView_hanning.plot(window)
            print("3")
        elif self.ui.windows_tabs.currentIndex() ==3:   
            self.ui.graphicsView_gaussian.plot(gaussian(5 , 1))

    def pause(self , timer):
        timer.stop()
        sd.stop()
        
    def play_audio(self, signal , k , slider , timer):
        slider.setValue(0)
        sd.play(signal *k , self.sample_rate)
        slider.setMaximum(int(self.length*1000))  # Assuming 5 seconds, as the range is in milliseconds
        print(f"lengt{self.length} slide{slider.maximum()}")

        timer.start(100)
        
    def spectogram(self  ,signal , sample_rate ,widget):
        widget.axes.clear()
        widget.axes.specgram(signal , Fs = sample_rate)
        widget.draw()
        

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
