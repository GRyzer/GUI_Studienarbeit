
from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.base_form_widget import BaseFormWidget
from src.games.memory.button import Button
from src.games.memory.button_manager import ButtonManager


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
