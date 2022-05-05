import time

from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty, Clock
from kivy.properties import NumericProperty

from DatabaseManagement import connection


class Manager(ScreenManager):
    current_quiz = ObjectProperty(None, allownone=True)
    current_question_id = NumericProperty(-1)

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.points = 0
        self.time_start = None
        self.time_end = None
        self.multiply = 1

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
        self.points = 0
        self.get_screen("chooseOne").ids.user_points.text = "Points: 0"
        self.get_screen("correctOrder").ids.user_points.text = "Points: 0"
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
            self.current_screen.update_data(current_question)

    def set_time_start(self):
        self.time_start = time.time()

    def set_time_end(self):
        self.time_end = time.time()

    def reset_multiply(self):
        self.multiply = 1

    def increase_multiply(self):
        self.multiply *= 1.15

    def calculate_points(self, max_time):
        remaining_time = max(max_time - (self.time_end - self.time_start), 0)
        to_add = round(remaining_time / max_time * 1000 * self.multiply) + 1000
        return to_add

    def add_points(self, points):
        self.points += points

    def set_points(self, points):
        self.points = points

    def small_change(self, step, maxi, interval):
        if step + self.points >= maxi:
            interval.cancel()
            self.set_points(maxi)
            self.current_screen.ids.user_points.text = "Points: " + str(maxi)
        else:
            self.add_points(step)
            self.current_screen.ids.user_points.text = "Points: " + str(self.points)

    def smooth_change_points(self, old_points, to_add):
        maxi = old_points + to_add
        diff = to_add
        step = diff // 100
        interval = Clock.schedule_interval(lambda x: self.small_change(step, maxi, interval), 1 / 100)