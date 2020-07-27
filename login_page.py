from PyQt5 import QtWidgets, QtCore, QtGui

from form_widget import FormWidgetIF


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.form_layout = None
        self.form_layout2 = None
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

        self.horizontal_layout = QtWidgets.QHBoxLayout(login_page)

        self.form_layout2 = QtWidgets.QFormLayout(login_page)
        self.form_layout2.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.form_layout2.setContentsMargins(-1, -1, 20, 20)

        self.previous_window_button = QtWidgets.QPushButton('previous', login_page)
        self.previous_window_button.setSizePolicy(self.get_size_policy(self.previous_window_button))
        self.previous_window_button.setFont(QtGui.QFont('', 12))
        self.previous_window_button.setToolTip("Going back resets Log in fields")
        self.form_layout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previous_window_button)

        self.next_window_button = QtWidgets.QPushButton('next', login_page)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QtGui.QFont('', 12))
        self.form_layout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.vertical_layout.addLayout(self.form_layout)
        self.horizontal_layout.addLayout(self.form_layout2)
        self.vertical_layout.addLayout(self.horizontal_layout)

        login_page.setLayout(self.vertical_layout)
        QtCore.QMetaObject.connectSlotsByName(login_page)


class LogInWindow(QtWidgets.QWidget, FormWidget):
    next_window = QtCore.pyqtSignal(str)
    previous_window = QtCore.pyqtSignal()

    def __init__(self, account):
        super(LogInWindow, self).__init__()
        self.account = account
        self.setupUi(self)
        self.next_window_button.clicked.connect(self.go_to_next_window)
        self.previous_window_button.clicked.connect(self.go_to_previous_window)

    def go_to_next_window(self):
        try:
            self.account.check_credentials(self.username_line_edit.text(), self.password_line_edit.text())
            self.next_window.emit(self.username_line_edit.text())
        except ValueError as e:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle("Warning")
            msg_box.setText(str(e))
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.exec()

    def go_to_previous_window(self):
        self.previous_window.emit()
