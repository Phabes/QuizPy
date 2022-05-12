from kivy.uix.screenmanager import Screen

from Buttons.QuizButton import QuizButton
from DatabaseManagement import connection


class CategoryScreen(Screen):
    def __init__(self, sm, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        self.sm = sm
        self.category_name = ""
        self.quiz_list = []
        self.render = []
        self.ids.my_filter.bind(active=self.filter)
        self.ids.name_filter.bind(text=self.filter)

    def filter(self, instance, value):
        self.ids.quiz_grid.clear_widgets()
        checkbox_active = self.ids.my_filter.active
        quiz_name = self.ids.name_filter.text.lower()
        self.render = [False for _ in range(len(self.quiz_list))]

        for i in range(len(self.quiz_list)):
            quiz = self.quiz_list[i]
            if quiz_name == "":
                if checkbox_active:
                    if quiz["username"] == connection.user:
                        self.render[i] = True
                else:
                    self.render[i] = True
            else:
                if checkbox_active:
                    if quiz["username"] == connection.user and quiz["name"].lower().startswith(quiz_name):
                        self.render[i] = True
                else:
                    if quiz["name"].lower().startswith(quiz_name):
                        self.render[i] = True
        for i in range(len(self.quiz_list)):
            if self.render[i]:
                quiz = self.quiz_list[i]
                self.sm.current_screen.ids.quiz_grid.add_widget(QuizButton(self.sm, quiz, text=quiz["name"]))

    def set_category_name(self, category_name):
        self.category_name = category_name

    def refresh(self):
        self.sm.current_screen.ids.back_button.funbind("on_press", self.sm.back_click, "start")
        self.sm.current_screen.ids.back_button.fbind("on_press", self.sm.back_click, "start")
        self.ids.my_filter.active = False
        self.ids.name_filter.text = ""
        self.sm.current_screen.ids.quiz_grid.clear_widgets()
        self.quiz_list = connection.find_quizes(self.category_name)
        self.render = [True for _ in range(len(self.quiz_list))]
        for quiz in self.quiz_list:
            self.sm.current_screen.ids.quiz_grid.add_widget(QuizButton(self.sm, quiz, text=quiz["name"]))
