from kivy.uix.screenmanager import Screen
from Buttons.CategoryButton import CategoryButton
from DatabaseManagement import connection


class StartScreen(Screen):
    def __init__(self, sm, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.sm = sm
        self.refresh()

    def refresh(self):
        self.ids.categoriesGrid.clear_widgets()
        categories = connection.find_categories()
        for category in categories:
            self.ids.categoriesGrid.add_widget(CategoryButton(self.sm, text=category["name"]))
