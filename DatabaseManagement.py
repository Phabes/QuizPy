from ConnectionString import path
from pymongo import MongoClient
import bcrypt
import json


class Connection:
    def __init__(self):
        self.db = self.create_connection()
        self.user = None

    def create_connection(self):
        client = MongoClient(path)
        db = client.QuizPy
        return db

    def find_categories(self):
        collection = self.db.Categories
        categories = list(collection.find({}))
        return categories

    def find_quizes(self, categoryName):
        collection = self.db.Quizes
        quiz_list = list(collection.find({"category": categoryName}))
        return quiz_list

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
