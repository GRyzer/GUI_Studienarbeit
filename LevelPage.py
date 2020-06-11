from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from formWidget import FormWidgetIF


class FormWidget(FormWidgetIF):
    def __init__(self):
        self.level_rbutton_list = []
        self.username_layout = None
        self.verticalLayout = None
        self.username_label = None
        self.heading = None
        self.gridLayout = None
        self.horizontalLayout = None
        self.formLayout2 = None
        self.previous_window_button = None
        self.next_window_button = None
        self.radio_button_group = None

    def setupUi(self, level_page, username, unlocked_level_number):
        level_page.setMinimumSize(self.get_min_widget())
        level_page.setMaximumSize(self.get_max_widget())
        level_page.setWindowTitle("Select Level")
        level_page.resize(self.get_default_window_size())

        self.verticalLayout = QVBoxLayout(level_page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.username_layout = QtWidgets.QFormLayout(level_page)
        self.username_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.username_layout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.username_layout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.username_layout.setContentsMargins(-1, 20, 40, -1)

        self.username_label = QtWidgets.QLabel(username, level_page)
        self.username_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.username_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_label)
        self.verticalLayout.addLayout(self.username_layout)

        self.heading = QtWidgets.QLabel("Levels", level_page)
        self.heading.setSizePolicy(self.get_size_policy(self.heading, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.heading.setFont(QFont('', 26))
        self.heading.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.heading)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.radio_button_group = QButtonGroup()
        for row in range(0, 5):
            for column in range(1, 5):
                button = QRadioButton(f"Level {column + row * 4}", level_page)
                button.setSizePolicy(self.get_size_policy(button, QSizePolicy.Fixed, QSizePolicy.Maximum))
                button.setFont(QFont('', 14))
                button.setChecked(row == 0 and column == 1)
                if column + row * 4 > unlocked_level_number:
                    button.setCheckable(False)
                    button.setToolTip("Not unlocked.")
                self.level_rbutton_list.append(button)
                self.gridLayout.addWidget(button, row, column)
                self.radio_button_group.addButton(button, column + row * 4)

        self.verticalLayout.addLayout(self.gridLayout)
        spacer_up = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_up)

        self.horizontalLayout = QHBoxLayout(level_page)

        self.formLayout2 = QFormLayout(level_page)
        self.formLayout2.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.formLayout2.setContentsMargins(-1, -1, 20, 20)

        self.previous_window_button = QPushButton('return to game menu', level_page)
        self.previous_window_button.setSizePolicy(self.get_size_policy(self.previous_window_button))
        self.previous_window_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previous_window_button)

        self.next_window_button = QPushButton('play', level_page)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QFont('', 12))
        self.formLayout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.horizontalLayout.addLayout(self.formLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        QtCore.QMetaObject.connectSlotsByName(level_page)

    def make_all_rbuttons_checkable(self):
        for button in self.level_rbutton_list:
            button.setCheckable(True)


class LevelWindow(QtWidgets.QWidget, FormWidget):
    previous_window = QtCore.pyqtSignal()
    next_window = QtCore.pyqtSignal(int)
    unlock_all_levels_signal = QtCore.pyqtSignal()

    def __init__(self, username, unlocked_level_number):
        super(LevelWindow, self).__init__()
        self.setupUi(self, username, unlocked_level_number)
        self.shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        self.shortcut.activated.connect(self.unlock_all_levels)
        self.previous_window_button.clicked.connect(self.go_to_previous_window)
        self.next_window_button.clicked.connect(self.go_to_game)

    def go_to_previous_window(self):
        self.previous_window.emit()

    def go_to_game(self):
        self.next_window.emit(self.radio_button_group.checkedId())

    def unlock_all_levels(self):
        self.make_all_rbuttons_checkable()
        self.unlock_all_levels_signal.emit()
