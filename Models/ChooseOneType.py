from kivy.uix.button import Button

from .Question import BasicQuestion


class ChooseOneType(BasicQuestion):
    def __init__(self):
        super(ChooseOneType, self).__init__()
        self.correct = None

    def create_choose_correct_answer(self, ids, answers, fun):
        ids.message_to_user.text += "Click correct button"
        for i in range(len(answers)):
            button = Button(text=answers[i], size_hint=(1, 1))
            button.fbind("on_press", self.get_correct_answer, i, fun)
            ids.options_grid.add_widget(button)

    def get_correct_answer(self, index, fun, button):
        self.correct = index
        fun(index)
