from PyQt5.QtCore import QTimer
import time 
from datetime import datetime, timedelta
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pydub.playback import play
from pydub import AudioSegment
import librosa as librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import librosa.display
from IPython.display import Audio
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, shutil

from librosa.core.spectrum import _spectrogram
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from datetime import datetime
import pyqtgraph
import pyqtgraph.exporters
import matplotlib.pyplot as plt
import scipy.io.wavfile
import librosa.display
# from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from pyqtgraph import  ImageItem

from scipy import signal
import matplotlib.pyplot as plt


from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.io import wavfile
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pyqtgraph as pg
# from pyqtgraph import PlotWidget, ImageItem
from scipy import fftpack
# from pydub import AudioSegment
# from pydub.playback import play
# from PyQt5.QtCore import QBuffer, QIODevice, QByteArray  # Add these import statements
# from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from PyQt5.QtCore import QBuffer, QIODevice 
from scipy.signal import spectrogram
# import winsound
# import pyaudio
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
from PyQt5.QtWidgets import QApplication, QMainWindow , QGraphicsScene

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
from scipy.fftpack import rfft, rfftfreq, irfft , fft , fftfreq
from random import randint
from pyqtgraph import PlotWidget, plot, QtCore
# import simpleaudio as sa
from PyQt5.QtCore import pyqtSlot
from cmath import rect
import sys
import sounddevice as sd
from numba import jit

t = np.linspace(0  , 1 , 1000)
original_sig = (np.sin(2*t*np.pi* 5 )+3* np.sin(2*t*np.pi* 10 ) + 5* np.sin(t*np.pi* 40 ))

fft_ = rfft(original_sig)
freqs = np.fft.fftfreq(len(original_sig)) 
print(freqs)
# print(fft(original_sig))
