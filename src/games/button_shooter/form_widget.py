
from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.base_form_widget import BaseFormWidget


class FormWidget(BaseFormWidget):
    def __init__(self, button_shooter_page, selected_level, uptime):
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
        self.setupUi(button_shooter_page, selected_level, uptime)

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
