from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class RankingLabel(BoxLayout):
    position = StringProperty()
    username = StringProperty()
    score = StringProperty()
    date = StringProperty()


class RankingScreen(Screen):
    user_score = NumericProperty(-1)

    def __init__(self, sm, **kw):
        super().__init__(**kw)
        self.sm = sm

    def update_ranking(self, ranking, is_your_score_visible=True):
        self.ids.your_score_label.opacity = 0 if not is_your_score_visible else 1
        self.ids.user_score.opacity = 0 if not is_your_score_visible else 1
        self.ids.your_score_label1.opacity = 0 if not is_your_score_visible else 1

        self.ids.ranking_box.clear_widgets()
        i = 0
        self.ids.ranking_box.add_widget(
            RankingLabel(username="Username", score="Score", position="Position", date="Date"))
        for document in ranking:
            i += 1
            if not hasattr(document["results"], "date"):
                date = ""
            else:
                date = document["results"]["date"]
            self.ids.ranking_box.add_widget(
                RankingLabel(username=document["results"]["username"],
                             score=str(document["results"]["points"]),
                             position=str(i),
                             date=date
                             )
                )

    def set_user_score(self, score):
        self.user_score = score
        self.ids.user_score.text = str(self.user_score)
