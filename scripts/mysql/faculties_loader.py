# read objective_data.json and compose store in DB:
# - faculties
# - keywords

import json
from db_config import db

cursor = db.cursor(buffered=True)

with open('../../data/objective_data.json', 'r') as file:
    data = json.load(file)

    # store faculties in DB
    for faculty in data['faculties']:
        print(faculty)
        cursor = db.cursor()
        cursor.execute("INSERT INTO faculties (code, name) VALUES (%s, %s)", (faculty['code'], faculty['name']))
        db.commit()

    # store keywords in DB
    idf = data['idf']
    for keyword in idf.keys():
        cursor = db.cursor()
        cursor.execute("INSERT INTO keywords (word, idf) VALUES (%s, %s)", (keyword, idf[keyword]))
        db.commit()

    # store faculties_keywords in DB
    for faculty in data['faculties']:

        # retrieve faculty ID
        cursor.execute("SELECT id FROM faculties WHERE code = %s", (faculty['code'],))
        faculty_id = cursor.fetchone()[0]  # Ottenere l'ID della facoltà

        for word in faculty['tf'].keys():

            # retrieve keyword ID
            cursor.execute("SELECT id FROM keywords WHERE word = %s", (word,))
            keyword_id = cursor.fetchone()[0]
            print(faculty_id, keyword_id, faculty['tf'][word])
            # Esecuzione della query per inserire i dati nella tabella faculties_keywords
            insert_query = "INSERT INTO faculties_keywords (faculty_id, keyword_id, tf) VALUES (%s, %s, %s)"
            insert_data = (faculty_id, keyword_id, faculty['tf'][word])
            cursor.execute(insert_query, insert_data)

    db.commit()
    cursor.close()