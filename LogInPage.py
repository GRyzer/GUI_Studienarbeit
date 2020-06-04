from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from formWidget import FormWidgetIF


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.verticalLayout = None
        self.heading = None
        self.formLayout = None
        self.formLayout2 = None
        self.horizontalLayout = None
        self.username_label = None
        self.username_lineEdit = None
        self.previous_window_button = None
        self.next_window_button = None
        self.password_label = None
        self.password_lineEdit = None

    def setupUi(self, login_page):
        login_page.setMinimumSize(self.get_min_widget())
        login_page.setMaximumSize(self.get_max_widget())
        login_page.setWindowTitle("Login")
        login_page.resize(self.get_default_window_size())

        self.verticalLayout = QVBoxLayout(login_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.heading = QLabel("Login", login_page)
        self.heading.setFont(QFont('', 20))
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.verticalLayout.addWidget(self.heading, alignment=QtCore.Qt.AlignCenter)

        self.formLayout = QtWidgets.QFormLayout(login_page)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.formLayout.setContentsMargins(30, 10, 100, 20)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setHorizontalSpacing(14)

        self.username_label = QLabel("Username", login_page)
        self.username_label.setFont(QFont('', 16))
        self.username_label.setAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.username_label)

        self.username_lineEdit = QLineEdit(login_page)
        self.username_lineEdit.setPlaceholderText("Enter your Username")
        self.username_lineEdit.setSizePolicy(self.get_size_policy(self.username_lineEdit, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.username_lineEdit.setFont(QFont('', 16))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_lineEdit)

        self.password_label = QLabel("Password", login_page)
        self.password_label.setFont(QFont('', 16))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.password_label)

        self.password_lineEdit = QLineEdit(login_page)
        self.password_lineEdit.setPlaceholderText("Enter your Password")
        self.password_lineEdit.setSizePolicy(self.get_size_policy(self.password_lineEdit, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.password_lineEdit.setFont(QFont('', 16))
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.password_lineEdit)

        self.horizontalLayout = QHBoxLayout(login_page)

        self.formLayout2 = QFormLayout(login_page)
        self.formLayout2.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.formLayout2.setContentsMargins(-1, -1, 20, 20)

        self.previous_window_button = QPushButton('previous', login_page)
        self.previous_window_button.setSizePolicy(self.get_size_policy(self.previous_window_button))
        self.previous_window_button.setFont(QFont('', 12))
        self.previous_window_button.setToolTip("Going back resets Log in fields")
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previous_window_button)

        self.next_window_button = QPushButton('next', login_page)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout.addLayout(self.formLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        login_page.setLayout(self.verticalLayout)
        QtCore.QMetaObject.connectSlotsByName(login_page)


class LogInWindow(QtWidgets.QWidget, FormWidget):
    previous_window = QtCore.pyqtSignal()
    next_window = QtCore.pyqtSignal(str)

    def __init__(self, account):
        super(LogInWindow, self).__init__()
        self.setupUi(self)
        self.previous_window_button.clicked.connect(self.go_to_previous_window)
        self.next_window_button.clicked.connect(self.go_to_next_window)
        self.account = account

    def go_to_previous_window(self):
        self.previous_window.emit()

    def go_to_next_window(self):
        try:
            self.account.check_credentials(self.username_lineEdit.text(), self.password_lineEdit.text())
            self.next_window.emit(self.username_lineEdit.text())
        except ValueError as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Warning")
            msg_box.setText(str(e))
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
