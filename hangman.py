from functools import partial
from itertools import chain
import string

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random_word

from formWidget import FormWidgetIF
from gameDatabaseManagement import GameDatabaseManagement


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.alphabet_button_list = []
        self.used_letters_list = []
        self.hangman_pic_label = None
        self.verticalLayout = None
        self.verticalLayout2 = None
        self.searched_word_label = None
        self.horizontalLayout = None
        self.horizontalLayout_2 = None
        self.horizontalLayout3 = None
        self.formLayout2 = None
        self.gridLayout = None
        self.used_letters_label = None
        self.selected_level = None
        self.trials_left_label = None
        self.game_menu_button = None
        self.level_selection_button = None

    def setupUi(self, hangman_page, searched_word, used_letters, hangman_start_picture, allowed_trials, selected_level):
        hangman_page.setMinimumSize(self.get_min_widget())
        hangman_page.setMaximumSize(self.get_max_widget())
        hangman_page.setWindowTitle(f"Hangman, Level: {selected_level}")
        hangman_page.resize(self.get_default_window_size())

        self.verticalLayout = QtWidgets.QVBoxLayout(hangman_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.searched_word_label = QtWidgets.QLabel(searched_word, hangman_page)
        self.searched_word_label.setFont(QFont('', 26))
        self.searched_word_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.searched_word_label)

        self.horizontalLayout = QtWidgets.QHBoxLayout(hangman_page)

        self.hangman_pic_label = QtWidgets.QLabel("Hangman Picture", hangman_page)
        self.hangman_pic_label.setScaledContents(True)
        self.hangman_pic_label.setPixmap(QPixmap(hangman_start_picture))
        self.hangman_pic_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.hangman_pic_label)

        self.gridLayout = QtWidgets.QGridLayout(hangman_page)
        self.gridLayout.setContentsMargins(-1, -1, 2, -1)

        for index, letter in enumerate(string.ascii_uppercase):
            button = QPushButton(letter, hangman_page)
            self.alphabet_button_list.append(button)
            self.gridLayout.addWidget(button, index // 4, index % 4)

        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout2 = QtWidgets.QVBoxLayout(hangman_page)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(hangman_page)

        self.used_letters_label = QtWidgets.QLabel(used_letters, hangman_page)
        self.used_letters_label.setFont(QFont('', 20))
        self.used_letters_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout2.addWidget(self.used_letters_label)

        self.trials_left_label = QtWidgets.QLabel(f"Trials left: {allowed_trials}", hangman_page)
        self.trials_left_label.setFont(QFont('', 20))
        self.trials_left_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout2.addWidget(self.trials_left_label)
        self.horizontalLayout_2.addLayout(self.verticalLayout2)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout3 = QHBoxLayout(hangman_page)

        self.formLayout2 = QFormLayout(hangman_page)
        self.formLayout2.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.formLayout2.setContentsMargins(-1, -1, 20, 20)

        self.game_menu_button = QPushButton('return to game menu', hangman_page)
        self.game_menu_button.setSizePolicy(self.get_size_policy(self.game_menu_button))
        self.game_menu_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.game_menu_button)

        self.level_selection_button = QPushButton('go to level selection', hangman_page)
        self.level_selection_button.setSizePolicy(self.get_size_policy(self.level_selection_button))
        self.level_selection_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.level_selection_button)

        self.horizontalLayout3.addLayout(self.formLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout3)
        QtCore.QMetaObject.connectSlotsByName(hangman_page)


