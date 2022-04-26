from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from Buttons.CreateCategoryButton import CreateCategory
from ChooseOneType import ChooseOneType
from Question import Question


class CreateScreen(Screen):
    def __init__(self, sm, connection, **kwargs):
        super(CreateScreen, self).__init__(**kwargs)
        self.sm = sm
        self.connection = connection
        self.question_types = ["chooseOne", "correctOrder"]
        self.selected_category = None
        self.questions = []
        self.question: Question
        self.stage = 1

    def cancel_creating(self):
        self.selected_category = None
        self.sm.current = "start"

    def get_all_categories(self):
        self.ids.message_to_user.text = "Choose your category"
        categories = self.connection.find_categories()
        for category in categories:
            self.ids.optionsGrid.add_widget(CreateCategory(self.sm, self.connection, self, text=category["name"]))

    def set_category(self, category):
        self.ids.message_to_user.text = "Choose next question type"
        self.selected_category = category
        self.stage = 2
        self.sm.current_screen.ids.optionsGrid.clear_widgets()
        for type in self.question_types:
            self.ids.optionsGrid.add_widget(CreateCategory(self.sm, self.connection, self, text=type))

    def set_next_question_type(self, type):
        if type == "chooseOne":
            self.question = ChooseOneType()
            self.question.type = type
        self.ids.message_to_user.text = "Write your question"
        self.sm.current_screen.ids.optionsGrid.clear_widgets()
        text_input = TextInput(hint_text="Question", size_hint=(1, None), height=400)
        self.ids["question_input"] = text_input
        self.sm.current_screen.ids.optionsGrid.add_widget(text_input)
        self.sm.current_screen.ids.optionsGrid.add_widget(
            Button(text="NEXT", size_hint=(1, None), height=400, on_press=self.set_question))

    def set_question(self, button):
        self.ids.message_to_user.text = "Write your answers"
        question = self.sm.current_screen.ids.question_input.text
        if question != "":
            self.question.question = question
            self.sm.current_screen.ids.optionsGrid.clear_widgets()
            for i in range(1, 5):
                label = Label(text="Answer " + str(i))
                self.sm.current_screen.ids.optionsGrid.add_widget(label)
                text_input = TextInput(hint_text="Answer " + str(i), size_hint=(1, None), height=100)
                self.ids["answer" + str(i)] = text_input
                self.sm.current_screen.ids.optionsGrid.add_widget(text_input)
            self.sm.current_screen.ids.optionsGrid.add_widget(
                Button(text="NEXT", size_hint=(1, None), height=100, on_press=self.set_answers))

    def set_answers(self, button):
        ok = True
        # for i in range(1, 5):
        #     answer = self.sm.current_screen.ids["answer" + str(i)].text
        #     if answer == "":
        #         ok = False
        #         break
        if ok:
            for i in range(1, 5):
                answer = self.sm.current_screen.ids["answer" + str(i)].text
                self.question.answers.append(answer)

        self.sm.current_screen.ids.optionsGrid.clear_widgets()
        self.question.create_choose_correct_answer(self.sm.current_screen.ids.optionsGrid, self.set_correct_answer)

    def set_correct_answer(self, correct):
        self.question.correct = correct
        self.sm.current_screen.ids.optionsGrid.clear_widgets()
