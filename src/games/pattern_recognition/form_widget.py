
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.base_form_widget import BaseFormWidget


class FormWidget(BaseFormWidget):
    def __init__(self, memory_page, color, selected_level):
        self.button_list = []
        self.form_layout = None
        self.grid_layout = None
        self.horizontal_layout = None
        self.main_vertical_layout = None
        self.submit_button = None
        self.setupUi(memory_page, color, selected_level)

    def setupUi(self, memory_page, color, selected_level):
        memory_page.setMinimumSize(self.get_min_widget())
        memory_page.setMaximumSize(self.get_max_widget())
        memory_page.setWindowTitle(f"Memory, Level {selected_level}")
        memory_page.resize(QtCore.QSize(800, 800))

        self.main_vertical_layout = QtWidgets.QVBoxLayout(memory_page)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout = QtWidgets.QGridLayout(memory_page)
        self.grid_layout.setSpacing(5)

        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        for index in range(256):
            button = QtWidgets.QPushButton(memory_page)
            button.setFixedSize(QtCore.QSize(40, 40))
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            button.setStyleSheet(f"background-color: {color}")
            button.clicked.connect(partial(self.toggle_button_background, button))
            self.button_list.append(button)
            self.grid_layout.addWidget(button, index // 16, index % 16)

        self.main_vertical_layout.addLayout(self.grid_layout)
        self.horizontal_layout = QtWidgets.QHBoxLayout(memory_page)

        self.form_layout = QtWidgets.QFormLayout(memory_page)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.form_layout.setContentsMargins(-1, -1, 20, 20)

        self.submit_button = QtWidgets.QPushButton('submit', memory_page)
        self.submit_button.setSizePolicy(self.get_size_policy(self.submit_button))
        self.submit_button.setFont(QtGui.QFont('', 12))
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.submit_button)
        self.horizontal_layout.addLayout(self.form_layout)
        self.main_vertical_layout.addLayout(self.horizontal_layout)
        QtCore.QMetaObject.connectSlotsByName(memory_page)

    def toggle_button_background(self, button):
        if button.palette().button().color() == QtGui.QColor("red"):
            button.setStyleSheet(f"background-color: {self.palette().color(QtGui.QPalette.Background)}")
        else:
            button.setStyleSheet(f"background-color: red")