class HangmanWindow(QtWidgets.QWidget, FormWidget):
    database_path = "databases/hangman.csv"
    game_menu_window = QtCore.pyqtSignal()
    level_menu = QtCore.pyqtSignal()
    next_level = QtCore.pyqtSignal(int)
    play_level_again = QtCore.pyqtSignal(int)
    max_level = 20

    def __init__(self, username):
        super(HangmanWindow, self).__init__()
        self.game_database = GameDatabaseManagement(self.database_path, username)
        self.allowed_trials = None
        self.trials_left = None
        self.searched_word = None
        self.searched_blank_word = None
        self.hangman_picture_list = None
        self.used_letters = None

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

    def initialize_game(self):
        self.allowed_trials = self.get_allowed_trials(self.selected_level)
        self.trials_left = self.allowed_trials
        self.searched_word, self.searched_blank_word = self.get_searched_word()
        self.hangman_picture_list = self.get_hangman_picture_paths(self.allowed_trials)
        self.used_letters = "Used Letters: "

    @staticmethod
    def get_allowed_trials(selected_level):
        if selected_level < 5:
            allowed_trials = 10
        elif selected_level < 9:
            allowed_trials = 9
        elif selected_level < 13:
            allowed_trials = 8
        elif selected_level < 17:
            allowed_trials = 7
        else:
            allowed_trials = 6
        return allowed_trials

    @staticmethod
    def get_searched_word():
        # alternative method described here: https://github.com/vaibhavsingh97/random-word/issues/32
        r = random_word.RandomWords()
        while True:
            word = r.get_random_word()
            if word.isalpha():
                break
        word = word.upper()
        blank_word = ""
        for _ in word:
            blank_word += "_ "
        return word, blank_word

    @staticmethod
    def get_hangman_picture_paths(trials):
        folder = "hangman_assets"
        picture_paths = [f"{folder}/hangman1.png", f"{folder}/hangman2.png", f"{folder}/hangman3.png",
                         f"{folder}/hangman4.png", f"{folder}/hangman5.png", f"{folder}/hangman6.png",
                         f"{folder}/hangman7.png", f"{folder}/hangman8.png", f"{folder}/hangman9.png",
                         f"{folder}/hangman10.png"]
        paths_by_level = {6: list(chain([picture_paths[0]], picture_paths[1:5], [picture_paths[9]])),
                          7: list(chain([picture_paths[0]], picture_paths[1:6], [picture_paths[9]])),
                          8: list(chain([picture_paths[0]], picture_paths[1:7], [picture_paths[9]])),
                          9: list(chain([picture_paths[0]], picture_paths[1:8], [picture_paths[9]])),
                          10: picture_paths}
        return paths_by_level[trials]

    def play_game(self, selected_level):
        self.selected_level = selected_level
        self.initialize_game()
        self.setupUi(self, self.searched_blank_word, self.used_letters, "hangman_assets/hangman_start.png",
                     self.allowed_trials, selected_level)
        self.connect_buttons_to_game()
        self.show()

    def connect_buttons_to_game(self):
        for button in self.alphabet_button_list:
            button.clicked.connect(partial(self.update_game, button.text()))
        self.game_menu_button.clicked.connect(self.goto_game_menu)
        self.level_selection_button.clicked.connect(self.goto_level_selection)

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
        self.hangman_pic_label.setPixmap(QPixmap(self.hangman_picture_list[self.allowed_trials - self.trials_left -1]))

    def update_used_letters(self, letter):
        if letter not in self.used_letters_list:
            self.used_letters += f"{letter}, "
            self.used_letters_label.setText(self.used_letters)
            self.used_letters_list.append(letter)

    def update_searched_word(self, letter):
        searched_word_list = list(self.searched_blank_word)
        for index, element in enumerate(list(self.searched_word)):
            if letter == element:
                searched_word_list[2 * index] = letter
        self.searched_blank_word = "".join(searched_word_list)
        self.searched_word_label.setText(self.searched_blank_word)

    def check_for_end_of_game(self):
        if '_' not in self.searched_blank_word:
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
        elif self.trials_left == 0:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Lose")
            msg_box.setText(f"Unfortunately you lost! The searched word was: {self.searched_word}")
            msg_box.addButton(QPushButton('Go to game menu'), QMessageBox.AcceptRole)
            msg_box.addButton(QPushButton('Play level again'), QMessageBox.RejectRole)
            msg_box.addButton(QPushButton('Go to level selection'), QMessageBox.DestructiveRole)
            t = msg_box.exec()
            if t == QMessageBox.DestructiveRole:
                self.goto_level_selection()
            elif t == QMessageBox.AcceptRole:
                self.goto_game_menu()
            elif t == QMessageBox.RejectRole:
                self.goto_play_level_again()
