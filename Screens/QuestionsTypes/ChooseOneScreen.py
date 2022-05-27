import time
from random import shuffle

from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class ChooseOneScreen(Screen):
    question = ObjectProperty(None)
    isCorrect = NumericProperty(-1)

    def __init__(self, sm, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.time = 0
        self.interval: Clock.time = None
        self.block = False
        self.max_time = 15

    def next_question_callback(self, dt):
        self.block = False
        self.ids.back_button.disabled=False
        self.sm.next_question()

    # def small_change(self, step, maxi, interval):
    #     if step + self.sm.points >= maxi:
    #         interval.cancel()
    #         self.sm.set_points(maxi)
    #         self.ids.user_points.text = "Points: " + str(maxi)
    #     else:
    #         self.sm.add_points(step)
    #         self.ids.user_points.text = "Points: " + str(self.sm.points)
    #
    # def smooth_change_points(self, old_points, to_add):
    #     maxi = old_points + to_add
    #     diff = to_add
    #     step = diff // 100
    #     interval = Clock.schedule_interval(lambda x: self.small_change(step, maxi, interval), 1 / 100)

    def finalize_answer(self, *args):
        self.ids.back_button.disabled=True
        if not self.block:
            self.sm.set_time_end()
            if not self.ids.after_answer_label.visible:
                if args[0] == self.question["correct"]:
                    self.ids.after_answer_label.text = "Correct!"
                    self.ids.after_answer_label.color = (1, 0, 1, 1)
                    old_points = self.sm.points
                    to_add = self.sm.calculate_points(self.max_time)
                    self.sm.smooth_change_points(old_points, to_add)
                    self.sm.increase_multiply()
                else:
                    self.ids.after_answer_label.text = "Incorrect!"
                    self.ids.after_answer_label.color = (1, 0, 0, 1)
                    self.sm.reset_multiply()
                self.ids.after_answer_label.visible = True
                self.isCorrect = self.question["correct"]
            self.block = True
            self.interval.cancel()
            Clock.schedule_once(self.next_question_callback, 2)

    def update_time(self, dt):
        self.time -= 1
        self.ids.remaining_time.text = "Remaining time: " + str(self.time)
        if self.time == 0:
            self.finalize_answer(None)

    def shuffle_answers(self):
        zipped = list(
            zip(self.question['answers'],
                [self.question['correct'] == i for i in range(len(self.question['answers']))]))
        shuffle(zipped)
        order = [answer for answer, _ in zipped]
        index = [correct for _, correct in zipped].index(True)
        self.question['answers'] = order
        self.question['correct'] = index

    def update_data(self, question):
        self.isCorrect = -1
        self.question = question
        self.shuffle_answers()
        self.ids.main_question.text = self.question['question']
        self.sm.current_screen.ids.firstAnswer.text = self.question['answers'][0]
        self.sm.current_screen.ids.secondAnswer.text = self.question['answers'][1]
        self.sm.current_screen.ids.thirdAnswer.text = self.question['answers'][2]
        self.sm.current_screen.ids.fourthAnswer.text = self.question['answers'][3]
        self.ids.after_answer_label.visible = False
        self.time = self.max_time
        self.ids.remaining_time.text = "Remaining time: " + str(self.time)
        self.ids.user_points.text = "Points: " + str(self.sm.points)
        self.sm.set_time_start()
        self.interval = Clock.schedule_interval(self.update_time, 1)
