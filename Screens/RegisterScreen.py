from kivy.uix.screenmanager import Screen

from DatabaseManagement import connection


class RegisterScreen(Screen):
    def __init__(self, sm, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.sm = sm

    def register_button_click(self):
        login = self.ids.login_input.text
        password = self.ids.password_input.text
        confirm_password = self.ids.confirm_password_input.text
        if password == confirm_password:
            print("same passwords")
            if not connection.check_if_user_exist(login):
                print("user doesnt exist")
                created = connection.create_user(login, password)
                if created:
                    self.ids.login_input.text = ""
                    self.ids.password_input.text = ""
                    self.ids.confirm_password_input.text = ""
                    self.sm.current = "start"
                    self.sm.change_user_label(self.manager.get_screen("start").ids.user_hello)
            else:
                print("user exists")
        else:
            print("different passwords")
