import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

class Faculty:

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return self.id

    def name(self):
        cursor = db.cursor()
        cursor.execute("SELECT name FROM faculties WHERE id = %s", (self.id,))
        result = cursor.fetchone()
        return result[0]

