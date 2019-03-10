 # -*- coding:utf-8 -*-
'''
Created on 2019年3月10日

@author: bkd
'''
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot,Qt,pyqtSignal
from PyQt5.QtWidgets import QWidget
from .fileutil import get_file_realpath


class show_mainwin(QWidget):
    show_mainwin_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        loadUi(get_file_realpath("show_mainwin.ui"), self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    pyqtSlot()
    def on_pb_show_mainwin_pressed(self):
        self.show_mainwin_signal.emit()