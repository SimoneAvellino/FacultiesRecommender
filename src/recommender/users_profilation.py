from src.recommender.university import Faculty
from src.utility.table import Table, Row, Header
import json
import os


class FeatureRow(Row):

    def faculty(self) -> Faculty:
        """
        Get the faculty from the row
        """
        # FIX: in the subject_data.json the faculty is a string and not an integer
        return Faculty(name=self[-2])

    def rate(self) -> int:
        """
        Get the rate from the row
        """
        return self[-1]


class SubjectiveFeatureRow(FeatureRow):

    def subjective_features(self) -> list[int]:
        """
        Get the subjective features from the row
        """
        return self[0: len(self) - 2]


class UsersProfilerDB(Table):

    def __init__(self, header: Header, path: str):
        super().__init__(header)
        # load the data from the database
        with open(os.path.abspath(path), 'r') as file:
            db = json.load(file)['subjective_data']
        for user_profile in db:
            # create a new row with: answers, faculty and rate
            row = [user_profile[key] for key in user_profile if key != "faculty" and key != "rate"]
            row.append(user_profile["faculty"])
            row.append(user_profile["rate"])
            self += SubjectiveFeatureRow(row)

    def faculties(self) -> list[Faculty]:
        """
        Get the faculties from the table
        """
        faculties = []
        for row in self.rows:
            faculties.append(row.faculty())
        return faculties

    def __str__(self):
        return "Subjective Features Table\n" + super().__str__()

    def __getitem__(self, item) -> FeatureRow:
        return super().__getitem__(item)
