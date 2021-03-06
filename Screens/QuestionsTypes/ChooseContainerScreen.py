from random import shuffle

from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.draggable import KXDraggableBehavior
from kivy_garden.draggable import KXDroppableBehavior
from kivy.clock import Clock
import asynckivy as ak


class Container(BoxLayout):
    answer_option = NumericProperty(-1)
    text = StringProperty()
    parent_object = ObjectProperty()


class DraggableLabel(KXDraggableBehavior, Label):
    answer_option = NumericProperty(-1)
    text = StringProperty()
    is_correct = NumericProperty(-1)

    pass


class CategoryBox(KXDroppableBehavior, BoxLayout):
    answer_option = NumericProperty(-1)
    parent_object = ObjectProperty()

    def add_widget(self, widget, *args, **kwargs):
        widget.pos_hint = {'x': 0., 'y': 0.}
        return super().add_widget(widget)

    def accepts_drag(self, touch, draggable):
        if self.answer_option == draggable.answer_option:
            self.parent_object.correct_answer_drop()
            draggable.parent.remove_widget(draggable)
            self.add_widget(draggable)
            ak.start(self._dispose_item(draggable))
            return True
        else:
            return False

    async def _dispose_item(self, draggable):
        await ak.animate(draggable, opacity=0, d=.5)
        self.remove_widget(draggable)


class ChooseContainerScreen(Screen):
    question = ObjectProperty(None)
    is_correct = NumericProperty(-1)
    remaining_answers = NumericProperty(-1)

    def __init__(self, sm, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.time = 0
        self.interval: Clock.time = None
        self.max_time = 30

    def next_question_callback(self, dt):
        for box in self.ids.answer_destination_fields.children:
            if len(box.children) != 0:
                element = box.children[0]
                box.clear_widgets()
                self.ids.answer_grid.add_widget(element)
        self.ids.back_button.disabled = False
        self.sm.next_question()

    def correct_answer_drop(self):
        self.remaining_answers -= 1
        if self.remaining_answers == 0:
            self.finalize_answer()

    def finalize_answer(self, *args):
        self.ids.back_button.disabled = True
        if self.time == 0:
            self.ids.after_answer_label.text = "Time's up!"
            self.ids.after_answer_label.color = (1, 0, 0, 1)
            self.ids.after_answer_label.visible = True
            self.interval.cancel()
            Clock.schedule_once(self.next_question_callback, 2)
        else:
            self.sm.set_time_end()
            self.ids.after_answer_label.text = "Correct!"
            self.ids.after_answer_label.color = (1, 0, 1, 1)
            old_points = self.sm.points
            to_add = self.sm.calculate_points(self.max_time)
            self.sm.smooth_change_points(old_points, to_add)
            self.sm.increase_multiply()

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
        self.is_correct = -1
        self.ids.after_answer_label.visible = False
        self.question = question
        self.ids.main_question.text = question['question']
        shuffle(self.question['answers'])
        self.remaining_answers = len(self.question['answers'])
        self.ids.answer_destination_fields.clear_widgets()
        self.ids.answer_grid.clear_widgets()
        for i, text in enumerate(self.question['containers']):
            self.ids.answer_destination_fields.add_widget(
                Container(answer_option=i, text=text, parent_object=self)
            )
        for answer in self.question['answers']:
            self.ids.answer_grid.add_widget(
                DraggableLabel(answer_option=answer['container_id'], text=answer['text'])
            )
        self.time = self.max_time
        self.ids.remaining_time.text = "Remaining time: " + str(self.time)
        self.ids.user_points.text = "Points: " + str(self.sm.points)
        self.sm.set_time_start()
        self.interval = Clock.schedule_interval(self.update_time, 1)
