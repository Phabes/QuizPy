from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import database_management as database

db = database.create_connection()


class Category(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs["text"]

    def click(self):
        sm.current = "category"
        sm.current_screen.ids.back_button.bind(on_press=self.back_click)
        sm.current_screen.ids.quiz_grid.clear_widgets()
        quiz_list = database.find_quizes(db, self.name)
        for quiz in quiz_list:
            sm.current_screen.ids.quiz_grid.add_widget(Quiz(quiz["_id"], text=quiz["name"]))
        for quiz in quiz_list:
            sm.current_screen.ids.quiz_grid.add_widget(Quiz(quiz["_id"], text=quiz["name"]))
        for quiz in quiz_list:
            sm.current_screen.ids.quiz_grid.add_widget(Quiz(quiz["_id"], text=quiz["name"]))

    def back_click(self, button):
        sm.current = "start"


class Quiz(Button):
    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs["text"]
        self.id = id

    def click(self):
        sm.current = "quiz"
        sm.current_screen.ids.back_button.bind(on_press=self.back_click)
        sm.current_screen.ids.questions.clear_widgets()
        sm.current_screen.ids.questions.add_widget(Button(text="PLAY", size_hint=(1, None), height=400))

    def back_click(self, button):
        sm.current = "category"


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        categories = database.find_categories(db)
        for category in categories:
            self.ids.categoriesGrid.add_widget(Category(text=category["name"]))
        for category in categories:
            self.ids.categoriesGrid.add_widget(Category(text=category["name"]))
        for category in categories:
            self.ids.categoriesGrid.add_widget(Category(text=category["name"]))


class CategoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LoginScreen(Screen):
    pass


class RegisterScreen(Screen):
    pass


sm = ScreenManager()


class QuizPyApp(App):
    def build(self):
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(CategoryScreen(name="category"))
        sm.add_widget(QuizScreen(name="quiz"))
        return sm
        # return QuizPyGame()


if __name__ == '__main__':
    QuizPyApp().run()
