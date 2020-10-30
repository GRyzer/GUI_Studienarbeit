import os
import pandas as pd


class AccountManagement:
    header = ["username", "password", "age", "gender", "security_query"]

    def __init__(self):
        self.file_path = "src/databases/accounts_database.csv"
        self.df = self.get_accounts()

    def get_accounts(self):
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path, header=0)
        else:
            df = pd.DataFrame(data=None, columns=self.header)
            df.to_csv(self.file_path, index=False)
        return df

    def is_username_available(self, username):
        if username not in self.df.username.values:
            return True
        return False

    def add_account(self, user_information: list):
        if self.is_username_available(user_information[0]):
            new_user_df = pd.DataFrame([user_information], columns=self.header)
            new_user_df.to_csv(self.file_path, mode='a', header=False, index=False)
            self.df = self.df.append(new_user_df, ignore_index=True)
        else:
            raise ValueError(f'Username: {user_information[0]} is already taken!')

    def check_credentials(self, username, password):
        user_account = self.get_user(username)
        if user_account.empty:
            raise ValueError("User does not exist!")
        if str(user_account.password.values[0]) != password:
            raise ValueError("Wrong Password")

    def get_user(self, username):
        return self.df.loc[self.df["username"] == username]

    def reset_account(self, username, security_query, password):
        user_account = self.get_user(username)
        if user_account.empty:
            raise ValueError("User does not exist!")
        if user_account["security_query"].item() != security_query:
            raise ValueError("Wrong answer to security query.")
        user_account["password"] = password
        self.df.update(user_account)
        self.df.to_csv(self.file_path, index=False)



