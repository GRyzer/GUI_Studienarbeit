
from PyQt5 import QtWidgets, QtCore, QtGui


class Button(QtWidgets.QPushButton):
    size = 90

    def __init__(self):
        super(Button, self).__init__()
        self.icon_path = None
        self.image_number = None
        self.is_icon_displayed = False
        self.setFixedSize(Button.size, Button.size)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet(f"background-color: grey")

    def show_icon(self):
        if not self.is_icon_displayed:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(self.icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            icon.addPixmap(QtGui.QPixmap(self.icon_path), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
            self.setIcon(icon)
            self.setIconSize(QtCore.QSize(90, 90))
            self.is_icon_displayed = True

    def reset_icon(self):
        icon = QtGui.QIcon()
        self.setIcon(icon)
        self.is_icon_displayed = False

    def set_icon_path(self, icon_path):
        self.icon_path = icon_path

    def set_image_number(self, number):
        self.image_number = number
