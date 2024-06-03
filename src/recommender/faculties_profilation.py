import mysql.connector
from dotenv import load_dotenv
import os
from src.utility.table import Table, Row, Header
from src.db import db

# Load environment variables from .env file
load_dotenv()


class FacultiesProfilerDB:


    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(FacultiesProfilerDB, self).__new__(self)
            self.db = db
            self.cursor = self.db.cursor(buffered=True)
        return self.instance

    def idf(self, word:str):
        self.cursor.execute("SELECT idf FROM keywords WHERE word = %s", (word,))
        result = self.cursor.fetchone()
        if result is None:
            return 0
        return result[0]

    def tf(self, word:str) -> list[tuple[int, str, str, float]]:
        cursor = self.db.cursor()
        cursor.execute("SELECT faculties.id, faculties.code, faculties.name, faculties_keywords.tf FROM faculties_keywords INNER JOIN faculties ON faculties.id = faculties_keywords.faculty_id INNER JOIN keywords ON keywords.id = faculties_keywords.keyword_id WHERE keywords.word = %s", (word,))
        result = cursor.fetchall()
        return result

    def tf_idf_table(self, words: list[str]) -> Table:

        # Costruiamo l'header
        header = Header(["faculty_id"] + words)
        t = Table(header)

        if len(words) == 0:
            return t

        # sort words by length
        words.sort(key=len, reverse=True)
        # consider only up to 50 words (because of the limit of the number of tables that can be joined)
        words = words[:50]

        # Costruiamo dinamicamente la parte della query che corrisponde ai LEFT JOIN per ciascuna parola
        left_join_part = ""
        for i, word in enumerate(words):
            left_join_part += f"""
                LEFT JOIN (
                    SELECT 
                        faculty_id,
                        tf
                    FROM faculties_keywords fk_{i}
                    JOIN keywords k_{i} ON fk_{i}.keyword_id = k_{i}.id AND k_{i}.word = '{word}'
                ) fk_{i} ON f.id = fk_{i}.faculty_id
            """
            if i < len(words) - 1:
                left_join_part += "\n"

        # Costruiamo la query completa
        query = f"""
            SELECT 
                f.id AS id_facolta,
                {', '.join([f"COALESCE(fk_{i}.tf, 0) AS tf_idf_keyword_{i + 1}" for i in range(len(words))])}
            FROM faculties f
            {left_join_part}
        """

        # Eseguiamo la query
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        for row in result:
            t += Row(row)
        return t