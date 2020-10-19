from PyQt5 import QtWidgets, QtCore

from src.games.button_shooter import button_shooter
from src.games.game_enum import Game
from src.games.hangman import hangman
from src.ui.level_page import LevelWindow
from src.games.memory import memory
from src.games.pattern_recognition import pattern_recognition


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
            game = hangman.HangmanWindow(self.username)
        elif self.selected_game == Game.PatternRecognition.value:
            game = pattern_recognition.PatternRecognitionWindow(self.username)
        elif self.selected_game == Game.ButtonShooter.value:
            game = button_shooter.ButtonShooter(self.username)
        elif self.selected_game == Game.Memory.value:
            game = memory.MemoryWindow(self.username)
        return game

    def play_level(self, level):
        self.game.hide()
        self.create_game()
        self.game.play_game(level)
