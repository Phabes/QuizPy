from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty

from DatabaseManagement import connection


class Manager(ScreenManager):
    current_quiz = ObjectProperty(None, allownone=True)
    current_question_id = NumericProperty(-1)

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)

    def back_click(self, screen_name, button):
        self.transition.direction = "right"
        self.current = screen_name
        self.current_screen.refresh()

    def change_user_label(self, label: Label):
        label.text = "HELLO " + connection.user + " !"

    def create_quiz(self):
        self.current = "create"
        self.current_screen.get_all_categories()

    def logout_user(self):
        if connection.logout_user():
            self.exit_quiz()
            self.current = "login"

    def start_quiz(self, quiz):
        self.current_quiz = quiz
        self.next_question()

    def exit_quiz(self):
        self.current_quiz = None
        self.current_question_id = -1
        self.current = "category"

    def next_question(self):
        self.current_question_id += 1
        if self.current_question_id >= len(self.current_quiz["questions"]):
            self.current = "category"
            self.current_question_id = -1
            self.current_quiz = None
        else:
            current_question = self.current_quiz["questions"][self.current_question_id]
            self.current = current_question["type"]
            print(current_question["type"])
            self.current_screen.update_data(current_question)
