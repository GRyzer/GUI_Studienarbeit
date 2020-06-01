from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from formWidget import FormWidgetIF
from validators import UsernameValidator, PasswordValidator


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.verticalLayout = None
        self.formLayout = None
        self.horizontalLayout = None
        self.formLayout2 = None
        self.heading = None
        self.label = None
        self.label2 = None
        self.label3 = None
        self.label4 = None
        self.lineEdit = None
        self.lineEdit2 = None
        self.spinBox = None
        self.comboBox = None
        self.previous_window_button = None
        self.next_window_button = None

    def setupUi(self, second_page):
        second_page.setMinimumSize(self.get_min_widget())
        second_page.setMaximumSize(self.get_max_widget())
        second_page.setWindowTitle("Log In screen")
        second_page.resize(self.get_default_window_size())

        self.verticalLayout = QVBoxLayout(second_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.heading = QLabel("Sign Up", second_page)
        self.heading.setFont(QFont('', 20))
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.verticalLayout.addWidget(self.heading, alignment=QtCore.Qt.AlignCenter)

        self.formLayout = QtWidgets.QFormLayout(second_page)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.formLayout.setContentsMargins(20, 10, 100, 20)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setHorizontalSpacing(14)

        self.label = QLabel("Username", second_page)
        self.label.setFont(QFont('', 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)

        self.lineEdit = QLineEdit(second_page)
        self.lineEdit.setValidator(UsernameValidator())
        self.lineEdit.setPlaceholderText("Enter your Username")
        self.lineEdit.setSizePolicy(self.get_size_policy(self.lineEdit, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.lineEdit.setFont(QFont('', 16))
        self.lineEdit.setToolTip("Username must have at least 5 characters")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.label2 = QLabel("Password", second_page)
        self.label2.setFont(QFont('', 16))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label2)

        self.lineEdit2 = QLineEdit(second_page)
        self.lineEdit2.setValidator(PasswordValidator())
        self.lineEdit2.setPlaceholderText("Enter your Password")
        self.lineEdit2.setSizePolicy(self.get_size_policy(self.lineEdit2, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.lineEdit2.setFont(QFont('', 16))
        self.lineEdit2.setEchoMode(QLineEdit.Password)
        self.lineEdit2.setToolTip("Password must have at least 8 characters")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit2)

        self.label3 = QLabel("Age", second_page)
        self.label3.setFont(QFont('', 16))
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label3)

        self.spinBox = QSpinBox(second_page)
        self.spinBox.setSizePolicy(self.get_size_policy(self.spinBox, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.spinBox.setFont(QFont('', 16))
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox.setAccelerated(True)
        self.spinBox.setMinimum(12)
        self.spinBox.setMaximum(120)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox)

        self.label4 = QLabel("Gender", second_page)
        self.label4.setFont(QFont('', 16))
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label4)

        self.comboBox = QComboBox(second_page)
        self.comboBox.setSizePolicy(self.get_size_policy(self.comboBox, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.comboBox.setFont(QFont('', 16))
        self.comboBox.addItem("divers")
        self.comboBox.addItem("male")
        self.comboBox.addItem("female")
        self.comboBox.setCurrentText("male")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox)

        self.horizontalLayout = QHBoxLayout(second_page)

        self.formLayout2 = QFormLayout(second_page)
        self.formLayout2.setFormAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.formLayout2.setContentsMargins(-1, -1, 20, 20)

        self.previous_window_button = QPushButton('previous', second_page)
        self.previous_window_button.setSizePolicy(self.get_size_policy(self.previous_window_button))
        self.previous_window_button.setFont(QFont('', 12))
        self.previous_window_button.setToolTip("Going back resets Log in fields")
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previous_window_button)

        self.next_window_button = QPushButton('next', second_page)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout.addLayout(self.formLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        second_page.setLayout(self.verticalLayout)
        QtCore.QMetaObject.connectSlotsByName(second_page)


class SignUpWindow(QtWidgets.QWidget, FormWidget):

    previous_window = QtCore.pyqtSignal()
    next_window = QtCore.pyqtSignal()

    def __init__(self):
        super(SignUpWindow, self).__init__()
        self.setupUi(self)
        self.previous_window_button.clicked.connect(self.go_to_previous_window)
        self.next_window_button.clicked.connect(self.go_to_next_window)

    def go_to_previous_window(self):
        self.previous_window.emit()

    def go_to_next_window(self):
        if self.conditions_are_met():
            print("has acceptable input")
        else:
            print("No")
        self.next_window.emit()

    def conditions_are_met(self, *args, **kwargs):
        print("it is fine")
        print(*args)
        return False
