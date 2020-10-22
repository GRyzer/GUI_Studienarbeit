from functools import partial
from random import sample, shuffle

from PyQt5 import QtWidgets, QtCore, QtGui

from src.games.memory.form_widget import FormWidget
from src.database_managers.game_database_management import GameDatabaseManagement
from src.games.game import Game


class MemoryWindow(Game, FormWidget, QtWidgets.QWidget):
    database_path = "src/databases/memory.csv"
    header = ["unlocked_level", "achieved_points"]
    default_values = [1, 0]
    max_level = 20

    def __init__(self, username):
        QtWidgets.QWidget.__init__(self)
        self.achieved_points = None
        self.game_database = None
        self.moves = None
        self.required_points = None
        self.data_to_update = {"achieved_points": "achieved_points"}
        self.initialize_database(username)

    def initialize_database(self, username):
        self.game_database = GameDatabaseManagement(self.database_path, username, self.header)
        self.game_database.initialize_user_account(self.default_values)

    def play_game(self, selected_level):
        self.initialize_game(selected_level)
        self.show()
        text = f"Required points for this round are: {self.required_points}\nDo you want to start?"
        user_decision = self.show_start_screen(text)
        if user_decision == QtWidgets.QMessageBox.RejectRole:
            self.emit_game_menu_signal()

    def initialize_game(self, selected_level):
        self.achieved_points = 0
        self.moves = 0
        self.required_points = 800 + selected_level * 50
        self.selected_level = selected_level
        FormWidget.__init__(self, self, self.selected_level)
        Game.__init__(self, self.game_database, self.selected_level)
        self.set_memory_images()
        self.connect_buttons_to_game()

    def set_memory_images(self):
        random_number_list = [number//2 for number in range(2, 38)]
        icon_paths = sample(range(1, 26), 18)
        dictionary = {}
        for number in range(1, 19):
            dictionary[number] = icon_paths.pop(0)
        shuffle(random_number_list)
        for element in self.button_manager.buttons():
            image_number = random_number_list.pop(0)
            icon_path = f"src/assets/memory/icon{dictionary[image_number]}"
            element.set_image_number(image_number)
            element.set_icon_path(icon_path)

    def connect_buttons_to_game(self):
        self.game_menu_button.clicked.connect(self.emit_game_menu_signal)
        self.level_selection_button.clicked.connect(self.emit_level_menu_signal)
        self.button_manager.buttonClicked.connect(self.check_round)

    def update_moves(self):
        self.moves += 1
        self.moves_label.setText(f"Moves: {self.moves}")

    def update_points(self, points):
        self.achieved_points += points
        self.points_label.setText(f"Points: {self.achieved_points}")

    def check_round(self, button1):
        self.button_manager.disable_buttons()
        button1.show_icon()
        time = 0
        if self.button_manager.has_a_button_been_clicked_before():
            self.update_moves()
            button2 = self.button_manager.clicked_buttons.pop(0)
            if self.button_manager.do_images_match(button1, button2):
                points = 100
                self.button_manager.remove_memory_pair(button1, button2)
            else:
                points = -20
                time = 2500
                timer2 = QtCore.QTimer(self)
                timer2.setSingleShot(True)
                timer2.start(time)
                timer2.timeout.connect(partial(self.button_manager.reset_memory_pair, button1, button2))
            self.update_points(points)
        else:
            self.button_manager.add_first_clicked_button(button1)
        timer = QtCore.QTimer(self)
        timer.setSingleShot(True)
        timer.start(time)
        timer.timeout.connect(self.button_manager.enable_buttons)
        self.check_for_end_of_game()

    def check_for_end_of_game(self):
        if self.button_manager.is_memory_solved():
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
        if self.achieved_points >= self.required_points:
            if self.selected_level == self.max_level:
                self.show_every_level_completed()
                self.emit_game_menu_signal()
            else:
                self.unlock_next_level(self.selected_level)
                text = f"Congratulation you won!\nYou scored {self.achieved_points} points in " \
                       f"{self.moves} moves"
                user_decision = self.show_selection_for_next_game(text)
                if user_decision == QtWidgets.QMessageBox.AcceptRole:
                    self.emit_game_menu_signal()
                elif user_decision == QtWidgets.QMessageBox.RejectRole:
                    self.emit_play_next_level_signal()
        else:
            text = f"Unfortunately you lost! You scored only {self.achieved_points} points. Required points were: " \
                   f"{self.required_point}!"
            user_decision = self.show_losing_screen(text)
            if user_decision == QtWidgets.QMessageBox.DestructiveRole:
                self.emit_level_menu_signal()
            elif user_decision == QtWidgets.QMessageBox.AcceptRole:
                self.emit_game_menu_signal()
            elif user_decision == QtWidgets.QMessageBox.RejectRole:
                self.emit_play_level_again_signal()
        self.game_database.save_user_data()
