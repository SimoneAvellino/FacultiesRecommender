import mysql.connector

try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='faculties_recommender'
    )

    if db.is_connected():
        print('Connected to the MySQL database')
    else:
        # shut down the program if the connection to the database is not established
        print('Connection to the MySQL database failed')
        exit()
except Exception as e:
    print('Connection to the MySQL database failed')
    exit()