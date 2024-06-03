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
    def recommend(user_query: UserQuery) -> list[tuple[Faculty, float]]:
        # get faculties based on user query interests answers
        # these faculties are based on the interest of other users
        subjective_interests_faculties = Recommender.users_profiler.recommend(user_query.user_interests)

        # get faculties based on user query interests text
        # these faculties are based only on the interest text of the user
        positive_interests = user_query.positive_interests()
        negative_interests = user_query.negative_interests()

        objective_interests_faculties = Recommender.faculties_profiler.recommend(positive_interests, negative_interests)

        # merge both faculties lists
        return Recommender._merge(subjective_interests_faculties, objective_interests_faculties)

    @staticmethod
    def _merge(subjective_interests_faculties, objective_interests_faculties) -> list[tuple[Faculty, float]]:
        """
        Merge the two lists of faculties. Each list is made up with tuples (faculty, score).\n
        Loop for each tuple in the first list and initialize the dictionary with the faculty and the score\n
        Loop for each tuple in the second list and add the score\n
        -If the score is positive it will have a positive effect on the final score\n
        -If the score is negative it will have a negative effect on the final score\n
        :param subjective_interests_faculties:
        :param objective_interests_faculties:
        :return: list[Faculty]
        """

        # initialize the dictionary with the scores of the faculties in the first list
        # the scores are ordered in descending order
        # a faculty in the subjective list can appear multiple times
        # we only keep the highest score
        faculties_final_scores = {}
        for faculty, score in subjective_interests_faculties:
            faculty_id = faculty.get_id()
            if faculty_id not in faculties_final_scores:
                faculties_final_scores[faculty_id] = score

        # sum the scores of the faculties in the dictionary with the faculty scores in the second list
        for faculty, score in objective_interests_faculties:
            faculty_id = faculty.get_id()
            if faculty_id in faculties_final_scores:
                faculties_final_scores[faculty_id] += score
            else:
                # if the faculty is not in the dictionary it means that the faculty
                # is not in the first list so we add it to the dictionary
                faculties_final_scores[faculty_id] = score


        # sort the faculties by score and append only the faculties

        faculties_ids = sorted(faculties_final_scores.keys(), key=lambda faculty_id: faculties_final_scores[faculty_id], reverse=True)
        return [(Faculty(faculty_id), faculties_final_scores[faculty_id]) for faculty_id in faculties_ids]
        # faculties_ids = sorted(faculties_final_scores.keys(), key=lambda faculty_id: faculties_final_scores[faculty_id], reverse=True)
        # return [Faculty(faculty_id) for faculty_id in faculties_ids]
