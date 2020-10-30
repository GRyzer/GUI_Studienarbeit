import unittest
import unittest.mock as mc
from PyQt5.QtWidgets import QApplication
from src.game_launcher.game_launcher import GameLauncher


class TestGameLauncher(unittest.TestCase):
    def setUp(self) -> None:
        self.app = QApplication([])

    def tearDown(self) -> None:
        self.app.closeAllWindows()
        GameLauncher.clear_instance()

    @mc.patch("src.game_launcher.game_launcher.AccountManagement")
    def test_init_of_game_launcher(self, mocked_class):
        game_launcher = GameLauncher()

        self.assertIs(game_launcher, game_launcher.__instance__)

    @mc.patch("src.game_launcher.game_launcher.AccountManagement")
    def test_init_of_game_launcher_two_instances(self, mocked_class):
        game_launcher = GameLauncher()

        with self.assertRaises(Exception) as context:
            game_launcher2 = GameLauncher()

        self.assertTrue("Only one instance of GameLauncher is allowed!" in str(context.exception))

    @mc.patch("src.game_launcher.game_launcher.AccountManagement")
    def test_get_same_object_of_game_launcher_twice(self, mocked_class):
        game_launcher = GameLauncher()

        game_launcher2 = GameLauncher.get_instance()

        self.assertIs(game_launcher, game_launcher2)

    @mc.patch("src.game_launcher.game_launcher.AccountManagement")
    @mc.patch("src.game_launcher.game_launcher.GameMenuWindow")
    def test_show_game_menu_window(self, mocked_game_menu, mocked_account):
        mocked_game_menu.return_value.game_signal.connect = mc.MagicMock()
        mocked_game_menu.return_value.main_menu_signal.connect = mc.MagicMock()
        game_launcher = GameLauncher()
        game_launcher.main_menu_window = mc.MagicMock()
        game_launcher.main_menu_window.hide = mc.MagicMock()
        game_launcher.show_game_menu_window("username")

        game_launcher.main_menu_window.hide.assert_called()
        mocked_game_menu.return_value.show.assert_called()

    @mc.patch("src.game_launcher.game_launcher.AccountManagement")
    @mc.patch("src.game_launcher.game_launcher.GameController")
    def test_start_selected_game(self, mocked_game_controller, mocked_account):
        mocked_game_controller.return_value.game_menu_signal.connect = mc.MagicMock()
        mocked_game_controller.return_value.start_the_game = mc.MagicMock()
        game_launcher = GameLauncher()
        game_launcher.game_menu_window = mc.MagicMock()
        game_launcher.game_menu_window.hide = mc.MagicMock()
        game_launcher.start_selected_game(1, "username")

        game_launcher.game_menu_window.hide.assert_called()
        mocked_game_controller.return_value.start_the_game.assert_called()


if __name__ == '__main__':
    unittest.main()
