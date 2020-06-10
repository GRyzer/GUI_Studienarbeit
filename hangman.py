from functools import partial
import string

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from formWidget import FormWidgetIF
from gameDatabaseManagement import GameDatabaseManagement
from LevelPage import LevelWindow


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.used_letters = "Used Letters: "
        self.searched_word = ""
        self.original_word = ""
        self.alphabet_button_list = []
        self.hangman_pic_label = None
        self.verticalLayout = None
        self.searched_word_label = None
        self.horizontalLayout = None
        self.horizontalLayout_2 = None
        self.gridLayout = None
        self.used_letters_label = None
        self.current_trials = 0
        self.maximum_trials = 0

    def setup(self, hangman_page, word):
        self.setup_searched_word(word)
        self.setupUi(hangman_page)

    def setup_searched_word(self, word):
        self.original_word = word
        self.searched_word = ""
        for _ in self.original_word:
            self.searched_word += "_ "

    def setupUi(self, hangman_page):
        hangman_page.setMinimumSize(self.get_min_widget())
        hangman_page.setMaximumSize(self.get_max_widget())
        hangman_page.setWindowTitle("Hangman")
        hangman_page.resize(self.get_default_window_size())
        hangman_page.setPalette(self.get_background())

        self.verticalLayout = QtWidgets.QVBoxLayout(hangman_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.searched_word_label = QtWidgets.QLabel(self.searched_word, hangman_page)
        self.searched_word_label.setFont(QFont('', 26))
        self.searched_word_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.searched_word_label)

        self.horizontalLayout = QtWidgets.QHBoxLayout(hangman_page)

        self.hangman_pic_label = QtWidgets.QLabel("Hangman Picture", hangman_page)
        self.hangman_pic_label.setScaledContents(True)
        self.hangman_pic_label.setPixmap(QPixmap('hangman_assets/hangman1.png'))
        self.hangman_pic_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.hangman_pic_label)

        self.gridLayout = QtWidgets.QGridLayout(hangman_page)
        self.gridLayout.setContentsMargins(-1, -1, 2, -1)

        for index, letter in enumerate(string.ascii_uppercase):
            button = QPushButton(letter, hangman_page)
            # button.setStyleSheet("border: 1px solid black;")
            self.alphabet_button_list.append(button)
            self.gridLayout.addWidget(button, index // 4, index % 4)

        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(hangman_page)

        self.used_letters_label = QtWidgets.QLabel(self.used_letters, hangman_page)
        self.used_letters_label.setFont(QFont('', 20))
        self.used_letters_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_2.addWidget(self.used_letters_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        QtCore.QMetaObject.connectSlotsByName(hangman_page)

    def update_game(self, letter):
        if self.letter_not_in_searched_word(letter):
            self.update_trials()
        else:
            self.update_searched_word(letter)
        self.update_used_letters(letter)
        self.check_for_end_of_game()

    def letter_not_in_searched_word(self, letter):
        if letter not in self.original_word:
            return True
        return False

    def update_trials(self):
        self.hangman_pic_label.setPixmap(QPixmap('hangman_assets/hangman1.png'))
        self.current_trials += 1

    def update_searched_word(self, letter):
        searched_word_list = list(self.searched_word)
        for index, element in enumerate(list(self.original_word)):
            if letter == element:
                searched_word_list[2 * index] = letter
        self.searched_word = "".join(searched_word_list)
        self.searched_word_label.setText(self.searched_word)

    def update_used_letters(self, letter):
        self.used_letters += f"{letter}, "
        self.used_letters_label.setText(self.used_letters)

    def check_for_end_of_game(self):
        if '_' not in self.searched_word:
            # create a winning window
            # update reached level
            pass
        elif self.current_trials > self.maximum_trials:
            pass

    def set_maximum_trials(self, current_level):
        if current_level < 5:
            self.maximum_trials = 10
        elif current_level < 9:
            self.maximum_trials = 9
        elif current_level < 13:
            self.maximum_trials = 8
        elif current_level < 17:
            self.maximum_trials = 7
        else:
            self.maximum_trials = 6


class HangmanWindow(QtWidgets.QWidget, FormWidget):
    database_path = "hangman.csv"
    game_menu_window = QtCore.pyqtSignal(str)

    def __init__(self, username):
        super(HangmanWindow, self).__init__()
        self.game_database = GameDatabaseManagement(self.database_path, username)
        self.level_window = LevelWindow(username, self.game_database.get_unlocked_level())
        self.level_window.previous_window.connect(partial(self.goto_game_menu, username))
        self.level_window.next_window.connect(self.play_game)
        self.level_window.unlock_level.connect(self.unlock_all_levels)
        self.level_window.show()

    def goto_game_menu(self, username):
        self.level_window.hide()
        self.game_menu_window.emit(username)

    def play_game(self):
        self.setup(self, "TIGER")
        self.connect_buttons_to_game()
        self.level_window.hide()

    def unlock_all_levels(self):
        self.game_database.unlock_all_levels()

    def connect_buttons_to_game(self):
        for button in self.alphabet_button_list:
            button.clicked.connect(partial(self.update_game, button.text()))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    control = HangmanWindow("Tiger")
    control.show()
    sys.exit(app.exec())