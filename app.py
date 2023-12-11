'''
code reptesion done exept some part of  windowing
here is a function for the ecg signal
animal mode has some problems
gutar range is not the best
'''
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
        self.ui.std_input.setText("5000")
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


        # self.ui.actionUpload_file.triggered.connect(self.upload_signal_file)
        
        self.ui.btn_play_input.clicked.connect(lambda: self.play_audio(self.original_sig , 1 , self.ui.input_slider , self.timer_1 , self.timer_2)) #this is for the input signal
        self.ui.btn_play_output.clicked.connect(lambda: self.play_audio(self.modified_signal , 8 , self.ui.output_slider , self.timer_2 , self.timer_1)) #this is for the input signal

        self.ui.btn_pause_input.clicked.connect(lambda:self.pause(self.timer_1))
        self.ui.btn_pause_output.clicked.connect(lambda:self.pause(self.timer_2))

        self.ui.btn_fast_input.clicked.connect(lambda: self.playpack_speed(1))
        self.ui.btn_slow_input.clicked.connect(lambda: self.playpack_speed(0))
        
        self.ui.windows_tabs.currentChanged.connect(lambda :self.window_function(5000 , self.ui.windows_tabs.currentIndex()))
        # self.ui.btn_apply.clicked.connect(self.modfy_frq_component())
        
        # self.ui.btn_srt_begin_input.clicked.connect(lambda :self.pause(self.timer_1))
        self.ui.btn_srt_begin_input.clicked.connect(lambda :self.play_audio(self.original_sig , 1 , self.ui.input_slider , self.timer_1 , self.timer_2))
        
        
        # self.slider_names = ["bass", "voil", "piano", "drum" , "cat" , "dog" , "duck",  "cow" ,"arthmya_1" , "arthmya_2" , "arthmya_3"  , "arthmya_4" , "range_1", "range_2", "range_3", "range_4", "range_5", "range_6"]

    
        
        # for i in range(1, 11):
        #     slider = getattr(self.ui, f"uniform_slider_range_{i}")
        #     slider.valueChanged.connect(lambda value, idx=i-1: self.modfy_frq_component(self.uniform_ranges()[idx], value))

       
        self.freq_ranges = {
            "range_1":[],      
            "range_2":[],      
            "range_3":[],      
            "range_4":[],      
            "range_5":[],      
            "range_6":[],      
            "range_7":[],      
            "range_8":[],      
            "range_9":[],      
            "range_10":[],      
            
            
            


            "cat" :   [(90 , 120) , (260 , 320) , (500 , 605) , (1000 , 1200) , (2200 , 2400)  , (550 , 600) , (1700 , 1800) , (2750 , 3000) , (3300 , 3500) , (3900 , 4200) , (4500 , 4700 ) , (5100 , 5300)], #new sound not completly disapear but the cat sound is lowr cat1
            "dog" :  [(200 , 1133) , (1150 , 1900)], #new so bad 
            "duck" :  [(0 , 400) , (600 , 650) , (750 , 850) , (950 , 1090) , (1280 , 1340)], #duck2
            "cow" :   [(200, 400) , (500 , 700) , (790 , 860) , (800 , 1020) , (1040 , 1280) , (1300 , 1400)  , (1600 , 1640) , (1400, 1500) , (1560 , 1660)], #new and done (just the sound is lowered)
            
            "bass" : [(0 , 250) , (260 , 300) , (320 , 360) , (370 , 430) , (440 , 480)] ,  # new and done
            "voil" : [(504 , 556 ) , (1014 , 1070) ,  (1530 , 1601) , (2048 , 2120) , (2566 , 2644) , (3080 , 3190) , (3600, 3710 ) , (4120 , 4220)], # new (done but replaced with noise)
            "piano" : [(260 , 264 ) , (520 , 532) ,  (780 , 790) ,  (1045 , 1052) , (1574 , 1584) , (1840 , 1850)], #done
            "drum" : [(3120 , 3800) , (11500 , 12200)  , (8400 , 8800)  , (16200 , 16600) ], #new oxi   
          
            # ____case 1_____ norma_signal
            # "arthmya_1" : [(81 , 100) , (58 , 75) , (160, 175)], #arr_1
            # "arthmya_2" : [(110 , 120) , (140 , 150) ], # arr_2
            # "arthmya_3" : [(81 , 100)  ,(268 , 280 ) , (140 , 150) , (190 , 200)], # arr_2
            # "arthmya_4" : [(20 , 35) , (40 ,60), (76 , 80) , (96 , 112) , (124 , 140) , (152 , 162) , (174 , 192) , (200 , 220) , (230 , 240) , (250 , 270)  , (280 , 290) , (308 , 317) , (335 , 345) ],     #normal


            # ______
            # ____case 2_____ bidmc_01_Signals.csv not perfect
            # "arthmya_1" : [(2 , 2.9) , (5 , 5.9) ],
            # "arthmya_2" : [(6.6 , 7.5) , (17.4 , 18) ],
            # "arthmya_3" : [(9.5 , 10.5)  ,(12.8, 13.4) , (8 , 9)],
            # "arthmya_4" : [(1.4 , 2) , (2.9 , 3.4) , (4.4, 5) , (5.9 , 6.6) , (7.5 , 8) , (9 , 9.5) , (10.5 , 11.2) , (12 , 12.8) , (13.4 , 14.4) , (15 , 16) , (16.6 , 17.4) , (18 ,19)], #same as 2

            # ____case 3____ bidmc_02_Signals.csv
            # "arthmya_1" : [(2 , 2.9) , (5 , 5.9) ],
            # "arthmya_2" : [(6.6 , 7.5) , (17.4 , 18) ],
            # "arthmya_3" : [(9.5 , 10.5)  ,(12.8, 13.4) , (8 , 9)],
            # "arthmya_4" : [(1.4 , 2) , (2.9 , 3.4) , (4.4, 5) , (5.9 , 6.6) , (7.5 , 8) , (9 , 9.5) , (10.5 , 11.2) , (12 , 12.8) , (13.4 , 14.4) , (15 , 16) , (16.6 , 17.4) , (18 ,19)], #same as 1
            
            # ____case 4____ 
            # "arthmya_1" : [(22 , 34) , (38 , 42) , (49 , 51) ],
            # "arthmya_2" : [(25 , 31) , (9 , 20) ],
            # "arthmya_3" : [(52 , 54) , (63 , 67) , (13, 17) , (33 , 40)],
            # "arthmya_4" : [(1.2 , 1.3) , (2.6 , 2.9) , (4 , 4.2) , (5.3,  5.7) , (6.6 , 7.1) , (8 , 8.4) , (9.4 , 9.8) , (10.8 , 11.1), (12 , 12.4) ],
            
            # ____case 5____ 
            # "arthmya_1" : [(300 , 320) , (305 , 310) , (401 , 430)],
            # "arthmya_2" : [(160 , 163) , (153 , 159) , (197 , 202) , (207 , 220)],
            # "arthmya_3" : [(401 , 420) ,(250 , 273) , (309 , 415)],
            # "arthmya_4" : [(15 , 22) , (33 , 42) , (53 , 56) , (68 , 78) , (85 , 97) , (104 , 115) , (122 , 133), (140 , 152)],
            # "arthmya_4" : [(15 , 22) , (33 , 42) , (53 , 56) , (68 , 78) , (85 , 97) , (104 , 115) , (122 , 133), (140 , 152) , (158 , 170) , (177 , 188) , (195 , 203)],
            
            
            
            # final_case
            "arthmya_1" : [(81 , 100) , (58 , 75) , (160, 175)], #arr_1
            "arthmya_2" : [(6.6 , 7.5) , (17.4 , 18) ],
            "arthmya_3" : [(52 , 54) , (63 , 67) , (13, 17) , (33 , 40)],

            "arthmya_4" : [(1.4 , 2) , (2.9 , 3.4) , (4.4, 5) , (5.9 , 6.6) , (7.5 , 8) , (9 , 9.5) , (10.5 , 11.2) , (12 , 12.8) , (13.4 , 14.4) , (15 , 16) , (16.6 , 17.4) , (18 ,19)], #same as 2


            
            
        }
   
   
        for name in self.freq_ranges:
            slider = getattr(self.ui, f"{name}_slider")
            slider.valueChanged.connect(lambda value, n=name: self.modfy_frq_component(self.freq_ranges[n], value))

    
        self.slider_history = [1]

        QShortcut(QKeySequence("Ctrl+o"), self).activated.connect(self.upload_signal_file)
    
        QShortcut(QKeySequence("Ctrl+m"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(1))
        QShortcut(QKeySequence("Ctrl+b"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(3))
        QShortcut(QKeySequence("Ctrl+n"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(2))
        QShortcut(QKeySequence("Ctrl+u"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(0))



  
    def handleComboBox(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
    
    def update_slider(self , slider):
        current_value = slider.value()
        if current_value < slider.maximum():
            slider.setValue(current_value + 100)  # Increment by 100 milliseconds
   
    def uniform_ranges(self ):
        freq_batches = np.array_split(self.frequency, 10)
        for i, batch in enumerate(freq_batches):
            idx=i+1
            key = f"range_{idx}"

            if self.freq_ranges[key]:
                self.freq_ranges[key].clear()

            self.freq_ranges[key].append((batch[0], batch[-1]))

        # freq_ranges = [[(batch[0], batch[-1])] for batch in freq_batches]
        # return(freq_ranges)    
    
   
   
        
    def upload_signal_file(self):
        
        file_path , _ = QFileDialog.getOpenFileName(self, "Open Song", "~")
        
        if file_path[-3:]== "csv":
            df = pd.read_csv(file_path)
            self.time = df.iloc[:, 0].values
            self.original_sig = df.iloc[:, 1].values
            self.sample_rate = 1/(self.time[1]-self.time[0])
            
        elif file_path[-3:]== "wav":
            self.sample_rate, self.original_sig = wavfile.read(file_path)
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
        # widget.plotItem.vb.setLimits( xMin=min(time) , xMax=max(time), yMin=min(samples) , yMax=max(samples)) 
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
            window = gaussian(length , std = int(self.ui.std_input.text()))

        
        page_widget = self.ui.windows_tabs.widget(window_type)
        graph_widget = page_widget.findChild(PlotWidget)
        graph_widget.clear()
        graph_widget.plot(window)

        return window
            
    def playpack_speed(self , speed):
        if speed == 1:
            self.sample_rate += self.sample_rate*.25
        else :
            self.sample_rate -= self.sample_rate*.25
        self.length = self.original_sig.shape[0] / self.sample_rate
        
        
    def modfy_frq_component(self, freq_range , slider_gain ):
        all_indices = np.array([], dtype=int)
        windows = []
        for range in freq_range:
            indices_to_modify = np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0]
            all_indices = np.concatenate((all_indices, indices_to_modify))
        
        

        all_indices = np.sort(all_indices)
        window = self.window_function( len(self.magnitude[all_indices])  , self.ui.windows_tabs.currentIndex() ) 

        self.magnitude_to_bodfy[all_indices] = self.magnitude[all_indices] * slider_gain *window
        windows.append((window * max(self.magnitude_to_bodfy[all_indices]) ,self.frequency[all_indices]))

        
        
        self.plot_specrtum(self.frequency , self.magnitude_to_bodfy)
        complex_signal = self.magnitude_to_bodfy * np.exp(1j * self.phase)
        self.modified_signal = np. fft.irfft(complex_signal)
        self.plot_signal(self.time ,self.modified_signal , self.sample_rate , self.ui.grph_output_sig )
        self.spectogram(self.modified_signal , self.sample_rate , self.spectrogram_canvas_output)  
        
        self.plot_windw( freq_range)

    
    def plot_specrtum(self , freq , magnitude):
        self.ui.signal_view.clear()
        self.ui.signal_view.plot(freq , magnitude)
        # self.ui.signal_view.plotItem.vb.setLimits( xMin=min(freq) , xMax=max(freq), yMin=min(magnitude) , yMax=max(magnitude)) 
        self.ui.signal_view.getViewBox().autoRange()
        
   
    def plot_windw(self , freq_range):
        
        if self.ui.combo_bx_mode.currentIndex() == 0:
            for _ ,range in list(self.freq_ranges.items())[:10]:
                my_range = np.where((self.frequency >= range[0][0]) & (self.frequency <= range[0][1]))[0]
                self.ui.signal_view.plot(self.frequency[my_range] , self.window_function(len(self.frequency[my_range] ), self.ui.windows_tabs.currentIndex()) *max(self.magnitude_to_bodfy[my_range]) , pen =pg.mkPen(color=(255, 0, 0)))
            
        else:
            for range in freq_range:
                my_range = np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0]
                self.ui.signal_view.plot(self.frequency[my_range] , self.window_function(len(self.frequency[my_range] ), self.ui.windows_tabs.currentIndex()) *max(self.magnitude_to_bodfy[my_range]) , pen =pg.mkPen(color=(255, 0, 0)))
        
    def reset_slider(self):
        for name in self.freq_ranges:
            slider = getattr(self.ui, f"{name}_slider")
            slider.setValue(1)


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
