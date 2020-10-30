import unittest
import unittest.mock as mock
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.games.memory.memory import MemoryWindow


class TestMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.app = QApplication([])
        self.memory = MemoryWindow("test_username")
        self.memory.initialize_game(1)

    def tearDown(self) -> None:
        self.app.closeAllWindows()

    def test_check_if_memory_is_solved(self):
        self.memory.button_manager = mock.MagicMock()
        self.memory.button_manager.is_memory_solved.return_value = True

        self.memory.end_the_game = mock.MagicMock()
        self.memory.check_for_end_of_game()

        self.memory.end_the_game.assert_called_once_with()

    def test_check_if_memory_is_solved2(self):
        self.memory.button_manager = mock.MagicMock()
        self.memory.button_manager.is_memory_solved.return_value = False

        self.memory.end_the_game = mock.MagicMock()
        self.memory.check_for_end_of_game()

        self.memory.end_the_game.assert_not_called()

    @mock.patch("src.games.memory.memory.GameDatabaseManagement", autospec=True)
    def test_initialize_database(self, mock_class1):
        self.memory1 = MemoryWindow("username")
        mock_class1.assert_called_once_with("src/databases/memory.csv", "username",
                                            ["unlocked_level", "achieved_points"])
        mock_class1.return_value.initialize_user_account.assert_called_once_with([1, 0])

    def test_initialize_game(self):
        self.memory.set_memory_images = mock.MagicMock()
        self.memory.connect_buttons_to_game = mock.MagicMock()
        self.memory.initialize_game(2)

        self.memory.connect_buttons_to_game.assert_called()
        self.memory.set_memory_images.assert_called()
        self.assertEqual(900, self.memory.required_points)

    def test_memory_images(self):
        id_list = []
        for button in self.memory.button_manager.buttons():
            id_list.append(button.image_number)
        for i in range(1, self.memory.memory_card_pairs + 1):
            self.assertEqual(2, id_list.count(i))

    def test_update_moves(self):
        self.memory.update_moves()
        self.assertEqual(1, self.memory.moves)
        self.assertEqual("Moves: 1", self.memory.moves_label.text())

    def test_update_points(self):
        self.memory.update_points(500)
        self.assertEqual(500, self.memory.achieved_points)
        self.assertEqual("Points: 500", self.memory.points_label.text())

    def test_end_of_game1(self):
        self.memory.update_values = mock.MagicMock()
        self.memory.achieved_points = 2000
        self.memory.selected_level = 20
        self.memory.show_every_level_completed = mock.MagicMock()
        self.memory.emit_game_menu_signal = mock.MagicMock()

        self.memory.end_the_game()

        self.memory.show_every_level_completed.assert_called()
        self.memory.emit_game_menu_signal.assert_called()

    def test_end_of_game2(self):
        self.memory.update_values = mock.MagicMock()
        self.memory.achieved_points = 2000
        self.memory.unlock_next_level = mock.MagicMock()
        self.memory.show_selection_for_next_game = mock.MagicMock(return_value=QMessageBox.AcceptRole)
        self.memory.game_database.save_user_data = mock.MagicMock()
        self.memory.emit_game_menu_signal = mock.MagicMock()
        self.memory.end_the_game()

        self.memory.emit_game_menu_signal.assert_called()

    def test_end_of_game3(self):
        self.memory.update_values = mock.MagicMock()
        self.memory.achieved_points = 2000
        self.memory.unlock_next_level = mock.MagicMock()
        self.memory.show_selection_for_next_game = mock.MagicMock(return_value=QMessageBox.RejectRole)
        self.memory.game_database.save_user_data = mock.MagicMock()
        self.memory.emit_play_next_level_signal = mock.MagicMock()
        self.memory.end_the_game()

        self.memory.emit_play_next_level_signal.assert_called()

    def test_end_of_game_losing(self):
        self.memory.update_values = mock.MagicMock()
        self.memory.achieved_points = 100
        self.memory.game_database.save_user_data = mock.MagicMock()
        self.memory.emit_level_menu_signal = mock.MagicMock()

        self.memory.show_losing_screen = mock.MagicMock(return_value=QMessageBox.DestructiveRole)
        self.memory.end_the_game()
        self.memory.emit_level_menu_signal.assert_called()

        self.memory.emit_game_menu_signal = mock.MagicMock()
        self.memory.show_losing_screen = mock.MagicMock(return_value=QMessageBox.AcceptRole)
        self.memory.end_the_game()
        self.memory.emit_game_menu_signal.assert_called()

        self.memory.emit_play_level_again_signal = mock.MagicMock()
        self.memory.show_losing_screen = mock.MagicMock(return_value=QMessageBox.RejectRole)
        self.memory.end_the_game()
        self.memory.emit_play_level_again_signal.assert_called()


if __name__ == '__main__':
    unittest.main()




