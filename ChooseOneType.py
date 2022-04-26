from kivy.uix.button import Button

from Question import Question


class ChooseOneType(Question):
    def __init__(self):
        super(ChooseOneType, self).__init__()
        self.fun = None
        self.correct = None

    def create_choose_correct_answer(self, parent, fun):
        self.fun = fun
        for i in range(4):
            button = Button(text=str(i), size_hint=(1, None), height=100, on_press=self.get_correct_answer)
            parent.add_widget(button)

    def get_correct_answer(self, button):
        self.fun(int(button.text))