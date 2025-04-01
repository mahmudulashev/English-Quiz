from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

def is_admin():
    return "user_id" in session and session.get("is_admin") == 1

def conn_databaza():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn






# HOME

@app.route("/")
def index():
    return render_template("index.html")



# REGISTER

@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        password = request.form["password"]

        conn = conn_databaza()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = "This username already taken"
        else:
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)",
                           (first_name, last_name, username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for("testcover"))

        conn.close()
    
    return render_template("register.html", error=error)




# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""  
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            error = "Username or password cannot be empty."
        else:
            conn = conn_databaza()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["first_name"] = user["first_name"]
                session["last_name"] = user["last_name"]
                session["is_admin"] = user["is_admin"]

                if user["is_admin"]:
                    return redirect(url_for("admin_panel"))
                return redirect(url_for("testcover"))
            else:
                error = "Invalid username or password."  

    return render_template("login.html", error=error)  



# TEST

@app.route("/test-cover") 
def testcover():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("test-cover.html")


@app.route("/test", methods=["GET", "POST"])
def test():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = conn_databaza()
    cursor = conn.cursor()

    if "question_index" not in session:
        session["question_index"] = 0
        session["ball"] = 0

    cursor.execute("SELECT * FROM questions ORDER BY id LIMIT 1 OFFSET ?", (session["question_index"],))
    question = cursor.fetchone()
    conn.close()

    if not question:
        return redirect(url_for("result"))

    if request.method == "POST":
        belgilash = request.form.get("option")
        if belgilash and int(belgilash) == question["togri"]:
            session["ball"] += 1

        session["question_index"] += 1
        return redirect(url_for("test"))

    return render_template("test.html", question=question, index=session["question_index"] + 1)



# RESULT

@app.route("/result")
def result():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    ball = session.get("ball", 0)

    if ball <= 3:
        level = "A1"
    elif ball <= 5:
        level = "A2"
    elif ball <= 7:
        level = "B1"
    elif ball <= 9:
        level = "B2"
    else:
        level = "C1"

    conn = conn_databaza()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (user_id, ball, test_date) VALUES (?, ?, ?)", 
                   (user_id, ball, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    session.pop("question_index", None)
    session.pop("ball", None)

    return render_template("result.html", ball=ball, level=level)




# PROFILE

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = conn_databaza()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results WHERE user_id = ? ORDER BY test_date DESC", (user_id,))
    results = cursor.fetchall()
    conn.close()

    return render_template("profile.html", results=results, first_name=session["first_name"], last_name=session["last_name"])




# LEADERBOARD

@app.route("/leaderboard")
def leaderboard():
    conn = conn_databaza()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.first_name, users.last_name, results.ball, results.test_date 
        FROM results 
        JOIN users ON results.user_id = users.id
        ORDER BY results.ball DESC, results.test_date ASC
    """)
    leaders = cursor.fetchall()
    conn.close()

    return render_template("leaderboard.html", leaders=leaders)




# LOGOUT

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("first_name", None)
    session.pop("last_name", None)
    session.pop("is_admin", None)
    return redirect(url_for("login"))



# ADMIN PANEL

@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if not is_admin():  
        return "You do not have admin rights!"

    conn = conn_databaza()
    cursor = conn.cursor()

    if request.method == "POST":
        question = request.form["question"]
        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]
        togri = int(request.form["togri"])

        cursor.execute(
            "INSERT INTO questions (question, option1, option2, option3, option4, togri) VALUES (?, ?, ?, ?, ?, ?)", 
            (question, option1, option2, option3, option4, togri)
        )
        conn.commit()

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()

    return render_template("admin.html", questions=questions)

@app.route("/delete_question/<int:question_id>", methods=["POST"])
def delete_question(question_id):
    if not is_admin():
        return "You do not have admin rights!"

    conn = conn_databaza()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_panel"))

if __name__ == "__main__":
    app.run(debug=True)