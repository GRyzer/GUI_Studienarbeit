from PyQt5 import QtCore


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

    def unlock_all_levels(self):
        self.game_database.unlock_all_levels()

    def unlock_next_level(self, level):
        if level == self.get_unlocked_level():
            self.game_database.unlock_level(level + 1)
