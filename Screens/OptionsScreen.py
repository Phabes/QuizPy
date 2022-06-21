from kivy.uix.screenmanager import Screen

from DatabaseManagement import connection


class ChooseOptionsScreen(Screen):
    def __init__(self, sm, **kwargs):
        super(ChooseOptionsScreen, self).__init__(**kwargs)
        self.sm = sm
        self.quiz = None

    def check_ranking(self):
        ranking = connection.find_k_best_results(self.sm.current_quiz["_id"], 5)
        self.sm.current = "ranking"
        self.sm.current_screen.update_ranking(ranking, False)

    def start_game(self):
        self.sm.start_quiz(self.quiz)

    def set_quiz(self, quiz):
        self.quiz = quiz
