import pandas as pd
import unittest
import unittest.mock as mc
from src.database_managers.account_management import AccountManagement


class TestingDF:
    def __init__(self, usernames: list):
        self.username = {"values": usernames}

    def __iter__(self):
        for element in self.username["values"]:
            yield element


class TestAccountManagement(unittest.TestCase):

    @mc.patch("src.database_managers.account_management.AccountManagement.get_accounts")
    def test_is_username_available(self, mock_method):
        mock_method.return_value = mc.MagicMock(TestingDF([]))
        account_manager = AccountManagement()
        self.assertTrue(account_manager.is_username_available("username"))

    @mc.patch("src.database_managers.account_management.AccountManagement.get_accounts")
    def test_add_account_username_not_available(self, mock_method):
        mock_method.return_value = mc.MagicMock(TestingDF([]))
        account_manager = AccountManagement()
        account_manager.is_username_available = mc.MagicMock(return_value=False)

        with self.assertRaises(ValueError) as context:
            account_manager.add_account(["username"])
        self.assertTrue("Username: username is already taken!" in str(context.exception))

    @mc.patch("src.database_managers.account_management.AccountManagement.get_accounts")
    @mc.patch("src.database_managers.account_management.pd.DataFrame.to_csv")
    def test_add_account_username_is_available(self, csv_mock, mock_method):
        mock_method.return_value = pd.DataFrame(data=None, columns=AccountManagement.header)
        user_information = ["username", "password", "12", "male", "song"]
        account_manager = AccountManagement()
        account_manager.is_username_available = mc.MagicMock(return_value=True)

        account_manager.add_account(user_information)
        expected_df = pd.DataFrame(data=[user_information], columns=AccountManagement.header)
        self.assertTrue(account_manager.df.equals(expected_df))

    @mc.patch("src.database_managers.account_management.AccountManagement.get_accounts")
    def test_check_credentials_user_does_not_exist(self, mock_method):
        user_information = ["username", "password", "12", "male", "song"]
        mock_method.return_value = pd.DataFrame(data=[user_information], columns=AccountManagement.header)
        account_manager = AccountManagement()
        account_manager.is_username_available = mc.MagicMock(return_value=True)

        with self.assertRaises(ValueError) as context:
            account_manager.check_credentials("test", "pass")
        self.assertTrue("User does not exist!" in str(context.exception))

    @mc.patch("src.database_managers.account_management.AccountManagement.get_accounts")
    def test_check_credentials_password_is_wrong(self, mock_method):
        user_information = ["username", "password", "12", "male", "song"]
        mock_method.return_value = pd.DataFrame(data=[user_information], columns=AccountManagement.header)
        account_manager = AccountManagement()
        account_manager.is_username_available = mc.MagicMock(return_value=True)

        with self.assertRaises(ValueError) as context:
            account_manager.check_credentials("username", "pass")
        self.assertTrue("Wrong Password" in str(context.exception))

