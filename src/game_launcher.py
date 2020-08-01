import sys

from PyQt5.QtWidgets import QApplication

from src.account_management import AccountManagement
from src.game_menu_page import GameMenuWindow
from src.game_controller import GameController
from src.login_page import LogInWindow
from src.main_menu_page import WindowOne
from src.sign_up_page import SignUpWindow

# TODO language change german english
# TODO create an Interface for DatabaseManagement


class GameLauncher:
    def __init__(self):
        self.account = AccountManagement()
        self.game_controller = None
        self.game_menu_window = None
        self.login_window = None
        self.main_menu = None
        self.signup_window = None

    def show_main(self):
        self.main_menu = WindowOne()
        self.main_menu.game_menu_window.connect(self.show_game_menu_page)
        self.main_menu.log_in_window.connect(self.show_login_page)
        self.main_menu.signup_window.connect(self.show_signup_page)
        if self.game_menu_window is not None:
            self.game_menu_window.hide()
        if self.login_window is not None:
            self.login_window.hide()
        if self.signup_window is not None:
            self.signup_window.hide()
        self.main_menu.show()

    def show_signup_page(self):
        self.signup_window = SignUpWindow(self.account)
        self.signup_window.next_window.connect(self.show_game_menu_page)
        self.signup_window.previous_window.connect(self.show_main)
        if self.login_window is not None:
            self.login_window.hide()
        self.main_menu.hide()
        self.signup_window.show()

    def show_login_page(self):
        self.login_window = LogInWindow(self.account)
        self.login_window.next_window.connect(self.show_game_menu_page)
        self.login_window.previous_window.connect(self.show_main)
        self.main_menu.hide()
        self.login_window.show()

    def show_game_menu_page(self, username=None):
        if username is None:
            username = 'Anonymous'
        self.game_menu_window = GameMenuWindow(username=username)
        self.game_menu_window.game_window.connect(self.game_controller_page)
        self.game_menu_window.main_menu_window.connect(self.show_main)
        if self.login_window is not None:
            self.login_window.hide()
        if self.signup_window is not None:
            self.signup_window.hide()
        self.main_menu.hide()
        self.game_menu_window.show()

    def game_controller_page(self, selected_game, username):
        self.game_controller = GameController(selected_game, username)
        self.game_controller.game_menu_window.connect(self.show_game_menu_page)
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
    control.show_main()
    try:
        sys.exit(app.exec())
    except:
        print("Exiting")