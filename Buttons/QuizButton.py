from kivy.uix.button import Button

class Quiz(Button):
    def __init__(self, sm, quiz, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs["text"]
        self.sm = sm
        self.quiz = quiz

    def click(self):
        self.sm.transition.direction = "left"
        self.sm.current = "quiz"
        self.sm.current_screen.ids.back_button.bind(on_press=self.back_click)
        self.sm.current_screen.ids.questions.clear_widgets()
        self.sm.current_screen.ids.questions.add_widget(Button(text="PLAY", size_hint=(1, None), height=400,
                                                          on_press=self.start_quiz))

    def back_click(self, button):
        self.sm.transition.direction = "right"
        self.sm.current = "category"

    def back_click2(self, button):
        self.sm.transition.direction = "right"
        self.sm.current = "quiz"

    def start_quiz(self, button):
        self.sm.transition.direction = "left"
        self.sm.current = "question"
        self.sm.current_screen.ids.back_button.bind(on_press=self.back_click2)
        questions = self.quiz["questions"]
        index = 1
        self.sm.current_screen.set_question(self.quiz["questions"][index])
        answers = questions[index]["answers"]
        self.sm.current_screen.ids.mainQuestion.text = questions[index]["question"]
        self.sm.current_screen.ids.firstAnswer.text = answers[0]
        self.sm.current_screen.ids.secondAnswer.text = answers[1]
        self.sm.current_screen.ids.thirdAnswer.text = answers[2]
        self.sm.current_screen.ids.fourthAnswer.text = answers[3]
