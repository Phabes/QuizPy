from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class QuizScreen(Screen):
    def __init__(self, sm, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self.sm = sm
        self.time = 0
        self.interval: Clock.time = None

    # def refresh(self):
    #     self.sm.current_screen.ids.back_button.funbind("on_press", self.sm.back_click, "category")
    #     self.sm.current_screen.ids.back_button.fbind("on_press", self.sm.back_click, "category")
    #     self.sm.current_screen.ids.questions.clear_widgets()
    #     self.sm.current_screen.ids.questions.add_widget(Button(text="PLAY", size_hint=(0.5, 0.5),
    #                                                            on_press=self.start_quiz))
    #
    # def set_quiz(self, quiz):
    #     self.quiz = quiz

    # def start_quiz(self, button):
    #     self.sm.transition.direction = "left"
    #     self.sm.current = "question"
    #     self.sm.current_screen.ids.back_button.fbind("on_press", self.sm.back_click, "quiz")
    #     questions = self.quiz["questions"]
    #     index = 1
    #     self.sm.current_screen.set_question(self.quiz["questions"][index])
    #     answers = questions[index]["answers"]
    #     self.sm.current_screen.ids.mainQuestion.text = questions[index]["question"]
    #     self.sm.current_screen.ids.firstAnswer.text = answers[0]
    #     self.sm.current_screen.ids.secondAnswer.text = answers[1]
    #     self.sm.current_screen.ids.thirdAnswer.text = answers[2]
    #     self.sm.current_screen.ids.fourthAnswer.text = answers[3]

    def update_time(self, dt):
        print(self.time)
        if self.time == 0:
            self.choose_answer(None)
        self.time -= 1
