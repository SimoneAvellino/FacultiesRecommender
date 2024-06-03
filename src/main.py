from src.recommender.recommender import Recommender
from src.recommender.query import UserQuery

recommender = Recommender()

while True:

    interests_text = input("Write your interests: ")
    if interests_text == "exit":
        break

    query = UserQuery([], interests_text)
    query.ask_quetions()

    faculties = recommender.recommend(query)
    print("\nTop faculties: ")
    for faculty in faculties[:8]:
        print(faculty.name())
