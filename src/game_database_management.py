import os
import pandas as pd


class GameDatabaseManagement:

    def __init__(self, file_path, username, header, max_level=20):
        self.file_path = file_path
        self.header = header
        self.max_level = max_level
        self.username = username
        self.df = self.get_game_database()
        self.user_df = None

    def get_game_database(self):
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path, header=0, index_col=0)
        else:
            df = pd.DataFrame(data=None, columns=self.header)
        return df

    def initialize_user_account(self, default_data):
        try:
            self.user_df = self.df.loc[[self.username]]
        except KeyError:
            self.user_df = self.create_user_account(default_data)

    def create_user_account(self, default_data):
        return pd.DataFrame([default_data], columns=self.header, index=[self.username])

    def unlock_level(self, level):
        if self.max_level >= level > 0:
            self.user_df['unlocked_level'] = level

    def get_unlocked_level(self):
        return self.user_df['unlocked_level'].item()

    def unlock_all_levels(self):
        self.user_df['unlocked_level'] = self.max_level

    def update_values(self, data_dict):
        for key, value in data_dict.items():
            if key == "unlocked_level":
                self.unlock_level(value)
                continue
            self.user_df[key] = value

    def get_values(self):
        return self.user_df.to_dict('index')[self.username]

    def save_user_data(self):
        if self.username == 'Anonymous':
            return None
        elif self.user_df.index.values[0] in self.df.index.values:
            self.df.update(self.user_df)
        else:
            self.df = self.df.append(self.user_df)
        self.df.to_csv(self.file_path, index=True)
