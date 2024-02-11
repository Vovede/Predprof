import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMainWindow
from PyQt5 import uic, QtCore


class WindowPush(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('WindowPush.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.MessagePush.clicked.connect(self.closePush)
        QTimer.singleShot(3000, self.closePush)


    def closePush(self):
        self.close()