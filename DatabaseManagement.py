from ConnectionString import path
from pymongo import MongoClient
import bcrypt
import json


class Connection:
    def __init__(self):
        self.db = None
        self.user = None

    def create_connection(self):
        client = MongoClient(path)
        db = client.QuizPy
        self.db = db

    def find_categories(self):
        collection = self.db.Categories
        categories = list(collection.find({}))
        return categories

    def find_quizes(self, categoryName):
        collection = self.db.Quizes
        quiz_list = list(collection.find({"category": categoryName}, {"results": 0}))
        return quiz_list

    def find_k_best_results(self, quiz_id, k):
        collection = self.db.Quizes
        ranking = list(collection.aggregate([
            {"$match": {
                "_id": quiz_id
            }},
            {"$unwind": "$results"},
            {"$sort": {
                "results.points": -1
            }},
            {"$project": {
                "_id": 0,
                "results": 1
            }},
            {"$limit": k}
        ]))
        return ranking

    def check_if_user_exist(self, username):
        collection = self.db.Users
        if collection.count_documents({"username": username}) == 0:
            return False
        return True

    def create_user(self, username, password):
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        x = self.db.Users.insert_one({"username": username, "password": hashed})
        if x:
            self.user = username
            return True
        self.user = None
        return False

    def login_user(self, username, password):
        print(username, password)
        user = self.db.Users.find_one({"username": username})
        if user:
            if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
                self.user = username
                return True
        self.user = None
        return False

    def logout_user(self):
        self.user = None
        return True

    def save_quiz(self, quiz):
        # quiz_obj = json.dumps(quiz.__dict__)
        quiz_obj = quiz.toJSON()
        quiz_obj = json.loads(quiz_obj)
        a = self.db.Quizes.insert_one(quiz_obj)
        if a:
            return True
        return False

    def save_score(self, quiz_id, points):
        new_result = {"username": self.user, "points": points}
        self.db.Quizes.update_one({"_id": quiz_id}, {"$push": {"results": new_result}})


connection = Connection()
connection.create_connection()
