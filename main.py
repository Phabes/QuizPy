from kivy.uix.widget import Widget
from kivy.app import App
from Screens.StartScreen import StartScreen
from Screens.CategoryScreen import CategoryScreen
from Screens.QuizScreen import QuizScreen
from Screens.QuestionsTypes.ChooseOneScreen import ChooseOneScreen
from Screens.QuestionsTypes.CorrectOrderScreen import CorrectOrderScreen
from Screens.LoginScreen import LoginScreen
from Screens.RegisterScreen import RegisterScreen
from Screens.CreateScreen import CreateScreen
from Screens.Manager import Manager
from DatabaseManagement import Connection
from kivy.properties import (
    NumericProperty, ObjectProperty
)

connection = Connection()
sm = Manager(connection)



class QuizPyApp(App):
    def build(self):
        sm.add_widget(LoginScreen(sm, connection, name="login"))
        sm.add_widget(RegisterScreen(sm, connection, name="register"))
        sm.add_widget(StartScreen(sm, connection, name="start"))
        sm.add_widget(CategoryScreen(sm, connection, name="category"))
        sm.add_widget(QuizScreen(sm, name="quiz"))
        sm.add_widget(ChooseOneScreen(sm,name="chooseOne"))
        sm.add_widget(CorrectOrderScreen(sm,name="correctOrder"))
        sm.add_widget(CreateScreen(sm, connection, name="create"))
        return sm


if __name__ == '__main__':
    QuizPyApp().run()
