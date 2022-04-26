from kivy.uix.button import Button


class CreateCategory(Button):
    def __init__(self, sm, connection, create_screen, **kwargs):
        super(CreateCategory, self).__init__(**kwargs)
        self.sm = sm
        self.connection = connection
        self.create_screen = create_screen
        self.name = kwargs["text"]

    def click(self):
        if self.create_screen.stage == 1:
            self.create_screen.set_category(self.name)
        elif self.create_screen.stage == 2:
            self.create_screen.set_next_question_type(self.name)
