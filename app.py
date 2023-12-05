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
        self.ui.specto_layout_input.addWidget(self.spectrogram_canvas_input)
        self.ui.specto_layout_output.addWidget(self.spectrogram_canvas_output)
        
        self.timer_1 = QTimer(self)
        self.timer_1.timeout.connect(lambda :self.update_slider( self.ui.input_slider))
        self.ui.input_slider.setMinimum(0)
        self.ui.input_slider.setValue(0)
        
        self.timer_2 = QTimer(self)
        self.timer_2.timeout.connect(lambda :self.update_slider( self.ui.output_slider))
        self.ui.output_slider.setMinimum(0)
        self.ui.output_slider.setValue(0)
        
        
        self.ui.chek_bx_show_spect_input.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_input.isChecked(), self.spectrogram_canvas_input))
        self.ui.chek_bx_show_spect_output.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_output.isChecked(), self.spectrogram_canvas_output))

        self.ui.btn_zoom_in_input.clicked.connect(lambda: self.zoom( 1))
        self.ui.btn_zoom_out_input.clicked.connect(lambda: self.zoom( 0))

        self.ui.btn_zoom_in_output.clicked.connect(lambda: self.zoom( 1))
        self.ui.btn_zoom_out_output.clicked.connect(lambda: self.zoom( 0))

        self.ui.actionUpload_file.triggered.connect(self.upload_signal_file)
        
        self.ui.btn_play_input.clicked.connect(lambda: self.play_audio(self.original_sig , 1 , self.ui.input_slider , self.timer_1 , self.timer_2)) #this is for the input signal
        self.ui.btn_play_output.clicked.connect(lambda: self.play_audio(self.modified_signal , 5 , self.ui.output_slider , self.timer_2 , self.timer_1)) #this is for the input signal

        self.ui.btn_pause_input.clicked.connect(lambda:self.pause(self.timer_1))
        self.ui.btn_pause_output.clicked.connect(lambda:self.pause(self.timer_2))

        self.ui.btn_fast_input.clicked.connect(lambda: self.playpack_speed(1))
        self.ui.btn_slow_input.clicked.connect(lambda: self.playpack_speed(0))
        
        self.ui.windows_tabs.currentChanged.connect(self.plot_window)
        
        # self.ui.btn_srt_begin_input.clicked.connect(lambda :self.pause(self.timer_1))
        self.ui.btn_srt_begin_input.clicked.connect(lambda :self.play_audio(self.original_sig , 1 , self.ui.input_slider , self.timer_1))
        self.ui.btn_srt_begin_output.clicked.connect(lambda :self.play_audio(self.modified_signal , 8 , self.ui.output_slider , self.timer_2))
        
        self.ui.cat_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["cat"] ,self.ui.cat_slider.value() )) 
        self.ui.dog_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["dog"] ,self.ui.dog_slider.value() )) 
        self.ui.duck_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["duck"] ,self.ui.duck_slider.value() )) 
        # self.ui.cow_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["elephant"] ,self.ui.cow_slider.value() )) 
        self.ui.cow_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["cow"] ,self.ui.cow_slider.value() )) 

        self.ui.bass_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["bass"] ,self.ui.bass_slider.value() )) 
        self.ui.voil_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["Voil_c5"] ,self.ui.voil_slider.value() )) 
        self.ui.piano_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["piano"] ,self.ui.piano_slider.value() )) 
        self.ui.drum_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["drum"] ,self.ui.drum_slider.value() )) 

        # self.ui.uniform_slider_range_1.valueChanged.connect(self.uniform_ranges) 
        self.ui.uniform_slider_range_1.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[0] ,self.ui.uniform_slider_range_1.value() )) 
        self.ui.uniform_slider_range_2.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[1] ,self.ui.uniform_slider_range_2.value() )) 
        self.ui.uniform_slider_range_3.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[2] ,self.ui.uniform_slider_range_3.value() )) 
        self.ui.uniform_slider_range_4.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[3] ,self.ui.uniform_slider_range_4.value() )) 
        self.ui.uniform_slider_range_5.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[4] ,self.ui.uniform_slider_range_5.value() )) 
        self.ui.uniform_slider_range_6.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[5] ,self.ui.uniform_slider_range_6.value() )) 
        self.ui.uniform_slider_range_7.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[6] ,self.ui.uniform_slider_range_7.value() )) 
        self.ui.uniform_slider_range_8.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[7] ,self.ui.uniform_slider_range_8.value() )) 
        self.ui.uniform_slider_range_9.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[8] ,self.ui.uniform_slider_range_9.value() )) 
        self.ui.uniform_slider_range_10.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[9] ,self.ui.uniform_slider_range_10.value() )) 

        self.freq_ranges = {
            "cat" : [(2200 , 2400)  , (550 , 600) , (1700 , 1800) , (2800 , 3000)],
            "dog" : [(300 , 1700)],
            "duck" :[ (450 , 550) , (800 , 840) ,( 880 , 920) , (960,  1000) , (1100 , 2200)], #duck2
            "cow" : [(250, 400)],
            
            # "dog" : [(220 , 300 ) , (520 , 680) , (800 , 850) , (900,  1000) , (1060 , 110) , (1040 , 1220)],
            # "duck" :[ (800, 2500)], #duck2
            # "duck" :[ (0, 2500)], #duck2
            # "elephant" : [(100 , 300) ]  , 
            "bass" : [(0 , 400)] , 
            # "glock" : [(650 , 400) , (690 , 710) , (785 , 790) , (833 , 836),  (936 , 942) , (992 , 996) , (1070 , 1090) , (1315 , 1340) , (1400 , 1415)] , 
            # "voil" : [(485 ,500) , (515 ,530) , (770 , 790) , (980 , 1000),  (1030 , 1065) , (1480 , 1490) , (1560 , 1580) , (1970 , 1985) , (2085 , 2110) , (2460 , 2480) , (2600 , 2630) , (2970 , 2980) , (3130 , 3155) , (3454 , 3477) , (3654 , 3680)] , 
            "Voil_c5" : [(510 , 540 ) , (1020 , 1060) ,  (1530 , 1590) , (2060 , 2120) , (2570 , 2640)],
            # "T" : [(775 , 795 ) , (1560 , 1580) ,  (2345 , 2365) ],
            # "f" : [(1540 , 1610 ) ],
            "piano" : [(260 , 264 ) , (520 , 532) ,  (780 , 790) , (1045 , 1052) , (1574 , 1584) , (1840 , 1850)],
            # # "p" : [(255 , 267 ) , (218 , 532) ,  (780 , 790) , (1045 , 1052) , (1574 , 1584) , (1840 , 1850)],
            "drum" : [(0 , 250)],
            # # "uniform":[(0 , 2000) , (2000 , 4000) , (4000 , 6000) , (6000 , 8000) , (8000 , 10000) (10000 , 12000), (12000 , 14000) , (14000 , 16000) , (16000 , 18000) , (18000, 20000)]

            # "cat" : [(500 , 600)  , (100 , 1200) , (1600 , 1800) , (2200 , 2400) ], #cat_121
            # # "cat" : [(540 , 570)  , (590 , 605) , (1040 , 1140) , (1640 , 1700) , (1780, 1800) , (2200 , 2260), (1160,  1200)], #cat_121
            # "dog" : [(0 , 2000)],


            
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
    
   
    def min_max(self , grph_widget):
        '''
        this funcrion is to cala the min and max of graph to set it limits
        '''

        x_min, x_max = grph_widget.getViewBox().viewRange()[0]
        y_min, y_max = grph_widget.getViewBox().viewRange()[1]

        return x_min  , x_max , y_min , y_max
        
        
    def upload_signal_file(self):
        
        file_path , _ = QFileDialog.getOpenFileName(self, "Open Song", "~")
        
        self.ui.grph_input_sig.clear()
        self.ui.grph_output_sig.clear()
        if file_path[-3:]== "csv":
            self.is_ecg = True
            print("csvvv")
            df = pd.read_csv(file_path)
            # t = np.arange(0 , 7 , 1/125)
            t = df.iloc[:, 0].values
            self.original_sig = df.iloc[:, 1].values
            self.ui.grph_input_sig.clear()
            self.ui.grph_input_sig.plot(t , self.original_sig)
            self.ui.grph_input_sig.getViewBox().autoRange()
            
            self.sample_rate = 1/(t[1]-t[0])
            print(self.sample_rate)
            self.spectogram(self.original_sig , 60 , self.spectrogram_canvas_input)
            self.ui.grph_input_sig.plotItem.vb.setLimits(xMin=min(t), xMax=max(t), yMin=min(self.original_sig), yMax=max(self.original_sig))
            # self.play_audio(self.original_sig , 1 ,self.ui.input_slider , self.timer_1 )
            
        elif file_path[-3:]== "wav":
            print("wavvv")
            self.sample_rate, self.original_sig = wavfile.read(file_path)
            self.is_sound = True
            self.plot_audio_signal(self.original_sig , self.sample_rate , self.ui.grph_input_sig)
        
        self.reset_slider()
        

            
            
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
        widget.plotItem.vb.setLimits( xMin=min(time) , xMax=max(time), yMin=min(samples) , yMax=max(samples)) 
        widget.getViewBox().autoRange()
        self.spectogram(self.original_sig , self.sample_rate , self.spectrogram_canvas_input)
  
    def fourier_function(self):
        complex_fft = np.fft.rfft(self.original_sig)
        # magnitude = np.abs(complex_fft)
        magnitude = np.abs(complex_fft / len(self.original_sig))
        phase = np.angle(complex_fft)
        frequency = np.fft.rfftfreq(len(self.original_sig), 1 / self.sample_rate)
        
        self.ui.signal_view.clear()
        self.ui.signal_view.plot(frequency[:len(frequency)//2] , magnitude[:len(frequency)//2])
        self.ui.signal_view.plotItem.vb.setLimits( xMin=min(frequency[:len(frequency)//2]) , xMax=max(frequency[:len(frequency)//2]), yMin=min(magnitude[:len(frequency)//2]) , yMax=max(magnitude[:len(frequency)//2])) 
        self.ui.signal_view.getViewBox().autoRange()
        self.plot_window()
        
        

        return magnitude, phase, frequency

    def window_function(self   , length  ,  window_type  , range ):
        print(f"here{window_type}")
        if window_type == 0 :
            window = np.hamming(length)
            print(0)
        elif window_type == 1:
            window = np.ones(length) 
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
        self.ui.signal_view.plotItem.vb.setLimits( xMin=min(frequency[:len(frequency)//2]) , xMax=max(frequency[:len(frequency)//2]), yMin=min(magnitude[:len(frequency)//2]) , yMax=max(magnitude[:len(frequency)//2])) 
        self.ui.signal_view.getViewBox().autoRange()
        
        

        self.plot_audio_signal(self.modified_signal , self.sample_rate , self.ui.grph_output_sig )
        
        self.ui.graphicsView_rectangle.clear()
        for (window , range) in windows:
            self.ui.signal_view.plot(frequency[indices_to_modify] , magnitude[indices_to_modify])
            # self.ui.graphicsView_rectangle.plot(frequency[indices_to_modify] , magnitude[indices_to_modify])
            # self.ui.graphicsView_rectangle.plot( window , pen ="r")
            print(range)
            self.ui.signal_view.plot(range , window , pen = pg.mkPen(color=(255, 0, 0), width=0.5))

    def reset_slider(self):
        for i in range(1, 10):
            slider_name = f'uniform_slider_range_{i}'
            current_slider = getattr(self.ui, slider_name)
            print(current_slider.setValue(1))
        self.ui.cat_slider.setValue(1)
        self.ui.dog_slider.setValue(1)
        self.ui.duck_slider.setValue(1)
        self.ui.cow_slider.setValue(1)
        self.ui.piano_slider.setValue(1)
        self.ui.voil_slider.setValue(1)
        self.ui.drum_slider.setValue(1)
        self.ui.bass_slider.setValue(1)

    def plot_window(self  ):
        # window = self.window_function()
        print("dd")
        window = self.window_function(50000 ,  self.ui.windows_tabs.currentIndex() , 2500)
        if self.ui.windows_tabs.currentIndex() ==0:
            print("0")
            # self.ui.graphicsView_rectangle.plot( , pen ="r")

            self.ui.graphicsView_hamming.plot(window)
        elif self.ui.windows_tabs.currentIndex() ==1:
            print("1")
            self.ui.graphicsView_rectangle.plot(window)
        elif self.ui.windows_tabs.currentIndex() ==2:
            print("2")
            self.ui.graphicsView_hanning.plot(window)
            print("3")
        elif self.ui.windows_tabs.currentIndex() ==3:   
            self.ui.graphicsView_gaussian.plot(gaussian(5 , 1))

    def pause(self , timer):
        timer.stop()
        sd.stop()
        
    def play_audio(self, signal , k , slider , timer , timer_2):
        slider.setValue(0)
        timer_2.stop()
        sd.play(signal *k , self.sample_rate)
        slider.setMaximum(int(self.length*1000))  # Assuming 5 seconds, as the range is in milliseconds
        print(f"lengt{self.length} slide{slider.maximum()}")
        timer.start(100)
        
    def spectogram(self  ,signal , sample_rate ,widget):
        widget.axes.clear()
        widget.axes.specgram(signal ,  Fs = sample_rate)
        widget.draw()
        

    def show_hide_specto_grph(self  , state  , specto_grph_widget ):
        if state:
            specto_grph_widget.show()
        else:
            specto_grph_widget.hide()
      
    def zoom(self  , state): # it state = 0 zoom out , 1 zoom in
        if state:
            self.ui.grph_input_sig.getViewBox().scaleBy((1 / 1.2, 1 / 1.2))
            self.ui.grph_output_sig.getViewBox().scaleBy((1 / 1.2, 1 / 1.2))
        else:
            self.ui.grph_input_sig.getViewBox().scaleBy((1.2, 1.2))
            self.ui.grph_output_sig.getViewBox().scaleBy((1.2, 1.2))
        
          
      

def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
