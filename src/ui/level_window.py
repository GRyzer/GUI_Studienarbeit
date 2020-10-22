from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.base_form_widget import BaseFormWidget


class FormWidget(BaseFormWidget):
    def __init__(self):
        self.form_layout = None
        self.form_layout2 = None
        self.grid_layout = None
        self.heading = None
        self.horizontal_layout = None
        self.level_rbutton_list = []
        self.next_window_button = None
        self.previous_window_button = None
        self.radio_button_group = None
        self.username_label = None
        self.vertical_layout = None

    def setupUi(self, level_page, username, unlocked_level_number):
        level_page.setMinimumSize(self.get_min_widget())
        level_page.setMaximumSize(self.get_max_widget())
        level_page.setWindowTitle("Select Level")
        level_page.resize(self.get_default_window_size())

        self.vertical_layout = QtWidgets.QVBoxLayout(level_page)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.form_layout = QtWidgets.QFormLayout(level_page)
        self.form_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.form_layout.setContentsMargins(-1, 20, 40, -1)

        self.username_label = QtWidgets.QLabel(username, level_page)
        self.username_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_label)
        self.vertical_layout.addLayout(self.form_layout)

        self.heading = QtWidgets.QLabel("Levels", level_page)
        self.heading.setSizePolicy(self.get_size_policy(self.heading, QtWidgets.QSizePolicy.Minimum,
                                                        QtWidgets.QSizePolicy.Expanding))
        self.heading.setFont(QtGui.QFont('', 26))
        self.heading.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.vertical_layout.addWidget(self.heading)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.radio_button_group = QtWidgets.QButtonGroup()
        for row in range(0, 5):
            for column in range(1, 5):
                button = QtWidgets.QRadioButton(f"Level {column + row * 4}", level_page)
                button.setSizePolicy(self.get_size_policy(button, QtWidgets.QSizePolicy.Fixed,
                                                          QtWidgets.QSizePolicy.Maximum))
                button.setFont(QtGui.QFont('', 14))
                button.setChecked(row == 0 and column == 1)
                if column + row * 4 > unlocked_level_number:
                    button.setCheckable(False)
                    button.setToolTip("Not unlocked.")
                self.level_rbutton_list.append(button)
                self.grid_layout.addWidget(button, row, column)
                self.radio_button_group.addButton(button, column + row * 4)

        self.vertical_layout.addLayout(self.grid_layout)
        spacer_up = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout.addItem(spacer_up)

        self.horizontal_layout = QtWidgets.QHBoxLayout(level_page)

        self.form_layout2 = QtWidgets.QFormLayout(level_page)
        self.form_layout2.setFormAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.form_layout2.setContentsMargins(-1, -1, 20, 20)

        self.previous_window_button = QtWidgets.QPushButton('return to game menu', level_page)
        self.previous_window_button.setSizePolicy(self.get_size_policy(self.previous_window_button))
        self.previous_window_button.setFont(QtGui.QFont('', 12))
        self.form_layout2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previous_window_button)

        self.next_window_button = QtWidgets.QPushButton('play', level_page)
        self.next_window_button.setSizePolicy(self.get_size_policy(self.next_window_button))
        self.next_window_button.setFont(QtGui.QFont('', 12))
        self.form_layout2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.next_window_button)

        self.horizontal_layout.addLayout(self.form_layout2)
        self.vertical_layout.addLayout(self.horizontal_layout)

        QtCore.QMetaObject.connectSlotsByName(level_page)


class LevelWindow(QtWidgets.QWidget, FormWidget):
    next_window_signal = QtCore.pyqtSignal(int)
    previous_window_signal = QtCore.pyqtSignal()
    unlock_all_levels_signal = QtCore.pyqtSignal()

    def __init__(self, username, unlocked_level_number):
        super(LevelWindow, self).__init__()
        self.setupUi(self, username, unlocked_level_number)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+U"), self)
        self.next_window_button.clicked.connect(self.emit_next_window_signal)
        self.previous_window_button.clicked.connect(self.emit_previous_window_signal)
        self.shortcut.activated.connect(self.unlock_all_levels)

    def emit_next_window_signal(self):
        self.next_window_signal.emit(self.radio_button_group.checkedId())

    def emit_previous_window_signal(self):
        self.previous_window_signal.emit()

    def unlock_all_levels(self):
        self.make_all_rbuttons_checkable()
        self.unlock_all_levels_signal.emit()

    def make_all_rbuttons_checkable(self):
        for button in self.level_rbutton_list:
            button.setCheckable(True)
