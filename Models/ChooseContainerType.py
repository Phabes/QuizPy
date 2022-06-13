from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from .Question import ContainerQuestion
from kivy.properties import ObjectProperty


class ContainerTypeCheckboxes(BoxLayout):
    all_containers_box = ObjectProperty(None)

    def checkbox_choose(self, instance, value, containers_number):
        if value:
            self.all_containers_box.clear_widgets()
            for i in range(containers_number):
                self.all_containers_box.add_widget(NewContainerBox())


class NewContainerBox(BoxLayout):

    def add_answer(self):
        if len(self.ids.answers_box.children) < 3:
            self.ids.answers_box.add_widget(ContainerAnswerType())


class ContainerAnswerType(BoxLayout):

    def remove_answer(self):
        self.parent.remove_widget(self)


class AllContainersBox(BoxLayout):
    pass


class ChooseContainerType(ContainerQuestion):
    def __init__(self):
        super(ChooseContainerType, self).__init__()
