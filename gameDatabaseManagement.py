import pandas as pd
import os

# TODO Anonymous user should be temporary and shall be deleted, not sure where exactly maybe at game menu


class GameDatabaseManagement:
    header = ["username", "unlocked_level"]

    def __init__(self, file_path, username, max_level=20):
        self.max_level = max_level
        self.file_path = file_path
        self.username = username
        self.df = self.get_game_database()
        self.initialize_user_account(username)

    def get_game_database(self):
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path, header=0)
        else:
            df = pd.DataFrame(data=None, columns=self.header)
            df.to_csv(self.file_path, index=False)
        return df

    def initialize_user_account(self, username):
        df = self.df.loc[self.df["username"] == username]
        if df.empty:
            self.create_user_account(username)

    def create_user_account(self, username):
        default_data = [username, 1]
        df2 = pd.DataFrame([default_data], columns=self.header)
        self.df = self.df.append(df2, ignore_index=True)
        self.df.to_csv(self.file_path, index=False)

    def unlock_level(self, level):
        if level < self.max_level:
            self.df.loc[self.df["username"] == self.username, 'unlocked_level'] = level
            self.df.to_csv(self.file_path, index=False)

    def get_unlocked_level(self):
        return self.df.loc[self.df["username"] == self.username, 'unlocked_level'].item()

    def unlock_all_levels(self):
        self.df.loc[self.df["username"] == self.username, 'unlocked_level'] = self.max_level
        self.df.to_csv(self.file_path, index=False)
