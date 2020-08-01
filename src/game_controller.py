from PyQt5 import QtWidgets, QtCore

from src.button_shooter_page import ButtonShooter
from src.games_enum import Game
from src.hangman_page import HangmanWindow
from src.level_page import LevelWindow
from src.memory_page import MemoryWindow
from src.pattern_recognition_page import PatternRecognitionWindow


class GameController(QtWidgets.QWidget):
    game_menu_window = QtCore.pyqtSignal(str)

    def __init__(self, selected_game, username):
        super(GameController, self).__init__()
        self.game = None
        self.level_window = None
        self.selected_game = selected_game
        self.username = username

    def start(self):
        self.create_game()
        self.goto_level_menu()

    def start_again(self):
        self.game.hide()
        self.create_game()
        self.goto_level_menu()

    def create_game(self):
        self.game = self.select_game()
        self.game.game_menu_window.connect(self.goto_game_menu)
        self.game.level_menu.connect(self.start_again)
        self.game.next_level.connect(self.play_level)
        self.game.play_level_again.connect(self.play_level)

    def goto_game_menu(self):
        self.level_window.hide()
        self.game.hide()
        self.game_menu_window.emit(self.username)

    def goto_level_menu(self):
        self.game.hide()
        self.level_window = LevelWindow(self.username, self.game.get_unlocked_level())
        self.level_window.previous_window.connect(self.goto_game_menu)
        self.level_window.next_window.connect(self.start_game)
        self.level_window.unlock_all_levels_signal.connect(self.game.unlock_all_levels)
        self.level_window.show()

    def start_game(self, level):
        self.level_window.hide()
        self.game.play_game(level)

    def select_game(self):
        game = None
        if self.selected_game == Game.Hangman.value:
            game = HangmanWindow(self.username)
        elif self.selected_game == Game.PatternRecognition.value:
            game = PatternRecognitionWindow(self.username)
        elif self.selected_game == Game.ButtonShooter.value:
            game = ButtonShooter(self.username)
        elif self.selected_game == Game.Memory.value:
            game = MemoryWindow(self.username)
        return game

    def play_level(self, level):
        self.game.hide()
        self.create_game()
        self.game.play_game(level)
