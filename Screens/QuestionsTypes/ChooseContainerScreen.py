from random import shuffle

from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.draggable import KXDraggableBehavior
from kivy_garden.draggable import KXDroppableBehavior
from kivy.clock import Clock


class Container(BoxLayout):
    answer_option = NumericProperty(-1)
    text = StringProperty()
    parentObject = ObjectProperty()



class DraggableLabel(KXDraggableBehavior, Label):
    answer_option = NumericProperty(-1)
    text = StringProperty()
    isCorrect = NumericProperty(-1)

    pass


class CategoryBox(KXDroppableBehavior, BoxLayout):
    answer_option = NumericProperty(-1)
    parentObject = ObjectProperty()
    def add_widget(self, widget, *args, **kwargs):
        widget.pos_hint = {'x': 0., 'y': 0.}
        return super().add_widget(widget)

    def accepts_drag(self, touch, draggable):
        if(self.answer_option == draggable.answer_option):
            self.parentObject.correct_answer_drop()
            return True
        else:
            return False


class ChooseContainerScreen(Screen):
    question = ObjectProperty(None)
    isCorrect = NumericProperty(-1)
    remainingAnswers = NumericProperty(-1)

    def __init__(self, sm, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.time = 0
        self.interval: Clock.time = None
        self.max_time = 2000

    def next_question_callback(self, dt):
        for box in self.ids.answer_destination_fields.children:
            if len(box.children) != 0:
                element = box.children[0]
                box.clear_widgets()
                self.ids.answer_grid.add_widget(element)
        self.sm.next_question()
    def correct_answer_drop(self):
        self.remainingAnswers-=1
        if self.remainingAnswers==0:
            self.finalize_answer()

    def finalize_answer(self,*args):
        print("XD")
        pass
    def update_time(self,dt):
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
        self.ids.main_question.text = question['question']
        shuffle(self.question['answers'])
        self.remainingAnswers = len(self.question['answers'])
        for i, text in enumerate(self.question['containers']):
            self.ids.answer_destination_fields.add_widget(
                Container(answer_option=i, text=text,parentObject=self)
            )
        for answer in self.question['answers']:
            print(answer)
            self.ids.answer_grid.add_widget(
                DraggableLabel(answer_option=answer['container_id'], text=answer['text'])
            )
        self.time = self.max_time
        self.ids.remaining_time.text = "Remaining time: " + str(self.time)
        self.ids.user_points.text = "Points: " + str(self.sm.points)
        self.sm.set_time_start()
        self.interval = Clock.schedule_interval(self.update_time, 1)
