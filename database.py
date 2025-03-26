import sqlite3

ulanish = sqlite3.connect("users.db")
cursor = ulanish.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
''')


ulanish.commit()
ulanish.close()