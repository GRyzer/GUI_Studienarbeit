
import string

from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.base_form_widget import BaseFormWidget


class FormWidget(BaseFormWidget):
    def __init__(self, hangman_page, searched_word, used_letters, hangman_start_picture, allowed_trials, selected_level):
        self.alphabet_button_list = []
        self.form_layout2 = None
        self.game_menu_button = None
        self.grid_layout = None
        self.hangman_pic_label = None
        self.horizontal_layout = None
        self.horizontal_layout2 = None
        self.horizontal_layout3 = None
        self.level_selection_button = None
        self.main_vertical_layout = None
        self.searched_blank_word_label = None
        self.trials_left_label = None
        self.used_letters_label = None
        self.vertical_layout = None
        self.setupUi(hangman_page, searched_word, used_letters, hangman_start_picture, allowed_trials, selected_level)

    def setupUi(self, hangman_page, searched_word, used_letters, hangman_start_picture, allowed_trials, selected_level):
        hangman_page.setMinimumSize(self.get_min_widget())
        hangman_page.setMaximumSize(self.get_max_widget())
        hangman_page.setWindowTitle(f"Hangman, Level: {selected_level}")
        hangman_page.resize(self.get_default_window_size())

        self.main_vertical_layout = QtWidgets.QVBoxLayout(hangman_page)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.searched_blank_word_label = QtWidgets.QLabel(searched_word, hangman_page)
        self.searched_blank_word_label.setFont(QtGui.QFont('', 26))
        self.searched_blank_word_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_vertical_layout.addWidget(self.searched_blank_word_label)

        self.horizontal_layout = QtWidgets.QHBoxLayout(hangman_page)

        self.hangman_pic_label = QtWidgets.QLabel("Hangman Picture", hangman_page)
        self.hangman_pic_label.setScaledContents(True)
        self.hangman_pic_label.setPixmap(QtGui.QPixmap(hangman_start_picture))
        self.hangman_pic_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontal_layout.addWidget(self.hangman_pic_label)

        self.grid_layout = QtWidgets.QGridLayout(hangman_page)
        self.grid_layout.setContentsMargins(-1, -1, 2, -1)

        for index, letter in enumerate(string.ascii_uppercase):
            button = QtWidgets.QPushButton(letter, hangman_page)
            self.alphabet_button_list.append(button)
            self.grid_layout.addWidget(button, index // 4, index % 4)

        self.horizontal_layout.addLayout(self.grid_layout)
        self.main_vertical_layout.addLayout(self.horizontal_layout)

        self.vertical_layout = QtWidgets.QVBoxLayout(hangman_page)
        self.horizontal_layout2 = QtWidgets.QHBoxLayout(hangman_page)

        self.used_letters_label = QtWidgets.QLabel(used_letters, hangman_page)
        self.used_letters_label.setFont(QtGui.QFont('', 20))
        self.used_letters_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vertical_layout.addWidget(self.used_letters_label)

        self.trials_left_label = QtWidgets.QLabel(f"Trials left: {allowed_trials}", hangman_page)
        self.trials_left_label.setFont(QtGui.QFont('', 20))
        self.trials_left_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vertical_layout.addWidget(self.trials_left_label)
        self.horizontal_layout2.addLayout(self.vertical_layout)

        self.main_vertical_layout.addLayout(self.horizontal_layout2)

        self.horizontal_layout3 = QtWidgets.QHBoxLayout(hangman_page)

        self.form_layout2 = QtWidgets.QFormLayout(hangman_page)
        self.form_layout2.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.form_layout2.setContentsMargins(-1, -1, 20, 20)

        self.game_menu_button = QtWidgets.QPushButton('return to game menu', hangman_page)
        self.game_menu_button.setSizePolicy(self.get_size_policy(self.game_menu_button))
        self.game_menu_button.setFont(QtGui.QFont('', 12))
        self.form_layout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.game_menu_button)

        self.level_selection_button = QtWidgets.QPushButton('go to level selection', hangman_page)
        self.level_selection_button.setSizePolicy(self.get_size_policy(self.level_selection_button))
        self.level_selection_button.setFont(QtGui.QFont('', 12))
        self.form_layout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.level_selection_button)

        self.horizontal_layout3.addLayout(self.form_layout2)
        self.main_vertical_layout.addLayout(self.horizontal_layout3)
        QtCore.QMetaObject.connectSlotsByName(hangman_page)
