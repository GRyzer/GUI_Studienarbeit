
from functools import partial
from itertools import chain
import random
import pickle

from PyQt5 import QtWidgets, QtCore, QtGui

from src.games.hangman.form_widget import FormWidget
from src.database_managers.game_database_management import GameDatabaseManagement
from src.games.game import Game


class HangmanWindow(Game, FormWidget, QtWidgets.QWidget):
    database_path = "src/databases/hangman.csv"
    header = ["unlocked_level", "word_guessed_by_letter"]
    default_values = [1, 0.0]
    max_level = 20

    def __init__(self, username):
        QtWidgets.QWidget.__init__(self)
        self.game_database = None
        self.trials_left = None
        self.searched_word = None
        self.searched_blank_word = None
        self.selected_level = None
        self.hangman_picture_list = None
        self.used_letters = None
        self.used_letters_list = []
        self.initialize_database(username)

    def initialize_database(self, username):
        self.game_database = GameDatabaseManagement(self.database_path, username, self.header)
        self.game_database.initialize_user_account(self.default_values)

    def play_game(self, selected_level):
        self.initialize_game(selected_level)
        self.show()

    def initialize_game(self, selected_level):
        self.trials_left = self.get_trials(selected_level)
        self.hangman_picture_list = self.get_hangman_picture_paths(self.trials_left)
        self.searched_word = self.get_searched_word()
        self.searched_blank_word = self.get_blanked_word(self.searched_word)
        self.selected_level = selected_level
        self.used_letters = "Used Letters: "
        FormWidget.__init__(self, self, self.searched_blank_word, self.used_letters, "src/assets/hangman/hangman_start.png",
                            self.trials_left, self.selected_level)
        Game.__init__(self, self.game_database, self.selected_level)
        self.connect_buttons_to_game()

    @staticmethod
    def get_trials(selected_level):
        trials = 6
        if selected_level < 5:
            trials = 10
        elif selected_level < 9:
            trials = 9
        elif selected_level < 13:
            trials = 8
        elif selected_level < 17:
            trials = 7
        return trials

    @staticmethod
    def get_hangman_picture_paths(trials):
        """
        A selection of pictures which shall be shown.
        paths_by_level: keys are related to method: get_trials
        """
        folder = "src/assets/hangman"
        picture_paths = [f"{folder}/hangman1.png", f"{folder}/hangman2.png", f"{folder}/hangman3.png",
                         f"{folder}/hangman4.png", f"{folder}/hangman5.png", f"{folder}/hangman6.png",
                         f"{folder}/hangman7.png", f"{folder}/hangman8.png", f"{folder}/hangman9.png",
                         f"{folder}/hangman10.png"]
        paths_by_level = {6: list(chain([picture_paths[1]], picture_paths[3:6], [picture_paths[7]], [picture_paths[9]])),
                          7: list(chain(picture_paths[0:2], picture_paths[3:6], [picture_paths[7]], [picture_paths[9]])),
                          8: list(chain([picture_paths[0]], picture_paths[1:6], [picture_paths[7]], [picture_paths[9]])),
                          9: list(chain([picture_paths[0]], picture_paths[1:8], [picture_paths[9]])),
                          10: picture_paths}
        return paths_by_level[trials]

    @staticmethod
    def get_searched_word():
        with open("src/games/hangman/word_list.data", "rb") as file_handle:
            word_list = pickle.load(file_handle)
        return random.choice(word_list).upper()

    @staticmethod
    def get_blanked_word(word):
        blank_word = ""
        for _ in word:
            blank_word += "_ "
        return blank_word

    def connect_buttons_to_game(self):
        for button in self.alphabet_button_list:
            button.clicked.connect(partial(self.update_game, button.text()))
        self.game_menu_button.clicked.connect(self.emit_game_menu_signal)
        self.level_selection_button.clicked.connect(self.emit_level_menu_signal)

    def update_game(self, letter):
        if self.letter_not_in_searched_word(letter):
            self.update_hangman()
        else:
            self.update_searched_word(letter)
        self.update_used_letters(letter)
        self.check_for_end_of_game()

    def letter_not_in_searched_word(self, letter):
        if letter not in self.searched_word:
            return True
        return False

    def update_hangman(self):
        self.trials_left -= 1
        self.trials_left_label.setText(f"Trials left: {self.trials_left}")
        self.hangman_pic_label.setPixmap(QtGui.QPixmap(self.hangman_picture_list[-self.trials_left-1]))

    def update_searched_word(self, letter):
        searched_word_list = list(self.searched_blank_word)
        for index, element in enumerate(list(self.searched_word)):
            if letter == element:
                searched_word_list[2 * index] = letter
        self.searched_blank_word = "".join(searched_word_list)
        self.searched_blank_word_label.setText(self.searched_blank_word)

    def update_used_letters(self, letter):
        if letter not in self.used_letters_list:
            self.used_letters += f"{letter}, "
            self.used_letters_label.setText(self.used_letters)
            self.used_letters_list.append(letter)

    def check_for_end_of_game(self):
        if '_' not in self.searched_blank_word or self.trials_left == 0:
            self.end_the_game()

    def update_values(self):
        values = self.game_database.get_values()
        updated_values = {}
        current_value = len(self.searched_word)/len(self.used_letters_list)
        if current_value > values["word_guessed_by_letter"]:
            updated_values["word_guessed_by_letter"] = current_value
        self.game_database.update_values(updated_values)

    def end_the_game(self):
        if '_' not in self.searched_blank_word:
            self.update_values()
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
            text = f"Unfortunately you lost! The searched word was: {self.searched_word}"
            user_decision = self.show_losing_screen(text)
            if user_decision == QtWidgets.QMessageBox.DestructiveRole:
                self.emit_level_menu_signal()
            elif user_decision == QtWidgets.QMessageBox.AcceptRole:
                self.emit_game_menu_signal()
            elif user_decision == QtWidgets.QMessageBox.RejectRole:
                self.emit_play_level_again_signal()
