from random import shuffle

from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.draggable import KXDraggableBehavior
from kivy_garden.draggable import KXReorderableBehavior
from kivy_garden.draggable import KXDroppableBehavior
from kivy.clock import Clock


class DraggableLabel(KXDraggableBehavior, Label):
    answer_option = NumericProperty(-1)
    pass


class AnswerBox(KXDroppableBehavior, BoxLayout):
    answer_option = NumericProperty(-1)

    def add_widget(self, widget, *args, **kwargs):
        widget.pos_hint = {'x': 0., 'y': 0.}
        return super().add_widget(widget)

    def accepts_drag(self, touch, draggable):
        return not self.children


class ReordableGridLayout(KXReorderableBehavior, GridLayout):
    pass


# class DraggableLabel(DragBehavior,Label):
#         dragging = BooleanProperty(False)
#         original_pos = ListProperty()
#
#         def on_touch_down(self, touch):
#             if self.collide_point(*touch.pos):
#                 print('on touch down')
#                 self.original_pos = self.pos
#             return super().on_touch_down(touch)
#
#         def on_touch_move(self, touch):
#             if touch.grab_current is self:
#                 self.opacity = 0.4
#                 self.dragging = True
#             return super().on_touch_move(touch)
#
#         def on_touch_up(self, touch):
#             if self.dragging:
#                 self.opacity = 1
#                 self.dragging = False
#                 if self.collide_widget(self.parent):
#                     # self.parent.remove_widget(self)
#                     pass
#                 else:
#                     anim = Animation(pos=self.original_pos, duration=1)
#                     anim.start(self)
#             return super().on_touch_up(touch)


class CorrectOrderScreen(Screen):
    question = ObjectProperty(None)
    isCorrect = NumericProperty(-1)
    isFilled = BooleanProperty(False)

    def __init__(self, sm, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.time = 0
        self.interval: Clock.time = None
        self.max_time = 5

    def next_question_callback(self, dt):
        for box in self.ids.answer_destination_fields.children:
            if len(box.children) != 0:
                element = box.children[0]
                box.clear_widgets()
                self.ids.answer_grid.add_widget(element)
        self.sm.next_question()

    def check_fill(self):
        self.isFilled = True
        for box in self.ids.answer_destination_fields.children:
            if len(box.children) == 0:
                self.isFilled = False

        # self.ids.submit.disabled = not self.isFilled

    def choose_answer(self, *args):
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
                    # self.sm.change_points(self.sm.calculate_points(self.max_time))
                    # self.ids.user_points.text = "Points: " + str(self.sm.points)
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
            self.choose_answer(None)

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
        self.ids.firstAnswer.text = zipped[0][0]
        self.ids.firstAnswer.answer_option = zipped[0][1]
        self.ids.secondAnswer.text = zipped[1][0]
        self.ids.secondAnswer.answer_option = zipped[1][1]
        self.ids.thirdAnswer.text = zipped[2][0]
        self.ids.thirdAnswer.answer_option = zipped[2][1]
        self.ids.fourthAnswer.text = zipped[3][0]
        self.ids.fourthAnswer.answer_option = zipped[3][1]
        self.time = self.max_time
        self.ids.remaining_time.text = "Remaining time: " + str(self.time)
        self.ids.user_points.text = "Points: " + str(self.sm.points)
        self.sm.set_time_start()
        self.interval = Clock.schedule_interval(self.update_time, 1)
