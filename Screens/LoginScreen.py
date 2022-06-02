from kivy.uix.screenmanager import Screen

from DatabaseManagement import connection


class LoginScreen(Screen):
    def __init__(self, sm, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.sm = sm
        self.l = "qwe"
        self.p = "qwe"

    def login_button_click(self):
        login = self.ids.login_input.text
        password = self.ids.password_input.text
        if not connection.check_if_user_exist(login):
            print("USER", login, "DOESNT EXIST")
        else:
            logged = connection.login_user(login, password)
            if logged:
                self.ids.login_input.text = ""
                self.ids.password_input.text = ""
                self.sm.current = "start"
                self.sm.change_user_label(self.manager.get_screen("start").ids.user_hello)
            else:
                print("ERROR DURING LOGIN")
