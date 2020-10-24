from PyQt5 import QtWidgets, QtCore

from src.games.button_shooter import button_shooter
from src.games.game_enum import Game
from src.games.hangman import hangman
from src.ui.level_window import LevelWindow
from src.games.memory import memory
from src.games.pattern_recognition import pattern_recognition


class GameController(QtWidgets.QWidget):
    game_menu_signal = QtCore.pyqtSignal(str)

    def __init__(self, selected_game, username):
        super(GameController, self).__init__()
        self.game = None
        self.level_window = None
        self.selected_game = selected_game
        self.username = username

    @staticmethod
    def create_game(game_id, username):
        if game_id == Game.Hangman.value:
            return hangman.HangmanWindow(username)
        elif game_id == Game.PatternRecognition.value:
            return pattern_recognition.PatternRecognitionWindow(username)
        elif game_id == Game.ButtonShooter.value:
            return button_shooter.ButtonShooter(username)
        elif game_id == Game.Memory.value:
            return memory.MemoryWindow(username)
        raise Exception(f"game id {game_id} does not exist!")

    def emit_game_menu_signal(self):
        self.level_window.hide()
        self.game.hide()
        self.game_menu_signal.emit(self.username)

    def start_the_game(self, level=None):
        self.game = self.create_game(self.selected_game, self.username)
        self._connect_signals_to_game(self.game)
        if level is None:
            self.select_level()
        else:
            self.game.hide()
            self.level_window.hide()
            self._play_selected_level(level)

    def _connect_signals_to_game(self, game):
        game.game_menu_signal.connect(self.emit_game_menu_signal)
        game.level_menu_signal.connect(self.select_level)
        game.play_next_level_signal.connect(self.start_again)
        game.play_level_again_signal.connect(self.start_again)

    def select_level(self):
        self.game.hide()
        self.level_window = LevelWindow(self.username, self.game.get_unlocked_level())
        self.level_window.previous_window_signal.connect(self.emit_game_menu_signal)
        self.level_window.next_window_signal.connect(self.start_the_game)
        self.level_window.unlock_all_levels_signal.connect(self.game.unlock_all_levels)
        self.level_window.show()

    def _play_selected_level(self, level):
        self.game.play_game(level)

    def start_again(self, level):
        self.game.hide()
        self.start_the_game(level)
