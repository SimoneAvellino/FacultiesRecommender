# from text.analyzer import TextAnalyzer
#
# text = "I love this product. It is the best product I have ever used. I will definitely buy it again. I hate this product. It is the worst product I have ever used. I will never buy it again. I am not sure if I like this product. It is not the best product I have ever used. I might buy it again. I am not sure if I dislike this product. It is not the worst product I have ever used. I might not buy it again."
#
# # Create a TextAnalyzer object
# analyzer = TextAnalyzer()
# for sub in analyzer.sub_sentences(text):
#     print("----------------------")
#     print(sub)
#     print("Sentiment:", analyzer.sentiment(sub))
#     for word in analyzer.relevant_words(sub):
#         print("-", word)
#         print("Similar words:", analyzer.similar_words(word))
#     print("----------------------")



# from recommender.query import UserQuery
#
# query = UserQuery([1, 2, 3], "i would like to study something that has to do with economy, in particlar I want to have an important impact on the macro economy and I'm also keen on helping people manage thei income")
# print(query.positive_interests())
# print(query.negative_interests())



from src.recommender.recommender import Recommender
from src.recommender.query import UserQuery
from src.recommender.faculties_profilation import FacultiesProfilerDB
# print(FacultiesProfilerDB().tf("mathematic"))
interests = [0.1, 0.2, 0.1, 0.1, 0.2, 0.4, 0.3, 0.1, 0.2, 0.9]
interests_text = "I like mathematics. I am interested in the economy"
query = UserQuery(interests, interests_text)
recommender = Recommender()
print(recommender.recommend(query))
