from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.form_widget import BaseFormWidget
from src.ui.validators import UsernameValidator, PasswordValidator


class FormWidget(BaseFormWidget):
    def __init__(self):
        self.combo_box = None
        self.form_layout = None
        self.form_layout2 = None
        self.heading = None
        self.horizontal_layout = None
        self.label = None
        self.label2 = None
        self.label3 = None
        self.label4 = None
        self.main_vertical_layout = None
        self.next_window_button = None
        self.password_line_edit = None
        self.previous_window_button = None
        self.spin_box = None
        self.username_line_edit = None

    def setupUi(self, signup_page):
        signup_page.setMinimumSize(self.get_min_widget())
        signup_page.setMaximumSize(self.get_max_widget())
        signup_page.setWindowTitle("Sign Up")
        signup_page.resize(self.get_default_window_size())

        self.main_vertical_layout = QtWidgets.QVBoxLayout(signup_page)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.heading = QtWidgets.QLabel("Sign Up", signup_page)
        self.heading.setFont(QtGui.QFont('', 20))
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.main_vertical_layout.addWidget(self.heading, alignment=QtCore.Qt.AlignCenter)

        self.form_layout = QtWidgets.QFormLayout(signup_page)
        self.form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.form_layout.setContentsMargins(20, 10, 100, 20)
        self.form_layout.setVerticalSpacing(20)
        self.form_layout.setHorizontalSpacing(14)

        self.label = QtWidgets.QLabel("Username", signup_page)
        self.label.setFont(QtGui.QFont('', 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)

        self.username_line_edit = QtWidgets.QLineEdit(signup_page)
        self.username_line_edit.setValidator(UsernameValidator())
        self.username_line_edit.setPlaceholderText("Enter your Username")
        self.username_line_edit.setSizePolicy(self.get_size_policy(self.username_line_edit,
                                                                   QtWidgets.QSizePolicy.Expanding,
                                                                   QtWidgets.QSizePolicy.Preferred))
        self.username_line_edit.setFont(QtGui.QFont('', 16))
        self.username_line_edit.setToolTip("Username must have at least 5 characters")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_line_edit)

        self.label2 = QtWidgets.QLabel("Password", signup_page)
        self.label2.setFont(QtGui.QFont('', 16))
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label2)

        self.password_line_edit = QtWidgets.QLineEdit(signup_page)
        self.password_line_edit.setValidator(PasswordValidator())
        self.password_line_edit.setPlaceholderText("Enter your Password")
        self.password_line_edit.setSizePolicy(self.get_size_policy(self.password_line_edit,
                                                                   QtWidgets.QSizePolicy.Expanding,
                                                                   QtWidgets.QSizePolicy.Preferred))
        self.password_line_edit.setFont(QtGui.QFont('', 16))
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line_edit.setToolTip("Password must have at least 8 characters")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.password_line_edit)

        self.label3 = QtWidgets.QLabel("Age", signup_page)
        self.label3.setFont(QtGui.QFont('', 16))
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label3)

        self.spin_box = QtWidgets.QSpinBox(signup_page)
        self.spin_box.setSizePolicy(self.get_size_policy(self.spin_box, QtWidgets.QSizePolicy.Expanding,
                                                         QtWidgets.QSizePolicy.Preferred))
        self.spin_box.setFont(QtGui.QFont('', 16))
        self.spin_box.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_box.setAccelerated(True)
        self.spin_box.setMinimum(12)
        self.spin_box.setMaximum(120)
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spin_box)

        self.label4 = QtWidgets.QLabel("Gender", signup_page)
        self.label4.setFont(QtGui.QFont('', 16))
        self.form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label4)

        self.combo_box = QtWidgets.QComboBox(signup_page)
        self.combo_box.setSizePolicy(self.get_size_policy(self.combo_box, QtWidgets.QSizePolicy.Expanding,
                                                          QtWidgets.QSizePolicy.Preferred))
        self.combo_box.setFont(QtGui.QFont('', 16))
        self.combo_box.addItem("divers")
        self.combo_box.addItem("male")
        self.combo_box.addItem("female")
        self.combo_box.setCurrentText("male")
        self.form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.combo_box)

        self.horizontal_layout = QtWidgets.QHBoxLayout(signup_page)

        self.form_layout2 = QtWidgets.QFormLayout(signup_page)
        self.form_layout2.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.form_layout2.setContentsMargins(-1, -1, 20, 20)

        self.previous_window_button = QtWidgets.QPushButton('previous', signup_page)
        self.previous_window_button.setSizePolicy(self.get_size_policy(self.previous_window_button))
        self.previous_window_button.setFont(QtGui.QFont('', 12))
        self.previous_window_button.setToolTip("Going back resets Log in fields")
        self.form_layout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previous_window_button)

        self.next_window_button = QtWidgets.QPushButton('next', signup_page)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QtGui.QFont('', 12))
        self.form_layout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.main_vertical_layout.addLayout(self.form_layout)
        self.horizontal_layout.addLayout(self.form_layout2)
        self.main_vertical_layout.addLayout(self.horizontal_layout)

        signup_page.setLayout(self.main_vertical_layout)
        QtCore.QMetaObject.connectSlotsByName(signup_page)


class SignUpWindow(QtWidgets.QWidget, FormWidget):
    next_window = QtCore.pyqtSignal(str)
    previous_window = QtCore.pyqtSignal()

    def __init__(self, account):
        super(SignUpWindow, self).__init__()
        self.setupUi(self)
        self.account = account
        self.next_window_button.clicked.connect(self.go_to_next_window)
        self.previous_window_button.clicked.connect(self.go_to_previous_window)

    def go_to_next_window(self):
        try:
            self.validate_credentials()
            self.add_user_account()
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

    def validate_credentials(self):
        if not self.username_line_edit.hasAcceptableInput():
            raise ValueError(f'Username is not valid')
        if not self.password_line_edit.hasAcceptableInput():
            raise ValueError(f'Password is not valid')

    def add_user_account(self):
        self.account.add_account([self.username_line_edit.text(), self.password_line_edit.text(), self.spin_box.value(),
                                  self.combo_box.currentText()])
