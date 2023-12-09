from scipy import signal
from scipy.signal import gaussian
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import  QApplication, QMainWindow, QShortcut, QFileDialog , QSplitter , QFrame , QSlider
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
        
        self.uin_sliders = []
        self.ui.chek_bx_show_spect_input.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_input.isChecked(), self.spectrogram_canvas_input))
        self.ui.chek_bx_show_spect_output.stateChanged.connect(lambda : self.show_hide_specto_grph( self.ui.chek_bx_show_spect_output.isChecked(), self.spectrogram_canvas_output))

        self.ui.btn_zoom_in_input.clicked.connect(lambda: self.zoom( 1 / 1.2))
        self.ui.btn_zoom_out_input.clicked.connect(lambda: self.zoom(  1.2))

        self.ui.btn_zoom_in_output.clicked.connect(lambda: self.zoom( 1))
        self.ui.btn_zoom_out_output.clicked.connect(lambda: self.zoom( 0))

        # self.ui.actionUpload_file.triggered.connect(self.upload_signal_file)
        
        self.ui.btn_play_input.clicked.connect(lambda: self.play_audio(self.original_sig , 1 , self.ui.input_slider , self.timer_1 , self.timer_2)) #this is for the input signal
        self.ui.btn_play_output.clicked.connect(lambda: self.play_audio(self.modified_signal , 5 , self.ui.output_slider , self.timer_2 , self.timer_1)) #this is for the input signal

        self.ui.btn_pause_input.clicked.connect(lambda:self.pause(self.timer_1))
        self.ui.btn_pause_output.clicked.connect(lambda:self.pause(self.timer_2))

        self.ui.btn_fast_input.clicked.connect(lambda: self.playpack_speed(1))
        self.ui.btn_slow_input.clicked.connect(lambda: self.playpack_speed(0))
        
        self.ui.windows_tabs.currentChanged.connect(self.plot_window)
        # self.ui.btn_apply.clicked.connect(self.modfy_frq_component())
        
        # self.ui.btn_srt_begin_input.clicked.connect(lambda :self.pause(self.timer_1))
        self.ui.btn_srt_begin_input.clicked.connect(lambda :self.play_audio(self.original_sig , 1 , self.ui.input_slider , self.timer_1 , self.timer_2))
        self.ui.btn_srt_begin_output.clicked.connect(lambda :self.play_audio(self.modified_signal , 8 , self.ui.output_slider , self.timer_2 ,self.timer_1 ))
        
        
        self.slider_names = ["bass", "voil", "piano", "drum" , "cat" , "dog" , "duck",  "cow" ,"arthmya_1" , "arthmya_2" , "arthmya_3"  , "arthmya_4"]

        for name in self.slider_names:
            slider = getattr(self.ui, f"{name}_slider")
            slider.valueChanged.connect(lambda value, n=name: self.modfy_frq_component(self.freq_ranges[n], value))

        
        for i in range(1, 11):
            slider = getattr(self.ui, f"uniform_slider_range_{i}")
            slider.valueChanged.connect(lambda value, idx=i-1: self.modfy_frq_component(self.uniform_ranges()[idx], value))

       
        self.freq_ranges = {
            "cat" :   [(500 , 605) , (1000 , 1200) , (2200 , 2400)  , (550 , 600) , (1700 , 1800) , (2750 , 3000) , (3300 , 3500) , (3900 , 4200) , (4500 , 4700 ) , (5100 , 5300)], #new sound not completly disapear but the cat sound is lowr
            "dog" :  [(200 , 1133) , (1150 , 1900)], #new so bad 
            "duck" :  [(400 , 550) , (800 , 840) ,( 880 , 920) , (960,  1000) , (1100 , 2200)], #duck2
            "cow" :   [(200, 400) , (500 , 700) , (790 , 860) , (800 , 1020) , (1040 , 1280) , (1300 , 1400)], #new and done (just the sound is lowered)
            
            "bass" : [(0 , 600)] ,  # new and done
            "voil" : [(504 , 556 ) , (1014 , 1070) ,  (1530 , 1601) , (2048 , 2120) , (2566 , 2644) , (3080 , 3190) , (3600, 3710 ) , (4120 , 4220)], # new (done but replaced with noise)
            "piano" : [(260 , 264 ) , (520 , 532) ,  (780 , 790) ,  (1045 , 1052) , (1574 , 1584) , (1840 , 1850)], #done
            "drum" : [(25 , 150) , (156 , 170  ) , (200 , 264) ,(264 , 300) , (360 , 440) , (485 , 520 ), (532 , 640) , (640 , 780)  , (900 , 950 ) , (1020 , 1045) , (1052 , 1140) , (1160 , 1220) , (1300 , 1350)  , (1420 , 1460) , (1540 , 1600) , (1680 , 1730) , (1830 , 1860) , (1960 , 2000) , (2090 , 2130) , (2220 , 2270) , (2370 , 2400) , (2780 , 2810) , (2920 , 2950) , (3060 , 3090) , (3190 , 3220) ], #new gitur

            "arthmya_1" : [(81 , 100) , (58 , 75) , (160, 175)],
            "arthmya_2" : [(110 , 120) , (140 , 150) ],
            "arthmya_3" : [(81 , 100)  ,(268 , 280 ) , (140 , 150) , (190 , 200)],

            
        }
        self.slider_history = [1]

        QShortcut(QKeySequence("Ctrl+o"), self).activated.connect(self.upload_signal_file)
    
        QShortcut(QKeySequence("Ctrl+m"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(1))
        QShortcut(QKeySequence("Ctrl+b"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(3))
        QShortcut(QKeySequence("Ctrl+p"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(2))
        QShortcut(QKeySequence("Ctrl+u"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(0))



    
    def handleComboBox(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
    
    def update_slider(self , slider):
        current_value = slider.value()
        if current_value < slider.maximum():
            slider.setValue(current_value + 100)  # Increment by 100 milliseconds
   
    def uniform_ranges(self ):
        freq_batches = np.array_split(self.frequency, 10)
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
        print(file_path)
        
        if file_path[-3:]== "csv":
            self.is_sound = False
            self.is_ecg = True
            print("csvvv")
            df = pd.read_csv(file_path)
            self.time = df.iloc[:, 0].values
            self.original_sig = df.iloc[:, 1].values
            self.sample_rate = 1/(self.time[1]-self.time[0])
            
        elif file_path[-3:]== "wav":
            self.is_sound = True
            self.is_ecg = False
            print("wavvv")
            self.sample_rate, self.original_sig = wavfile.read(file_path)
            self.time = np.array(range(0 , len(self.original_sig) )) / self.sample_rate

        self.plot_signal(self.time , self.original_sig , self.sample_rate , self.ui.grph_input_sig)
        
        self.reset_slider()
        
        self.fourier_function()
        
    def plot_signal(self ,time ,  samples , sampling_rate , widget):

        self.length = samples.shape[0] / sampling_rate
        time = np.array(range(0 , len(samples) )) / sampling_rate
        widget.clear()
        widget.plot(time, samples)
        # widget.plotItem.vb.setLimits( xMin=min(time) , xMax=max(time), yMin=min(samples) , yMax=max(samples)) 
        widget.getViewBox().autoRange()
        self.spectogram(self.original_sig , self.sample_rate , self.spectrogram_canvas_input)
  
    def fourier_function(self):
        complex_fft = np.fft.rfft(self.original_sig)
        self.magnitude = np.abs(complex_fft / len(self.original_sig))
        self.phase = np.angle(complex_fft)
        self.frequency = np.fft.rfftfreq(len(self.original_sig), 1 / self.sample_rate)
        self.magnitude_to_bodfy = self.magnitude.copy()
        
        print(f"freq shape {self.frequency.shape} ,magnitude.shape {self.magnitude.shape}")
        print(f"slef.magnitude {self.magnitude}")
        
        
        self.plot_specrtum(self.frequency , self.magnitude)
        self.plot_window()
        
        


    def window_function(self   , length  ,  window_type  ):
        print(f"here{window_type}")
        if window_type == 0 :
            window = np.hamming(length)
        elif window_type == 1:
            window = signal.windows.boxcar(length) 
        elif window_type == 2:
            window = np.hanning(length)
        elif window_type == 3:
            window = gaussian(length , std = int(self.ui.std_input.text()))
        
        return window
            
    def playpack_speed(self , speed):
        if speed == 1:
            self.sample_rate += self.sample_rate*.25
        else :
            self.sample_rate -= self.sample_rate*.25
        self.length = self.original_sig.shape[0] / self.sample_rate
        
        
    def modfy_frq_component(self, freq_range , slider_gain ):
        all_indices = np.array([], dtype=int)
        print(freq_range)
        print("please")
        windows = []
        for range in freq_range:
            indices_to_modify = np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0]
            all_indices = np.concatenate((all_indices, indices_to_modify))
        
        

        all_indices = np.sort(all_indices)
        window = self.window_function( len(self.magnitude[all_indices])  , self.ui.windows_tabs.currentIndex() ) 

        self.magnitude_to_bodfy[all_indices] = self.magnitude[all_indices] * slider_gain *window
        print(f"diff : {self.magnitude_to_bodfy[all_indices] - self.magnitude[all_indices]}")
        windows.append((window * max(self.magnitude_to_bodfy[all_indices]) ,self.frequency[all_indices]))

        
        
        self.plot_specrtum(self.frequency , self.magnitude_to_bodfy)
        
        if self.ui.combo_bx_mode.currentIndex() == 0:
            print("uniform mode")
            window = self.window_function(1102, self.ui.windows_tabs.currentIndex())
    
            for range in self.uniform_ranges():
                my_range = np.where((self.frequency >= range[0][0]) & (self.frequency <= range[0][1]))[0]
                print(f"range[0]{range}")
                print(f"points{int(range[0][0])}, {int(range[0][1])}")
                self.ui.signal_view.plot(self.frequency[my_range] , self.window_function(len(self.frequency[my_range] ), self.ui.windows_tabs.currentIndex()) *max(self.magnitude_to_bodfy[my_range]) , pen =pg.mkPen(color=(255, 0, 0)))
            print(f"range length {len(self.frequency[int(range[0][0]) :int(range[0][1])])}")

            # for window in windows:
        else:
            for range in freq_range:
                print(f"range[0]{range}")
                my_range = np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0]
                self.ui.signal_view.plot(self.frequency[my_range] , self.window_function(len(self.frequency[my_range] ), self.ui.windows_tabs.currentIndex()) *max(self.magnitude_to_bodfy[my_range]) , pen =pg.mkPen(color=(255, 0, 0)))
        

        complex_signal = self.magnitude_to_bodfy * np.exp(1j * self.phase)
        self.modified_signal = np. fft.irfft(complex_signal)
        self.plot_signal(self.time ,self.modified_signal , self.sample_rate , self.ui.grph_output_sig )
        self.spectogram(self.modified_signal , self.sample_rate , self.spectrogram_canvas_output)  

    def plot_specrtum(self , freq , magnitude):
        self.ui.signal_view.clear()
        self.ui.signal_view.plot(freq , magnitude)
        # self.ui.signal_view.plotItem.vb.setLimits( xMin=min(freq) , xMax=max(freq), yMin=min(magnitude) , yMax=max(magnitude)) 
        self.ui.signal_view.getViewBox().autoRange()
        
   
    def reset_slider(self):
        for i in range(1, 10):
            slider_name = f'uniform_slider_range_{i}'
            current_slider = getattr(self.ui, slider_name)
            current_slider.setValue(1)
            
        for name in self.slider_names:
            slider = getattr(self.ui, f"{name}_slider")
            slider.setValue(1)

    def plot_window(self  ):
        window = self.window_function(50000 ,  self.ui.windows_tabs.currentIndex() )
        if self.ui.windows_tabs.currentIndex() ==0:
            self.ui.graphicsView_hamming.plot(window)
        elif self.ui.windows_tabs.currentIndex() ==1:
            self.ui.graphicsView_rectangle.plot(window)
        elif self.ui.windows_tabs.currentIndex() ==2:
            self.ui.graphicsView_hanning.plot(window)
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
        self.ui.grph_input_sig.getViewBox().scaleBy((state, state))
        self.ui.grph_output_sig.getViewBox().scaleBy((state, state))
        
          
      

def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
