from PyQt5.QtWidgets import QApplication
import sys
from SignUpPage import SignUpWindow
from MainMenuPage import WindowOne
from LogInPage import LogInWindow
from accountManagement import AccountManagement
from GameMenuPage import GameMenuWindow
from GameController import GameController

# TODO language change german english
# TODO create an Interface for DatabaseManagement


class Controller:
    def __init__(self):
        self.main_menu = None
        self.signup_window = None
        self.login_window = None
        self.game_menu_window = None
        self.game_controller = None
        self.account = AccountManagement()

    def show_main(self):
        self.main_menu = WindowOne()
        self.main_menu.signup_window.connect(self.show_signup_page)
        self.main_menu.log_in_window.connect(self.show_login_page)
        self.main_menu.game_menu_window.connect(self.show_game_menu_page)
        if self.signup_window is not None:
            self.signup_window.hide()
        if self.login_window is not None:
            self.login_window.hide()
        if self.game_menu_window is not None:
            self.game_menu_window.hide()
        self.main_menu.show()

    def show_signup_page(self):
        self.signup_window = SignUpWindow(self.account)
        self.signup_window.previous_window.connect(self.show_main)
        self.signup_window.next_window.connect(self.show_game_menu_page)
        if self.login_window is not None:
            self.login_window.hide()
        self.main_menu.hide()
        self.signup_window.show()

    def show_login_page(self):
        self.login_window = LogInWindow(self.account)
        self.login_window.previous_window.connect(self.show_main)
        self.login_window.next_window.connect(self.show_game_menu_page)
        self.main_menu.hide()
        self.login_window.show()

    def show_game_menu_page(self, username=None):
        if username is None:
            username = 'Anonymous'
        self.game_menu_window = GameMenuWindow(username=username)
        self.game_menu_window.main_menu_window.connect(self.show_main)
        self.game_menu_window.game_window.connect(self.game_controller_page)
        if self.signup_window is not None:
            self.signup_window.hide()
        if self.login_window is not None:
            self.login_window.hide()
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
    control = Controller()
    control.show_main()
    try:
        sys.exit(app.exec())
    except:
        print("Exiting")