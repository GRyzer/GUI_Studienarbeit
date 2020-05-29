from PyQt5.QtWidgets import QApplication
import sys
from secondPage import WindowTwo
from firstPage import WindowOne


class Controller:
    def __init__(self):
        self.first_window = None
        self.second_page = None

    def show_main(self):
        self.first_window = WindowOne()
        self.first_window.switch_window.connect(self.show_second_page)
        if hasattr(self, "second_page"):
            if self.second_page is not None:
                self.second_page.hide()
        self.first_window.show()

    def show_second_page(self):
        self.second_page = WindowTwo()
        self.second_page.switch_window.connect(self.show_main)
        self.first_window.hide()
        self.second_page.show()

    def show_third_page(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Controller()
    game.show_main()
    sys.exit(app.exec())