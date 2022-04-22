from kivy.uix.screenmanager import Screen
from database_management import Connection


class LoginScreen(Screen):
    def __init__(self, connection: Connection, **kw):
        super().__init__(**kw)
        self.connection = connection

    def login_button_click(self):
        login = self.ids.login_input.text
        password = self.ids.password_input.text
        print("SAS")
        if not self.connection.check_if_user_exist(login):
            pass
        else:
            logged = self.connection.login_user(login, password)
            if logged:
                print("SUCCESS")
            else:
                print("ERROR")