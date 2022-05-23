from kivy.uix.button import Button


class QuizButton(Button):
    def __init__(self, sm, quiz, **kwargs):
        super(QuizButton, self).__init__(**kwargs)
        self.name = kwargs["text"]
        self.sm = sm
        self.quiz = quiz

    def click(self):
        self.sm.transition.direction = "left"
        # self.sm.current = "quiz"
        # self.sm.change_user_label(self.sm.current_screen.ids.user_hello)
        self.sm.change_user_label(self.sm.get_screen("chooseOne").ids.user_hello)
        self.sm.change_user_label(self.sm.get_screen("correctOrder").ids.user_hello)
        # ranking = sorted(self.quiz["results"], key=lambda x: x["points"], reverse=True)
        # print(ranking)
        self.sm.start_quiz(self.quiz)
