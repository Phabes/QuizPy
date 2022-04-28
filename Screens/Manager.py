from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager


class Manager(ScreenManager):
    def __init__(self, connection, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.connection = connection

    def back_click(self, screen_name, button):
        self.transition.direction = "right"
        self.current = screen_name
        self.current_screen.refresh()

    def change_user_label(self, label: Label):
        label.text = "HELLO " + self.connection.user + " !"

    def create_quiz(self):
        self.current = "create"
        self.current_screen.get_all_categories()

    def logout_user(self):
        if self.connection.logout_user():
            self.current = "login"
