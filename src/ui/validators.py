from PyQt5.QtGui import QValidator


class UsernameValidator(QValidator):
    def __init__(self):
        super(UsernameValidator, self).__init__()

    def validate(self, p_str, p_int):
        if p_int < 5:
            return QValidator.Intermediate, p_str, p_int
        return QValidator.Acceptable, p_str, p_int


class PasswordValidator(QValidator):
    def __init__(self):
        super(PasswordValidator, self).__init__()

    def validate(self, p_str, p_int):
        if p_int < 8:
            return QValidator.Intermediate, p_str, p_int
        return QValidator.Acceptable, p_str, p_int


class SecurityQueryValidator(QValidator):
    def __init__(self):
        super(SecurityQueryValidator, self).__init__()

    def validate(self, p_str, p_int):
        if p_int == 0:
            return QValidator.Intermediate, p_str, p_int
        return QValidator.Acceptable, p_str, p_int
