from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class ChooseOneScreen(Screen):
    question = ObjectProperty(None)
    isCorrect = NumericProperty(-1)

    def __init__(self, sm, **kw):
        super().__init__(**kw)
        self.sm = sm

    def next_question_callback(self,dt):
        self.sm.next_question()

    def choose_answer(self, *args):
        if not self.ids.after_answer_label.visible:
            if args[0] == self.question["correct"]:
                self.ids.after_answer_label.text = "Correct!"
                self.ids.after_answer_label.color = (1, 0, 1, 1)
                self.ids.after_answer_label.visible = True
            else:
                self.ids.after_answer_label.text = "Incorrect!"
                self.ids.after_answer_label.color = (1, 0, 0, 1)
                self.ids.after_answer_label.visible = True
            self.isCorrect = self.question["correct"]
        Clock.schedule_once(self.next_question_callback,2)

    def update_data(self, question):
        self.isCorrect = -1
        self.question = question
        self.ids.main_question.text = question['question']
        self.sm.current_screen.ids.firstAnswer.text = question['answers'][0]
        self.sm.current_screen.ids.secondAnswer.text = question['answers'][1]
        self.sm.current_screen.ids.thirdAnswer.text = question['answers'][2]
        self.sm.current_screen.ids.fourthAnswer.text = question['answers'][3]
        self.ids.after_answer_label.visible = False

