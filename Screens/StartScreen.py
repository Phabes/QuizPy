from kivy.uix.screenmanager import Screen
from Buttons.CategoryButton import Category

class StartScreen(Screen):
    def __init__(self, sm, connection, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.connection = connection
        categories = connection.find_categories()
        for category in categories:
            self.ids.categoriesGrid.add_widget(Category(self.sm, self.connection, text=category["name"]))
        for category in categories:
            self.ids.categoriesGrid.add_widget(Category(self.sm, self.connection,text=category["name"]))
        for category in categories:
            self.ids.categoriesGrid.add_widget(Category(self.sm, self.connection,text=category["name"]))
