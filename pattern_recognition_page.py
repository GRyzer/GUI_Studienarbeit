from functools import partial
import random

from PyQt5 import QtWidgets, QtCore, QtGui

from form_widget import FormWidgetIF
from game_database_management import GameDatabaseManagement
from games import Game


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
    def __init__(self, memory_page, color, selected_level):
        self.button_list = []
        self.form_layout = None
        self.grid_layout = None
        self.horizontal_layout = None
        self.main_vertical_layout = None
        self.submit_button = None
        self.setupUi(memory_page, color, selected_level)

    def setupUi(self, memory_page, color, selected_level):
        memory_page.setMinimumSize(self.get_min_widget())
        memory_page.setMaximumSize(self.get_max_widget())
        memory_page.setWindowTitle(f"Memory, Level {selected_level}")
        memory_page.resize(QtCore.QSize(800, 800))

        self.main_vertical_layout = QtWidgets.QVBoxLayout(memory_page)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout = QtWidgets.QGridLayout(memory_page)
        self.grid_layout.setSpacing(5)

        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        for index in range(256):
            button = QtWidgets.QPushButton(memory_page)
            button.setFixedSize(QtCore.QSize(40, 40))
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            button.setStyleSheet(f"background-color: {color}")
            button.clicked.connect(partial(self.toggle_button_background, button))
            self.button_list.append(button)
            self.grid_layout.addWidget(button, index // 16, index % 16)

        self.main_vertical_layout.addLayout(self.grid_layout)
        self.horizontal_layout = QtWidgets.QHBoxLayout(memory_page)

        self.form_layout = QtWidgets.QFormLayout(memory_page)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.form_layout.setContentsMargins(-1, -1, 20, 20)

        self.submit_button = QtWidgets.QPushButton('submit', memory_page)
        self.submit_button.setSizePolicy(self.get_size_policy(self.submit_button))
        self.submit_button.setFont(QtGui.QFont('', 12))
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.submit_button)
        self.horizontal_layout.addLayout(self.form_layout)
        self.main_vertical_layout.addLayout(self.horizontal_layout)
        QtCore.QMetaObject.connectSlotsByName(memory_page)

    def toggle_button_background(self, button):
        if button.palette().button().color() == QtGui.QColor("red"):
            button.setStyleSheet(f"background-color: {self.palette().color(QtGui.QPalette.Background)}")
        else:
            button.setStyleSheet(f"background-color: red")


class PatternRecognitionWindow(Game, FormWidget, QtWidgets.QWidget):
    database_path = "databases/patternrecognition.csv"
    max_level = 20

    def __init__(self, username):
        QtWidgets.QWidget.__init__(self)
        self.game_database = GameDatabaseManagement(self.database_path, username)
        self.level_dict = {}
        self.program_selected_buttons = []

    def play_game(self, selected_level):
        self.initialize_game(selected_level)
        self.show()
        user_decision = self.show_start_screen()
        if user_decision == QtWidgets.QMessageBox.AcceptRole:
            self.flicker_the_buttons(Level.get_play_dict(selected_level))
        elif user_decision == QtWidgets.QMessageBox.RejectRole:
            self.goto_game_menu()

    def initialize_game(self, selected_level):
        self.selected_level = selected_level
        FormWidget.__init__(self, self, self.palette().color(QtGui.QPalette.Background), self.selected_level)
        Game.__init__(self, self.game_database, self.selected_level)

    @staticmethod
    def show_start_screen():
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Round screen")
        msg_box.setText("Do you want to start?")
        msg_box.addButton(QtWidgets.QPushButton('Start'), QtWidgets.QMessageBox.AcceptRole)
        msg_box.addButton(QtWidgets.QPushButton('Go to main menu'), QtWidgets.QMessageBox.RejectRole)
        return msg_box.exec()

    def flicker_the_buttons(self, play_dict):
        rnd_button_list = random.sample(range(0, len(self.button_list)), play_dict["buttons"])
        start_value = play_dict["start_time"]
        self.disable_buttons()
        for element in rnd_button_list:
            button = self.button_list[element]
            self.program_selected_buttons.append(button)
            self.change_button_background(button, "red")
            start_value += play_dict["increment"]
            timer2 = QtCore.QTimer(self)
            timer2.setSingleShot(True)
            if play_dict["stay_on"]:
                timer2.start(play_dict["end_time"])
            else:
                timer2.start(start_value)
            timer2.timeout.connect(partial(self.change_button_background, button,
                                           self.palette().color(QtGui.QPalette.Background)))
        timer = QtCore.QTimer(self)
        timer.setSingleShot(True)
        timer.start(play_dict["end_time"])
        timer.timeout.connect(self.enable_buttons)

    def disable_buttons(self):
        for button in self.button_list:
            button.setEnabled(False)
        self.submit_button.disconnect()

    @staticmethod
    def change_button_background(button, color):
        button.setStyleSheet(f"background-color: {color}")

    def enable_buttons(self):
        for button in self.button_list:
            button.setEnabled(True)
        self.submit_button.clicked.connect(self.end_the_game)

    def end_the_game(self):
        self.disable_buttons()
        user_selected_list = []
        for button in self.button_list:
            if button.palette().button().color() == QtGui.QColor("red"):
                user_selected_list.append(button)
        self.show_solution()
        if set(user_selected_list) == set(self.program_selected_buttons):
            if self.selected_level == self.max_level:
                self.show_every_level_completed()
                self.goto_game_menu()
            else:
                self.unlock_next_level(self.selected_level)
                user_decision = self.show_selection_for_next_game()
                if user_decision == QtWidgets.QMessageBox.AcceptRole:
                    self.goto_game_menu()
                elif user_decision == QtWidgets.QMessageBox.RejectRole:
                    self.goto_next_level()
        else:
            user_decision = self.show_losing_screen()
            if user_decision == QtWidgets.QMessageBox.DestructiveRole:
                self.goto_level_selection()
            elif user_decision == QtWidgets.QMessageBox.AcceptRole:
                self.goto_game_menu()
            elif user_decision == QtWidgets.QMessageBox.RejectRole:
                self.goto_play_level_again()

    def show_solution(self):
        for button in self.program_selected_buttons:
            self.change_button_background(button, "green")

    @staticmethod
    def show_every_level_completed():
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Win")
        msg_box.setText("Congratulation you completed every level!")
        msg_box.addButton(QtWidgets.QPushButton('Go back to game menu'), QtWidgets.QMessageBox.AcceptRole)
        msg_box.exec()

    @staticmethod
    def show_selection_for_next_game():
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Win")
        msg_box.setText("Congratulation you won!")
        msg_box.addButton(QtWidgets.QPushButton('Go to game menu'), QtWidgets.QMessageBox.AcceptRole)
        msg_box.addButton(QtWidgets.QPushButton('Play next level'), QtWidgets.QMessageBox.RejectRole)
        return msg_box.exec()

    @staticmethod
    def show_losing_screen():
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Lose")
        msg_box.setText(f"Unfortunately you lost!")
        msg_box.addButton(QtWidgets.QPushButton('Go to game menu'), QtWidgets.QMessageBox.AcceptRole)
        msg_box.addButton(QtWidgets.QPushButton('Play level again'), QtWidgets.QMessageBox.RejectRole)
        msg_box.addButton(QtWidgets.QPushButton('Go to level selection'), QtWidgets.QMessageBox.DestructiveRole)
        return msg_box.exec()
