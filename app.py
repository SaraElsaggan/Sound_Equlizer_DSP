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

        self.ui.btn_zoom_in_input.clicked.connect(lambda: self.zoom( 1))
        self.ui.btn_zoom_out_input.clicked.connect(lambda: self.zoom( 0))

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
        
        # self.ui.cat_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["cat"] ,self.ui.cat_slider.value() )) 
        # self.ui.dog_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["dog"] ,self.ui.dog_slider.value() )) 
        # self.ui.duck_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["duck"] ,self.ui.duck_slider.value() )) 
        # # self.ui.cow_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["elephant"] ,self.ui.cow_slider.value() )) 
        # self.ui.cow_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["cow"] ,self.ui.cow_slider.value() )) 

        # self.ui.bass_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["bass"] ,self.ui.bass_slider.value() )) 
        # self.ui.voil_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["voil"] ,self.ui.voil_slider.value() )) 
        # self.ui.piano_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["piano"] ,self.ui.piano_slider.value() )) 
        # self.ui.drum_slider.valueChanged.connect(lambda: self.modfy_frq_component(self.freq_ranges["drum"] ,self.ui.drum_slider.value() )) 

        self.slider_names = ["bass", "voil", "piano", "drum" , "cat" , "dog" , "duck",  "cow" ,"arthmya_1" , "arthmya_2" , "arthmya_3"  , "arthmya_4"]

        for name in self.slider_names:
            slider = getattr(self.ui, f"{name}_slider")
            slider.valueChanged.connect(lambda value, n=name: self.modfy_frq_component(self.freq_ranges[n], value))

        
        for i in range(1, 11):
            slider = getattr(self.ui, f"uniform_slider_range_{i}")
            slider.valueChanged.connect(lambda value, idx=i-1: self.modfy_frq_component(self.uniform_ranges()[idx], value))

        # self.uniform_sliders = self.ui.uniform_page.findChildren(QSlider)
        # for slider, i in zip( self.uniform_sliders , range(10)):
        #     slider.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[i] ,slider.value() )) 

        
        # self.ui.uniform_slider_range_1.valueChanged.connect(self.uniform_ranges) 
        # self.ui.uniform_slider_range_1.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[0] ,self.ui.uniform_slider_range_1.value() )) 
        # self.ui.uniform_slider_range_2.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[1] ,self.ui.uniform_slider_range_2.value() )) 
        # self.ui.uniform_slider_range_3.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[2] ,self.ui.uniform_slider_range_3.value() )) 
        # self.ui.uniform_slider_range_4.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[3] ,self.ui.uniform_slider_range_4.value() )) 
        # self.ui.uniform_slider_range_5.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[4] ,self.ui.uniform_slider_range_5.value() )) 
        # self.ui.uniform_slider_range_6.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[5] ,self.ui.uniform_slider_range_6.value() )) 
        # self.ui.uniform_slider_range_7.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[6] ,self.ui.uniform_slider_range_7.value() )) 
        # self.ui.uniform_slider_range_8.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[7] ,self.ui.uniform_slider_range_8.value() )) 
        # self.ui.uniform_slider_range_9.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[8] ,self.ui.uniform_slider_range_9.value() )) 
        # self.ui.uniform_slider_range_10.valueChanged.connect(lambda: self.modfy_frq_component(self.uniform_ranges()[9] ,self.ui.uniform_slider_range_10.value() )) 

        self.freq_ranges = {
            # "cat" :   [(2200 , 2400)  , (550 , 600) , (1700 , 1800) , (2800 , 3000)],
            "cat" :   [(500 , 605) , (1000 , 1200) , (2200 , 2400)  , (550 , 600) , (1700 , 1800) , (2750 , 3000) , (3300 , 3500) , (3900 , 4200) , (4500 , 4700 ) , (5100 , 5300)], #new sound not completly disapear but the cat sound is lowr
            # "dog" :  [(300 , 1700)],
            "dog" :  [(200 , 1133) , (1150 , 1900)], #new so bad 
            "duck" :  [(400 , 550) , (800 , 840) ,( 880 , 920) , (960,  1000) , (1100 , 2200)], #duck2
            # "cow" :   [(250, 400)],
            "cow" :   [(200, 400) , (500 , 700) , (790 , 860) , (800 , 1020) , (1040 , 1280) , (1300 , 1400)], #new and done (just the sound is lowered)
            
            # "bass" : [(0 , 400)] , 
            "bass" : [(0 , 600)] ,  # new and done
            # "voil" : [(510 , 540 ) , (1020 , 1060) ,  (1530 , 1590) , (2060 , 2120) , (2570 , 2640)],
            "voil" : [(504 , 556 ) , (1014 , 1070) ,  (1530 , 1601) , (2048 , 2120) , (2566 , 2644) , (3080 , 3190) , (3600, 3710 ) , (4120 , 4220)], # new (done but replaced with noise)
            # "voil" : [(504 , 556 ) , (1014 , 1070) ,  (1530 , 1601) , (2048 , 2120) , (2566 , 2644)],
            # "drum" : [(0 , 250)],
            # "drum" : [(1900 , 2700) , (2860 , 2960) , (5200 , 5600) , (6400 ,7400  ) , (11040 , 11340) , (12400 , 12760),  (15300 , 15800)  ], #new for glass
            # "drum" : [(0 , 80) , (90 , 116) , (120 , 150) , (160 , 170) , (188 , 205) , (226 , 233) , (255 , 280)  , (288 , 297) , (316 , 340) , (382 , 404) , (455 , 466) , (520 , 528) , (550 , 560) , (580 , 600) , (616 , 626) , (650 , 660) , (680 , 690) , (715 , 725) , (745 , 755) , (775 , 800)  ], #C_Synth_67_561

            # "drum" : [(0 , 300) ], #new
            "piano" : [(260 , 264 ) , (520 , 532) ,  (780 , 790) ,  (1045 , 1052) , (1574 , 1584) , (1840 , 1850)], #done
            "drum" : [(25 , 150) , (156 , 170  ) , (200 , 264) ,(264 , 300) , (360 , 440) , (485 , 520 ), (532 , 640) , (640 , 780)  , (900 , 950 ) , (1020 , 1045) , (1052 , 1140) , (1160 , 1220) , (1300 , 1350)  , (1420 , 1460) , (1540 , 1600) , (1680 , 1730) , (1830 , 1860) , (1960 , 2000) , (2090 , 2130) , (2220 , 2270) , (2370 , 2400) , (2780 , 2810) , (2920 , 2950) , (3060 , 3090) , (3190 , 3220) ], #new gitur
            # "drum" : [(25 , 150) , (156 , 170  ) , (200 , 300) , (360 , 440) , (485 , 640 ) , (640 , 790) , (900 , 950 ) , (1020 , 1140) , (1160 , 1220) , (1300 , 1350)  , (1420 , 1460) , (1540 , 1600) , (1680 , 1730) , (1830 , 1860) , (1960 , 2000) , (2090 , 2130) , (2220 , 2270) , (2370 , 2400) , (2780 , 2810) , (2920 , 2950) , (3060 , 3090)], #new
            
            
            
            # "cat" : [self.ui.cat_slider , [1] , [(2200 , 2400)  , (550 , 600) , (1700 , 1800) , (2800 , 3000)]],
            # "dog" : [self.ui.dog_slider , [1] ,[(300 , 1700)]],
            # "duck" :[ self.ui.duck_slider , [1]  , [(450 , 550) , (800 , 840) ,( 880 , 920) , (960,  1000) , (1100 , 2200)]], #duck2
            # "cow" : [self.ui.cow_slider , [1] , [(250, 400)]],
            
            # "dog" : [(220 , 300 ) , (520 , 680) , (800 , 850) , (900,  1000) , (1060 , 110) , (1040 , 1220)],
            # "duck" :[ (800, 2500)], #duck2
            # "duck" :[ (0, 2500)], #duck2
            # "elephant" : [(100 , 300) ]  , 
            # "glock" : [(650 , 400) , (690 , 710) , (785 , 790) , (833 , 836),  (936 , 942) , (992 , 996) , (1070 , 1090) , (1315 , 1340) , (1400 , 1415)] , 
            # "voil" : [(485 ,500) , (515 ,530) , (770 , 790) , (980 , 1000),  (1030 , 1065) , (1480 , 1490) , (1560 , 1580) , (1970 , 1985) , (2085 , 2110) , (2460 , 2480) , (2600 , 2630) , (2970 , 2980) , (3130 , 3155) , (3454 , 3477) , (3654 , 3680)] , 
            # "T" : [(775 , 795 ) , (1560 , 1580) ,  (2345 , 2365) ],
            # "f" : [(1540 , 1610 ) ],
            # # "p" : [(255 , 267 ) , (218 , 532) ,  (780 , 790) , (1045 , 1052) , (1574 , 1584) , (1840 , 1850)],
            # # "uniform":[(0 , 2000) , (2000 , 4000) , (4000 , 6000) , (6000 , 8000) , (8000 , 10000) (10000 , 12000), (12000 , 14000) , (14000 , 16000) , (16000 , 18000) , (18000, 20000)]

            # "cat" : [(500 , 600)  , (100 , 1200) , (1600 , 1800) , (2200 , 2400) ], #cat_121
            # # "cat" : [(540 , 570)  , (590 , 605) , (1040 , 1140) , (1640 , 1700) , (1780, 1800) , (2200 , 2260), (1160,  1200)], #cat_121
            # "dog" : [(0 , 2000)],
            "arthmya_1" : [(81 , 100) , (58 , 75) , (160, 175)],
            "arthmya_2" : [(110 , 120) , (140 , 150) ],
            "arthmya_3" : [(81 , 100)  ,(268 , 280 ) , (140 , 150) , (190 , 200)],

            # '''outside'''
            # "arthmya_1" : [(30 , 50) ],
            # "arthmya_2" : [(58 , 75) ],
            # "arthmya_3" : [(81 , 100) ],
            # "arthmya_4" : [(110 , 120) ],
            
            # "cat" :   [(140 , 150) ],
            # "dog" :  [(160 , 175)],
            # "duck" :  [(190 , 200) ], #duck2
            # "cow" :   [(220, 230)],
            
            # "bass" : [(240 , 255)] , 
            # "voil" : [(268 , 280 ) ],
            # "piano" : [(270 , 280 ) ],
            # "drum" : [(300 , 320)],
            
            # # '''outside random'''
            # "arthmya_1" : [(33 , 54) ],
            # "arthmya_2" : [(61 , 73) ],
            # "arthmya_3" : [(88 , 109) ],
            # "arthmya_4" : [(111 , 120) ],
            
            # "cat" :   [(140 , 150) ],
            # "dog" :  [(160 , 175)],
            # "duck" :  [(180 , 206) ], #duck2
            # "cow" :   [(220, 230)],
            
            # "bass" : [(240 , 180)] , 
            # "voil" : [(186 , 255 ) ],
            # "piano" : [(270 , 283 ) ],
            # "drum" : [(300 , 320)],
            
            
            
            
            # '''step 20'''
            
            # "arthmya_1" : [(0 , 20) ],
            # "arthmya_2" : [(20 , 40) ],
            # "arthmya_3" : [(40 , 60) ],
            # "arthmya_4" : [(60 , 80) ],
            
            # "cat" :   [(80 , 100) ],
            # "dog" :  [(100 , 120)],
            # "duck" :  [(120 , 140) ], #duck2
            # "cow" :   [(140, 160)],
            
            # "bass" : [(160 , 180)] , 
            # "voil" : [(180 , 200 ) ],
            # "piano" : [(220 , 240 ) ],
            # "drum" : [(240 , 260)],
            # '''actual normal ranges'''
            # "arthmya_1" : [(23 , 30) ],
            # "arthmya_2" : [(50 , 58) ],
            # "arthmya_3" : [(75 , 81) ],
            
            # "cat" :   [(100 , 110) ],
            # "dog" :  [(120 , 140)],
            # "duck" :  [(150 , 160) ], #duck2
            # "cow" :   [(175, 190)],
            
            # "bass" : [(200 , 220)] , 
            # "voil" : [(230 , 240 ) ],
            # "piano" : [(255 , 268 ) ],
            # "drum" : [(280 , 300)],

            
        }
        self.slider_history = [1]
        self.ui.actionUpload_file.triggered.connect(self.save_ecg_file)
        # self.ui.btn_srt_begin_output.clicked.connect(self.fun)
        QShortcut(QKeySequence("Ctrl+o"), self).activated.connect(self.upload_signal_file)
        QShortcut(QKeySequence("Ctrl+s"), self).activated.connect(self.save_ecg_file)
        QShortcut(QKeySequence("Ctrl+n"), self).activated.connect(self.open_normal)
    
        QShortcut(QKeySequence("Ctrl+m"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(1))
        QShortcut(QKeySequence("Ctrl+b"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(3))
        QShortcut(QKeySequence("Ctrl+p"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(2))
        QShortcut(QKeySequence("Ctrl+u"), self).activated.connect(lambda :self.ui.combo_bx_mode.setCurrentIndex(0))



    # def fun(self):
    #     current_page_index = self.ui.stackedWidget.currentIndex()
    #     current_page = self.ui.stackedWidget.widget(current_page_index)

    #     sliders = current_page.findChildren(QSlider)
        
    #     for slider ,i in zip(sliders , range(10)):
    #         print(f"Slider value: {slider.value()} {i}")
    
    
    def handleComboBox(self, index):
        # Hide or show controls in the stacked widget based on the index
        self.ui.stackedWidget.setCurrentIndex(index)
    
    def update_slider(self , slider):
        current_value = slider.value()
        if current_value < slider.maximum():
            slider.setValue(current_value + 100)  # Increment by 100 milliseconds
   
    def uniform_ranges(self ):
        # freq = self.frequency
        # _ , __  , freq = self.fourier_function()
        
        # freq_batches = np.array_split(self.ui.signal_view.plotItem.curves[0].getData(), 10 )
        freq_batches = np.array_split(self.frequency, 10)
        # freq_batches = np.array_split(self.frequency[:len(self.frequency) //2], 10)
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
            # self.ui.grph_input_sig.plotItem.vb.setLimits(xMin=min(t), xMax=max(t), yMin=min(self.original_sig), yMax=max(self.original_sig))
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
        # widget.plotItem.vb.setLimits( xMin=min(time) , xMax=max(time), yMin=min(samples) , yMax=max(samples)) 
        widget.getViewBox().autoRange()
        self.spectogram(self.original_sig , self.sample_rate , self.spectrogram_canvas_input)
  
    def fourier_function(self):
        complex_fft = np.fft.rfft(self.original_sig)
        self.magnitude = np.abs(complex_fft / len(self.original_sig))
        # self.magnitude = np.abs(complex_fft / len(self.original_sig))
        self.phase = np.angle(complex_fft)
        # self.magnitude = np.abs(complex_fft)
        self.frequency = np.fft.rfftfreq(len(self.original_sig), 1 / self.sample_rate)
        
        # self.frequency = frequency[:len(frequency)//2]
        # self.magnitude = magnitude[:len(magnitude)//2]
        self.magnitude_to_bodfy = self.magnitude.copy()
        
        print(f"freq shape {self.frequency.shape} ,magnitude.shape {self.magnitude.shape}")
        print(f"slef.magnitude {self.magnitude}")
        
        
        self.ui.signal_view.clear()
        self.ui.signal_view.plot(self.frequency , self.magnitude)
        # self.ui.signal_view.plot(self.frequency[:len(self.frequency)//2] , self.magnitude[:len(self.frequency)//2])
        # self.ui.signal_view.plotItem.vb.setLimits( xMin=min(self.frequency[:len(self.frequency)]) , xMax=max(self.frequency[:len(self.frequency)]), yMin=min(self.magnitude[:len(self.frequency)]) , yMax=max(self.magnitude[:len(self.frequency)])) 
        self.ui.signal_view.getViewBox().autoRange() 
        self.plot_window()
        
        

        # return magnitude, phase, frequency

    def window_function(self   , length  ,  window_type  ):
        print(f"here{window_type}")
        if window_type == 0 :
            window = np.hamming(length)
            print(0)
        elif window_type == 1:
            window = signal.windows.boxcar(length) 
            print(1)
        elif window_type == 2:
            window = np.hanning(length)
            print(2)
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
        '''
        # slider = freq_range[0]
        slider_history  = freq_range[1]
        
        slider_history.append(slider_gain)
        # magnitude, phase, frequency = self.fourier_function()
        for range in freq_range[2]:
            print(f"range{range}")
            indices_to_modify = np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0]
            
            window = self.window_function( len(magnitude[indices_to_modify])  , self.ui.windows_tabs.currentIndex() , range) 
            # magnitude[indices_to_modify] *= (slider_gain/(slider_gain-1)) *window
            copy = magnitude[indices_to_modify]
            # if slider_gain == 0:
            if slider_history[0] == 0:
                magnitude[indices_to_modify] =copy * (slider_gain) *window
            else:
                magnitude[indices_to_modify] *= (slider_gain/(slider_history[0])) *window
            windows.append((window * max(magnitude[indices_to_modify]) ,self.frequency[indices_to_modify]))
            
        complex_signal = magnitude * np.exp(1j * self.phase)
        self.modified_signal = np. fft.irfft(complex_signal)
        slider_history.pop(0)
        '''
        # magnitude, phase, frequency = self.fourier_function()
        # for range in freq_range:
        #     indices_to_modify = np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0]
        #     print(f"indices_to_modify{indices_to_modify}")
            
        #     window = self.window_function( len(self.magnitude[indices_to_modify])  , self.ui.windows_tabs.currentIndex() , range) 

        #     self.magnitude_to_bodfy[indices_to_modify] = self.magnitude[indices_to_modify] * slider_gain *window
        #     print(f"diff : {self.magnitude_to_bodfy[indices_to_modify] - self.magnitude[indices_to_modify]}")
        #     windows.append((window * max(self.magnitude_to_bodfy[indices_to_modify]) ,self.frequency[indices_to_modify]))

        for range in freq_range:
            indices_to_modify = np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0]
            all_indices = np.concatenate((all_indices, indices_to_modify))
        
        

        # Sort the array for better visualization (optional)
        all_indices = np.sort(all_indices)
        window = self.window_function( len(self.magnitude[all_indices])  , self.ui.windows_tabs.currentIndex() ) 

        self.magnitude_to_bodfy[all_indices] = self.magnitude[all_indices] * slider_gain *window
        print(f"diff : {self.magnitude_to_bodfy[all_indices] - self.magnitude[all_indices]}")
        windows.append((window * max(self.magnitude_to_bodfy[all_indices]) ,self.frequency[all_indices]))

        
        # print()
        
        self.ui.signal_view.clear()
        self.ui.signal_view.plot(self.frequency , self.magnitude_to_bodfy)
        # self.ui.signal_view.plot(self.frequency[:len(self.frequency)//2] , self.magnitude_to_bodfy[:len(self.frequency)//2])
        # self.ui.signal_view.plot(self.frequency[indices_to_modify] , window * max(self.magnitude_to_bodfy[indices_to_modify]), pen =pg.mkPen(color=(255, 0, 0)))
        # self.ui.signal_view.plotItem.vb.setLimits( xMin=min(self.frequency[:len(self.frequency)]) , xMax=max(self.frequency[:len(self.frequency)]), yMin=min(self.magnitude_to_bodfy[:len(self.frequency)]) , yMax=max(self.magnitude_to_bodfy[:len(self.frequency)])) 
        self.ui.signal_view.getViewBox().autoRange()
        
        if self.ui.combo_bx_mode.currentIndex() == 0:
            print("uniform mode")
            window = self.window_function(1102, self.ui.windows_tabs.currentIndex())
    
            for range in self.uniform_ranges():
                my_range = np.where((self.frequency >= range[0][0]) & (self.frequency <= range[0][1]))[0]
                print(f"range[0]{range}")
                print(f"points{int(range[0][0])}, {int(range[0][1])}")
                # self.ui.signal_view.plot(self.frequency[all_indices] , window *max(self.magnitude_to_bodfy[all_indices]) )
                # self.ui.signal_view.plot(self.frequency[int(range[0][0]) :int(range[0][1])] , self.window_function(len(self.frequency[int(range[0][0]) :int(range[0][1])]) , self.ui.windows_tabs.currentIndex()) *max(self.magnitude_to_bodfy[int(range[0][0]) :int(range[0][1])]) , pen =pg.mkPen(color=(255, 0, 0)))
                # self.ui.signal_view.plot(self.frequency[int(range[0][0]) :int(range[0][1])] , window, pen =pg.mkPen(color=(255, 0, 0)))
                self.ui.signal_view.plot(self.frequency[my_range] , self.window_function(len(self.frequency[my_range] ), self.ui.windows_tabs.currentIndex()) *max(self.magnitude_to_bodfy[my_range]) , pen =pg.mkPen(color=(255, 0, 0)))
            print(f"range length {len(self.frequency[int(range[0][0]) :int(range[0][1])])}")

            # for window in windows:
        else:
            for range in freq_range:
                print(f"range[0]{range}")
                my_range = np.where((self.frequency >= range[0]) & (self.frequency <= range[1]))[0]
                # print(f"points{int(range[0][0])}, {int(range[0][1])}")
                # self.ui.signal_view.plot(self.frequency[all_indices] , window *max(self.magnitude_to_bodfy[all_indices]) )
                # self.ui.signal_view.plot(self.frequency[int(range[0][0]) :int(range[0][1])] , self.window_function(len(self.frequency[int(range[0][0]) :int(range[0][1])]) , self.ui.windows_tabs.currentIndex()) *max(self.magnitude_to_bodfy[int(range[0][0]) :int(range[0][1])]) , pen =pg.mkPen(color=(255, 0, 0)))
                # self.ui.signal_view.plot(self.frequency[int(range[0][0]) :int(range[0][1])] , window, pen =pg.mkPen(color=(255, 0, 0)))
                self.ui.signal_view.plot(self.frequency[my_range] , self.window_function(len(self.frequency[my_range] ), self.ui.windows_tabs.currentIndex()) *max(self.magnitude_to_bodfy[my_range]) , pen =pg.mkPen(color=(255, 0, 0)))
            # print(f"range length {len(self.frequency[int(range[0][0]) :int(range[0][1])])}")

                
        
       
        # self.ui.graphicsView_rectangle.clear()
        # for (window , range) in windows:
        #     self.ui.signal_view.plot(self.frequency[indices_to_modify] , self.magnitude_to_bodfy[indices_to_modify])
        #     # self.ui.graphicsView_rectangle.plot(frequency[indices_to_modify] , magnitude[indices_to_modify])
        #     # self.ui.graphicsView_rectangle.plot( window , pen ="r")
        #     print(range)
        #     self.ui.signal_view.plot(range , window , pen = pg.mkPen(color=(255, 0, 0), width=0.5))

        

        complex_signal = self.magnitude_to_bodfy * np.exp(1j * self.phase)
        self.modified_signal = np. fft.irfft(complex_signal)
        self.plot_audio_signal(self.modified_signal , self.sample_rate , self.ui.grph_output_sig )
        self.spectogram(self.modified_signal , self.sample_rate , self.spectrogram_canvas_output)  

    def open_normal(self):
        # file_path = "C:/Users/Sara/Desktop/Sara_Signal_Equalizer/normal_ecg.csv"
        # df = pd.read_csv(file_path)
        #     # t = np.arange(0 , 7 , 1/125)
        # t = df.iloc[:, 0].values
        # self.original_sig = df.iloc[:, 1].values
        # self.ui.grph_input_sig.clear()
        # self.ui.grph_input_sig.plot(t , self.original_sig)
        # self.ui.grph_input_sig.getViewBox().autoRange()
        
        # self.sample_rate = 1/(t[1]-t[0])
        # print(self.sample_rate)
        # self.spectogram(self.original_sig , 60 , self.spectrogram_canvas_input)
        # self.reset_slider()
        
        # file_path  = "C:/Users/Sara/Desktop/Sara_Signal_Equalizer/music/violin-C5.wav"
        # file_path  = "C:/Users/Sara/Desktop/Sara_Signal_Equalizer/animal/cat_1_cow_dog_2_suck_2.wav"
        file_path  = "C:/Users/Sara/Desktop/Sara_Signal_Equalizer/music/pc4_drykickone_vc5_bass10.wav"
        print(file_path)
        
        self.ui.grph_input_sig.clear()
        self.ui.grph_output_sig.clear()
        
        print("wavvv")
        self.sample_rate, self.original_sig = wavfile.read(file_path)
        self.is_sound = True
        self.plot_audio_signal(self.original_sig , self.sample_rate , self.ui.grph_input_sig)
        
        self.reset_slider()
        

            
            
        self.fourier_function()
        
        

            
            
        self.fourier_function()
        
    def save_ecg_file(self):
        # modified_df = pd.DataFrame({np.arange(0, len(self.modified_signal)) / self.sample_rate, self.modified_signal})
        # modified_df = pd.DataFrame({np.arange(0, len(self.modified_signal)) / self.sample_rate, self.modified_signal})
        # modified_df = pd.DataFrame([np.arange(0, len(self.modified_signal)) / self.sample_rate, self.modified_signal])
# 

        modified_df = pd.DataFrame({'Time': np.arange(0, len(self.modified_signal)) / self.sample_rate,'Modified_Signal': self.modified_signal})
        
        modified_file_path, _ = QFileDialog.getSaveFileName(self, "Save Modified Signal", "~", "CSV Files (*.csv)")
        if modified_file_path:
                modified_df.to_csv(modified_file_path, index=False)
    
    def reset_slider(self):
        for i in range(1, 10):
            slider_name = f'uniform_slider_range_{i}'
            current_slider = getattr(self.ui, slider_name)
            current_slider.setValue(1)
            
        for name in self.slider_names:
            slider = getattr(self.ui, f"{name}_slider")
            slider.setValue(1)

    def plot_window(self  ):
        # window = self.window_function()
        print("dd")
        window = self.window_function(50000 ,  self.ui.windows_tabs.currentIndex() )
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
