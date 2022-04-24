from kivy.uix.screenmanager import Screen
from database_management import Connection


class RegisterScreen(Screen):
    def __init__(self, sm, connection: Connection, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.connection = connection

    def register_button_click(self):
        login = self.ids.login_input.text
        password = self.ids.password_input.text
        confirm_password = self.ids.confirm_password_input.text
        if password == confirm_password:
            print("same passwords")
            if not self.connection.check_if_user_exist(login):
                print("user doesnt exist")
                created = self.connection.create_user(login, password)
                if created:
                    self.sm.current = "start"
            else:
                print("user exists")
        else:
            print("different passwords")