import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

hashed_password = generate_password_hash("admin123")  
cursor.execute("INSERT INTO users (first_name, last_name, username, password, is_admin) VALUES (?, ?, ?, ?, ?)", 
               ("Admin", "User", "admin", hashed_password, 1))  

conn.commit()
conn.close()



