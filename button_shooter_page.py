from random import randint

from PyQt5 import QtWidgets, QtCore, QtGui

from form_widget import FormWidgetIF
from game_database_management import GameDatabaseManagement


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.button_list = []
        self.countdown_label = None
        self.form_layout = None
        self.game_menu_button = None
        self.grid_layout_of_buttons = None
        self.hit_target_label = None
        self.horizontal_layout = None
        self.horizontal_layout2 = None
        self.level_selection_button = None
        self.main_vertical_layout = None

    def setupUi(self, button_shooter_page, selected_level, uptime):
        button_shooter_page.setMinimumSize(self.get_min_widget())
        button_shooter_page.setMaximumSize(self.get_max_widget())
        button_shooter_page.setWindowTitle(f"Button Shooter, Level: {selected_level}")
        button_shooter_page.resize(self.get_default_window_size())

        self.main_vertical_layout = QtWidgets.QVBoxLayout(button_shooter_page)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.horizontal_layout = QtWidgets.QHBoxLayout(button_shooter_page)

        self.hit_target_label = QtWidgets.QLabel(f"Hit Targets: 0", button_shooter_page)
        self.hit_target_label.setFont(QtGui.QFont('', 26))
        self.hit_target_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontal_layout.addWidget(self.hit_target_label, alignment=QtCore.Qt.AlignCenter)

        self.countdown_label = QtWidgets.QLabel(f"Time Left: {uptime}", button_shooter_page)
        self.countdown_label.setFont(QtGui.QFont('', 26))
        self.countdown_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontal_layout.addWidget(self.countdown_label, alignment=QtCore.Qt.AlignCenter)
        self.main_vertical_layout.addLayout(self.horizontal_layout)

        self.grid_layout_of_buttons = QtWidgets.QGridLayout(button_shooter_page)
        self.grid_layout_of_buttons.setContentsMargins(11, -1, 11, -1)

        for index in range(300):
            button = QtWidgets.QPushButton(button_shooter_page)
            button.setFixedSize(QtCore.QSize(30, 30))
            button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            button.setStyleSheet(f"background-color: {button_shooter_page}")
            self.button_list.append(button)
            self.grid_layout_of_buttons.addWidget(button, index // 20, index % 20)

        self.main_vertical_layout.addLayout(self.grid_layout_of_buttons)
        self.horizontal_layout2 = QtWidgets.QHBoxLayout(button_shooter_page)

        self.form_layout = QtWidgets.QFormLayout(button_shooter_page)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.form_layout.setContentsMargins(-1, -1, 20, 20)

        self.game_menu_button = QtWidgets.QPushButton('return to game menu', button_shooter_page)
        self.game_menu_button.setSizePolicy(self.get_size_policy(self.game_menu_button))
        self.game_menu_button.setFont(QtGui.QFont('', 12))
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.game_menu_button)

        self.level_selection_button = QtWidgets.QPushButton('go to level selection', button_shooter_page)
        self.level_selection_button.setSizePolicy(self.get_size_policy(self.level_selection_button))
        self.level_selection_button.setFont(QtGui.QFont('', 12))
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.level_selection_button)

        self.horizontal_layout2.addLayout(self.form_layout)
        self.main_vertical_layout.addLayout(self.horizontal_layout2)
        button_shooter_page.setLayout(self.main_vertical_layout)
        QtCore.QMetaObject.connectSlotsByName(button_shooter_page)


