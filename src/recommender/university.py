import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = 'faculties_recommender'
DB_USER = 'root'
DB_PASSWORD = ''
DB_HOST = 'localhost'

db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)


class Faculty:

    def __init__(self, id_faculty=None, name=None):
        self.id = None
        if id_faculty is not None:
            self.id = id_faculty
        self.name = name

    def __str__(self):
        return f"<{str(self.get_id())}, {self.get_name()}>"

    def get_name(self):
        if self.name is not None:
            return self.name
        cursor = db.cursor()
        cursor.execute("SELECT name FROM faculties WHERE id = %s", (self.id,))
        result = cursor.fetchone()
        return result[0]

    def get_id(self):
        if self.id is not None:
            return self.id
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT id FROM faculties WHERE LOWER(name) LIKE %s", (self.name.lower(),))
        result = cursor.fetchone()
        if result is not None:
            self.id = result[0]
        return self.id


