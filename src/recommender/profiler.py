import math

from src.recommender.university import Faculty
from src.recommender.users_profilation import UsersProfilerDB, Header
from src.utility.table import Row, Header, Table
from src.recommender.faculties_profilation import FacultiesProfilerDB

db_user = UsersProfilerDB(Header(["1", "2", "3", "4", "5", "6", "7", "8", "faculty", "rate"]),
                          "./data/subjective_data.json")
db_faculties = FacultiesProfilerDB()


class UsersProfiler(object):

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(UsersProfiler, self).__new__(self)
        return self.instance

    @staticmethod
    def recommend(interest_array: list[float]) -> list[tuple[Faculty, float]]:
        # save the cosine distance between the user and the faculties
        distances = []
        for row in db_user.rows:
            distance = Row.cosine_distance(row.subjective_features(), Row(interest_array))
            distances.append(distance)
        # sort the faculties by cosine distance
        faculties = db_user.faculties()
        # sort the index of array distance and use it to sort the faculties
        indices = sorted(range(len(distances)), key=lambda x: distances[x])
        faculties = [(faculties[i], UsersProfiler.score_function(distances[i])) for i in indices]
        return faculties

    @staticmethod
    def score_function(distance) -> float:
        """
        The score function is a function that takes the distance between the user and the faculty
        and return a score that is used to sort the faculties.
        """
        return 2 - distance


class FacultiesProfiler(object):

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(FacultiesProfiler, self).__new__(self)
        return self.instance

    @staticmethod
    def recommend(positive_interests: list[str], negative_interests: list[str]) -> list[tuple[Faculty, float]]:

        recommended_faculties = FacultiesProfiler._recommend_helper(positive_interests)
        not_recommended_faculties = FacultiesProfiler._recommend_helper(negative_interests)

        faculties = recommended_faculties
        faculties.extend([(f[0], -f[1]) for f in not_recommended_faculties])

        return faculties

    @staticmethod
    def _recommend_helper(interests) -> list[tuple[Faculty, float]]:
        if len(interests) == 0:
            return []
        # construct the query vector
        interests, query_vector = FacultiesProfiler.query_vector(interests)
        # retrieve the faculties table with all tf-idf of the query words
        interests_table = db_faculties.tf_idf_table(interests)
        # calculate the similarity between the query vector and each faculty
        similarities = []
        for row in interests_table:
            # row[1:] because the first element is the faculty_id
            s = Row.cosine_similarity(row[1:], query_vector)
            similarities.append(Row.cosine_similarity(row[1:], query_vector))

        # if similarity is -inf it means that the faculty has no words in common with the query
        # so we remove it from the list and save a list of tuples with the faculty and the similarity
        faculties = []
        for i, row in enumerate(interests_table):
            if similarities[i] != -math.inf:
                faculties.append((Faculty(row[0]), similarities[i]))

        # sort the faculties by similarity
        # the most similar faculty is the first (high similarity near 1)
        faculties = sorted(faculties, key=lambda x: x[1], reverse=True)
        # apply score function
        for i, faculty in enumerate(faculties):
            faculties[i] = (faculty[0], FacultiesProfiler.score_function(faculty[1]))
        return faculties

    @staticmethod
    def score_function(similarity: float) -> float:
        return 2 * similarity

    @staticmethod
    def words_vector_table(words: list[str]) -> Table:
        header = Header([w for w in words].append("faculty_id"))
        for i, word in enumerate(words):
            db_faculties.tf(word)
        return Table(header)

    @staticmethod
    def query_vector(interests: list[str]) -> tuple[list[str], Row]:

        # find idf for each interest
        idf_interests = {}
        for word in interests:
            idf_interests[word] = db_faculties.idf(word)

        # find tf for each interest
        tf_interests = FacultiesProfiler.tf(interests)

        # find tf-idf for each interest
        tf_idf_interests = {}
        for word in interests:
            tf_idf_interests[word] = tf_interests[word] * idf_interests[word]

        # remove all interests with tf-idf equal to 0 (FIND SIMILAR WORD INSTEAD??)
        tf_idf_interests = {k: v for k, v in tf_idf_interests.items() if v != 0}

        return (list(tf_idf_interests.keys()), Row(tf_idf_interests.values()))

    @staticmethod
    def tf(words):
        tf = {}
        for word in words:
            if word in tf:
                tf[word] += 1
            else:
                tf[word] = 1
        for word in tf:
            tf[word] = tf[word] / len(words)
        return tf
