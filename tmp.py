import connection

db = connection.create_connection()

def find_categories():
  collection = db.Categories
  categories = list(collection.find({}))
  return categories

def find_quizes(categoryName):
  collection = db.Quizes
  categories = list(collection.find({"category": categoryName}))
  return categories

categories = find_categories()
print(categories)
# print(categories[0]["name"])
quizes = find_quizes(categories[0]["name"])
print(quizes)
questions = quizes[0]["questions"]
print(questions)
for question in questions:
  print(question)