from PyQt5 import QtWidgets


class ButtonManager(QtWidgets.QButtonGroup):
    def __init__(self):
        super(ButtonManager, self).__init__()
        self.clicked_buttons = []

    def add_first_clicked_button(self, button):
        if not self.clicked_buttons:
            self.clicked_buttons.append(button)

    def has_a_button_been_clicked_before(self):
        if self.clicked_buttons:
            return True
        return False

    @staticmethod
    def do_images_match(button1, button2):
        if button1.id == button2.id:
            return True
        return False

    def is_memory_solved(self):
        if not self.buttons():
            return True
        return False

    def disable_buttons(self):
        for button in self.buttons():
            button.setDisabled(True)

    def enable_buttons(self):
        for button in self.buttons():
            button.setEnabled(True)

    def remove_memory_pair(self, button1, button2):
        button1.setDisabled(True)
        button2.setDisabled(True)
        self.removeButton(button1)
        self.removeButton(button2)

    @staticmethod
    def reset_memory_pair(button1, button2):
        button1.reset_icon()
        button2.reset_icon()

    def show_all_icons(self):
        for button in self.buttons():
            button.show_icon()
