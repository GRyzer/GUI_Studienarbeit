from PyQt5 import QtCore, QtWidgets


class BaseFormWidget:
    min_height = 300
    min_width = 400
    max_height = 1080
    max_width = 1920
    default_height = 600
    default_width = 800

    def get_min_widget(self):
        return QtCore.QSize(self.min_width, self.min_height)

    def get_max_widget(self):
        return QtCore.QSize(self.max_width, self.max_height)

    def get_default_window_size(self):
        return QtCore.QSize(self.default_width, self.default_height)

    @staticmethod
    def get_size_policy(q_object, h_policy=QtWidgets.QSizePolicy.Fixed, v_policy=QtWidgets.QSizePolicy.Fixed):
        size_policy = QtWidgets.QSizePolicy(h_policy, v_policy)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(q_object.sizePolicy().hasHeightForWidth())
        return size_policy
