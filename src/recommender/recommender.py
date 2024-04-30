from src.recommender.profiler import UsersProfiler, FacultiesProfiler
from src.recommender.query import UserQuery
from src.recommender.university import Faculty


class Recommender(object):

    users_profiler = UsersProfiler()
    faculties_profiler = FacultiesProfiler()

    def __new__(self):
        """
        This system aims to ask the user as fewer questions as possible.
        The user query is a list of answers to questions while the
        interests text is a text that the user write about his interests.
        The recommendation is based on the following steps:\n
        1 - Finding users with similar interests.\n
        2 - Recommend faculties based on the user interests text.\n
        3 - The third step is to recommend faculties using information from
        point 1 and 2.\n

        This approach is based on the assumption that users with similar interests
        have similar preferences, but it's not always true especially
        when the questions are not enough to determine the user preferences.
        The text the user inputs is used to improve the recommendation.
        This idea comes from "4 Ristoranti", it uses the approach "Il mio voto
        può confermare o ribaltare la situazione".
        """
        if not hasattr(self, 'instance'):
            self.instance = super(Recommender, self).__new__(self)

        return self.instance

    @staticmethod
    def recommend(user_query: UserQuery) -> list[Faculty]:
        # get faculties based on user query interests answers
        # these faculties are based on the interest of other users
        subjective_interests_faculties = Recommender.users_profiler.recommend(user_query.user_interests)
        print("Subjective interests faculties:")
        for faculty in subjective_interests_faculties:
            print(faculty[0], faculty[1])
        print()
        # get faculties based on user query interests text
        # these faculties are based only on the interest text of the user
        positive_interests = user_query.positive_interests()
        negative_interests = user_query.negative_interests()
        print("Positive interests:", positive_interests)
        print("Negative interests:", negative_interests)
        print()
        objective_interests_faculties = Recommender.faculties_profiler.recommend(positive_interests, negative_interests)
        print("Objective interests faculties:")
        for faculty in objective_interests_faculties:
            print(faculty[0], faculty[1])
        # merge both faculties lists
        return Recommender._merge(subjective_interests_faculties, objective_interests_faculties)

    @staticmethod
    def _merge(self, subjective_interests_faculties, objective_interests_faculties) -> list[Faculty]:
        return subjective_interests_faculties + objective_interests_faculties
