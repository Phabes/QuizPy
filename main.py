from kivy.app import App
from Screens.StartScreen import StartScreen
from Screens.CategoryScreen import CategoryScreen
from kivy.core.window import Window
from Screens.QuestionsTypes.ChooseOneScreen import ChooseOneScreen
from Screens.QuestionsTypes.CorrectOrderScreen import CorrectOrderScreen
from Screens.QuestionsTypes.ChooseContainerScreen import ChooseContainerScreen
from Screens.LoginScreen import LoginScreen
from Screens.RegisterScreen import RegisterScreen
from Screens.OptionsScreen import ChooseOptionsScreen
from Screens.CreateScreen import CreateScreen
from Screens.Manager import Manager
from Screens.RankingScreen import RankingScreen

sm = Manager()


class QuizPyApp(App):
    def build(self):
        Window.size = (1000,700)
        Window.minimum_width, Window.minimum_height = 600,700
        sm.add_widget(LoginScreen(sm, name="login"))
        sm.add_widget(RegisterScreen(sm, name="register"))
        sm.add_widget(ChooseOptionsScreen(sm, name="chooseOptions"))
        sm.add_widget(StartScreen(sm, name="start"))
        sm.add_widget(CategoryScreen(sm, name="category"))
        sm.add_widget(ChooseOneScreen(sm, name="chooseOne"))
        sm.add_widget(CorrectOrderScreen(sm, name="correctOrder"))
        sm.add_widget(ChooseContainerScreen(sm, name="chooseContainer"))
        sm.add_widget(CreateScreen(sm, name="create"))
        sm.add_widget(RankingScreen(sm, name="ranking"))
        return sm


if __name__ == '__main__':
    QuizPyApp().run()
