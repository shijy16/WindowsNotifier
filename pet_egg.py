from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
import json
import sys

config_path = 'config.js'

def write_config():
    config = {}
    config['pet_path'] = 'pets/naruto'
    config['timer'] = []
    config['timer'].append(['drink water and rest eyes', 40])
    config['timer'].append(['stand up', 90])
    config['plan'] = []
    config['plan'].append(['book time', 12.0])
    config['plan'].append(['book time', 18.0])
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

class Pet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Pet, self).__init__(parent)
        self.config_path = kwargs['config']
        self.read_configs()
        self.show()
        # self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        # self.setAutoFillBackground(False)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.repaint()

    def read_configs(self):
        with open(self.config_path, 'r') as f:
            self.configs = json.load(f)
        self.pet_path = self.configs['pet_path']
        

if __name__ == '__main__':
    app = QApplication(sys.argv)  
    pet = Pet(config=config_path)