from functools import partial
from random import sample, shuffle

from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.form_widget import BaseFormWidget
from src.database_managers.game_database_management import GameDatabaseManagement
from src.games.game import Game


class Button(QtWidgets.QPushButton):
    size = 90

    def __init__(self):
        super(Button, self).__init__()
        self.icon_path = None
        self.image_number = None
        self.is_icon_displayed = False
        self.setFixedSize(Button.size, Button.size)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet(f"background-color: grey")

    def show_icon(self):
        if not self.is_icon_displayed:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(self.icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            icon.addPixmap(QtGui.QPixmap(self.icon_path), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
            self.setIcon(icon)
            self.setIconSize(QtCore.QSize(90, 90))
            self.is_icon_displayed = True

    def reset_icon(self):
        icon = QtGui.QIcon()
        self.setIcon(icon)
        self.is_icon_displayed = False

    def set_icon_path(self, icon_path):
        self.icon_path = icon_path

    def set_image_number(self, number):
        self.image_number = number


class ButtonManager(QtWidgets.QButtonGroup):
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

    @staticmethod
    def do_images_match(button1, button2):
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

    @staticmethod
    def reset_memory_pair(button1, button2):
        button1.reset_icon()
        button2.reset_icon()

    def show_all_icons(self):
        for button in self.buttons():
            button.show_icon()


class FormWidget(BaseFormWidget):
    def __init__(self, memory_page, selected_level):
        self.button_manager = ButtonManager()
        self.form_layout = None
        self.game_menu_button = None
        self.grid_layout = None
        self.horizontal_layout = None
        self.horizontal_layout2 = None
        self.level_selection_button = None
        self.main_vertical_layout = None
        self.moves_label = None
        self.points_label = None
        self.setupUi(memory_page, selected_level)

    def setupUi(self, memory_page, selected_level):
        memory_page.setMinimumSize(self.get_min_widget())
        memory_page.setMaximumSize(self.get_max_widget())
        memory_page.setWindowTitle(f"Memory, Level: {selected_level}")
        memory_page.resize(QtCore.QSize(1000, 800))

        self.main_vertical_layout = QtWidgets.QVBoxLayout(memory_page)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.horizontal_layout = QtWidgets.QHBoxLayout(memory_page)

        self.points_label = QtWidgets.QLabel(f"Points: 0", memory_page)
        self.points_label.setFont(QtGui.QFont('', 26))
        self.points_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontal_layout.addWidget(self.points_label, alignment=QtCore.Qt.AlignCenter)

        self.moves_label = QtWidgets.QLabel(f"Moves: 0", memory_page)
        self.moves_label.setFont(QtGui.QFont('', 26))
        self.moves_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontal_layout.addWidget(self.moves_label, alignment=QtCore.Qt.AlignCenter)
        self.main_vertical_layout.addLayout(self.horizontal_layout)

        self.grid_layout = QtWidgets.QGridLayout(memory_page)
        self.grid_layout.setContentsMargins(10, 0, 10, 0)

        for index in range(36):
            button = Button()
            self.button_manager.addButton(button, index)
            self.grid_layout.addWidget(button, index // 6, index % 6)

        self.main_vertical_layout.addLayout(self.grid_layout)
        self.horizontal_layout2 = QtWidgets.QHBoxLayout(memory_page)

        self.form_layout = QtWidgets.QFormLayout(memory_page)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.form_layout.setContentsMargins(-1, -1, 20, 20)
        self.game_menu_button = QtWidgets.QPushButton('return to game menu', memory_page)
        self.game_menu_button.setSizePolicy(self.get_size_policy(self.game_menu_button))
        self.game_menu_button.setFont(QtGui.QFont('', 12))
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.game_menu_button)

        self.level_selection_button = QtWidgets.QPushButton('go to level selection', memory_page)
        self.level_selection_button.setSizePolicy(self.get_size_policy(self.level_selection_button))
        self.level_selection_button.setFont(QtGui.QFont('', 12))
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.level_selection_button)

        self.horizontal_layout2.addLayout(self.form_layout)
        self.main_vertical_layout.addLayout(self.horizontal_layout2)
        memory_page.setLayout(self.main_vertical_layout)
        QtCore.QMetaObject.connectSlotsByName(memory_page)


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
            self.goto_game_menu()

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
        self.game_menu_button.clicked.connect(self.goto_game_menu)
        self.level_selection_button.clicked.connect(self.goto_level_selection)
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
                self.goto_game_menu()
            else:
                self.unlock_next_level(self.selected_level)
                text = f"Congratulation you won!\nYou scored {self.achieved_points} points in " \
                       f"{self.moves} moves"
                user_decision = self.show_selection_for_next_game(text)
                if user_decision == QtWidgets.QMessageBox.AcceptRole:
                    self.goto_game_menu()
                elif user_decision == QtWidgets.QMessageBox.RejectRole:
                    self.goto_next_level()
        else:
            text = f"Unfortunately you lost! You scored only {self.achieved_points} points. Required points were: " \
                   f"{self.required_point}!"
            user_decision = self.show_losing_screen(text)
            if user_decision == QtWidgets.QMessageBox.DestructiveRole:
                self.goto_level_selection()
            elif user_decision == QtWidgets.QMessageBox.AcceptRole:
                self.goto_game_menu()
            elif user_decision == QtWidgets.QMessageBox.RejectRole:
                self.goto_play_level_again()
        self.game_database.save_user_data()
