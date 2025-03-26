import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO users (first_name, last_name, username, password, is_admin) VALUES (?, ?, ?, ?, ?)", 
               ("Admin", "User", "admin", "admin123", 1))

conn.commit()
conn.close()

# Username: admin, Password: admin123
