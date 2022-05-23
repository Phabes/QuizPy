from kivy.app import App
from Screens.StartScreen import StartScreen
from Screens.CategoryScreen import CategoryScreen
# from Screens.QuizScreen import QuizScreen
from Screens.QuestionsTypes.ChooseOneScreen import ChooseOneScreen
from Screens.QuestionsTypes.CorrectOrderScreen import CorrectOrderScreen
from Screens.QuestionsTypes.ChooseContainerScreen import ChooseContainerScreen
from Screens.LoginScreen import LoginScreen
from Screens.RegisterScreen import RegisterScreen
from Screens.CreateScreen import CreateScreen
from Screens.Manager import Manager

sm = Manager()


class QuizPyApp(App):
    def build(self):
        sm.add_widget(LoginScreen(sm, name="login"))
        sm.add_widget(RegisterScreen(sm, name="register"))
        sm.add_widget(StartScreen(sm, name="start"))
        sm.add_widget(CategoryScreen(sm, name="category"))
        # sm.add_widget(QuizScreen(sm, name="quiz"))
        sm.add_widget(ChooseOneScreen(sm, name="chooseOne"))
        sm.add_widget(CorrectOrderScreen(sm, name="correctOrder"))
        sm.add_widget(ChooseContainerScreen(sm, name="chooseContainer"))
        sm.add_widget(CreateScreen(sm, name="create"))
        return sm


if __name__ == '__main__':
    QuizPyApp().run()
