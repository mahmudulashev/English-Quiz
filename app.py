from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"


def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/register", methods=["GET", "POST"])
def register():
    error_message = ""
    
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            error_message = "Bu username allaqachon mavjud!"
        else:

            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)",
                           (first_name, last_name, username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))

        conn.close()
    
    return render_template("register.html", error_message=error_message)


@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = ""
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            error_message = "Username va parol kiritish shart!"
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user["password"], password):
                session["user"] = user["username"]
                return redirect('/')
            else:
                error_message = "Noto‘g‘ri username yoki parol!"

    return render_template("login.html", error_message=error_message)


@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", username=session["user"])
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
