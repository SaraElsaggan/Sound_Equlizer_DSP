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
from mainwindow import Ui_MainWindow , PlotWidget 
from pyqtgraph import PlotWidget, ROI

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
        # self.ui.std_input.setText("5000")
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


        self.ui.actionUpload_file.triggered.connect(self.upload_signal_file)
        
        self.ui.btn_play_input.clicked.connect(lambda: self.play_audio(self.original_sig , 1 , self.ui.input_slider , self.timer_1 , self.timer_2)) #this is for the input signal
        self.ui.btn_play_output.clicked.connect(lambda: self.play_audio(self.modified_signal , 8 , self.ui.output_slider , self.timer_2 , self.timer_1)) #this is for the input signal

        self.ui.btn_pause_input.clicked.connect(lambda:self.pause(self.timer_1))
        self.ui.btn_pause_output.clicked.connect(lambda:self.pause(self.timer_2))

        self.ui.btn_fast_input.clicked.connect(lambda: self.playpack_speed(.25))
        self.ui.btn_slow_input.clicked.connect(lambda: self.playpack_speed(-.25))
        
        self.ui.windows_tabs.currentChanged.connect(lambda :self.window_function(5000 , self.ui.windows_tabs.currentIndex()))
        self.ui.std_slider.valueChanged.connect(lambda :self.window_function(5000 , self.ui.windows_tabs.currentIndex()))
        self.ui.std_slider.valueChanged.connect(lambda value: self.ui.std_lbl.setText(str(value)))
        self.ui.btn_srt_begin_input.clicked.connect(lambda :self.play_audio(self.original_sig , 1 , self.ui.input_slider , self.timer_1 , self.timer_2))
        
       
        self.freq_ranges = {
            "wolf" :  [(187.5, 1300)] ,
            "horse" :   [(1300, 3300)], 
            "bat" :  [(3300, 6000)], 
            # "wolf" :  [(170, 1290)] ,
            # "duck" :   [(6000  , 20000)],
            "duck" :   [(140  , 190) , (220 , 360) , (500 , 720) , (800 , 1080)],# cow 
            # "duck" :   [(2000, 7500) , (16000, 20000)],

            "xylophone" : [(300, 1000) ],    
            "triangle" : [(4200, 22000)] ,
            # "xylophone" : [(0, 300) ],     
            # "triangle" : [(1000, 22000)] ,
            "voil" : [(504 , 556 ) , (1014 , 1070) ,  (1530 , 1601) , (2048 , 2120) , (2566 , 2644) , (3080 , 3190) , (3600, 3710 ) , (4120 , 4220)], # new (done but replaced with noise)
            "piano" : [(0 ,10) , (60 , 80) , (100 , 200) , (240 , 280 ) , (260 , 264 ) , (480 , 580), (520 , 532) ,  (780 , 790) ,  (1045 , 1052) , (1574 , 1584) , (1840 , 1850) , (2000 , 2200) , (2350 , 2450) , (2640 , 2680) , (2900 , 2950 ), (3180,3260) ], #done
          
            "arthmya_1" : [( 0,12 )], 
            "arthmya_2" : [(405 , 589)], 
            
            "arthmya_3" : [(40 , 70) ], 
            # "arthmya_3" : [(95 , 105)  , (140 , 155) ], 

        }
        for i in range(10):
            self.freq_ranges[f"range_{i+1}"] = []
   
   
        for name in self.freq_ranges:
            slider = getattr(self.ui, f"{name}_slider")
            slider.valueChanged.connect(lambda value, n=name: self.modfy_frq_component(self.freq_ranges[n], value))
      
            # slider.valueChanged.connect(lambda value : self.update_tooltip(slider , value))
            slider.valueChanged.connect(lambda value, s=slider: self.update_tooltip(s, value))

            
            # slider.setToolTip(f"{slider.value()}")

    

        QShortcut(QKeySequence("Ctrl+o"), self).activated.connect(self.upload_signal_file)
        QShortcut(QKeySequence("Ctrl+m"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(1))
        QShortcut(QKeySequence("Ctrl+b"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(3))
        QShortcut(QKeySequence("Ctrl+n"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(2))
        QShortcut(QKeySequence("Ctrl+u"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(0))

        QShortcut(QKeySequence("Ctrl+z"), self).activated.connect(self.save_sound_file)
        QShortcut(QKeySequence("Ctrl+s"), self).activated.connect(self.save_ecg_file)

    def save_sound_file(self):
        modified_file_path, _ = QFileDialog.getSaveFileName(self, "Save Modified Signal", "~", "WAV Files (*.wav);;All Files (*)")
        # output_file_path = "path/to/your/output/file.wav"
        if modified_file_path:
            wavfile.write(modified_file_path, self.sample_rate, self.modified_signal)
        
    def save_ecg_file(self):
        # modified_df = pd.DataFrame({np.arange(0, len(self.modified_signal)) / self.sample_rate, self.modified_signal})
        # modified_df = pd.DataFrame({np.arange(0, len(self.modified_signal)) / self.sample_rate, self.modified_signal})
        # modified_df = pd.DataFrame([np.arange(0, len(self.modified_signal)) / self.sample_rate, self.modified_signal])
# 

        modified_df = pd.DataFrame({'Time': np.arange(0, len(self.modified_signal)) / self.sample_rate,'Modified_Signal': self.modified_signal})
        
        modified_file_path, _ = QFileDialog.getSaveFileName(self, "Save Modified Signal", "~", "CSV Files (*.csv)")
        if modified_file_path:
                modified_df.to_csv(modified_file_path, index=False)
    
    def update_tooltip(self , slider , slider_value):
        # Set the tooltip to be the current value of the slider
        slider.setToolTip(f"{str(slider_value)} db")
        
    def handleComboBox(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
   
    def uniform_ranges(self ):
        freq_batches = np.array_split(self.frequency, 10)
        for i, batch in enumerate(freq_batches):
            idx=i+1
            lbl = getattr(self.ui, f"range_{idx}_lbl")
            key = f"range_{idx}"
            lbl.setText(f"{int(batch[0])} ,{int(batch[-1])} ")
            if self.freq_ranges[key]:
                self.freq_ranges[key].clear()

            self.freq_ranges[key].append((batch[0], batch[-1]))

  
    
   
   
         
    def upload_signal_file(self):
        
        self.file_path , _ = QFileDialog.getOpenFileName(self, "Open file", "~")
        
        if self.file_path[-3:]== "csv":
            df = pd.read_csv(self.file_path)
            self.time = df.iloc[:, 0].values
            self.original_sig = df.iloc[:, 1].values
            self.sample_rate = 1/(self.time[1]-self.time[0])
            
        elif self.file_path[-3:]== "wav":
            self.sample_rate, self.original_sig = wavfile.read(self.file_path)
            self.time = np.array(range(0 , len(self.original_sig) )) / self.sample_rate

        self.plot_signal(self.time , self.original_sig , self.sample_rate , self.ui.grph_input_sig)
        self.reset_slider()
        self.ui.grph_output_sig.clear()
        
        
        self.fourier_function()
        self.uniform_ranges()
        
    def plot_signal(self ,time ,  samples , sampling_rate , widget):
    

        self.length = samples.shape[0] / sampling_rate
        time = np.array(range(0 , len(samples) )) / sampling_rate
        widget.clear()
        widget.plot(time, samples)
        widget.getViewBox().autoRange()
        self.spectogram(self.original_sig , self.sample_rate , self.spectrogram_canvas_input)
  
    def fourier_function(self):
        complex_fft = np.fft.rfft(self.original_sig)
        self.magnitude = np.abs(complex_fft / len(self.original_sig))
        self.phase = np.angle(complex_fft)
        self.frequency = np.fft.rfftfreq(len(self.original_sig), 1 / self.sample_rate)
        self.magnitude_to_bodfy = self.magnitude.copy()
        
        
        
        self.plot_specrtum(self.frequency , self.magnitude)
        
        


    def window_function(self   , length  ,  window_type  ):
        
        if window_type == 0 :
            window = np.hamming(length)
        elif window_type == 1:
            window = signal.windows.boxcar(length) 
        elif window_type == 2:
            window = np.hanning(length)
        elif window_type == 3:
            # window = gaussian(length , std = int(self.ui.std_input.text()))
            window = gaussian(length , std = self.ui.std_slider.value())

        
        page_widget = self.ui.windows_tabs.widget(window_type)
        graph_widget = page_widget.findChild(PlotWidget)
        graph_widget.clear()
        graph_widget.plot(window)

        return window
            
    def playpack_speed(self , speed):
        self.sample_rate += self.sample_rate*speed
        self.length = self.original_sig.shape[0] / self.sample_rate
        
        
    def modfy_frq_component(self, freq_range , slider_gain ):
        
        all_indices = np.array([], dtype=int)
        for range in freq_range:
            indices_to_modify = np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0]
            #self.frequency >= range[0]
            all_indices = np.concatenate((all_indices, indices_to_modify))
        
        

        all_indices = np.sort(all_indices)
        window = self.window_function( len(self.magnitude[all_indices])  , self.ui.windows_tabs.currentIndex() ) 

        # outside_indices = np.setdiff1d(np.arange(len(self.frequency)), all_indices)

        # # Modify the magnitude for elements outside all_indices
        # self.magnitude_to_bodfy[outside_indices] = self.magnitude[outside_indices] * 0

        # self.ui.xylophone_slider.setMinimum(-50)
        # self.ui.xylophone_slider.setMaximum(50)
        # # min_db = -50
        # max_db = 50
        # max_linear_value = 100

        # db_value = min_db + (slider_gain / max_linear_value) * (max_db - min_db)
        self.magnitude_to_bodfy[all_indices] = self.magnitude[all_indices] * (10 ** (slider_gain / 20))*window
        # print(f"slider_value :{self.ui.xylophone_slider.value()}")
        # x = 10 ** (slider_gain / 20)
        # print(f"db_value :{x}")
        # self.magnitude_to_bodfy[all_indices] = self.magnitude[all_indices] * slider_gain *window

        
        
        self.plot_specrtum(self.frequency , self.magnitude_to_bodfy)
        complex_signal = self.magnitude_to_bodfy * np.exp(1j * self.phase)
        self.modified_signal = np. fft.irfft(complex_signal)
        self.plot_signal(self.time ,self.modified_signal , self.sample_rate , self.ui.grph_output_sig )
        self.spectogram(self.modified_signal , self.sample_rate , self.spectrogram_canvas_output)  
        
        self.plot_windw( freq_range)

    
    def plot_specrtum(self , freq , magnitude):
        self.ui.signal_view.clear()
        self.ui.signal_view.plot(freq , magnitude)
        self.ui.signal_view.getViewBox().autoRange()
        
        
        
   
    def plot_windw(self , freq_range):
        ranges = []
        if self.ui.combo_bx_mode.currentIndex() == 0:
            for _ ,range in list(self.freq_ranges.items())[10:]:
                ranges.append(np.where((self.frequency >= range[0][0]) & (self.frequency <= range[0][1]))[0])
            
        else:
            for range in freq_range:
                ranges.append(np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0])

        self.plot(ranges)

    def plot(self , ranges  ):
        for my_range in ranges:
            self.ui.signal_view.plot(self.frequency[my_range] , self.window_function(len(self.frequency[my_range] ), self.ui.windows_tabs.currentIndex()) *max(self.magnitude_to_bodfy[my_range]) , pen =pg.mkPen(color=(255, 0, 0)))
        
        
    def reset_slider(self):
        for name in self.freq_ranges:
            slider = getattr(self.ui, f"{name}_slider")
            slider.setValue(0)


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
        
     
    def update_slider(self , slider):
        current_value = slider.value()
        if current_value < slider.maximum():
            slider.setValue(current_value + 100)  
   
      

def main():
    app = QApplication(sys.argv)
    window = MyWindow() 
   
   
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
