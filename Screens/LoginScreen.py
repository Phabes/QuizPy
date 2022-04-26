import time

from kivy.uix.screenmanager import Screen

from database_management import Connection


class LoginScreen(Screen):
    def __init__(self, sm, connection: Connection, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.connection = connection
        self.l = "qwe"
        self.p = "qwe"


    def login_button_click(self):
        # login = self.ids.login_input.text
        # password = self.ids.password_input.text
        login = self.l
        password = self.p
        if not self.connection.check_if_user_exist(login):
            print("USER", login, "DOESNT EXIST")
        else:
            logged = self.connection.login_user(login, password)
            if logged:
                print("SUCCESS")
                self.ids.login_input.text = ""
                self.ids.password_input.text = ""
                self.sm.current = "start"
                self.sm.change_user_label(self.manager.get_screen("start").ids.user_hello)
            else:
                print("ERROR")
