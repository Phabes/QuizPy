from kivy.uix.screenmanager import Screen

from Buttons.QuizButton import QuizButton


class CategoryScreen(Screen):
    def __init__(self, sm, connection, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        self.sm = sm
        self.connection = connection
        self.category_name = ""

    def set_category_name(self, category_name):
        self.category_name = category_name

    def refresh(self):
        self.sm.current_screen.ids.back_button.funbind("on_press", self.sm.back_click, "start")
        self.sm.current_screen.ids.back_button.fbind("on_press", self.sm.back_click, "start")
        self.sm.current_screen.ids.quiz_grid.clear_widgets()
        quiz_list = self.connection.find_quizes(self.category_name)
        for quiz in quiz_list:
            self.sm.current_screen.ids.quiz_grid.add_widget(QuizButton(self.sm, quiz, text=quiz["name"]))
