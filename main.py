from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.win_height = 800
        self.win_width = 600
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, self.win_height, self.win_width)
        self.setMinimumSize(QtCore.QSize(400, 300))
        self.setMaximumSize(QtCore.QSize(1920, 1080))
        self.setWindowTitle("GRazor Game Launcher")

        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)


class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout1 = QVBoxLayout(self)

        self.label = QLabel("Welcome to GRazors Game Launcher!")
        self.label.setFont(QFont('', 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.layout1.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

        self.layout2 = QVBoxLayout(self)

        self.label2 = QLabel("Do you want to play anonymously or log in?")
        self.label2.setFont(QFont('', 10))
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.layout2.addWidget(self.label2, alignment=QtCore.Qt.AlignCenter)

        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignCenter)

        self.radioButton_3 = QtWidgets.QRadioButton("Anonymously")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.radioButton_3)

        self.radioButton_4 = QtWidgets.QRadioButton("Log in")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.radioButton_4)

        self.layout2.addLayout(self.formLayout_2)
        self.layout1.addLayout(self.layout2)

        self.button1 = QPushButton("next")
        self.layout1.addWidget(self.button1, alignment=QtCore.Qt.AlignRight)
        self.setLayout(self.layout1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MainWindow()
    game.show()
    sys.exit(app.exec())