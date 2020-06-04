from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functools import partial
from formWidget import FormWidgetIF
from GamesEnum import Game


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.game_button_storage = []
        self.verticalLayout = None
        self.horizontalLayout = None
        self.gridLayout2 = None
        self.gridLayout = None
        self.heading = None
        self.main_menu_button = None
        self.username_label = None
        self.game1_button = None
        self.game2_button = None
        self.game3_button = None
        self.game4_button = None

    def setupUi(self, game_menu_page, username):
        game_menu_page.setMinimumSize(self.get_min_widget())
        game_menu_page.setMaximumSize(self.get_max_widget())
        game_menu_page.setWindowTitle("Login")
        game_menu_page.resize(self.get_default_window_size())

        self.verticalLayout = QVBoxLayout(game_menu_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout = QtWidgets.QGridLayout(game_menu_page)

        self.heading = QtWidgets.QLabel('Game Menu', game_menu_page)
        self.heading.setFont(QFont('', 20))
        self.heading.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.heading.setWordWrap(True)
        self.gridLayout.addWidget(self.heading, 2, 0, 1, 1)

        self.horizontalLayout = QtWidgets.QHBoxLayout(game_menu_page)
        self.horizontalLayout.setContentsMargins(-1, 100, -1, -1)

        self.main_menu_button = QtWidgets.QPushButton('Main Menu', game_menu_page)
        self.main_menu_button.setSizePolicy(self.get_size_policy(self.main_menu_button))

        self.horizontalLayout.addWidget(self.main_menu_button)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.username_label = QtWidgets.QLabel(username, game_menu_page)
        self.username_label.setSizePolicy(self.get_size_policy(self.username_label, QSizePolicy.Minimum,
                                                               QSizePolicy.Minimum))
        self.username_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.gridLayout.addWidget(self.username_label, 0, 0, 1, 1)

        self.gridLayout2 = QtWidgets.QGridLayout(game_menu_page)
        self.gridLayout2.setContentsMargins(20, -1, 20, -1)
        self.gridLayout2.setHorizontalSpacing(20)
        self.gridLayout2.setVerticalSpacing(10)

        self.game1_button = QtWidgets.QPushButton('Game 1', game_menu_page)
        self.game_button_storage.append(self.game1_button)
        self.gridLayout2.addWidget(self.game1_button, 0, 0, 1, 1)

        self.game2_button = QtWidgets.QPushButton('Game 2', game_menu_page)
        self.game_button_storage.append(self.game2_button)
        self.gridLayout2.addWidget(self.game2_button, 0, 1, 1, 1)

        self.game3_button = QtWidgets.QPushButton('Game 3', game_menu_page)
        self.game_button_storage.append(self.game3_button)
        self.gridLayout2.addWidget(self.game3_button, 1, 0, 1, 1)

        self.game4_button = QtWidgets.QPushButton('Game 4', game_menu_page)
        self.game_button_storage.append(self.game4_button)
        self.gridLayout2.addWidget(self.game4_button, 1, 1, 1, 1)

        self.gridLayout.addLayout(self.gridLayout2, 3, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        QtCore.QMetaObject.connectSlotsByName(game_menu_page)


class GameMenuWindow(QtWidgets.QWidget, FormWidget):
    main_menu_window = QtCore.pyqtSignal()
    game_window = QtCore.pyqtSignal(int)

    def __init__(self, username):
        super(GameMenuWindow, self).__init__()
        self.setupUi(self, username)
        self.connect_buttons_to_game()

    def connect_buttons_to_game(self):
        for enum_value, button in enumerate(self.game_button_storage, 1):
            button.clicked.connect(partial(self.go_to_game, Game(enum_value)))
        self.main_menu_button.clicked.connect(self.go_to_main_menu)

    def go_to_game(self, game_enum_number):
        self.game_window.emit(game_enum_number.value)

    def go_to_main_menu(self):
        self.main_menu_window.emit()
