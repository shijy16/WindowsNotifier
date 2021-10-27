from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
import json

class Pet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Pet, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()

    def read_configs(self):
        self.configs = 
if __name__ == '__main__':
