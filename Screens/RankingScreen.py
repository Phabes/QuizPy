from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class RankingLabel(BoxLayout):
    position = StringProperty()
    username = StringProperty()
    score = StringProperty()
    #
    # def get_username(self):
    #     print(self.rank["username"])
    #     return self.rank["username"]
    #
    # def get_points(self):
    #     print(self.rank["points"])
    #     return self.rank["points"]
    #
    # def get_position(self):
    #     return str(self.position)


class RankingScreen(Screen):
    user_score = NumericProperty(-1)

    def __init__(self, sm, **kw):
        super().__init__(**kw)
        self.sm = sm

    def update_ranking(self, ranking):
        self.ids.ranking_box.clear_widgets()
        i = 0
        for document in ranking:
            i += 1
            self.ids.ranking_box.add_widget(
                RankingLabel(username=document["results"]["username"], score=str(document["results"]["points"]),
                             position=str(i)))
            print(document["results"])

    def set_user_score(self, score):
        self.user_score = score
        self.ids.user_score.text = str(self.user_score)
