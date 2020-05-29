from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class FormWidget:
    def __init__(self):
        self.win_height = 800
        self.win_width = 600
        self.layout1 = None
        self.button1 = None
        self.label = None
        self.layout2 = None
        self.label2 = None
        self.formLayout_2 = None
        self.radioButton_3 = None
        self.radioButton_4 = None

    def setupUi(self, main_window):

        # main_window.setGeometry(100, 100, self.win_height, self.win_width)
        main_window.setMinimumSize(QtCore.QSize(400, 300))
        main_window.setMaximumSize(QtCore.QSize(1920, 1080))
        main_window.setWindowTitle("GRazor Game Launcher")
        main_window.resize(self.win_height, self.win_width)

        self.layout1 = QVBoxLayout(main_window)

        self.label = QLabel("Welcome to GRazors Game Launcher!", main_window)
        self.label.setFont(QFont('', 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.layout1.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

        self.layout2 = QVBoxLayout(main_window)

        self.label2 = QLabel("Do you want to play anonymously or log in?", main_window)
        self.label2.setFont(QFont('', 10))
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.layout2.addWidget(self.label2, alignment=QtCore.Qt.AlignCenter)

        self.formLayout_2 = QtWidgets.QFormLayout(main_window)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignCenter)

        self.radioButton_3 = QtWidgets.QRadioButton("Anonymously", main_window)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.radioButton_3)

        self.radioButton_4 = QtWidgets.QRadioButton("Log in", main_window)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.radioButton_4)

        self.layout2.addLayout(self.formLayout_2)
        self.layout1.addLayout(self.layout2)

        self.button1 = QPushButton("next", main_window)

        self.layout1.addWidget(self.button1, alignment=QtCore.Qt.AlignRight)
        main_window.setLayout(self.layout1)

        QtCore.QMetaObject.connectSlotsByName(main_window)


class WindowOne(QWidget, FormWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(WindowOne, self).__init__()
        self.setupUi(self)
        self.button1.clicked.connect(self.pushbutton_handler)

    def pushbutton_handler(self):
        self.switch_window.emit()