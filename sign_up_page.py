from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from form_widget import FormWidgetIF
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
        self.username_lineEdit = None
        self.password_lineEdit = None
        self.spinBox = None
        self.comboBox = None
        self.previous_window_button = None
        self.next_window_button = None

    def setupUi(self, signup_page):
        signup_page.setMinimumSize(self.get_min_widget())
        signup_page.setMaximumSize(self.get_max_widget())
        signup_page.setWindowTitle("Sign Up")
        signup_page.resize(self.get_default_window_size())

        self.verticalLayout = QVBoxLayout(signup_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.heading = QLabel("Sign Up", signup_page)
        self.heading.setFont(QFont('', 20))
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.verticalLayout.addWidget(self.heading, alignment=QtCore.Qt.AlignCenter)

        self.formLayout = QtWidgets.QFormLayout(signup_page)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.formLayout.setContentsMargins(20, 10, 100, 20)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setHorizontalSpacing(14)

        self.label = QLabel("Username", signup_page)
        self.label.setFont(QFont('', 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)

        self.username_lineEdit = QLineEdit(signup_page)
        self.username_lineEdit.setValidator(UsernameValidator())
        self.username_lineEdit.setPlaceholderText("Enter your Username")
        self.username_lineEdit.setSizePolicy(self.get_size_policy(self.username_lineEdit, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.username_lineEdit.setFont(QFont('', 16))
        self.username_lineEdit.setToolTip("Username must have at least 5 characters")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_lineEdit)

        self.label2 = QLabel("Password", signup_page)
        self.label2.setFont(QFont('', 16))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label2)

        self.password_lineEdit = QLineEdit(signup_page)
        self.password_lineEdit.setValidator(PasswordValidator())
        self.password_lineEdit.setPlaceholderText("Enter your Password")
        self.password_lineEdit.setSizePolicy(self.get_size_policy(self.password_lineEdit, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.password_lineEdit.setFont(QFont('', 16))
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        self.password_lineEdit.setToolTip("Password must have at least 8 characters")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.password_lineEdit)

        self.label3 = QLabel("Age", signup_page)
        self.label3.setFont(QFont('', 16))
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label3)

        self.spinBox = QSpinBox(signup_page)
        self.spinBox.setSizePolicy(self.get_size_policy(self.spinBox, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.spinBox.setFont(QFont('', 16))
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox.setAccelerated(True)
        self.spinBox.setMinimum(12)
        self.spinBox.setMaximum(120)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox)

        self.label4 = QLabel("Gender", signup_page)
        self.label4.setFont(QFont('', 16))
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label4)

        self.comboBox = QComboBox(signup_page)
        self.comboBox.setSizePolicy(self.get_size_policy(self.comboBox, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.comboBox.setFont(QFont('', 16))
        self.comboBox.addItem("divers")
        self.comboBox.addItem("male")
        self.comboBox.addItem("female")
        self.comboBox.setCurrentText("male")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox)

        self.horizontalLayout = QHBoxLayout(signup_page)

        self.formLayout2 = QFormLayout(signup_page)
        self.formLayout2.setFormAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.formLayout2.setContentsMargins(-1, -1, 20, 20)

        self.previous_window_button = QPushButton('previous', signup_page)
        self.previous_window_button.setSizePolicy(self.get_size_policy(self.previous_window_button))
        self.previous_window_button.setFont(QFont('', 12))
        self.previous_window_button.setToolTip("Going back resets Log in fields")
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previous_window_button)

        self.next_window_button = QPushButton('next', signup_page)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout.addLayout(self.formLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        signup_page.setLayout(self.verticalLayout)
        QtCore.QMetaObject.connectSlotsByName(signup_page)


class SignUpWindow(QtWidgets.QWidget, FormWidget):

    previous_window = QtCore.pyqtSignal()
    next_window = QtCore.pyqtSignal(str)

    def __init__(self, account):
        super(SignUpWindow, self).__init__()
        self.setupUi(self)
        self.previous_window_button.clicked.connect(self.go_to_previous_window)
        self.next_window_button.clicked.connect(self.go_to_next_window)
        self.account = account

    def go_to_previous_window(self):
        self.previous_window.emit()

    def go_to_next_window(self):
        try:
            self.validate_credentials()
            self.add_user_account()
            self.next_window.emit(self.username_lineEdit.text())
        except ValueError as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Warning")
            msg_box.setText(str(e))
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def validate_credentials(self):
        if not self.username_lineEdit.hasAcceptableInput():
            raise ValueError(f'Username is not valid')
        if not self.password_lineEdit.hasAcceptableInput():
            raise ValueError(f'Password is not valid')

    def add_user_account(self):
        self.account.add_account([self.username_lineEdit.text(), self.password_lineEdit.text(), self.spinBox.value(), self.comboBox.currentText()])
