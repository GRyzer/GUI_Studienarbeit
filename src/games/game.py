from PyQt5 import QtCore, QtWidgets


class Game:
    game_menu_window = QtCore.pyqtSignal()
    level_menu = QtCore.pyqtSignal()
    next_level = QtCore.pyqtSignal(int)
    play_level_again = QtCore.pyqtSignal(int)

    def __init__(self, game_database, level):
        self.game_database = game_database
        self.selected_level = level

    def get_unlocked_level(self):
        return self.game_database.get_unlocked_level()

    def goto_game_menu(self):
        self.game_menu_window.emit()

    def goto_level_selection(self):
        self.level_menu.emit()

    def goto_next_level(self):
        if self.selected_level + 1 <= self.get_unlocked_level():
            self.next_level.emit(self.selected_level + 1)

    def goto_play_level_again(self):
        self.play_level_again.emit(self.selected_level)

    @staticmethod
    def show_every_level_completed():
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Win")
        msg_box.setText("Congratulation you completed every level!")
        msg_box.addButton(QtWidgets.QPushButton('Go back to game menu'), QtWidgets.QMessageBox.AcceptRole)
        msg_box.exec()

    @staticmethod
    def show_losing_screen(text=None):
        displayed_text = "Unfortunately you lost!"
        if text is not None:
            displayed_text = text
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Lose")
        msg_box.setText(displayed_text)
        msg_box.addButton(QtWidgets.QPushButton('Go to game menu'), QtWidgets.QMessageBox.AcceptRole)
        msg_box.addButton(QtWidgets.QPushButton('Play level again'), QtWidgets.QMessageBox.RejectRole)
        msg_box.addButton(QtWidgets.QPushButton('Go to level selection'), QtWidgets.QMessageBox.DestructiveRole)
        return msg_box.exec()

    @staticmethod
    def show_selection_for_next_game(text=None):
        displayed_text = "Congratulation you won!"
        if text is not None:
            displayed_text = text
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Win")
        msg_box.setText(displayed_text)
        msg_box.addButton(QtWidgets.QPushButton('Go to game menu'), QtWidgets.QMessageBox.AcceptRole)
        msg_box.addButton(QtWidgets.QPushButton('Play next level'), QtWidgets.QMessageBox.RejectRole)
        return msg_box.exec()

    @staticmethod
    def show_start_screen(text=None):
        displayed_text = "Do you want to start?"
        if text is not None:
            displayed_text = text
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Round screen")
        msg_box.setText(displayed_text)
        msg_box.addButton(QtWidgets.QPushButton('Start'), QtWidgets.QMessageBox.AcceptRole)
        msg_box.addButton(QtWidgets.QPushButton('Go to main menu'), QtWidgets.QMessageBox.RejectRole)
        return msg_box.exec()

    def unlock_all_levels(self):
        self.game_database.unlock_all_levels()

    def unlock_next_level(self, level):
        if level == self.get_unlocked_level():
            self.game_database.unlock_level(level + 1)
