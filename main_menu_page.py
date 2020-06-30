from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from form_widget import FormWidgetIF


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.win_height = 800
        self.win_width = 600
        self.verticalLayout = None
        self.horizontalLayout = None
        self.radio_buttons_layout = None
        self.LayoutSwitchWindowButtons = None
        self.next_window_button = None
        self.heading = None
        self.layout2 = None
        self.label2 = None
        self.anonymous_rbutton = None
        self.log_in_rbutton = None
        self.sign_up_rbutton = None

    def setupUi(self, main_window):
        main_window.setMinimumSize(self.get_min_widget())
        main_window.setMaximumSize(self.get_max_widget())
        main_window.setWindowTitle("GRazor Game Launcher")
        main_window.resize(self.get_default_window_size())

        self.verticalLayout = QVBoxLayout(main_window)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.heading = QLabel("Welcome to GRazors Game Launcher!", main_window)
        self.heading.setFont(QFont('', 24))
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.verticalLayout.addWidget(self.heading, alignment=QtCore.Qt.AlignCenter)

        self.layout2 = QVBoxLayout(main_window)

        self.label2 = QLabel("Do you want to play anonymously or log in?", main_window)
        self.label2.setFont(QFont('', 10))
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.layout2.addWidget(self.label2, alignment=QtCore.Qt.AlignCenter)

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
        self.layout2.addLayout(self.radio_buttons_layout)

        self.verticalLayout.addLayout(self.layout2)

        self.horizontalLayout = QHBoxLayout(main_window)

        self.LayoutSwitchWindowButtons = QFormLayout(main_window)
        self.LayoutSwitchWindowButtons.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight |
                                                        QtCore.Qt.AlignTrailing)
        self.LayoutSwitchWindowButtons.setContentsMargins(-1, -1, 20, 20)

        self.next_window_button = QPushButton('next', main_window)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QFont('', 12))
        self.LayoutSwitchWindowButtons.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.horizontalLayout.addLayout(self.LayoutSwitchWindowButtons)
        self.verticalLayout.addLayout(self.horizontalLayout)

        main_window.setLayout(self.verticalLayout)

        QtCore.QMetaObject.connectSlotsByName(main_window)


class WindowOne(QWidget, FormWidget):

    signup_window = QtCore.pyqtSignal()
    log_in_window = QtCore.pyqtSignal()
    game_menu_window = QtCore.pyqtSignal()

    def __init__(self):
        super(WindowOne, self).__init__()
        self.setupUi(self)
        self.next_window_button.clicked.connect(self.go_to_next_window)

    def go_to_next_window(self):
        if self.sign_up_rbutton.isChecked():
            self.signup_window.emit()
        elif self.log_in_rbutton.isChecked():
            self.log_in_window.emit()
        elif self.anonymous_rbutton.isChecked():
            self.game_menu_window.emit()
