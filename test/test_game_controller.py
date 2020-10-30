import unittest
import unittest.mock as mc
from src.game_controller.game_controller import GameController
from src.games.game_enum import Game
from PyQt5.QtWidgets import QApplication
from src.games.hangman import hangman


class TestGameController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication([])

    def tearDown(self) -> None:
        self.app.closeAllWindows()

    @mc.patch("src.game_controller.game_controller.hangman.HangmanWindow.initialize_database")
    def test_create_game(self, mock_method):
        hangman_instance = GameController.create_game(Game.Hangman.value, "hello")
        self.assertIsInstance(hangman_instance, hangman.HangmanWindow)

    def test_emit_game_window_signal(self):
        game_controller = GameController(1, "username")
        game_controller.game = mc.MagicMock().return_value
        game_controller.game.hide = mc.MagicMock()
        game_controller.level_window = mc.MagicMock().return_value
        game_controller.level_window.hide = mc.MagicMock()
        game_controller.game_menu_signal = mc.MagicMock().return_value
        game_controller.game_menu_signal.emit = mc.MagicMock()
        game_controller.emit_game_menu_signal()
        game_controller.game_menu_signal.emit.assert_called_once_with("username")

    def test_play_selected_level(self):
        game_controller = GameController(1, "username")
        game_controller.game = mc.MagicMock()
        game_controller.game.play_game = mc.MagicMock()
        game_controller._play_selected_level(1)
        game_controller.game.play_game.assert_called_once_with(1)

    def test_start_again(self):
        game_controller = GameController(1, "username")
        game_controller.game = mc.MagicMock()
        game_controller.game.hide = mc.MagicMock()
        game_controller.start_the_game = mc.MagicMock()
        game_controller.start_again(1)

        game_controller.game.hide.assert_called()
        game_controller.start_the_game.assert_called_once_with(1)

    def test_start_the_game_no_level_provided(self):
        game_controller = GameController(1, "username")
        mocked_game = mc.MagicMock()
        game_controller.create_game = mc.MagicMock(return_value=mocked_game)
        game_controller._connect_signals_to_game = mc.MagicMock()
        game_controller.select_level = mc.MagicMock()
        game_controller.start_the_game()

        game_controller._connect_signals_to_game.assert_called_once_with(mocked_game)
        game_controller.select_level.assert_called()

    def test_start_the_game_with_level_inserted(self):
        game_controller = GameController(1, "username")
        mocked_game = mc.MagicMock().return_value
        mocked_game.hide = mc.MagicMock()
        game_controller.create_game = mc.MagicMock(return_value=mocked_game)
        game_controller._connect_signals_to_game = mc.MagicMock()
        game_controller.level_window = mc.MagicMock().return_value
        game_controller.level_window.hide = mc.MagicMock()
        game_controller._play_selected_level = mc.MagicMock()
        game_controller.start_the_game(1)

        game_controller._connect_signals_to_game.assert_called_once_with(mocked_game)
        game_controller.level_window.hide.assert_called()
        game_controller.game.hide.assert_called()
        game_controller._play_selected_level.assert_called_once_with(1)
