from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.base_form_widget import BaseFormWidget
from src.ui.validators import PasswordValidator


class FormWidget(BaseFormWidget):
    def __init__(self):
        self.account_reset_button = None
        self.form_layout = None
        self.heading = None
        self.horizontal_layout = None
        self.next_window_button = None
        self.password_label = None
        self.password_line_edit = None
        self.previous_window_button = None
        self.username_label = None
        self.username_line_edit = None
        self.vertical_layout = None

    def setupUi(self, login_page):
        login_page.setMinimumSize(self.get_min_widget())
        login_page.setMaximumSize(self.get_max_widget())
        login_page.setWindowTitle("Login")
        login_page.resize(self.get_default_window_size())

        self.vertical_layout = QtWidgets.QVBoxLayout(login_page)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.heading = QtWidgets.QLabel("Login", login_page)
        self.heading.setFont(QtGui.QFont('', 20))
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.vertical_layout.addWidget(self.heading, alignment=QtCore.Qt.AlignCenter)

        self.form_layout = QtWidgets.QFormLayout(login_page)
        self.form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.form_layout.setContentsMargins(30, 10, 100, 20)
        self.form_layout.setVerticalSpacing(20)
        self.form_layout.setHorizontalSpacing(14)

        self.username_label = QtWidgets.QLabel("Username", login_page)
        self.username_label.setFont(QtGui.QFont('', 16))
        self.username_label.setAlignment(QtCore.Qt.AlignCenter)
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.username_label)

        self.username_line_edit = QtWidgets.QLineEdit(login_page)
        self.username_line_edit.setPlaceholderText("Enter your Username")
        self.username_line_edit.setSizePolicy(self.get_size_policy(self.username_line_edit,
                                                                   QtWidgets.QSizePolicy.Expanding,
                                                                   QtWidgets.QSizePolicy.Preferred))
        self.username_line_edit.setFont(QtGui.QFont('', 16))
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_line_edit)

        self.password_label = QtWidgets.QLabel("Password", login_page)
        self.password_label.setFont(QtGui.QFont('', 16))
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.password_label)

        self.password_line_edit = QtWidgets.QLineEdit(login_page)
        self.password_line_edit.setPlaceholderText("Enter your Password")
        self.password_line_edit.setSizePolicy(self.get_size_policy(self.password_line_edit,
                                                                   QtWidgets.QSizePolicy.Expanding,
                                                                   QtWidgets.QSizePolicy.Preferred))
        self.password_line_edit.setFont(QtGui.QFont('', 16))
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.password_line_edit)

        self.set_buttons(login_page)

        self.vertical_layout.addLayout(self.form_layout)
        self.vertical_layout.addLayout(self.horizontal_layout)

        login_page.setLayout(self.vertical_layout)
        QtCore.QMetaObject.connectSlotsByName(login_page)

    def set_buttons(self, login_page):
        self.horizontal_layout = QtWidgets.QHBoxLayout(login_page)
        self.horizontal_layout.setContentsMargins(-1, -1, 20, 20)

        self.previous_window_button = QtWidgets.QPushButton('previous', login_page)
        self.previous_window_button.setSizePolicy(self.get_size_policy(self.previous_window_button))
        self.previous_window_button.setFont(QtGui.QFont('', 12))
        self.previous_window_button.setToolTip("Going to start page resets Log in fields")

        self.next_window_button = QtWidgets.QPushButton('Game menu', login_page)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QtGui.QFont('', 12))

        self.account_reset_button = QtWidgets.QPushButton('Reset password', login_page)
        self.account_reset_button.setSizePolicy(self.get_size_policy(self.account_reset_button))
        self.account_reset_button.setFont(QtGui.QFont('', 12))

        self.horizontal_layout.addWidget(self.account_reset_button)
        self.horizontal_layout.addWidget(self.previous_window_button)
        self.horizontal_layout.addWidget(self.next_window_button)
        self.horizontal_layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)


