import unittest
import unittest.mock as mock
from PyQt5.QtWidgets import QApplication
import PyQt5.QtWidgets as QtWidgets
from src.games.hangman.hangman import HangmanWindow


class TestMemory(unittest.TestCase):
    @mock.patch("src.games.hangman.hangman.HangmanWindow.initialize_database")
    def setUp(self, method) -> None:
        self.app = QApplication([])
        self.hangman = HangmanWindow("username")

    def tearDown(self) -> None:
        self.app.closeAllWindows()

    @mock.patch("src.games.hangman.hangman.GameDatabaseManagement", autospec=True)
    def test_initialize_database(self, mock_class):
        hangman = HangmanWindow("username")
        mock_class.assert_called_once_with("src/databases/hangman.csv", "username",
                                           ["unlocked_level", "word_guessed_by_letter"])
        mock_class.return_value.initialize_user_account.assert_called_once_with([1, 0.0])

    def test_get_trials(self):
        self.assertTrue(HangmanWindow.get_trials(4), 10)
        self.assertTrue(HangmanWindow.get_trials(8), 9)
        self.assertTrue(HangmanWindow.get_trials(12), 8)
        self.assertTrue(HangmanWindow.get_trials(16), 7)
        self.assertTrue(HangmanWindow.get_trials(18), 6)

    def test_get_hangman_picture_paths(self):
        folder = "src/assets/hangman"
        self.assertEqual(HangmanWindow.get_hangman_picture_paths(6),
                        [f"{folder}/hangman1.png", f"{folder}/hangman2.png", f"{folder}/hangman3.png",
                         f"{folder}/hangman4.png", f"{folder}/hangman5.png", f"{folder}/hangman10.png"])

    def test_get_blanked_word(self):
        self.assertEqual(HangmanWindow.get_blanked_word("hallo"), "_ _ _ _ _ ")

    def test_letter_not_in_searched_word(self):
        self.hangman.searched_word = "letter"
        self.assertTrue(self.hangman.letter_not_in_searched_word("x"))
        self.assertFalse(self.hangman.letter_not_in_searched_word("e"))

    @mock.patch("src.games.hangman.hangman.QtGui.QPixmap")
    def test_update_hangman(self, mock_class):
        self.hangman.trials_left = 5
        self.hangman.trials_left_label = QtWidgets.QLabel(f"Trials left: {self.hangman.trials_left}")
        self.hangman.hangman_pic_label = mock.MagicMock()
        self.hangman.hangman_pic_label.setPixmap = mock.MagicMock()
        self.hangman.hangman_picture_list = [1, 2, 3, 4, 5]
        self.hangman.update_hangman()

        self.assertEqual(4, self.hangman.trials_left)
        self.assertEqual("Trials left: 4", self.hangman.trials_left_label.text())

    def test_update_searched_word(self):
        self.hangman.searched_blank_word = "_ _ _ "
        self.hangman.searched_word = "UHU"
        self.hangman.searched_blank_word_label = QtWidgets.QLabel(f"Trials left: {self.hangman.trials_left}")

        self.hangman.update_searched_word("H")
        self.assertEqual("_ H _ ", self.hangman.searched_blank_word)
        self.assertEqual("_ H _ ", self.hangman.searched_blank_word_label.text())

    def test_update_used_letters(self):
        self.hangman.used_letters_list = ["E", "A"]
        self.hangman.update_used_letters("E")
        self.assertEqual(self.hangman.used_letters_list, ["E", "A"])


