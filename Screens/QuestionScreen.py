from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen

class QuestionScreen(Screen):
    question = ObjectProperty(None)
    isCorrect = NumericProperty(-1)

    def choose_answer(self, *args):
        if not self.ids.afterAnswerLabel.visible:
            if args[0] == self.question["correct"]:
                self.ids.afterAnswerLabel.text = "Correct!"
                self.ids.afterAnswerLabel.color = (1, 0, 1, 1)
                self.ids.afterAnswerLabel.visible = True
            else:
                self.ids.afterAnswerLabel.text = "Incorrect!"
                self.ids.afterAnswerLabel.color = (1, 0, 0, 1)
                self.ids.afterAnswerLabel.visible = True
            self.isCorrect = self.question["correct"]

    def set_question(self, question):
        self.question = question