class LogInWindow(QtWidgets.QWidget, FormWidget):
    next_window_signal = QtCore.pyqtSignal(str)
    previous_window_signal = QtCore.pyqtSignal()

    def __init__(self, account):
        super(LogInWindow, self).__init__()
        self.account = account
        self.setupUi(self)
        self.next_window_button.clicked.connect(self.emit_next_window_signal)
        self.previous_window_button.clicked.connect(self.emit_previous_window_signal)
        self.account_reset_button.clicked.connect(self.reset_account)

    def emit_next_window_signal(self):
        try:
            self.account.check_credentials(self.username_line_edit.text(), self.password_line_edit.text())
            self.next_window_signal.emit(self.username_line_edit.text())
        except ValueError as e:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle("Warning")
            msg_box.setText(str(e))
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.exec()

    def emit_previous_window_signal(self):
        self.previous_window_signal.emit()

    def reset_account(self):
        self.reset_account = ResetAccountWindow(self.account)
        self.reset_account.show()
        print("Hallo")


class ResetAccountWindow(QtWidgets.QWidget, BaseFormWidget):
    submit_signal = QtCore.pyqtSignal()

    def __init__(self, account):
        self.account = account
        super(ResetAccountWindow, self).__init__()
        self.setMinimumSize(QtCore.QSize(600, 400))
        self.setMaximumSize(self.get_max_widget())
        self.setWindowTitle("Reset account")
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.heading = QtWidgets.QLabel("Reset your account.", self)
        self.heading.setFont(QtGui.QFont('', 20))
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.vertical_layout.addWidget(self.heading, alignment=QtCore.Qt.AlignCenter)

        self.form_layout = QtWidgets.QFormLayout(self)
        self.form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.form_layout.setContentsMargins(30, 10, 30, 20)
        self.form_layout.setVerticalSpacing(20)
        self.form_layout.setHorizontalSpacing(14)

        self.username_label = QtWidgets.QLabel("Username", self)
        self.username_label.setFont(QtGui.QFont('', 16))
        self.username_label.setAlignment(QtCore.Qt.AlignCenter)
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.username_label)

        self.username_line_edit = QtWidgets.QLineEdit(self)
        self.username_line_edit.setPlaceholderText("Enter your Username.")
        self.username_line_edit.setSizePolicy(self.get_size_policy(self.username_line_edit,
                                                                   QtWidgets.QSizePolicy.Expanding,
                                                                   QtWidgets.QSizePolicy.Preferred))
        self.username_line_edit.setFont(QtGui.QFont('', 16))
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_line_edit)

        self.security_query = QtWidgets.QLabel("Security query", self)
        self.security_query.setFont(QtGui.QFont('', 16))
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.security_query)

        self.security_query_line_edit = QtWidgets.QLineEdit(self)
        self.security_query_line_edit.setPlaceholderText("Enter your favorite song.")
        self.security_query_line_edit.setSizePolicy(self.get_size_policy(self.security_query_line_edit,
                                                                         QtWidgets.QSizePolicy.Expanding,
                                                                         QtWidgets.QSizePolicy.Preferred))
        self.security_query_line_edit.setFont(QtGui.QFont('', 16))
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.security_query_line_edit)

        self.password_label = QtWidgets.QLabel("Password", self)
        self.password_label.setFont(QtGui.QFont('', 16))
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.password_label)

        self.password_line_edit = QtWidgets.QLineEdit(self)
        self.password_line_edit.setValidator(PasswordValidator())
        self.password_line_edit.setPlaceholderText("Enter your new Password")
        self.password_line_edit.setSizePolicy(self.get_size_policy(self.password_line_edit,
                                                                   QtWidgets.QSizePolicy.Expanding,
                                                                   QtWidgets.QSizePolicy.Preferred))
        self.password_line_edit.setFont(QtGui.QFont('', 16))
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line_edit.setToolTip("Password must have at least 8 characters")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.password_line_edit)

        self.vertical_layout.addLayout(self.form_layout)

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(-1, -1, 20, 20)

        self.submit_button = QtWidgets.QPushButton('Submit', self)
        self.submit_button.setSizePolicy(self.get_size_policy(self.submit_button))
        self.submit_button.setFont(QtGui.QFont('', 12))

        self.horizontal_layout.addWidget(self.submit_button)
        self.horizontal_layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
        self.vertical_layout.addLayout(self.horizontal_layout)

        self.setLayout(self.vertical_layout)

        self.submit_button.clicked.connect(self.reset)

    def verify_password(self):
        if not self.password_line_edit.hasAcceptableInput():
            raise ValueError(f'Password is not valid.')

    def reset(self):
        try:
            self.verify_password()
            self.account.reset_account(self.username_line_edit.text(), self.security_query_line_edit.text(),
                                       self.password_line_edit.text())
            self.close()
        except ValueError as e:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle("Warning")
            msg_box.setText(str(e))
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.exec()