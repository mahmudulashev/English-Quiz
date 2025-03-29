import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    togri INTEGER NOT NULL
)
""")

questions = [
    ("1. Choose the grammatically correct sentence:", "She go to school every day.", "She goes to school every day.", "She going to school every day.", "She went to school every day.", 2),
    ("2. Choose the correct option: I___ my homework right now. ", "do", "does", "am doing", "did", 3),
    ("3. Choose the correct option: They ___ to the park yesterday.", "go", "going", "went", "gone", 3),
    ("4. Choose the correct negative sentence: She ___ like coffee.", "don't", "doesn't", "didn't", "isn't", 2),
    ("5. Choose the correct form of the verb: By the time we arrived, they ___ dinner.", "finish", "finished", "had finished", "finishing", 3),
    ("6. Choose the correct preposition: She is interested ___ learning new languages.", "on", "in", "at", "with", 2),
    ("7. Choose the correct pronoun: This book is not mine, it’s ___.", "yours", "your", "you", "you're", 1),
    ("8. Choose the correct comparative form: This exam is ___ than the last one.", "difficult", "more difficult", "most difficult", "difficultest", 2),
    ("9. Choose the correct preposition: The book is _____ the table.", "in", "on", "at", "by", 2),
    ("10. Choose the correct verb form: She usually ___ to work by bus.", "go", "goes", "going", "gone", 2)
]

cursor.executemany("INSERT INTO questions (question, option1, option2, option3, option4, togri) VALUES (?, ?, ?, ?, ?, ?)", questions)

cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ball INTEGER NOT NULL,
    test_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()
