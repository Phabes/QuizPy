from kivy.uix.screenmanager import Screen
from Buttons.CategoryButton import CategoryButton


class StartScreen(Screen):
    def __init__(self, sm, connection, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.sm = sm
        self.connection = connection
        self.refresh()

    def refresh(self):
        self.ids.categoriesGrid.clear_widgets()
        categories = self.connection.find_categories()
        for category in categories:
            self.ids.categoriesGrid.add_widget(CategoryButton(self.sm, self.connection, text=category["name"]))
