from tkinter import Label
from tkinter.messagebox import QUESTION
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter

from kivy.properties import (
    NumericProperty, ObjectProperty, StringProperty
)

import connection as C

db = C.create_connection()


def find_categories():
    collection = db.Categories
    categories = list(collection.find({}))
    return categories


def find_quizes(categoryName):
    collection = db.Quizes
    categories = list(collection.find({"category": categoryName}))
    return categories


class ChooseOneQuestion(Widget):
    question = ObjectProperty(None)
    isCorrect = NumericProperty(-1)

    def __init__(self, question, **kwargs):
        super(ChooseOneQuestion, self).__init__(**kwargs)
        self.question = question
        answers = question["answers"]
        self.ids.mainQuestion.text = question["question"]
        self.ids.firstAnswer.text = answers[0]
        self.ids.secondAnswer.text = answers[1]
        self.ids.thirdAnswer.text = answers[2]
        self.ids.fourthAnswer.text = answers[3]

    def chooseAnswer(self, *args):
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


class CorrectOrderQuestion(Widget):
    question = ObjectProperty(None)
    isCorrect = NumericProperty(-1)

    def __init__(self, question, **kwargs):
        super(CorrectOrderQuestion, self).__init__(**kwargs)
        self.question = question
        print(question)
        answers = question["answers"]
        self.ids.mainQuestion.text = question["question"]
        self.ids.firstAnswer.text = answers[0]
        self.ids.secondAnswer.text = answers[1]
        self.ids.thirdAnswer.text = answers[2]
        self.ids.fourthAnswer.text = answers[3]

    def chooseAnswer(self, *args):
        if not self.ids.afterAnswerLabel.visible:
            # if args[0] == self.question["correct"]:
            #     self.ids.afterAnswerLabel.text = "Correct!"
            #     self.ids.afterAnswerLabel.color = (1, 0, 1, 1)
            #     self.ids.afterAnswerLabel.visible = True
            # else:
            #     self.ids.afterAnswerLabel.text = "Incorrect!"
            #     self.ids.afterAnswerLabel.color = (1, 0, 0, 1)
            #     self.ids.afterAnswerLabel.visible = True
            # self.isCorrect = self.question["correct"]
            pass


class LoginPanelWidget(Widget):
    pass


class QuizPyApp(App):
    def build(self):
        categories = find_categories()
        quizes = find_quizes(categories[0]["name"])
        questions = quizes[0]["questions"]

        return CorrectOrderQuestion(questions[3])


if __name__ == '__main__':
    QuizPyApp().run()
