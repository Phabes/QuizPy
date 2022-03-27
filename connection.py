from pymongo import MongoClient


def create_connection():
    client = MongoClient(
        "mongodb+srv://Admin:qwerty123@quizpy.qok1h.mongodb.net/QuizPy?retryWrites=true&w=majority")
    db = client.QuizPy
    return db


# collection = db.Quizes
#
# cursor = collection.find({})
#
# for document in cursor:
#   print(document)
