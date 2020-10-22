from random import randint

from PyQt5 import QtWidgets, QtCore, QtGui

from src.games.button_shooter.form_widget import FormWidget
from src.database_managers.game_database_management import GameDatabaseManagement
from src.games.game import Game


class ButtonShooter(Game, FormWidget, QtWidgets.QWidget):
    database_path = "databases/button_shooter.csv"
    header = ["unlocked_level", "hit_targets"]
    default_values = [1, 0]
    max_level = 20

    def __init__(self, username):
        QtWidgets.QWidget.__init__(self)
        self.countdown = None
        self.game_database = None
        self.hit_targets = None
        self.missed_targets = None
        self.required_targets = None
        self.selected_button = None
        self.selected_level = None
        self.timer = None
        self.data_to_update = {"hit_targets": "hit_targets"}
        self.initialize_database(username)

    def initialize_database(self, username):
        self.game_database = GameDatabaseManagement(self.database_path, username, self.header)
        self.game_database.initialize_user_account(self.default_values)

    def play_game(self, selected_level):
        self.initialize_game(selected_level)
        self.show()
        text = f"Required Targets: {self.required_targets}.\nDo you want to start?"
        user_decision = self.show_start_screen(text)
        if user_decision == QtWidgets.QMessageBox.AcceptRole:
            self.timer.start(1000)
            self.show_buttons()
        elif user_decision == QtWidgets.QMessageBox.RejectRole:
            self.goto_game_menu()

    def initialize_game(self, selected_level):
        self.countdown = 100
        self.hit_targets = 0
        self.missed_targets = 0
        self.required_targets = self.get_required_target(selected_level)
        self.selected_level = selected_level
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        FormWidget.__init__(self, self, self.selected_level, self.countdown)
        Game.__init__(self, self.game_database, self.selected_level)
        self.connect_buttons_to_game()

    @staticmethod
    def get_required_target(level):
        return level * 5 + 50

    def update_timer(self):
        self.countdown -= 1
        self.countdown_label.setText(f"Time left: {self.countdown}")
        if self.countdown == 0:
            self.timer.stop()
            self.end_the_game()

    def update_values(self):
        values = self.game_database.get_values()
        updated_values = {}
        for header_name, variable_name in self.data_to_update.items():
            value = getattr(self, variable_name)
            if value > values[header_name]:
                updated_values[header_name] = value
        self.game_database.update_values(updated_values)

    def end_the_game(self):
        self.update_values()
        if self.hit_targets >= self.required_targets:
            if self.selected_level == self.max_level:
                self.show_every_level_completed()
                self.goto_game_menu()
            else:
                self.unlock_next_level(self.selected_level)
                text = f"Congratulation you won!\nYou hit {self.hit_targets} targets and you missed " \
                       f"{self.missed_targets} targets."
                user_decision = self.show_selection_for_next_game(text)
                if user_decision == QtWidgets.QMessageBox.AcceptRole:
                    self.goto_game_menu()
                elif user_decision == QtWidgets.QMessageBox.RejectRole:
                    self.goto_next_level()
        else:
            text = f"Unfortunately you lost! You only hit {self.hit_targets} targets of required " \
                   f"{self.required_targets} targets. You missed {self.missed_targets} targets."
            user_decision = self.show_losing_screen(text)
            if user_decision == QtWidgets.QMessageBox.DestructiveRole:
                self.goto_level_selection()
            elif user_decision == QtWidgets.QMessageBox.AcceptRole:
                self.goto_game_menu()
            elif user_decision == QtWidgets.QMessageBox.RejectRole:
                self.goto_play_level_again()
        self.game_database.save_user_data()

    def connect_buttons_to_game(self):
        self.game_menu_button.clicked.connect(self.goto_game_menu)
        self.level_selection_button.clicked.connect(self.goto_level_selection)
        for button in self.button_list:
            button.clicked.connect(self.is_clicked_button_the_proper_target)

    def is_clicked_button_the_proper_target(self):
        if self.sender() is self.selected_button:
            self.change_button_background(self.selected_button, self.palette().color(QtGui.QPalette.Background))
            self.show_buttons()
            self.hit_targets += 1
            self.hit_target_label.setText(f"Hit Targets: {self.hit_targets}")
        else:
            self.change_button_background(self.selected_button, self.palette().color(QtGui.QPalette.Background))
            self.show_buttons()
            self.missed_targets += 1

    @staticmethod
    def change_button_background(button, color):
        button.setStyleSheet(f"background-color: {color}")

    def show_buttons(self):
        self.selected_button = self.button_list[randint(0, len(self.button_list)-1)]
        self.change_button_background(self.selected_button, "red")
