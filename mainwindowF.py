# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindowF.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1320, 1286)
        MainWindow.setStyleSheet("QGroupBox[border=\"none\"] {\n"
"    border: none;\n"
"\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    font-size: 10px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QWidget{\n"
" background: #7e7e7e;}\n"
"QSlider {\n"
"    border: 1px solid #000;\n"
"    background: #EEE;\n"
"border-radius:5px;\n"
"\n"
"}\n"
"QSlider::handle {\n"
"    background: rgb(252, 244, 163);\n"
"    border: 1px solid #000;\n"
"    width: 10px;\n"
"\n"
"   \n"
"}\n"
"QSlider::groove {\n"
"    background: #CCC;\'\n"
"\n"
"}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.verticalLayout_34 = QtWidgets.QVBoxLayout()
        self.verticalLayout_34.setObjectName("verticalLayout_34")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.combo_bx_mode = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.combo_bx_mode.setFont(font)
        self.combo_bx_mode.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.combo_bx_mode.setStyleSheet(" border: 1px solid #ccc;\n"
"border-radius:5px;\n"
"font-family: Arial, sans-serif;\n"
"color: black;\n"
"\n"
"background-color: rgb(85, 170, 255);\n"
"\n"
"")
        self.combo_bx_mode.setObjectName("combo_bx_mode")
        self.combo_bx_mode.addItem("")
        self.combo_bx_mode.addItem("")
        self.combo_bx_mode.addItem("")
        self.combo_bx_mode.addItem("")
        self.horizontalLayout_6.addWidget(self.combo_bx_mode)
        self.verticalLayout_34.addLayout(self.horizontalLayout_6)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setStyleSheet("QStackedWidget{ border: 2px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"    border-radius: 5px;\n"
"    padding: 10px;}\n"
"QLabel{\n"
" border: 2px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"font-weight: bold;}")
        self.stackedWidget.setObjectName("stackedWidget")
        self.uniform_page = QtWidgets.QWidget()
        self.uniform_page.setObjectName("uniform_page")
        self.gridLayout = QtWidgets.QGridLayout(self.uniform_page)
        self.gridLayout.setObjectName("gridLayout")
        self.uniform_slider_range_1 = QtWidgets.QSlider(self.uniform_page)
        font = QtGui.QFont()
        font.setBold(False)
        self.uniform_slider_range_1.setFont(font)
        self.uniform_slider_range_1.setMaximum(10)
        self.uniform_slider_range_1.setProperty("value", 1)
        self.uniform_slider_range_1.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_1.setObjectName("uniform_slider_range_1")
        self.gridLayout.addWidget(self.uniform_slider_range_1, 0, 0, 1, 1)
        self.uniform_slider_range_2 = QtWidgets.QSlider(self.uniform_page)
        self.uniform_slider_range_2.setMaximum(10)
        self.uniform_slider_range_2.setProperty("value", 1)
        self.uniform_slider_range_2.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_2.setObjectName("uniform_slider_range_2")
        self.gridLayout.addWidget(self.uniform_slider_range_2, 0, 1, 1, 1)
        self.uniform_slider_range_3 = QtWidgets.QSlider(self.uniform_page)
        self.uniform_slider_range_3.setMaximum(10)
        self.uniform_slider_range_3.setProperty("value", 1)
        self.uniform_slider_range_3.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_3.setObjectName("uniform_slider_range_3")
        self.gridLayout.addWidget(self.uniform_slider_range_3, 0, 2, 1, 1)
        self.uniform_slider_range_4 = QtWidgets.QSlider(self.uniform_page)
        self.uniform_slider_range_4.setMaximum(10)
        self.uniform_slider_range_4.setProperty("value", 1)
        self.uniform_slider_range_4.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_4.setObjectName("uniform_slider_range_4")
        self.gridLayout.addWidget(self.uniform_slider_range_4, 0, 3, 1, 1)
        self.uniform_slider_range_5 = QtWidgets.QSlider(self.uniform_page)
        self.uniform_slider_range_5.setMaximum(10)
        self.uniform_slider_range_5.setProperty("value", 1)
        self.uniform_slider_range_5.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_5.setObjectName("uniform_slider_range_5")
        self.gridLayout.addWidget(self.uniform_slider_range_5, 0, 4, 1, 1)
        self.uniform_slider_range_6 = QtWidgets.QSlider(self.uniform_page)
        self.uniform_slider_range_6.setMaximum(10)
        self.uniform_slider_range_6.setProperty("value", 1)
        self.uniform_slider_range_6.setSliderPosition(1)
        self.uniform_slider_range_6.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_6.setObjectName("uniform_slider_range_6")
        self.gridLayout.addWidget(self.uniform_slider_range_6, 0, 5, 1, 1)
        self.uniform_slider_range_7 = QtWidgets.QSlider(self.uniform_page)
        self.uniform_slider_range_7.setMaximum(10)
        self.uniform_slider_range_7.setProperty("value", 1)
        self.uniform_slider_range_7.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_7.setObjectName("uniform_slider_range_7")
        self.gridLayout.addWidget(self.uniform_slider_range_7, 0, 6, 1, 1)
        self.uniform_slider_range_8 = QtWidgets.QSlider(self.uniform_page)
        self.uniform_slider_range_8.setMaximum(10)
        self.uniform_slider_range_8.setProperty("value", 1)
        self.uniform_slider_range_8.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_8.setObjectName("uniform_slider_range_8")
        self.gridLayout.addWidget(self.uniform_slider_range_8, 0, 7, 1, 1)
        self.uniform_slider_range_9 = QtWidgets.QSlider(self.uniform_page)
        self.uniform_slider_range_9.setMaximum(10)
        self.uniform_slider_range_9.setProperty("value", 1)
        self.uniform_slider_range_9.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_9.setObjectName("uniform_slider_range_9")
        self.gridLayout.addWidget(self.uniform_slider_range_9, 0, 8, 1, 1)
        self.uniform_slider_range_10 = QtWidgets.QSlider(self.uniform_page)
        self.uniform_slider_range_10.setMaximum(10)
        self.uniform_slider_range_10.setProperty("value", 1)
        self.uniform_slider_range_10.setOrientation(QtCore.Qt.Vertical)
        self.uniform_slider_range_10.setObjectName("uniform_slider_range_10")
        self.gridLayout.addWidget(self.uniform_slider_range_10, 0, 9, 1, 1)
        self.stackedWidget.addWidget(self.uniform_page)
        self.music_page = QtWidgets.QWidget()
        self.music_page.setObjectName("music_page")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.music_page)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout()
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.bass_slider = QtWidgets.QSlider(self.music_page)
        self.bass_slider.setMaximum(10)
        self.bass_slider.setProperty("value", 1)
        self.bass_slider.setOrientation(QtCore.Qt.Vertical)
        self.bass_slider.setObjectName("bass_slider")
        self.verticalLayout_26.addWidget(self.bass_slider)
        self.label_35 = QtWidgets.QLabel(self.music_page)
        self.label_35.setObjectName("label_35")
        self.verticalLayout_26.addWidget(self.label_35)
        self.horizontalLayout_15.addLayout(self.verticalLayout_26)
        self.verticalLayout_27 = QtWidgets.QVBoxLayout()
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.voil_slider = QtWidgets.QSlider(self.music_page)
        self.voil_slider.setMaximum(10)
        self.voil_slider.setProperty("value", 1)
        self.voil_slider.setOrientation(QtCore.Qt.Vertical)
        self.voil_slider.setObjectName("voil_slider")
        self.verticalLayout_27.addWidget(self.voil_slider)
        self.label_36 = QtWidgets.QLabel(self.music_page)
        self.label_36.setObjectName("label_36")
        self.verticalLayout_27.addWidget(self.label_36)
        self.horizontalLayout_15.addLayout(self.verticalLayout_27)
        self.verticalLayout_28 = QtWidgets.QVBoxLayout()
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.piano_slider = QtWidgets.QSlider(self.music_page)
        self.piano_slider.setMaximum(10)
        self.piano_slider.setProperty("value", 1)
        self.piano_slider.setOrientation(QtCore.Qt.Vertical)
        self.piano_slider.setObjectName("piano_slider")
        self.verticalLayout_28.addWidget(self.piano_slider)
        self.label_37 = QtWidgets.QLabel(self.music_page)
        self.label_37.setObjectName("label_37")
        self.verticalLayout_28.addWidget(self.label_37)
        self.horizontalLayout_15.addLayout(self.verticalLayout_28)
        self.verticalLayout_29 = QtWidgets.QVBoxLayout()
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.drum_slider = QtWidgets.QSlider(self.music_page)
        self.drum_slider.setMaximum(10)
        self.drum_slider.setProperty("value", 1)
        self.drum_slider.setOrientation(QtCore.Qt.Vertical)
        self.drum_slider.setObjectName("drum_slider")
        self.verticalLayout_29.addWidget(self.drum_slider)
        self.label_38 = QtWidgets.QLabel(self.music_page)
        self.label_38.setObjectName("label_38")
        self.verticalLayout_29.addWidget(self.label_38)
        self.horizontalLayout_15.addLayout(self.verticalLayout_29)
        self.gridLayout_7.addLayout(self.horizontalLayout_15, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.music_page)
        self.animal_page = QtWidgets.QWidget()
        self.animal_page.setObjectName("animal_page")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.animal_page)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout()
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.cat_slider = QtWidgets.QSlider(self.animal_page)
        self.cat_slider.setMaximum(10)
        self.cat_slider.setProperty("value", 1)
        self.cat_slider.setOrientation(QtCore.Qt.Vertical)
        self.cat_slider.setObjectName("cat_slider")
        self.verticalLayout_30.addWidget(self.cat_slider)
        self.label_39 = QtWidgets.QLabel(self.animal_page)
        self.label_39.setObjectName("label_39")
        self.verticalLayout_30.addWidget(self.label_39)
        self.horizontalLayout_16.addLayout(self.verticalLayout_30)
        self.verticalLayout_31 = QtWidgets.QVBoxLayout()
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.dog_slider = QtWidgets.QSlider(self.animal_page)
        self.dog_slider.setMaximum(10)
        self.dog_slider.setProperty("value", 1)
        self.dog_slider.setOrientation(QtCore.Qt.Vertical)
        self.dog_slider.setObjectName("dog_slider")
        self.verticalLayout_31.addWidget(self.dog_slider)
        self.label_40 = QtWidgets.QLabel(self.animal_page)
        self.label_40.setObjectName("label_40")
        self.verticalLayout_31.addWidget(self.label_40)
        self.horizontalLayout_16.addLayout(self.verticalLayout_31)
        self.verticalLayout_32 = QtWidgets.QVBoxLayout()
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.duck_slider = QtWidgets.QSlider(self.animal_page)
        self.duck_slider.setMaximum(10)
        self.duck_slider.setProperty("value", 1)
        self.duck_slider.setOrientation(QtCore.Qt.Vertical)
        self.duck_slider.setObjectName("duck_slider")
        self.verticalLayout_32.addWidget(self.duck_slider)
        self.label_45 = QtWidgets.QLabel(self.animal_page)
        self.label_45.setObjectName("label_45")
        self.verticalLayout_32.addWidget(self.label_45)
        self.horizontalLayout_16.addLayout(self.verticalLayout_32)
        self.verticalLayout_33 = QtWidgets.QVBoxLayout()
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.cow_slider = QtWidgets.QSlider(self.animal_page)
        self.cow_slider.setMaximum(10)
        self.cow_slider.setProperty("value", 1)
        self.cow_slider.setOrientation(QtCore.Qt.Vertical)
        self.cow_slider.setObjectName("cow_slider")
        self.verticalLayout_33.addWidget(self.cow_slider)
        self.label_46 = QtWidgets.QLabel(self.animal_page)
        self.label_46.setObjectName("label_46")
        self.verticalLayout_33.addWidget(self.label_46)
        self.horizontalLayout_16.addLayout(self.verticalLayout_33)
        self.gridLayout_8.addLayout(self.horizontalLayout_16, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.animal_page)
        self.ECG_page = QtWidgets.QWidget()
        self.ECG_page.setObjectName("ECG_page")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.ECG_page)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.verticalLayout_35 = QtWidgets.QVBoxLayout()
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.verticalSlider_27 = QtWidgets.QSlider(self.ECG_page)
        self.verticalSlider_27.setMaximum(10)
        self.verticalSlider_27.setProperty("value", 1)
        self.verticalSlider_27.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_27.setObjectName("verticalSlider_27")
        self.verticalLayout_35.addWidget(self.verticalSlider_27)
        self.label_41 = QtWidgets.QLabel(self.ECG_page)
        self.label_41.setObjectName("label_41")
        self.verticalLayout_35.addWidget(self.label_41)
        self.horizontalLayout_24.addLayout(self.verticalLayout_35)
        self.verticalLayout_36 = QtWidgets.QVBoxLayout()
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.verticalSlider_31 = QtWidgets.QSlider(self.ECG_page)
        self.verticalSlider_31.setMaximum(10)
        self.verticalSlider_31.setProperty("value", 1)
        self.verticalSlider_31.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_31.setObjectName("verticalSlider_31")
        self.verticalLayout_36.addWidget(self.verticalSlider_31)
        self.label_42 = QtWidgets.QLabel(self.ECG_page)
        self.label_42.setObjectName("label_42")
        self.verticalLayout_36.addWidget(self.label_42)
        self.horizontalLayout_24.addLayout(self.verticalLayout_36)
        self.verticalLayout_37 = QtWidgets.QVBoxLayout()
        self.verticalLayout_37.setObjectName("verticalLayout_37")
        self.verticalSlider_32 = QtWidgets.QSlider(self.ECG_page)
        self.verticalSlider_32.setMaximum(10)
        self.verticalSlider_32.setProperty("value", 1)
        self.verticalSlider_32.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_32.setObjectName("verticalSlider_32")
        self.verticalLayout_37.addWidget(self.verticalSlider_32)
        self.label_49 = QtWidgets.QLabel(self.ECG_page)
        self.label_49.setObjectName("label_49")
        self.verticalLayout_37.addWidget(self.label_49)
        self.horizontalLayout_24.addLayout(self.verticalLayout_37)
        self.verticalLayout_38 = QtWidgets.QVBoxLayout()
        self.verticalLayout_38.setObjectName("verticalLayout_38")
        self.verticalSlider_34 = QtWidgets.QSlider(self.ECG_page)
        self.verticalSlider_34.setMaximum(10)
        self.verticalSlider_34.setProperty("value", 1)
        self.verticalSlider_34.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_34.setObjectName("verticalSlider_34")
        self.verticalLayout_38.addWidget(self.verticalSlider_34)
        self.label_50 = QtWidgets.QLabel(self.ECG_page)
        self.label_50.setObjectName("label_50")
        self.verticalLayout_38.addWidget(self.label_50)
        self.horizontalLayout_24.addLayout(self.verticalLayout_38)
        self.gridLayout_9.addLayout(self.horizontalLayout_24, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.ECG_page)
        self.verticalLayout_34.addWidget(self.stackedWidget)
        self.horizontalLayout_17.addLayout(self.verticalLayout_34)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.horizontalLayout_17, 3, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.grph_output_sig = PlotWidget(self.centralwidget)
        self.grph_output_sig.setObjectName("grph_output_sig")
        self.verticalLayout_4.addWidget(self.grph_output_sig)
        self.output_slider = QtWidgets.QSlider(self.centralwidget)
        self.output_slider.setStyleSheet("")
        self.output_slider.setOrientation(QtCore.Qt.Horizontal)
        self.output_slider.setObjectName("output_slider")
        self.verticalLayout_4.addWidget(self.output_slider)
        self.horz_control_btns_2 = QtWidgets.QHBoxLayout()
        self.horz_control_btns_2.setSpacing(10)
        self.horz_control_btns_2.setObjectName("horz_control_btns_2")
        spacerItem1 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horz_control_btns_2.addItem(spacerItem1)
        self.btn_srt_begin_output = QtWidgets.QPushButton(self.centralwidget)
        self.btn_srt_begin_output.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_srt_begin_output.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/strt_frm_begin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_srt_begin_output.setIcon(icon)
        self.btn_srt_begin_output.setFlat(True)
        self.btn_srt_begin_output.setObjectName("btn_srt_begin_output")
        self.horz_control_btns_2.addWidget(self.btn_srt_begin_output)
        self.btn_slow_output = QtWidgets.QPushButton(self.centralwidget)
        self.btn_slow_output.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_slow_output.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("imgs/slow_down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_slow_output.setIcon(icon1)
        self.btn_slow_output.setFlat(True)
        self.btn_slow_output.setObjectName("btn_slow_output")
        self.horz_control_btns_2.addWidget(self.btn_slow_output)
        self.btn_zoom_out_output = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zoom_out_output.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_zoom_out_output.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("imgs/aoom_out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_out_output.setIcon(icon2)
        self.btn_zoom_out_output.setFlat(True)
        self.btn_zoom_out_output.setObjectName("btn_zoom_out_output")
        self.horz_control_btns_2.addWidget(self.btn_zoom_out_output)
        self.btn_play_output = QtWidgets.QPushButton(self.centralwidget)
        self.btn_play_output.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_play_output.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("imgs/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_play_output.setIcon(icon3)
        self.btn_play_output.setFlat(True)
        self.btn_play_output.setObjectName("btn_play_output")
        self.horz_control_btns_2.addWidget(self.btn_play_output)
        self.btn_pause_output = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pause_output.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_pause_output.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("imgs/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_pause_output.setIcon(icon4)
        self.btn_pause_output.setFlat(True)
        self.btn_pause_output.setObjectName("btn_pause_output")
        self.horz_control_btns_2.addWidget(self.btn_pause_output)
        self.btn_zoom_in_output = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zoom_in_output.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_zoom_in_output.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("imgs/zoom_in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_in_output.setIcon(icon5)
        self.btn_zoom_in_output.setFlat(True)
        self.btn_zoom_in_output.setObjectName("btn_zoom_in_output")
        self.horz_control_btns_2.addWidget(self.btn_zoom_in_output)
        self.btn_fast_output = QtWidgets.QPushButton(self.centralwidget)
        self.btn_fast_output.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_fast_output.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("imgs/speed_up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_fast_output.setIcon(icon6)
        self.btn_fast_output.setFlat(True)
        self.btn_fast_output.setObjectName("btn_fast_output")
        self.horz_control_btns_2.addWidget(self.btn_fast_output)
        spacerItem2 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horz_control_btns_2.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.horz_control_btns_2)
        self.horizontalLayout_8.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.specto_layout_output = QtWidgets.QVBoxLayout()
        self.specto_layout_output.setObjectName("specto_layout_output")
        self.verticalLayout_2.addLayout(self.specto_layout_output)
        self.chek_bx_show_spect_output = QtWidgets.QCheckBox(self.centralwidget)
        self.chek_bx_show_spect_output.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.chek_bx_show_spect_output.setFont(font)
        self.chek_bx_show_spect_output.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chek_bx_show_spect_output.setStyleSheet("color: rgb(255, 255, 255);")
        self.chek_bx_show_spect_output.setObjectName("chek_bx_show_spect_output")
        self.verticalLayout_2.addWidget(self.chek_bx_show_spect_output)
        self.horizontalLayout_8.addLayout(self.verticalLayout_2)
        self.gridLayout_3.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.grph_input_sig = PlotWidget(self.centralwidget)
        self.grph_input_sig.setStyleSheet("QPlotWidget {\n"
"    border: 10px solid rgb(255, 161, 46);\n"
"    border-radius: 5px;\n"
"}")
        self.grph_input_sig.setObjectName("grph_input_sig")
        self.verticalLayout_3.addWidget(self.grph_input_sig)
        self.input_slider = QtWidgets.QSlider(self.centralwidget)
        self.input_slider.setStyleSheet("")
        self.input_slider.setOrientation(QtCore.Qt.Horizontal)
        self.input_slider.setObjectName("input_slider")
        self.verticalLayout_3.addWidget(self.input_slider)
        self.horz_control_btns = QtWidgets.QHBoxLayout()
        self.horz_control_btns.setSpacing(10)
        self.horz_control_btns.setObjectName("horz_control_btns")
        spacerItem3 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horz_control_btns.addItem(spacerItem3)
        self.btn_srt_begin_input = QtWidgets.QPushButton(self.centralwidget)
        self.btn_srt_begin_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_srt_begin_input.setText("")
        self.btn_srt_begin_input.setIcon(icon)
        self.btn_srt_begin_input.setFlat(True)
        self.btn_srt_begin_input.setObjectName("btn_srt_begin_input")
        self.horz_control_btns.addWidget(self.btn_srt_begin_input)
        self.btn_slow_input = QtWidgets.QPushButton(self.centralwidget)
        self.btn_slow_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_slow_input.setText("")
        self.btn_slow_input.setIcon(icon1)
        self.btn_slow_input.setFlat(True)
        self.btn_slow_input.setObjectName("btn_slow_input")
        self.horz_control_btns.addWidget(self.btn_slow_input)
        self.btn_zoom_out_input = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zoom_out_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_zoom_out_input.setText("")
        self.btn_zoom_out_input.setIcon(icon2)
        self.btn_zoom_out_input.setFlat(True)
        self.btn_zoom_out_input.setObjectName("btn_zoom_out_input")
        self.horz_control_btns.addWidget(self.btn_zoom_out_input)
        self.btn_play_input = QtWidgets.QPushButton(self.centralwidget)
        self.btn_play_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_play_input.setText("")
        self.btn_play_input.setIcon(icon3)
        self.btn_play_input.setFlat(True)
        self.btn_play_input.setObjectName("btn_play_input")
        self.horz_control_btns.addWidget(self.btn_play_input)
        self.btn_pause_input = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pause_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_pause_input.setText("")
        self.btn_pause_input.setIcon(icon4)
        self.btn_pause_input.setFlat(True)
        self.btn_pause_input.setObjectName("btn_pause_input")
        self.horz_control_btns.addWidget(self.btn_pause_input)
        self.btn_zoom_in_input = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zoom_in_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_zoom_in_input.setText("")
        self.btn_zoom_in_input.setIcon(icon5)
        self.btn_zoom_in_input.setFlat(True)
        self.btn_zoom_in_input.setObjectName("btn_zoom_in_input")
        self.horz_control_btns.addWidget(self.btn_zoom_in_input)
        self.btn_fast_input = QtWidgets.QPushButton(self.centralwidget)
        self.btn_fast_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_fast_input.setText("")
        self.btn_fast_input.setIcon(icon6)
        self.btn_fast_input.setFlat(True)
        self.btn_fast_input.setObjectName("btn_fast_input")
        self.horz_control_btns.addWidget(self.btn_fast_input)
        spacerItem4 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horz_control_btns.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horz_control_btns)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.specto_layout_input = QtWidgets.QVBoxLayout()
        self.specto_layout_input.setObjectName("specto_layout_input")
        self.verticalLayout.addLayout(self.specto_layout_input)
        self.chek_bx_show_spect_input = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.chek_bx_show_spect_input.setFont(font)
        self.chek_bx_show_spect_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chek_bx_show_spect_input.setStyleSheet("\n"
"color: rgb(255, 255, 255);\n"
"")
        self.chek_bx_show_spect_input.setObjectName("chek_bx_show_spect_input")
        self.verticalLayout.addWidget(self.chek_bx_show_spect_input)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.signal_view = PlotWidget(self.centralwidget)
        self.signal_view.setStyleSheet("")
        self.signal_view.setObjectName("signal_view")
        self.horizontalLayout_23.addWidget(self.signal_view)
        self.windows_tabs = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        self.windows_tabs.setFont(font)
        self.windows_tabs.setStyleSheet("\n"
"\n"
"QTabBar {\n"
"    background-color: rgb(85, 170, 255); /* Set the background color of the tab bar */\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    color: white; /* Set the color of the tab text */\n"
" size: 12px;\n"
"    padding: 8px; /* Adjust the padding as needed */\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: #0D72A1; /* Set the background color of the selected tab */\n"
"    border: 1px solid #ffaa2e; /* Add a border to the selected tab */\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"   border: 2px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"")
        self.windows_tabs.setObjectName("windows_tabs")
        self.Hamming_window = QtWidgets.QWidget()
        self.Hamming_window.setObjectName("Hamming_window")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.Hamming_window)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.graphicsView_hamming = PlotWidget(self.Hamming_window)
        self.graphicsView_hamming.setObjectName("graphicsView_hamming")
        self.gridLayout_11.addWidget(self.graphicsView_hamming, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_11.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.windows_tabs.addTab(self.Hamming_window, "")
        self.Rectangle_window = QtWidgets.QWidget()
        self.Rectangle_window.setObjectName("Rectangle_window")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.Rectangle_window)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.graphicsView_rectangle = PlotWidget(self.Rectangle_window)
        self.graphicsView_rectangle.setObjectName("graphicsView_rectangle")
        self.gridLayout_10.addWidget(self.graphicsView_rectangle, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_10.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.windows_tabs.addTab(self.Rectangle_window, "")
        self.Hanning_window = QtWidgets.QWidget()
        self.Hanning_window.setObjectName("Hanning_window")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Hanning_window)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_39 = QtWidgets.QVBoxLayout()
        self.verticalLayout_39.setObjectName("verticalLayout_39")
        self.graphicsView_hanning = PlotWidget(self.Hanning_window)
        self.graphicsView_hanning.setObjectName("graphicsView_hanning")
        self.verticalLayout_39.addWidget(self.graphicsView_hanning)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_25.addLayout(self.horizontalLayout_4)
        self.verticalLayout_39.addLayout(self.horizontalLayout_25)
        self.gridLayout_2.addLayout(self.verticalLayout_39, 0, 0, 1, 1)
        self.windows_tabs.addTab(self.Hanning_window, "")
        self.Gaussian_window = QtWidgets.QWidget()
        self.Gaussian_window.setObjectName("Gaussian_window")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.Gaussian_window)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.graphicsView_gaussian = PlotWidget(self.Gaussian_window)
        self.graphicsView_gaussian.setObjectName("graphicsView_gaussian")
        self.gridLayout_6.addWidget(self.graphicsView_gaussian, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_6.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.windows_tabs.addTab(self.Gaussian_window, "")
        self.horizontalLayout_23.addWidget(self.windows_tabs)
        self.gridLayout_3.addLayout(self.horizontalLayout_23, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1320, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionUpload_file = QtWidgets.QAction(MainWindow)
        self.actionUpload_file.setObjectName("actionUpload_file")
        self.menuFile.addAction(self.actionUpload_file)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.windows_tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Select mode"))
        self.combo_bx_mode.setItemText(0, _translate("MainWindow", "Uniform mode"))
        self.combo_bx_mode.setItemText(1, _translate("MainWindow", "Musical instruments"))
        self.combo_bx_mode.setItemText(2, _translate("MainWindow", "Animal sounds"))
        self.combo_bx_mode.setItemText(3, _translate("MainWindow", "ECG abnormalities"))
        self.label_35.setText(_translate("MainWindow", "bass"))
        self.label_36.setText(_translate("MainWindow", "voil"))
        self.label_37.setText(_translate("MainWindow", "piano"))
        self.label_38.setText(_translate("MainWindow", "drum"))
        self.label_39.setText(_translate("MainWindow", "cat"))
        self.label_40.setText(_translate("MainWindow", "dog"))
        self.label_45.setText(_translate("MainWindow", "duck"))
        self.label_46.setText(_translate("MainWindow", "cow"))
        self.label_41.setText(_translate("MainWindow", "arthmya 1"))
        self.label_42.setText(_translate("MainWindow", "arthmya 2"))
        self.label_49.setText(_translate("MainWindow", "arthmya 3"))
        self.label_50.setText(_translate("MainWindow", "TextLabel"))
        self.btn_srt_begin_output.setToolTip(_translate("MainWindow", "replay"))
        self.btn_srt_begin_output.setWhatsThis(_translate("MainWindow", "stast from beging\n"
""))
        self.btn_play_output.setToolTip(_translate("MainWindow", "paly\n"
""))
        self.btn_pause_output.setToolTip(_translate("MainWindow", "paly\n"
""))
        self.chek_bx_show_spect_output.setText(_translate("MainWindow", "Show"))
        self.btn_srt_begin_input.setToolTip(_translate("MainWindow", "replay"))
        self.btn_srt_begin_input.setWhatsThis(_translate("MainWindow", "stast from beging\n"
""))
        self.btn_play_input.setToolTip(_translate("MainWindow", "paly\n"
""))
        self.btn_pause_input.setToolTip(_translate("MainWindow", "paly\n"
""))
        self.chek_bx_show_spect_input.setText(_translate("MainWindow", "Show"))
        self.windows_tabs.setTabText(self.windows_tabs.indexOf(self.Hamming_window), _translate("MainWindow", "Hamming"))
        self.windows_tabs.setTabText(self.windows_tabs.indexOf(self.Rectangle_window), _translate("MainWindow", "Rectangle "))
        self.windows_tabs.setTabText(self.windows_tabs.indexOf(self.Hanning_window), _translate("MainWindow", "Hanning"))
        self.windows_tabs.setTabText(self.windows_tabs.indexOf(self.Gaussian_window), _translate("MainWindow", "Gaussian"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionUpload_file.setText(_translate("MainWindow", "Upload file"))
from pyqtgraph import PlotWidget