class ButtonShooter(QtWidgets.QWidget, FormWidget):
    database_path = "databases/buttonshooter.csv"
    game_menu_window = QtCore.pyqtSignal()
    level_menu = QtCore.pyqtSignal()
    next_level = QtCore.pyqtSignal(int)
    max_level = 20
    play_level_again = QtCore.pyqtSignal(int)

    def __init__(self, username):
        super(ButtonShooter, self).__init__()
        self.countdown = None
        self.game_database = GameDatabaseManagement(self.database_path, username)
        self.hit_targets = None
        self.missed_targets = None
        self.required_targets = None
        self.selected_button = None
        self.selected_level = None
        self.start_playing = None
        self.timer = None

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

    def initialize(self, level):
        self.countdown = 100
        self.hit_targets = 0
        self.missed_targets = 0
        self.required_targets = self.get_required_target(level)
        self.selected_level = level
        self.start_playing = True
        self.timer = QtCore.QTimer(self)

        self.setupUi(self, level, self.countdown)

    def connect_buttons_to_game(self):
        self.timer.timeout.connect(self.update_timer)
        self.game_menu_button.clicked.connect(self.goto_game_menu)
        self.level_selection_button.clicked.connect(self.goto_level_selection)
        for button in self.button_list:
            button.clicked.connect(self.is_clicked_button_the_proper_target)

    @staticmethod
    def get_required_target(level):
        return level * 5 + 50

    def play_game(self, level):
        self.initialize(level)
        self.connect_buttons_to_game()
        self.show()
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Round screen")
        msg_box.setText(f"Required Targets: {self.required_targets}.\nDo you want to start?")
        msg_box.addButton(QtWidgets.QPushButton('Start'), QtWidgets.QMessageBox.AcceptRole)
        msg_box.addButton(QtWidgets.QPushButton('Go to main menu'), QtWidgets.QMessageBox.RejectRole)
        t = msg_box.exec()
        if t == QtWidgets.QMessageBox.AcceptRole:
            self.timer.start(1000)
            self.show_buttons()
        elif t == QtWidgets.QMessageBox.RejectRole:
            self.goto_game_menu()

    def update_timer(self):
        # might be deletable
        if self.start_playing:
            self.countdown -= 1
            self.countdown_label.setText(f"Time left: {self.countdown}")
        if self.countdown == 0:
            self.timer.stop()
            self.end_of_game()

    def end_of_game(self):
        if self.hit_targets >= self.required_targets:
            if self.selected_level == self.max_level:
                msg_box = QtWidgets.QMessageBox()
                msg_box.setWindowTitle("Win")
                msg_box.setText("Congratulation you completed every level!")
                msg_box.addButton(QtWidgets.QPushButton('Go back to game menu'), QtWidgets.QMessageBox.AcceptRole)
                msg_box.exec()
                self.goto_game_menu()
            else:
                self.unlock_next_level(self.selected_level)
                msg_box = QtWidgets.QMessageBox()
                msg_box.setWindowTitle("Win")
                msg_box.setText(f"Congratulation you won!\nYou hit {self.hit_targets} targets and you missed "
                                f"{self.missed_targets} targets.")
                msg_box.addButton(QtWidgets.QPushButton('Go to game menu'), QtWidgets.QMessageBox.AcceptRole)
                msg_box.addButton(QtWidgets.QPushButton('Play next level'), QtWidgets.QMessageBox.RejectRole)
                t = msg_box.exec()
                if t == QtWidgets.QMessageBox.AcceptRole:
                    self.goto_game_menu()
                elif t == QtWidgets.QMessageBox.RejectRole:
                    self.goto_next_level()
        else:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Lose")
            msg_box.setText(f"Unfortunately you lost! You only hit {self.hit_targets} targets of required "
                            f"{self.required_targets} targets. You missed {self.missed_targets} targets.")
            msg_box.addButton(QtWidgets.QPushButton('Go to game menu'), QtWidgets.QMessageBox.AcceptRole)
            msg_box.addButton(QtWidgets.QPushButton('Play level again'), QtWidgets.QMessageBox.RejectRole)
            msg_box.addButton(QtWidgets.QPushButton('Go to level selection'), QtWidgets.QMessageBox.DestructiveRole)
            t = msg_box.exec()
            if t == QtWidgets.QMessageBox.DestructiveRole:
                self.goto_level_selection()
            elif t == QtWidgets.QMessageBox.AcceptRole:
                self.goto_game_menu()
            elif t == QtWidgets.QMessageBox.RejectRole:
                self.goto_play_level_again()

    def change_button_background(self, button, color):
        button.setStyleSheet(f"background-color: {color}")

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

    def show_buttons(self):
        self.selected_button = self.button_list[randint(0, len(self.button_list)-1)]
        self.change_button_background(self.selected_button, "red")
