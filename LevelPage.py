from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functools import partial
from formWidget import FormWidgetIF
from gameDatabaseManagement import GameDatabaseManagement
from GamesEnum import game_database


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.level_rbutton_list = []
        self.username_layout = None
        self.verticalLayout = None
        self.username_label = None
        self.heading = None
        self.gridLayout = None
        self.horizontalLayout = None
        self.formLayout2 = None
        self.previous_window_button = None
        self.next_window_button = None

    def setupUi(self, level_page, username, unlocked_level_number):
        level_page.setMinimumSize(self.get_min_widget())
        level_page.setMaximumSize(self.get_max_widget())
        level_page.setWindowTitle("Select Level")
        level_page.resize(self.get_default_window_size())

        self.verticalLayout = QVBoxLayout(level_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.username_layout = QtWidgets.QFormLayout(level_page)
        self.username_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.username_layout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.username_layout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.username_layout.setContentsMargins(-1, 20, 40, -1)

        self.username_label = QtWidgets.QLabel(username, level_page)
        self.username_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.username_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_label)
        self.verticalLayout.addLayout(self.username_layout)

        self.heading = QtWidgets.QLabel("Levels", level_page)
        self.heading.setSizePolicy(self.get_size_policy(self.heading, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.heading.setFont(QFont('', 26))
        self.heading.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.heading)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)

        for row in range(0, 5):
            for column in range(1, 5):
                button = QRadioButton(f"Level {column + row * 4}", level_page)
                button.setSizePolicy(self.get_size_policy(button, QSizePolicy.Fixed, QSizePolicy.Maximum))
                button.setFont(QFont('', 14))
                button.setChecked(row == 0 and column == 1)
                if column + row * 4 > unlocked_level_number:
                    button.setCheckable(False)
                    button.setToolTip("Not unlocked.")
                self.level_rbutton_list.append(button)
                self.gridLayout.addWidget(button, row, column)

        self.verticalLayout.addLayout(self.gridLayout)
        spacer_up = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_up)

        self.horizontalLayout = QHBoxLayout(level_page)

        self.formLayout2 = QFormLayout(level_page)
        self.formLayout2.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.formLayout2.setContentsMargins(-1, -1, 20, 20)

        self.previous_window_button = QPushButton('return to game menu', level_page)
        self.previous_window_button.setSizePolicy(self.get_size_policy(self.previous_window_button))
        self.previous_window_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previous_window_button)

        self.next_window_button = QPushButton('play', level_page)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.horizontalLayout.addLayout(self.formLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        QtCore.QMetaObject.connectSlotsByName(level_page)

    def make_all_rbuttons_checkable(self):
        for button in self.level_rbutton_list:
            button.setCheckable(True)


class LevelWindow(QtWidgets.QWidget, FormWidget):
    previous_window = QtCore.pyqtSignal(str)
    next_window = QtCore.pyqtSignal(int, str)

    def __init__(self, game_name, username):
        super(LevelWindow, self).__init__()
        unlocked_level_number = self.get_unlocked_level(game_name, username)
        self.shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        self.setupUi(self, username, unlocked_level_number)
        self.shortcut.activated.connect(partial(self.unlock_all_levels, game_name, username))
        self.previous_window_button.clicked.connect(partial(self.go_to_previous_window, username))
        self.next_window_button.clicked.connect(partial(self.go_to_game, game_name, username))

    def get_unlocked_level(self, game_name, username):
        file_path = game_database[game_name]
        database_manager = GameDatabaseManagement(file_path, username)
        unlocked_level_number = database_manager.get_unlocked_level()
        return unlocked_level_number

    def go_to_previous_window(self, username):
        self.previous_window.emit(username)

    def go_to_game(self, game_name, username):
        self.next_window.emit(game_name, username)

    def unlock_all_levels(self, game_name, username):
        file_path = game_database[game_name]
        database_manager = GameDatabaseManagement(file_path, username)
        database_manager.unlock_all_levels()
        self.make_all_rbuttons_checkable()
        print("All levels are unlocked now.")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    control = LevelWindow(username="username")
    control.show()
    sys.exit(app.exec())