from kivy.uix.button import Button
from Buttons.QuizButton import Quiz


class Category(Button):
    def __init__(self, sm, connection, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.connection = connection
        self.name = kwargs["text"]

    def click(self):
        self.sm.transition.direction = "left"
        self.sm.current = "category"
        self.sm.current_screen.ids.back_button.bind(on_press=self.back_click)
        self.sm.current_screen.ids.quiz_grid.clear_widgets()
        quiz_list = self.connection.find_quizes(self.name)
        for quiz in quiz_list:
            self.sm.current_screen.ids.quiz_grid.add_widget(Quiz(self.sm, quiz, text=quiz["name"]))
        # for quiz in quiz_list:
        #     self.sm.current_screen.ids.quiz_grid.add_widget(Quiz(self.sm, quiz, text=quiz["name"]))
        # for quiz in quiz_list:
        #     self.sm.current_screen.ids.quiz_grid.add_widget(Quiz(self.sm, quiz, text=quiz["name"]))

    def back_click(self, button):
        self.sm.transition.direction = "right"
        self.sm.current = "start"
