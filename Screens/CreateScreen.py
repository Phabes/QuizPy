from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from Buttons.CreateCategoryButton import CreateCategory
from DatabaseManagement import connection
from Models.ChooseOneType import ChooseOneType
from Models.CorrectOrderType import CorrectOrderType
from Models.Quiz import Quiz


class CreateScreen(Screen):
    def __init__(self, sm, **kwargs):
        super(CreateScreen, self).__init__(**kwargs)
        self.sm = sm
        self.question_types = ["chooseOne", "correctOrder"]
        self.quiz = Quiz()
        self.question = None
        self.stage = 1
        self.number_of_answers = 5

    def save_quiz(self, button):
        print("SAVE")
        self.sm.current_screen.ids.optionsGrid.size_hint = 1, None
        if connection.save_quiz(self.quiz):
            self.sm.current = "start"

    def cancel_creating(self):
        self.quiz = Quiz()
        self.question = None
        self.stage = 1
        self.sm.current = "start"

    def get_all_categories(self):
        self.sm.current_screen.ids.optionsGrid.clear_widgets()
        self.sm.current_screen.ids.message_to_user.text = "Choose your category"
        categories = connection.find_categories()
        for category in categories:
            self.sm.current_screen.ids.optionsGrid.add_widget(
                CreateCategory(self.sm, self, text=category["name"]))

    def set_category(self, category):
        self.quiz.category = category
        self.stage = 2
        self.sm.current_screen.ids.optionsGrid.clear_widgets()
        self.sm.current_screen.ids.optionsGrid.size_hint = 1, 1
        self.sm.current_screen.ids.message_to_user.text = "Write name of the quiz"
        text_input = TextInput(hint_text="Name", size_hint=(1, 1))
        self.sm.current_screen.ids["quiz_name"] = text_input
        self.sm.current_screen.ids.optionsGrid.add_widget(text_input)
        self.sm.current_screen.ids.optionsGrid.add_widget(
            Button(text="NEXT", size_hint=(1, 1), on_press=self.set_quiz_name))

    def set_quiz_name(self, button):
        name = self.sm.current_screen.ids.quiz_name.text
        if name != "":
            self.quiz.name = name
            self.choose_question_type()

    def choose_question_type(self, *args):
        self.sm.current_screen.ids.optionsGrid.clear_widgets()
        self.sm.current_screen.ids.optionsGrid.size_hint = 1, None
        self.sm.current_screen.ids.message_to_user.text = "Choose next question type"
        self.stage = 3
        for question_type in self.question_types:
            # self.ids.optionsGrid.add_widget(CreateCategory(self.sm, connection, self, text=question_type))
            self.ids.optionsGrid.add_widget(
                Button(text=question_type, size_hint=(1, None), height=400, on_press=self.set_next_question_type))

    def set_next_question_type(self, button):
        question_type = button.text
        if question_type == "chooseOne":
            self.question = ChooseOneType()
        elif question_type == "correctOrder":
            self.question = CorrectOrderType()
        self.question.type = question_type
        self.stage = 4
        self.sm.current_screen.ids.message_to_user.text = "Write your question"
        self.sm.current_screen.ids.optionsGrid.clear_widgets()
        self.sm.current_screen.ids.optionsGrid.size_hint = 1, 1
        text_input = TextInput(hint_text="Question", size_hint=(1, 1))
        self.sm.current_screen.ids["question_input"] = text_input
        self.sm.current_screen.ids.optionsGrid.add_widget(text_input)
        self.sm.current_screen.ids.optionsGrid.add_widget(
            Button(text="NEXT", size_hint=(1, 1), on_press=self.set_question))

    def set_question(self, button):
        question = self.sm.current_screen.ids.question_input.text
        if question != "":
            self.sm.current_screen.ids.optionsGrid.clear_widgets()
            self.sm.current_screen.ids.message_to_user.text = "Write your answers"
            self.stage = 5
            self.question.question = question
            for i in range(1, self.number_of_answers):
                label = Label(text="Answer " + str(i) + " -->")
                self.sm.current_screen.ids.optionsGrid.add_widget(label)
                text_input = TextInput(hint_text="Answer " + str(i), size_hint=(1, 1))
                self.ids["answer" + str(i)] = text_input
                self.sm.current_screen.ids.optionsGrid.add_widget(text_input)
            self.sm.current_screen.ids.optionsGrid.add_widget(Label(text="Ready answers? --> "))
            self.sm.current_screen.ids.optionsGrid.add_widget(
                Button(text="NEXT", size_hint=(1, 1), on_press=self.set_answers))

    def set_answers(self, button):
        ok = True
        # for i in range(1, 5):
        #     answer = self.sm.current_screen.ids["answer" + str(i)].text
        #     if answer == "":
        #         ok = False
        #         break
        if ok:
            self.stage = 6
            for i in range(1, self.number_of_answers):
                answer = self.sm.current_screen.ids["answer" + str(i)].text
                self.question.answers.append(answer)
            self.sm.current_screen.ids.message_to_user.text = self.question.question + "\n"
        self.sm.current_screen.ids.optionsGrid.clear_widgets()
        self.question.create_choose_correct_answer(self.sm.current_screen.ids, self.question.answers,
                                                   self.set_correct_answer)

    def set_correct_answer(self, correct):
        self.quiz.questions.append(self.question)
        self.sm.current_screen.ids.optionsGrid.clear_widgets()
        self.generate_last_stage()

    def generate_last_stage(self):
        self.question = None
        self.sm.current_screen.ids.message_to_user.text = "Choose your option?"
        self.sm.current_screen.ids.optionsGrid.add_widget(
            Button(text="ADD NEW QUESTION", size_hint=(1, 1), on_press=self.choose_question_type))
        self.sm.current_screen.ids.optionsGrid.add_widget(
            Button(text="SAVE QUIZ", size_hint=(1, 1), on_press=self.save_quiz))
