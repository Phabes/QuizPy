from random import shuffle

from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.draggable import KXDraggableBehavior
from kivy_garden.draggable import KXReorderableBehavior
from kivy_garden.draggable import KXDroppableBehavior
from kivy.clock import Clock


class DraggableLabel(KXDraggableBehavior, Label):
    answer_option = NumericProperty(-1)
    text = StringProperty()
    isCorrect = NumericProperty(-1)

    pass


class AnswerBox(KXDroppableBehavior, BoxLayout):
    answer_option = NumericProperty(-1)

    def add_widget(self, widget, *args, **kwargs):
        widget.pos_hint = {'x': 0., 'y': 0.}
        return super().add_widget(widget)

    def accepts_drag(self, touch, draggable):
        return not self.children


class ReordableBoxLayout(KXReorderableBehavior, BoxLayout):
    pass


class CorrectOrderScreen(Screen):
    question = ObjectProperty(None)
    isCorrect = NumericProperty(-1)
    isFilled = BooleanProperty(False)

    def __init__(self, sm, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.time = 0
        self.interval: Clock.time = None
        self.max_time = 30

    def getIsCorrect(self):
        return self.isCorrect

    def next_question_callback(self, dt):
        self.ids.answer_destination_fields.clear_widgets()
        self.ids.answer_grid.clear_widgets()
        self.ids.back_button.disabled = False
        self.sm.next_question()

    def check_fill(self):
        self.isFilled = True
        for box in self.ids.answer_destination_fields.children:
            if len(box.children) == 0:
                self.isFilled = False

        # self.ids.submit.disabled = not self.isFilled

    def finalize_answer(self, *args):
        self.ids.back_button.disabled = True
        if self.time == 0:
            self.ids.after_answer_label.text = "Time's up!"
            self.ids.after_answer_label.color = (1, 0, 0, 1)
            self.ids.after_answer_label.visible = True
            self.ids.submit.disabled = True
            self.interval.cancel()
            Clock.schedule_once(self.next_question_callback, 2)
        else:
            self.check_fill()
            if not self.isFilled:
                self.ids.back_button.disabled = False
                self.ids.submit.background_color = "#f5425d"
            else:
                self.sm.set_time_end()
                valid = True
                for i in self.ids.answer_destination_fields.children:
                    if self.question["correct"][i.answer_option] != i.children[0].answer_option:
                        valid = False
                        break
                if valid:
                    self.ids.after_answer_label.text = "Correct!"
                    self.ids.after_answer_label.color = (1, 0, 1, 1)
                    old_points = self.sm.points
                    to_add = self.sm.calculate_points(self.max_time)
                    self.sm.smooth_change_points(old_points, to_add)
                    self.sm.increase_multiply()
                else:
                    self.ids.after_answer_label.text = "Incorrect!"
                    self.ids.after_answer_label.color = (1, 0, 0, 1)
                self.ids.after_answer_label.visible = True
                self.ids.submit.disabled = True

                self.interval.cancel()
                Clock.schedule_once(self.next_question_callback, 2)

    def update_time(self, dt):
        self.time -= 1
        self.ids.remaining_time.text = "Remaining time: " + str(self.time)
        if self.time == 0:
            self.finalize_answer()

    def shuffle_answers(self):
        zipped = [(answer, index) for index, answer in enumerate(self.question['answers'])]
        shuffle(zipped)
        return zipped

    def update_data(self, question):
        self.isCorrect = -1
        self.ids.after_answer_label.visible = False
        self.question = question
        self.ids.submit.disabled = False
        self.ids.main_question.text = question['question']
        zipped = self.shuffle_answers()
        self.ids.answer_destination_fields.clear_widgets()
        self.ids.answer_grid.clear_widgets()
        for i in range(len(zipped)):
            self.ids.answer_destination_fields.add_widget(
                AnswerBox(answer_option=i)
            )
        for answer in zipped:
            newItem = DraggableLabel(answer_option=answer[1], text=answer[0])
            self.ids.answer_grid.add_widget(newItem)
        self.time = self.max_time
        self.ids.remaining_time.text = "Remaining time: " + str(self.time)
        self.ids.user_points.text = "Points: " + str(self.sm.points)
        self.sm.set_time_start()
        self.interval = Clock.schedule_interval(self.update_time, 1)
