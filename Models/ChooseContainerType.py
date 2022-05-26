from kivy.uix.button import Button
from Models.Question import Question


class ChooseContainerType(Question):
    def __init__(self):
        super(ChooseContainerType, self).__init__()
        self.correct = []

    def create_choose_correct_answer(self, ids, answers, fun):
        ids.message_to_user.text += "Click buttons in correct order"
        for i in range(len(answers)):
            button = Button(text=answers[i], size_hint=(1, 1))
            button.fbind("on_press", self.get_correct_answer, i, ids, fun)
            ids.optionsGrid.add_widget(button)

    def get_correct_answer(self, index, ids, fun, button):
        self.correct.append(index)
        ids.optionsGrid.remove_widget(button)
        if len(self.correct) == 4:
            fun(self.correct)
