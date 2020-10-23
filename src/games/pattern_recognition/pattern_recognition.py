from functools import partial
import random

from PyQt5 import QtWidgets, QtCore, QtGui

from src.games.pattern_recognition.form_widget import FormWidget
from src.database_managers.game_database_management import GameDatabaseManagement
from src.games.game import Game


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


class PatternRecognitionWindow(Game, FormWidget, QtWidgets.QWidget):
    database_path = "src/databases/patternrecognition.csv"
    header = ["unlocked_level"]
    default_values = [1]
    max_level = 20

    def __init__(self, username):
        QtWidgets.QWidget.__init__(self)
        self.game_database = None
        self.level_dict = {}
        self.program_selected_buttons = []
        self.initialize_database(username)

    def initialize_database(self, username):
        self.game_database = GameDatabaseManagement(self.database_path, username, self.header)
        self.game_database.initialize_user_account(self.default_values)

    def play_game(self, selected_level):
        self.initialize_game(selected_level)
        self.show()
        user_decision = self.show_start_screen()
        if user_decision == QtWidgets.QMessageBox.AcceptRole:
            self.flicker_the_buttons(Level.get_play_dict(selected_level))
        elif user_decision == QtWidgets.QMessageBox.RejectRole:
            self.emit_game_menu_signal()

    def initialize_game(self, selected_level):
        self.selected_level = selected_level
        FormWidget.__init__(self, self, self.palette().color(QtGui.QPalette.Background), self.selected_level)
        Game.__init__(self, self.game_database, self.selected_level)

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
                self.emit_game_menu_signal()
            else:
                self.unlock_next_level(self.selected_level)
                user_decision = self.show_selection_for_next_game()
                self.game_database.save_user_data()
                if user_decision == QtWidgets.QMessageBox.AcceptRole:
                    self.emit_game_menu_signal()
                elif user_decision == QtWidgets.QMessageBox.RejectRole:
                    self.emit_play_next_level_signal()
        else:
            self.game_database.save_user_data()
            user_decision = self.show_losing_screen()
            if user_decision == QtWidgets.QMessageBox.DestructiveRole:
                self.emit_level_menu_signal()
            elif user_decision == QtWidgets.QMessageBox.AcceptRole:
                self.emit_game_menu_signal()
            elif user_decision == QtWidgets.QMessageBox.RejectRole:
                self.emit_play_level_again_signal()

    def show_solution(self):
        for button in self.program_selected_buttons:
            self.change_button_background(button, "green")
