import pandas as pd
import os


class AccountManagement:
    header = ["username", "password", "age", "gender"]

    def __init__(self):
        self.file_name = "databases/userdatabase.csv"
        self.df = self.from_file()
        pass

    def from_file(self):
        if os.path.exists(self.file_name):
            df = pd.read_csv(self.file_name, header=0)
        else:
            df = pd.DataFrame(data=None, columns=self.header)
            df.to_csv(self.file_name, index=False)
        return df

    def is_username_available(self, username):
        if username not in self.df.username.values:
            return True
        return False

    def add_account(self, things: list):
        if self.is_username_available(things[0]):
            df2 = pd.DataFrame([things], columns=self.header)
            df2.to_csv(self.file_name, mode='a', header=False, index=False)
            self.df = self.df.append(df2, ignore_index=True)
        else:
            raise ValueError(f'Username: {things[0]} is already taken!')

    def check_credentials(self, username, password):
        user_account = self.get_user(username)
        if user_account.empty:
            raise ValueError("User does not exist!")
        if user_account.password.values[0] != password:
            raise ValueError("Wrong Password")

    def get_user(self, username):
        return self.df.loc[self.df["username"] == username]
