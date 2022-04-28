from kivy.uix.button import Button


class CategoryButton(Button):
    def __init__(self, sm, connection, **kwargs):
        super(CategoryButton, self).__init__(**kwargs)
        self.sm = sm
        self.connection = connection
        self.name = kwargs["text"]

    def click(self):
        self.sm.transition.direction = "left"
        self.sm.current = "category"
        self.sm.current_screen.set_category_name(self.name)
        self.sm.change_user_label(self.sm.current_screen.ids.user_hello)
        self.sm.current_screen.refresh()
