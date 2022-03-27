from tkinter import Label
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
import connection as C


# class Question()
db = C.create_connection()


def find_categories():
    collection = db.Categories
    categories = list(collection.find({}))
    return categories


def find_quizes(categoryName):
    collection = db.Quizes
    categories = list(collection.find({"category": categoryName}))
    return categories


class QuizPyGame(Widget):
    categories = find_categories()
    # print(categories)
    quizes = find_quizes(categories[0]["name"])
    # print(quizes)
    questions = quizes[0]["questions"]
    print(questions[0]["question"])
    quesion = Label(text=questions[0]["question"])


class QuizPyApp(App):
    def build(self):

        return QuizPyGame()


if __name__ == '__main__':

    QuizPyApp().run()
