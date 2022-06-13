from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from Buttons.CreateCategoryButton import CreateCategory
from Models.Question import ContainerAnswer
from DatabaseManagement import connection
from Models.ChooseOneType import ChooseOneType
from Models.CorrectOrderType import CorrectOrderType
from Models.ChooseContainerType import ChooseContainerType, ContainerTypeCheckboxes, AllContainersBox

from Models.Quiz import Quiz
from kivy.uix.boxlayout import BoxLayout


class BasicQuestionCreator(BoxLayout):
    pass


class CreateScreen(Screen):
    def __init__(self, sm, **kwargs):
        super(CreateScreen, self).__init__(**kwargs)
        self.all_containers_box = None
        self.sm = sm
        self.question_types = ["chooseOne", "correctOrder", "chooseContainer"]
        self.quiz = Quiz()
        self.question = None
        self.stage = 1
        self.number_of_answers = 5

    def save_quiz(self, button):
        self.sm.current_screen.ids.options_grid.size_hint = 1, None
        self.quiz.set_username(connection.user)
        if connection.save_quiz(self.quiz):
            self.sm.current = "start"

    def cancel_creating(self):
        self.sm.current_screen.ids.options_grid.cols = 2
        self.quiz = Quiz()
        self.question = None
        self.stage = 1
        self.sm.current = "start"

    def get_all_categories(self):
        self.sm.current_screen.ids.options_grid.clear_widgets()
        self.sm.current_screen.ids.message_to_user.text = "Choose your category"
        categories = connection.find_categories()
        for category in categories:
            self.sm.current_screen.ids.options_grid.add_widget(
                CreateCategory(self.sm, self, text=category["name"]))

    def set_category(self, category):
        self.quiz.category = category
        self.stage = 2
        self.sm.current_screen.ids.options_grid.clear_widgets()
        self.sm.current_screen.ids.options_grid.size_hint = 1, 1

        self.sm.current_screen.ids.message_to_user.text = "Write name of the quiz"
        text_input = TextInput(hint_text="Name", size_hint=(1, 1))
        self.sm.current_screen.ids["quiz_name"] = text_input
        self.sm.current_screen.ids.options_grid.cols = 1
        self.sm.current_screen.ids.options_grid.rows = 2
        self.sm.current_screen.ids.options_grid.add_widget(text_input)
        self.sm.current_screen.ids.options_grid.add_widget(
            Button(text="NEXT", size_hint=(1, 1), on_press=self.set_quiz_name))

    def set_quiz_name(self, button):

        name = self.sm.current_screen.ids.quiz_name.text
        if name != "":
            self.sm.current_screen.ids.options_grid.cols = 2
            self.sm.current_screen.ids.options_grid.rows = None
            self.quiz.name = name
            self.choose_question_type()

    def choose_question_type(self, *args):
        self.sm.current_screen.ids.options_grid.clear_widgets()
        self.sm.current_screen.ids.options_grid.size_hint = 1, None
        self.sm.current_screen.ids.message_to_user.text = "Choose next question type"
        self.stage = 3
        for question_type in self.question_types:
            # self.ids.options_grid.add_widget(CreateCategory(self.sm, connection, self, text=question_type))
            self.ids.options_grid.add_widget(
                Button(text=question_type, size_hint=(1, None), height=400, on_press=self.set_next_question_type))

    def set_next_question_type(self, button):
        question_type = button.text
        if question_type == "chooseOne":
            self.question = ChooseOneType()
        elif question_type == "correctOrder":
            self.question = CorrectOrderType()
        elif question_type == "chooseContainer":
            self.question = ChooseContainerType()
        self.question.type = question_type
        self.stage = 4
        self.sm.current_screen.ids.message_to_user.text = "Write your question"
        self.sm.current_screen.ids.options_grid.clear_widgets()
        self.sm.current_screen.ids.options_grid.size_hint = 1, 1
        text_input = TextInput(hint_text="Question", size_hint=(1, 1))
        self.sm.current_screen.ids["question_input"] = text_input
        self.sm.current_screen.ids.options_grid.add_widget(text_input)
        self.sm.current_screen.ids.options_grid.add_widget(
            Button(text="NEXT", size_hint=(1, 1), on_press=self.set_question))

    def set_question(self, button):
        question = self.sm.current_screen.ids.question_input.text
        if question != "":
            self.sm.current_screen.ids.options_grid.clear_widgets()
            self.sm.current_screen.ids.message_to_user.text = "Write your answers"
            self.question.question = question
            if self.question.type == "correctOrder" or self.question.type == "chooseOne":
                self.stage = 5

                for i in range(1, self.number_of_answers):
                    label = Label(text="Answer " + str(i) + " -->")
                    self.sm.current_screen.ids.options_grid.add_widget(label)
                    text_input = TextInput(hint_text="Answer " + str(i), size_hint=(1, 1))
                    self.ids["answer" + str(i)] = text_input
                    self.sm.current_screen.ids.options_grid.add_widget(text_input)
                self.sm.current_screen.ids.options_grid.add_widget(Label(text="Ready answers? --> "))
                self.sm.current_screen.ids.options_grid.add_widget(
                    Button(text="NEXT", size_hint=(1, 0.2), on_press=self.set_answers_basic))
            elif self.question.type == "chooseContainer":
                self.sm.current_screen.ids.options_grid.size_hint = (1, 1)
                self.sm.current_screen.ids.options_grid.cols = 1
                self.sm.current_screen.ids.options_grid.rows = None
                self.all_containers_box = AllContainersBox()
                self.sm.current_screen.ids.options_grid.add_widget(
                    ContainerTypeCheckboxes(all_containers_box=self.all_containers_box))
                self.sm.current_screen.ids.options_grid.add_widget(self.all_containers_box)
                self.sm.current_screen.ids.options_grid.add_widget(
                    Button(text="NEXT", size_hint=(1, 0.2), on_press=self.set_answers_container))

    def validate_containters_input(self, object):
        var = True
        if isinstance(object, BoxLayout) and not object.children:
            var = False
        for el in object.children:
            if isinstance(el, TextInput):
                el.text = el.text.strip()
                if el.text == "":
                    var = False
            elif isinstance(el, BoxLayout):
                if el.children:
                    if not self.validate_containters_input(el):
                        var = False
                else:
                    var = False

        return var

    def set_answers_container(self, arg):
        if self.validate_containters_input(self.all_containers_box):
            for i in range(len(self.all_containers_box.children) - 1, -1, -1):
                for el in self.all_containers_box.children[i].children:
                    if isinstance(el, TextInput):
                        self.question.containers.append(el.text)
                    elif isinstance(el, BoxLayout):
                        for answerBox in el.children:
                            for answer in answerBox.children:
                                if isinstance(answer, TextInput):
                                    self.question.answers.append(
                                        ContainerAnswer(answer.text, len(self.all_containers_box.children) - i-1))
            self.set_correct_answer(True)
        else:
            print("NOT GIT")

    def set_answers_basic(self, button):
        self.stage = 6
        for i in range(1, self.number_of_answers):
            answer = self.sm.current_screen.ids["answer" + str(i)].text
            self.question.answers.append(answer)
        self.sm.current_screen.ids.message_to_user.text = self.question.question + "\n"
        self.sm.current_screen.ids.options_grid.clear_widgets()
        self.question.create_choose_correct_answer(self.sm.current_screen.ids, self.question.answers,
                                                   self.set_correct_answer)

    def set_correct_answer(self, correct):
        self.quiz.questions.append(self.question)
        self.sm.current_screen.ids.options_grid.clear_widgets()

        self.generate_last_stage()

    def generate_last_stage(self):
        self.question = None
        self.sm.current_screen.ids.message_to_user.text = "Choose your option?"
        self.sm.current_screen.ids.options_grid.cols = 2
        self.sm.current_screen.ids.options_grid.add_widget(
            Button(text="ADD NEW QUESTION", size_hint=(1, 1), on_press=self.choose_question_type))
        self.sm.current_screen.ids.options_grid.add_widget(
            Button(text="SAVE QUIZ", size_hint=(1, 1), on_press=self.save_quiz))
