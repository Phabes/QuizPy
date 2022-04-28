from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
class Manager(ScreenManager):
    current_quiz=ObjectProperty(None)
    current_question_id = NumericProperty(-1)
    def __init__(self, connection, **kw):
        super().__init__(**kw)
        self.connection = connection

    def change_user_label(self, label: Label):
        label.text = "HELLO " + self.connection.user + " !"

    def start_quiz(self,quiz):
        self.current_quiz = quiz
        self.next_question()


    def exit_quiz(self):
        self.current_quiz = None
        self.current_question_id = -1
        self.current="category"

    def next_question(self):
        self.current_question_id += 1
        if self.current_question_id >= len(self.current_quiz["questions"]):
            self.current="category"
        else:
            current_question=self.current_quiz["questions"][self.current_question_id]
            self.current = current_question["type"]
            print(current_question["type"])
            self.current_screen.update_data(current_question)








