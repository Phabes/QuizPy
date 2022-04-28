from kivy.uix.button import Button


class QuizButton(Button):
    def __init__(self, sm, quiz, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs["text"]
        self.sm = sm
        self.quiz = quiz

    def click(self):
        self.sm.transition.direction = "left"
        self.sm.current = "quiz"
        self.sm.current_screen.set_quiz(self.quiz)
        self.sm.change_user_label(self.sm.current_screen.ids.user_hello)
        self.sm.current_screen.refresh()
