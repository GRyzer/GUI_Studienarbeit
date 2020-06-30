from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functools import partial
from form_widget import FormWidgetIF
from games_enum import Game


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.game_button_storage = []
        self.verticalLayout = None
        self.horizontalLayout = None
        self.username_layout = None
        self.username_label = None
        self.gridLayout = None
        self.heading = None
        self.main_menu_button = None

    def setupUi(self, game_menu_page, username):
        game_menu_page.setMinimumSize(self.get_min_widget())
        game_menu_page.setMaximumSize(self.get_max_widget())
        game_menu_page.setWindowTitle("Game Menu")
        game_menu_page.resize(self.get_default_window_size())

        self.verticalLayout = QVBoxLayout(game_menu_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.username_layout = QtWidgets.QFormLayout(game_menu_page)
        self.username_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.username_layout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.username_layout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.username_layout.setContentsMargins(-1, 20, 40, -1)

        self.username_label = QtWidgets.QLabel(username, game_menu_page)
        self.username_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.username_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_label)
        self.verticalLayout.addLayout(self.username_layout)

        self.heading = QtWidgets.QLabel('Game Menu', game_menu_page)
        self.heading.setSizePolicy(self.get_size_policy(self.heading, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.heading.setFont(QFont('', 26))
        self.heading.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.heading)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)

        for row in range(0, 2):
            for column in range(1, 3):
                button = QPushButton(f"{Game(2 * row + column).name}", game_menu_page)
                button.setSizePolicy(self.get_size_policy(button, QSizePolicy.Fixed, QSizePolicy.Maximum))
                button.setFont(QFont('', 14))

                self.game_button_storage.append(button)
                self.gridLayout.addWidget(button, row, column)

        self.verticalLayout.addLayout(self.gridLayout)
        spacer_up = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_up)

        self.horizontalLayout = QHBoxLayout(game_menu_page)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 10)

        self.main_menu_button = QPushButton('return to main menu', game_menu_page)
        self.main_menu_button.setSizePolicy(self.get_size_policy(self.main_menu_button))
        self.main_menu_button.setFont(QFont('', 12))
        self.horizontalLayout.addWidget(self.main_menu_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        QtCore.QMetaObject.connectSlotsByName(game_menu_page)


class GameMenuWindow(QtWidgets.QWidget, FormWidget):
    main_menu_window = QtCore.pyqtSignal()
    game_window = QtCore.pyqtSignal(int, str)

    def __init__(self, username):
        super(GameMenuWindow, self).__init__()
        self.username = username
        self.setupUi(self, username)
        self.connect_buttons_to_game()

    def connect_buttons_to_game(self):
        for enum_value, button in enumerate(self.game_button_storage, 1):
            button.clicked.connect(partial(self.go_to_game, Game(enum_value)))
        self.main_menu_button.clicked.connect(self.go_to_main_menu)

    def go_to_game(self, game_enum_number):
        self.game_window.emit(game_enum_number.value, self.username)

    def go_to_main_menu(self):
        self.main_menu_window.emit()
