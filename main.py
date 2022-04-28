from kivy.uix.widget import Widget
from kivy.app import App
from Screens.StartScreen import StartScreen
from Screens.CategoryScreen import CategoryScreen
from Screens.QuizScreen import QuizScreen
from Screens.QuestionScreen import QuestionScreen
from Screens.LoginScreen import LoginScreen
from Screens.RegisterScreen import RegisterScreen
from Screens.CreateScreen import CreateScreen
from Screens.Manager import Manager
from DatabaseManagement import Connection
from kivy.properties import (
    NumericProperty, ObjectProperty
)

connection = Connection()
sm = Manager(connection)


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


# class CorrectOrderQuestion(Widget):
#     question = ObjectProperty(None)
#     isCorrect = NumericProperty(-1)
#
#     def __init__(self, question, **kwargs):
#         super(CorrectOrderQuestion, self).__init__(**kwargs)
#         self.question = question
#         answers = question["answers"]
#         self.ids.mainQuestion.text = question["question"]
#         self.ids.firstAnswer.text = answers[0]
#         self.ids.secondAnswer.text = answers[1]
#         self.ids.thirdAnswer.text = answers[2]
#         self.ids.fourthAnswer.text = answers[3]
#
#     def chooseAnswer(self, *args):
#         if not self.ids.afterAnswerLabel.visible:
#             # if args[0] == self.question["correct"]:
#             #     self.ids.afterAnswerLabel.text = "Correct!"
#             #     self.ids.afterAnswerLabel.color = (1, 0, 1, 1)
#             #     self.ids.afterAnswerLabel.visible = True
#             # else:
#             #     self.ids.afterAnswerLabel.text = "Incorrect!"
#             #     self.ids.afterAnswerLabel.color = (1, 0, 0, 1)
#             #     self.ids.afterAnswerLabel.visible = True
#             # self.isCorrect = self.question["correct"]
#             pass


class QuizPyApp(App):
    def build(self):
        sm.add_widget(LoginScreen(sm, connection, name="login"))
        sm.add_widget(RegisterScreen(sm, connection, name="register"))
        sm.add_widget(StartScreen(sm, connection, name="start"))
        sm.add_widget(CategoryScreen(sm, connection, name="category"))
        sm.add_widget(QuizScreen(sm, name="quiz"))
        sm.add_widget(QuestionScreen(name="question"))
        sm.add_widget(CreateScreen(sm, connection ,name="create"))
        return sm


if __name__ == '__main__':
    QuizPyApp().run()
