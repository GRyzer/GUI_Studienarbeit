import unittest
import unittest.mock as mock
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.games.button_shooter.button_shooter import ButtonShooterWindow


class TestMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.app = QApplication([])

    def tearDown(self) -> None:
        self.app.closeAllWindows()

    @mock.patch("src.games.button_shooter.button_shooter.GameDatabaseManagement", autospec=True)
    def test_initialize_database(self, mock_class):
        button_shooter = ButtonShooterWindow("username")
        mock_class.assert_called_once_with("src/databases/button_shooter.csv", "username",
                                           ["unlocked_level", "hit_targets"])
        mock_class.return_value.initialize_user_account.assert_called_once_with([1, 0])

    @mock.patch("src.games.button_shooter.button_shooter.ButtonShooter.initialize_database", autospec=True)
    def test_play_game(self, mock_method):
        button_shooter = ButtonShooterWindow("username")
        button_shooter.initialize_game = mock.MagicMock()
        button_shooter.show = mock.MagicMock()
        button_shooter.required_targets = 100
        button_shooter.show_start_screen = mock.MagicMock(return_value=QMessageBox.AcceptRole)
        button_shooter.timer = mock.MagicMock()
        button_shooter.timer.start = mock.MagicMock()
        button_shooter.show_buttons = mock.MagicMock()
        button_shooter.play_game(1)
        button_shooter.show_buttons.assert_called()

    @mock.patch("src.games.button_shooter.button_shooter.ButtonShooter.initialize_database", autospec=True)
    def test_reject_play_game(self, mock_method):
        button_shooter = ButtonShooterWindow("username")
        button_shooter.initialize_game = mock.MagicMock()
        button_shooter.show = mock.MagicMock()
        button_shooter.required_targets = 100
        button_shooter.show_start_screen = mock.MagicMock(return_value=QMessageBox.RejectRole)
        button_shooter.emit_game_menu_signal = mock.MagicMock()
        button_shooter.play_game(1)
        button_shooter.emit_game_menu_signal.assert_called()

    @mock.patch("src.games.button_shooter.button_shooter.ButtonShooter.initialize_database", autospec=True)
    def test_update_timer(self, mock_method):
        button_shooter = ButtonShooterWindow("username")
        button_shooter.countdown = 5
        button_shooter.countdown_label = mock.MagicMock()
        button_shooter.countdown_label.setText = mock.MagicMock()
        button_shooter.timer = mock.MagicMock()
        button_shooter.timer.stop = mock.MagicMock()
        button_shooter.end_the_game = mock.MagicMock()

        for i in range(5):
            button_shooter.update_timer()

        button_shooter.timer.stop.assert_called()
        button_shooter.end_the_game.assert_called()

    @mock.patch("src.games.button_shooter.button_shooter.ButtonShooter.initialize_database", autospec=True)
    def test_update_values_is_true(self, mock_method):
        button_shooter = ButtonShooterWindow("username")
        button_shooter.game_database = mock.MagicMock()
        button_shooter.game_database.get_values = mock.MagicMock(return_value={"hit_targets": 50})
        button_shooter.game_database.update_values = mock.MagicMock()
        button_shooter.hit_targets = 100

        button_shooter.update_values()
        button_shooter.game_database.update_values.assert_called_once_with({"hit_targets": 100})

    @mock.patch("src.games.button_shooter.button_shooter.ButtonShooter.initialize_database", autospec=True)
    def test_update_values_is_false(self, mock_method):
        button_shooter = ButtonShooterWindow("username")
        button_shooter.game_database = mock.MagicMock()
        button_shooter.game_database.get_values = mock.MagicMock(return_value={"hit_targets": 150})
        button_shooter.game_database.update_values = mock.MagicMock()
        button_shooter.hit_targets = 100

        button_shooter.update_values()
        button_shooter.game_database.update_values.assert_called_once_with({})

    @mock.patch("src.games.button_shooter.button_shooter.ButtonShooter.initialize_database", autospec=True)
    def test_end_of_game1(self, mock_method):
        button_shooter = ButtonShooterWindow("username")
        button_shooter.update_values = mock.MagicMock()
        button_shooter.hit_targets = 2000
        button_shooter.required_targets = 2000
        button_shooter.selected_level = button_shooter.max_level
        button_shooter.show_every_level_completed = mock.MagicMock()
        button_shooter.emit_game_menu_signal = mock.MagicMock()

        button_shooter.end_the_game()

        button_shooter.show_every_level_completed.assert_called()
        button_shooter.emit_game_menu_signal.assert_called()

    def test_end_of_game2(self):
        button_shooter = ButtonShooterWindow("username")
        button_shooter.update_values = mock.MagicMock()
        button_shooter.hit_targets = 2000
        button_shooter.required_targets = 2000
        button_shooter.unlock_next_level = mock.MagicMock()
        button_shooter.show_selection_for_next_game = mock.MagicMock(return_value=QMessageBox.AcceptRole)
        button_shooter.game_database.save_user_data = mock.MagicMock()
        button_shooter.emit_game_menu_signal = mock.MagicMock()
        button_shooter.end_the_game()

        button_shooter.emit_game_menu_signal.assert_called()

    def test_end_of_game3(self):
        button_shooter = ButtonShooterWindow("username")
        button_shooter.update_values = mock.MagicMock()
        button_shooter.hit_targets = 2000
        button_shooter.required_targets = 2000
        button_shooter.unlock_next_level = mock.MagicMock()
        button_shooter.show_selection_for_next_game = mock.MagicMock(return_value=QMessageBox.RejectRole)
        button_shooter.game_database.save_user_data = mock.MagicMock()
        button_shooter.emit_play_next_level_signal = mock.MagicMock()
        button_shooter.end_the_game()

        button_shooter.emit_play_next_level_signal.assert_called()

    def test_end_of_game_losing(self):
        button_shooter = ButtonShooterWindow("username")
        button_shooter.update_values = mock.MagicMock()
        button_shooter.hit_targets = 200
        button_shooter.required_targets = 2000
        button_shooter.game_database.save_user_data = mock.MagicMock()
        button_shooter.emit_level_menu_signal = mock.MagicMock()

        button_shooter.show_losing_screen = mock.MagicMock(return_value=QMessageBox.DestructiveRole)
        button_shooter.end_the_game()
        button_shooter.emit_level_menu_signal.assert_called()

        button_shooter.emit_game_menu_signal = mock.MagicMock()
        button_shooter.show_losing_screen = mock.MagicMock(return_value=QMessageBox.AcceptRole)
        button_shooter.end_the_game()
        button_shooter.emit_game_menu_signal.assert_called()

        button_shooter.emit_play_level_again_signal = mock.MagicMock()
        button_shooter.show_losing_screen = mock.MagicMock(return_value=QMessageBox.RejectRole)
        button_shooter.end_the_game()
        button_shooter.emit_play_level_again_signal.assert_called()
