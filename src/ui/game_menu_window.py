from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.base_form_widget import BaseFormWidget
from src.games.game_enum import Game


class FormWidget(BaseFormWidget):
    def __init__(self):
        self.game_button_storage = []
        self.grid_layout = None
        self.heading = None
        self.horizontal_layout = None
        self.main_vertical_layout = None
        self.main_menu_button = None
        self.username_layout = None
        self.username_label = None

    def setupUi(self, game_menu_page, username):
        game_menu_page.setMinimumSize(self.get_min_widget())
        game_menu_page.setMaximumSize(self.get_max_widget())
        game_menu_page.setWindowTitle("Game Menu")
        game_menu_page.resize(self.get_default_window_size())

        self.main_vertical_layout = QtWidgets.QVBoxLayout(game_menu_page)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.username_layout = QtWidgets.QFormLayout(game_menu_page)
        self.username_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.username_layout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.username_layout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.username_layout.setContentsMargins(-1, 20, 40, -1)

        self.username_label = QtWidgets.QLabel(username, game_menu_page)
        self.username_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.username_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_label)
        self.main_vertical_layout.addLayout(self.username_layout)

        self.heading = QtWidgets.QLabel('Game Menu', game_menu_page)
        self.heading.setSizePolicy(self.get_size_policy(self.heading, QtWidgets.QSizePolicy.Minimum,
                                                        QtWidgets.QSizePolicy.Expanding))
        self.heading.setFont(QtGui.QFont('', 26))
        self.heading.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.main_vertical_layout.addWidget(self.heading)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        for row in range(0, 2):
            for column in range(1, 3):
                button = QtWidgets.QPushButton(f"{Game(2 * row + column).name}", game_menu_page)
                button.setSizePolicy(self.get_size_policy(button, QtWidgets.QSizePolicy.Fixed,
                                                          QtWidgets.QSizePolicy.Maximum))
                button.setFont(QtGui.QFont('', 14))

                self.game_button_storage.append(button)
                self.grid_layout.addWidget(button, row, column)

        self.main_vertical_layout.addLayout(self.grid_layout)
        spacer_up = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_vertical_layout.addItem(spacer_up)

        self.horizontal_layout = QtWidgets.QHBoxLayout(game_menu_page)
        self.horizontal_layout.setContentsMargins(-1, -1, -1, 10)

        self.main_menu_button = QtWidgets.QPushButton('return to main menu', game_menu_page)
        self.main_menu_button.setSizePolicy(self.get_size_policy(self.main_menu_button))
        self.main_menu_button.setFont(QtGui.QFont('', 12))
        self.horizontal_layout.addWidget(self.main_menu_button)

        self.main_vertical_layout.addLayout(self.horizontal_layout)

        QtCore.QMetaObject.connectSlotsByName(game_menu_page)


class GameMenuWindow(QtWidgets.QWidget, FormWidget):
    game_signal = QtCore.pyqtSignal(int, str)
    main_menu_signal = QtCore.pyqtSignal()

    def __init__(self, username):
        super(GameMenuWindow, self).__init__()
        self.username = username
        self.setupUi(self, username)
        self.connect_buttons_to_game()

    def connect_buttons_to_game(self):
        for enum_value, button in enumerate(self.game_button_storage, 1):
            button.clicked.connect(partial(self.emit_game_signal, Game(enum_value)))
        self.main_menu_button.clicked.connect(self.emit_main_menu_signal)

    def emit_game_signal(self, game_enum_number):
        self.game_signal.emit(game_enum_number.value, self.username)

    def emit_main_menu_signal(self):
        self.main_menu_signal.emit()
