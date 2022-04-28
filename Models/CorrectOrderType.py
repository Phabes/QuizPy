from kivy.uix.button import Button
from Models.Question import Question

class CorrectOrderType(Question):
    def __init__(self):
        super(CorrectOrderType, self).__init__()
        # self.fun = None
        # self.ids = None
        self.correct = []

    def create_choose_correct_answer(self, ids, answers, fun):
        ids.message_to_user.text += "Click buttons in correct order"
        # self.ids = ids
        # self.fun = fun
        for i in range(len(answers)):
            answer = Button(text=answers[i], size_hint=(1, None), height=100)

            ids.optionsGrid.add_widget(answer)

    def get_correct_answer(self, index, ids, fun, button):
        self.correct.append(index)
        ids.optionsGrid.remove_widget(button)
        if len(self.correct) == 4:
            fun(self.correct)
