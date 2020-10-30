import unittest
import unittest.mock as mc
import os
import pandas as pd
from src.database_managers.game_database_management import GameDatabaseManagement


class TestDatabase(unittest.TestCase):
    file_name = "game.csv"

    def setUp(self) -> None:
        self.header = ["unlocked_level", "surprise", "car"]
        self.default_data = [10, "big", "electric"]
        self.username = "tim"
        self.database = GameDatabaseManagement(self.file_name, self.username, self.header)

    def tearDown(self) -> None:
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_get_existing_game_database(self):
        original_df = pd.DataFrame(data=None, columns=self.header)
        df_to_test = self.database.get_game_database()
        self.assertTrue(original_df.equals(df_to_test))

        self.database.initialize_user_account(self.default_data)
        self.database.save_user_data()
        df_to_test = self.database.get_game_database()
        original_df = pd.DataFrame(data=[self.default_data], columns=self.header, index=[self.username])
        self.assertTrue(original_df.equals(df_to_test))

    def test_initialize_new_user_account(self):
        self.database.create_user_account = mc.MagicMock()
        self.database.create_user_account.return_value = pd.DataFrame(data=[self.default_data],
                                                                      columns=self.header, index=[self.username])
        original_df = pd.DataFrame(data=[self.default_data], columns=self.header, index=[self.username])
        self.database.initialize_user_account(self.default_data)

        self.database.create_user_account.assert_called_once_with(self.default_data)
        self.assertTrue(original_df.equals(self.database.user_df))

    def test_initialize_existing_user_account(self):
        self.database.user_df = pd.DataFrame(data=[self.default_data], columns=self.header, index=[self.username])
        self.database.save_user_data()
        new_database = GameDatabaseManagement(self.file_name, self.username, self.header)
        new_database.initialize_user_account(self.default_data)
        original_df = pd.DataFrame(data=[self.default_data], columns=self.header, index=[self.username])
        self.assertTrue(original_df.equals(new_database.user_df))

    def test_create_user_account(self):
        df_to_test = self.database.create_user_account(self.default_data)
        original_df = pd.DataFrame(data=[self.default_data], columns=self.header, index=[self.username])
        self.assertTrue(original_df.equals(df_to_test))

    def test_unlock_level(self):
        new_data = self.default_data.copy()
        test_levels = [-10, 1, 35]
        for level in test_levels:
            new_data[0] = level
            self.database.initialize_user_account(self.default_data)
            self.database.unlock_level(level)
            if level > 20 or level < 1:
                expected_df = pd.DataFrame(data=[self.default_data], columns=self.header, index=[self.username])
            else:
                expected_df = pd.DataFrame(data=[new_data], columns=self.header, index=[self.username])
            self.assertTrue(expected_df.equals(self.database.user_df))

    def test_get_unlocked_level(self):
        self.database.initialize_user_account(self.default_data)
        self.assertEqual(10, self.database.get_unlocked_level())

    def test_unlock_all_levels(self):
        self.database.initialize_user_account(self.default_data)
        self.database.unlock_all_levels()
        self.assertEqual(20, self.database.get_unlocked_level())

    def test_update_values(self):
        self.database.initialize_user_account(self.default_data)
        new_data_values = [15, "piano", "alarm"]
        new_data = dict(zip(self.header, new_data_values))
        self.database.update_values(new_data)
        expected_df = pd.DataFrame(data=new_data, columns=self.header, index=[self.username])
        self.assertTrue(expected_df.equals(self.database.user_df))

    def test_get_values(self):
        self.database.initialize_user_account(self.default_data)
        expected_data = dict(zip(self.header, self.default_data))
        self.assertTrue(expected_data == self.database.get_values())

    def test_save_user_data(self):
        self.database.initialize_user_account(self.default_data)
        self.database.save_user_data()
        expected_df = pd.DataFrame(data=[self.default_data], columns=self.header, index=[self.username])
        new_database = GameDatabaseManagement(self.file_name, self.username, self.header)
        self.assertTrue(expected_df.equals(new_database.df))

        new_data_values = [15, "piano", "alarm"]
        new_data = dict(zip(self.header, new_data_values))
        new_database.initialize_user_account(self.default_data)
        new_database.update_values(new_data)
        expected_df = pd.DataFrame(data=new_data, columns=self.header, index=[self.username])
        new_database.save_user_data()
        self.assertTrue(expected_df.equals(new_database.df))


if __name__ == '__main__':
    unittest.main()
