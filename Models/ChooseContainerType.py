from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from Models.Question import Question
from kivy.properties import ObjectProperty


class ContainerTypeCheckboxes(BoxLayout):
    all_containers_box=ObjectProperty(None)
    def checkbox_choose(self,instance,value,containers_number):
        if value==True:
            self.all_containers_box.clear_widgets()
            for i in range(containers_number):
                self.all_containers_box.add_widget(NewContainerBox())

class NewContainerBox(BoxLayout):

    def add_answer(self):
        if(len(self.ids.answers_box.children)<6):
            self.ids.answers_box.add_widget(ContainerAnswerType())

class ContainerAnswerType(BoxLayout):

    def remove_answer(self):
        self.parent.remove_widget(self)

class AllContainersBox(BoxLayout):
    pass


class ChooseContainerType(Question):
    def __init__(self):
        super(ChooseContainerType, self).__init__()
        self.correct = []

    def create_choose_correct_answer(self, ids, answers, fun):
        ids.message_to_user.text += "Click buttons in correct order"
        for i in range(len(answers)):
            button = Button(text=answers[i], size_hint=(1, 0.2))
            button.fbind("on_press", self.get_correct_answer, i, ids, fun)
            ids.optionsGrid.add_widget(button)

    def get_correct_answer(self, index, ids, fun, button):
        self.correct.append(index)
        ids.optionsGrid.remove_widget(button)
        if len(self.correct) == 4:
            fun(self.correct)
