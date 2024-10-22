import sqlite3

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    return conn

def add_user_to_db(user_id: int, name: str):
    conn = get_db_connection()
    conn.execute('INSERT INTO users (id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()

def get_users_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users