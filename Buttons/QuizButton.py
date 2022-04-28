from kivy.uix.button import Button


class QuizButton(Button):
    def __init__(self, sm, quiz, **kwargs):
        super(QuizButton, self).__init__(**kwargs)
        self.name = kwargs["text"]
        print(self.name)
        self.sm = sm
        self.quiz = quiz

    def click(self):
        self.sm.transition.direction = "left"
        self.sm.current = "quiz"
        self.sm.start_quiz(self.quiz)
