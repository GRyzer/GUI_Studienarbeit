from functools import partial
import random

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from formWidget import FormWidgetIF
from gameDatabaseManagement import GameDatabaseManagement


class Level:
    LEVEL1 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 9250, "buttons": 5}
    LEVEL2 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 8250, "buttons": 5}
    LEVEL3 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 9700, "buttons": 6}
    LEVEL4 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 8700, "buttons": 6}
    LEVEL5 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 10150, "buttons": 7}
    LEVEL6 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 9150, "buttons": 7}
    LEVEL7 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 10600, "buttons": 8}
    LEVEL8 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 9600, "buttons": 8}
    LEVEL9 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 11050, "buttons": 9}
    LEVEL10 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 10050, "buttons": 9}
    LEVEL11 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 10500, "buttons": 10}
    LEVEL12 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 10950, "buttons": 11}
    LEVEL13 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 11400, "buttons": 12}
    LEVEL14 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 11850, "buttons": 13}
    LEVEL15 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 12300, "buttons": 14}
    LEVEL16 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 12750, "buttons": 15}
    LEVEL17 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 12200, "buttons": 16}
    LEVEL18 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 12650, "buttons": 17}
    LEVEL19 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 13100, "buttons": 18}
    LEVEL20 = {"start_time": 1000, "increment": 450, "stay_on": True, "end_time": 13550, "buttons": 19}

    @classmethod
    def get_play_dict(cls, level_number):
        return getattr(cls, f"LEVEL{level_number}")


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.grid_layout = None
        self.button_list = []

    def setupUi(self, memory_page, color, selected_level):
        memory_page.setMinimumSize(self.get_min_widget())
        memory_page.setMaximumSize(self.get_max_widget())
        memory_page.setWindowTitle(f"Memory, Level {selected_level}")
        memory_page.resize(QtCore.QSize(800, 800))

        self.verticalLayout = QVBoxLayout(memory_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout = QtWidgets.QGridLayout(memory_page)
        self.grid_layout.setSpacing(5)

        self.grid_layout.setSizeConstraint(QLayout.SetFixedSize)

        for index in range(256):
            button = QPushButton(memory_page)
            button.setFixedSize(QtCore.QSize(40, 40))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setStyleSheet(f"background-color: {color}")
            button.clicked.connect(partial(self.change_button_background, button))
            self.button_list.append(button)
            self.grid_layout.addWidget(button, index // 16, index % 16)

        self.verticalLayout.addLayout(self.grid_layout)
        self.horizontalLayout = QHBoxLayout(memory_page)

        self.formLayout2 = QFormLayout(memory_page)
        self.formLayout2.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.formLayout2.setContentsMargins(-1, -1, 20, 20)

        self.submit_button = QPushButton('submit', memory_page)
        self.submit_button.setSizePolicy(self.get_size_policy(self.submit_button))
        self.submit_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.submit_button)
        self.horizontalLayout.addLayout(self.formLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        QtCore.QMetaObject.connectSlotsByName(memory_page)

    def change_button_background(self, button):
        if button.palette().button().color() == QColor("red"):
            button.setStyleSheet(f"background-color: {self.palette().color(QPalette.Background)}")
        else:
            button.setStyleSheet(f"background-color: red")


class MemoryWindow(QtWidgets.QWidget, FormWidget):
    database_path = "databases/memory.csv"
    game_menu_window = QtCore.pyqtSignal()
    level_menu = QtCore.pyqtSignal()
    next_level = QtCore.pyqtSignal(int)
    play_level_again = QtCore.pyqtSignal(int)
    max_level = 20

    def __init__(self, username):
        super(MemoryWindow, self).__init__()
        self.program_selected_buttons = []
        self.level_dict = {}
        self.game_database = GameDatabaseManagement(self.database_path, username)

    def get_unlocked_level(self):
        return self.game_database.get_unlocked_level()

    def unlock_next_level(self, level):
        if level == self.get_unlocked_level():
            self.game_database.unlock_level(level+1)

    def unlock_all_levels(self):
        self.game_database.unlock_all_levels()

    def goto_game_menu(self):
        self.game_menu_window.emit()

    def goto_next_level(self):
        if self.selected_level + 1 <= self.get_unlocked_level():
            self.next_level.emit(self.selected_level + 1)

    def goto_level_selection(self):
        self.level_menu.emit()

    def goto_play_level_again(self):
        self.play_level_again.emit(self.selected_level)

    def play_game(self, level):
        self.selected_level = level
        self.setupUi(self, self.palette().color(QPalette.Background), self.selected_level)
        self.show()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Round screen")
        msg_box.setText("Do you want to start?")
        msg_box.addButton(QPushButton('Start'), QMessageBox.AcceptRole)
        msg_box.addButton(QPushButton('Go to main menu'), QMessageBox.RejectRole)
        t = msg_box.exec()
        if t == QMessageBox.AcceptRole:
            self.flicker_the_buttons(Level.get_play_dict(level))
        elif t == QMessageBox.RejectRole:
            self.goto_game_menu()

    def flicker_the_buttons(self, play_dict):
        rnd_button_list = random.sample(range(0, len(self.button_list)), play_dict["buttons"])
        start_value = play_dict["start_time"]
        self.disable_buttons()
        for element in rnd_button_list:
            button = self.button_list[element]
            self.program_selected_buttons.append(button)
            self.change_button_background2(button, "red")
            start_value += play_dict["increment"]
            timer2 = QtCore.QTimer(self)
            timer2.setSingleShot(True)
            if play_dict["stay_on"]:
                timer2.start(play_dict["end_time"])
            else:
                timer2.start(start_value)
            timer2.timeout.connect(partial(self.change_button_background2, button,
                                           self.palette().color(QPalette.Background)))
        timer = QtCore.QTimer(self)
        timer.setSingleShot(True)
        timer.start(play_dict["end_time"])
        timer.timeout.connect(self.enable_buttons)

    def change_button_background2(self, button, color):
        button.setStyleSheet(f"background-color: {color}")

    def disable_buttons(self):
        for button in self.button_list:
            button.setEnabled(False)
        self.submit_button.disconnect()

    def enable_buttons(self):
        for button in self.button_list:
            button.setEnabled(True)
        self.submit_button.clicked.connect(self.end_of_game)

    def end_of_game(self):
        self.disable_buttons()
        user_selected_list = []
        for button in self.button_list:
            if button.palette().button().color() == QColor("red"):
                user_selected_list.append(button)
        self.show_solution()
        self.show_message_based_on_game_result(user_selected_list)

    def show_message_based_on_game_result(self, user_selected_list):
        if set(user_selected_list) == set(self.program_selected_buttons):
            if self.selected_level == self.max_level:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Win")
                msg_box.setText("Congratulation you completed every level!")
                msg_box.addButton(QPushButton('Go back to game menu'), QMessageBox.AcceptRole)
                msg_box.exec()
                self.goto_game_menu()
            else:
                self.unlock_next_level(self.selected_level)
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Win")
                msg_box.setText("Congratulation you won!")
                msg_box.addButton(QPushButton('Go to game menu'), QMessageBox.AcceptRole)
                msg_box.addButton(QPushButton('Play next level'), QMessageBox.RejectRole)
                t = msg_box.exec()
                if t == QMessageBox.AcceptRole:
                    self.goto_game_menu()
                elif t == QMessageBox.RejectRole:
                    self.goto_next_level()
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Lose")
            msg_box.setText(f"Unfortunately you lost!")
            msg_box.addButton(QPushButton('Go to game menu'), QMessageBox.AcceptRole)
            msg_box.addButton(QPushButton('Play level again'), QMessageBox.RejectRole)
            msg_box.addButton(QPushButton('Go to level selection'), QMessageBox.DestructiveRole)
            t = msg_box.exec()
            self.show_solution()
            if t == QMessageBox.DestructiveRole:
                self.goto_level_selection()
            elif t == QMessageBox.AcceptRole:
                self.goto_game_menu()
            elif t == QMessageBox.RejectRole:
                self.goto_play_level_again()

    def show_solution(self):
        for button in self.program_selected_buttons:
            self.change_button_background2(button, "green")
