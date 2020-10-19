from PyQt5 import QtWidgets, QtCore, QtGui

from src.form_widget import BaseFormWidget


class FormWidget(BaseFormWidget):
    def __init__(self):
        self.anonymous_rbutton = None
        self.form_layout = None
        self.heading = None
        self.horizontal_layout = None
        self.label = None
        self.log_in_rbutton = None
        self.next_window_button = None
        self.radio_buttons_layout = None
        self.sign_up_rbutton = None
        self.vertical_layout = None
        self.win_height = 800
        self.win_width = 600
        self.vertical_layout2 = None

    def setupUi(self, main_window):
        main_window.setMinimumSize(self.get_min_widget())
        main_window.setMaximumSize(self.get_max_widget())
        main_window.setWindowTitle("GRazor Game Launcher")
        main_window.resize(self.get_default_window_size())

        self.vertical_layout = QtWidgets.QVBoxLayout(main_window)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.heading = QtWidgets.QLabel("Welcome to GRazors Game Launcher!", main_window)
        self.heading.setFont(QtGui.QFont('', 24))
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.vertical_layout.addWidget(self.heading, alignment=QtCore.Qt.AlignCenter)

        self.vertical_layout2 = QtWidgets.QVBoxLayout(main_window)

        self.label = QtWidgets.QLabel("Do you want to play anonymously or log in?", main_window)
        self.label.setFont(QtGui.QFont('', 10))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.vertical_layout2.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

        self.radio_buttons_layout = QtWidgets.QHBoxLayout()
        self.radio_buttons_layout.setSpacing(14)

        spacer_left = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.radio_buttons_layout.addItem(spacer_left)

        self.anonymous_rbutton = QtWidgets.QRadioButton("Anonymous", main_window)
        self.anonymous_rbutton.setChecked(True)
        self.anonymous_rbutton.setSizePolicy(self.get_size_policy(self.anonymous_rbutton))
        self.radio_buttons_layout.addWidget(self.anonymous_rbutton, alignment=QtCore.Qt.AlignCenter)

        self.log_in_rbutton = QtWidgets.QRadioButton("Log in", main_window)
        self.log_in_rbutton.setSizePolicy(self.get_size_policy(self.log_in_rbutton))
        self.radio_buttons_layout.addWidget(self.log_in_rbutton, alignment=QtCore.Qt.AlignCenter)

        self.sign_up_rbutton = QtWidgets.QRadioButton("Sign Up", main_window)
        self.sign_up_rbutton.setSizePolicy(self.get_size_policy(self.sign_up_rbutton))
        self.radio_buttons_layout.addWidget(self.sign_up_rbutton, alignment=QtCore.Qt.AlignCenter)

        spacer_right = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.radio_buttons_layout.addItem(spacer_right)
        self.vertical_layout2.addLayout(self.radio_buttons_layout)

        self.vertical_layout.addLayout(self.vertical_layout2)

        self.horizontal_layout = QtWidgets.QHBoxLayout(main_window)

        self.form_layout = QtWidgets.QFormLayout(main_window)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight |
                                          QtCore.Qt.AlignTrailing)
        self.form_layout.setContentsMargins(-1, -1, 20, 20)

        self.next_window_button = QtWidgets.QPushButton('next', main_window)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QtGui.QFont('', 12))
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.horizontal_layout.addLayout(self.form_layout)
        self.vertical_layout.addLayout(self.horizontal_layout)

        main_window.setLayout(self.vertical_layout)

        QtCore.QMetaObject.connectSlotsByName(main_window)


class MainMenu(QtWidgets.QWidget, FormWidget):
    game_menu_window = QtCore.pyqtSignal()
    log_in_window = QtCore.pyqtSignal()
    signup_window = QtCore.pyqtSignal()

    def __init__(self):
        super(MainMenu, self).__init__()
        self.setupUi(self)
        self.next_window_button.clicked.connect(self.go_to_next_window)

    def go_to_next_window(self):
        if self.sign_up_rbutton.isChecked():
            self.signup_window.emit()
        elif self.log_in_rbutton.isChecked():
            self.log_in_window.emit()
        elif self.anonymous_rbutton.isChecked():
            self.game_menu_window.emit()
