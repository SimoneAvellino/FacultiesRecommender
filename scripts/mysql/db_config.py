import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='faculties_recommender'
)

if db.is_connected():
    print('Connected to the MySQL database')