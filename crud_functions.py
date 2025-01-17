import sqlite3

def initiate_db():

    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL, 
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)", (username, email, age, 1000,))
    connection.commit()

def is_included(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    check_user = cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))

    if check_user.fetchone() is not None:
        return True
    else:
        return False
def get_all_products():
    connection = sqlite3.connect("prod.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    users = cursor.fetchall()


    connection.commit()
    connection.close()
    return users
