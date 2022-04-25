from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager


class Manager(ScreenManager):
    def __init__(self, connection, **kw):
        super().__init__(**kw)
        self.connection = connection

    def change_user_label(self, label: Label):
        label.text = "HELLO " + self.connection.user + " !"
