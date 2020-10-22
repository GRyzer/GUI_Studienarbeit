import sys

from PyQt5.QtWidgets import QApplication

from src.database_managers.account_management import AccountManagement
from src.ui.game_menu_window import GameMenuWindow
from src.game_controller.game_controller import GameController
from src.ui.login_window import LogInWindow
from src.ui.main_menu_window import MainMenu
from src.ui.sign_up_window import SignUpWindow


class GameLauncher:
    def __init__(self):
        self.account = AccountManagement()
        self.game_controller = None
        self.game_menu_window = None
        self.login_window = None
        self.main_menu_window = None
        self.signup_window = None

    def show_main_menu_window(self):
        self.main_menu_window = MainMenu()
        self.main_menu_window.game_menu_signal.connect(self.show_game_menu_window)
        self.main_menu_window.log_in_signal.connect(self.show_login_window)
        self.main_menu_window.signup_signal.connect(self.show_signup_window)
        if self.game_menu_window is not None:
            self.game_menu_window.hide()
        if self.login_window is not None:
            self.login_window.hide()
        if self.signup_window is not None:
            self.signup_window.hide()
        self.main_menu_window.show()

    def show_signup_window(self):
        self.signup_window = SignUpWindow(self.account)
        self.signup_window.next_window_signal.connect(self.show_game_menu_window)
        self.signup_window.previous_window_signal.connect(self.show_main_menu_window)
        if self.login_window is not None:
            self.login_window.hide()
        self.main_menu_window.hide()
        self.signup_window.show()

    def show_login_window(self):
        self.login_window = LogInWindow(self.account)
        self.login_window.next_window_signal.connect(self.show_game_menu_window)
        self.login_window.previous_window_signal.connect(self.show_main_menu_window)
        self.main_menu_window.hide()
        self.login_window.show()

    def show_game_menu_window(self, username=None):
        if username is None:
            username = 'Anonymous'
        self.game_menu_window = GameMenuWindow(username=username)
        self.game_menu_window.game_signal.connect(self.start_selected_game)
        self.game_menu_window.main_menu_signal.connect(self.show_main_menu_window)
        if self.login_window is not None:
            self.login_window.hide()
        if self.signup_window is not None:
            self.signup_window.hide()
        self.main_menu_window.hide()
        self.game_menu_window.show()

    def start_selected_game(self, selected_game, username):
        self.game_controller = GameController(selected_game, username)
        self.game_controller.game_menu_signal.connect(self.show_game_menu_window)
        self.game_menu_window.hide()
        self.game_controller.start()


if __name__ == '__main__':
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = my_exception_hook
    app = QApplication(sys.argv)
    control = GameLauncher()
    control.show_main_menu_window()
    try:
        sys.exit(app.exec())
    except:
        print("Exiting")