from random import shuffle, sample
from functools import partial

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from form_widget import FormWidgetIF
from game_database_management import GameDatabaseManagement


class Button(QPushButton):
    size = 90

    def __init__(self):
        super(Button, self).__init__()
        self.icon_path = None
        self.is_icon_displayed = False
        self.image_number = None
        self.setFixedSize(Button.size, Button.size)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(f"background-color: grey")

    def show_icon(self):
        if not self.is_icon_displayed:
            icon = QIcon()
            icon.addPixmap(QPixmap(self.icon_path), QIcon.Normal, QIcon.Off)
            icon.addPixmap(QPixmap(self.icon_path), QIcon.Disabled, QIcon.Off)
            self.setIcon(icon)
            self.setIconSize(QtCore.QSize(90, 90))
            self.is_icon_displayed = True

    def reset_icon(self):
        icon = QIcon()
        self.setIcon(icon)
        self.is_icon_displayed = False

    def set_icon_path(self, icon_path):
        self.icon_path = icon_path

    def set_image_number(self, number):
        self.image_number = number


class ButtonManager(QButtonGroup):
    def __init__(self):
        super(ButtonManager, self).__init__()
        self.clicked_buttons = []

    def add_first_clicked_button(self, button):
        if not self.clicked_buttons:
            self.clicked_buttons.append(button)

    def has_a_button_been_clicked_before(self):
        if self.clicked_buttons:
            return True
        return False

    def do_images_match(self, button1, button2):
        if button1.image_number == button2.image_number:
            return True
        return False

    def is_memory_solved(self):
        if not self.buttons():
            return True
        return False

    def disable_buttons(self):
        for button in self.buttons():
            button.setDisabled(True)

    def enable_buttons(self):
        for button in self.buttons():
            button.setEnabled(True)

    def remove_memory_pair(self, button1, button2):
        button1.setDisabled(True)
        button2.setDisabled(True)
        self.removeButton(button1)
        self.removeButton(button2)

    def reset_memory_pair(self, button1, button2):
        button1.reset_icon()
        button2.reset_icon()

    def show_all_icons(self):
        for button in self.buttons():
            button.show_icon()

class FormWidget(FormWidgetIF):
    def __init__(self):
        self.button_manager = ButtonManager()

    def setupUi(self, memory_page, selected_level):
        memory_page.setMinimumSize(self.get_min_widget())
        memory_page.setMaximumSize(self.get_max_widget())
        memory_page.setWindowTitle(f"Memory, Level: {selected_level}")
        memory_page.resize(QtCore.QSize(1000, 800))

        self.verticalLayout = QtWidgets.QVBoxLayout(memory_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout = QHBoxLayout(memory_page)

        self.points_label = QLabel(f"Points: 0", memory_page)
        self.points_label.setFont(QFont('', 26))
        self.points_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.points_label, alignment=QtCore.Qt.AlignCenter)

        self.moves_label = QLabel(f"Moves: 0", memory_page)
        self.moves_label.setFont(QFont('', 26))
        self.moves_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.moves_label, alignment=QtCore.Qt.AlignCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.grid_layout = QtWidgets.QGridLayout(memory_page)
        self.grid_layout.setContentsMargins(10, 0, 10, 0)

        for index in range(36):
            button = Button()
            self.button_manager.addButton(button, index)
            self.grid_layout.addWidget(button, index // 6, index % 6)

        self.verticalLayout.addLayout(self.grid_layout)
        self.horizontalLayout2 = QHBoxLayout(memory_page)

        self.formLayout = QFormLayout(memory_page)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.formLayout.setContentsMargins(-1, -1, 20, 20)
        self.game_menu_button = QPushButton('return to game menu', memory_page)
        self.game_menu_button.setSizePolicy(self.get_size_policy(self.game_menu_button))
        self.game_menu_button.setFont(QFont('', 12))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.game_menu_button)

        self.level_selection_button = QPushButton('go to level selection', memory_page)
        self.level_selection_button.setSizePolicy(self.get_size_policy(self.level_selection_button))
        self.level_selection_button.setFont(QFont('', 12))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.level_selection_button)

        self.horizontalLayout2.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout2)
        memory_page.setLayout(self.verticalLayout)
        QtCore.QMetaObject.connectSlotsByName(memory_page)


class MemoryWindow(QtWidgets.QWidget, FormWidget):
    database_path = "databases/memory.csv"
    game_menu_window = QtCore.pyqtSignal()
    level_menu = QtCore.pyqtSignal()
    next_level = QtCore.pyqtSignal(int)
    play_level_again = QtCore.pyqtSignal(int)
    max_level = 20

    def __init__(self, username):
        super(MemoryWindow, self).__init__()
        self.game_database = GameDatabaseManagement(self.database_path, username)
        self.achieved_points = None
        self.required_points = None
        self.moves = None

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

    def connect_buttons_to_game(self):
        self.game_menu_button.clicked.connect(self.goto_game_menu)
        self.level_selection_button.clicked.connect(self.goto_level_selection)
        self.button_manager.buttonClicked.connect(self.check_round)

    def set_memory_images(self):
        random_number_list = [number//2 for number in range(2, 38)]
        icon_paths = sample(range(1, 26), 18)
        dictionary = {}
        for number in range(1, 19):
            dictionary[number] = icon_paths.pop(0)
        shuffle(random_number_list)
        for element in self.button_manager.buttons():
            image_number = random_number_list.pop(0)
            icon_path = f"memory_assets/icon{dictionary[image_number]}"
            element.set_image_number(image_number)
            element.set_icon_path(icon_path)

    def initialize_game(self, level):
        self.achieved_points = 0
        self.required_points = 800 + level * 50
        self.moves = 0

    def play_game(self, level):
        self.selected_level = level
        self.initialize_game(level)
        self.setupUi(self, level)
        self.set_memory_images()
        self.connect_buttons_to_game()
        self.show()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Round screen")
        msg_box.setText(f"Required points for this round are: {self.required_points}\nDo you want to start?")
        msg_box.addButton(QPushButton('Start'), QMessageBox.AcceptRole)
        msg_box.addButton(QPushButton('Go to main menu'), QMessageBox.RejectRole)
        t = msg_box.exec()
        if t == QMessageBox.AcceptRole:
            pass
        elif t == QMessageBox.RejectRole:
            self.goto_game_menu()

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
            if self.achieved_points >= self.required_points:
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
                    msg_box.setText(f"Congratulation you won!\nYou scored {self.achieved_points} points in "
                                    f"{self.moves} moves")
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
                msg_box.setText(
                    f"Unfortunately you lost! You scored only {self.achieved_points} points. Required points were: "
                    f"{self.required_point}!")
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