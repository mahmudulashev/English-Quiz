from flask import Flask, render_template, request, redirect, session
import sqlite3
import uuid
import datetime
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["UPLOAD_FOLDER"] = "static/uploads"


# Home


@app.route("/")
def home():
    return render_template("index.html")


#Register


@app.route("/register", methods=["GET", "POST"])
def register():
    error = ''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        ulanish = sqlite3.connect("users.db")
        cursor = ulanish.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = "Kechirasiz, bu username band."
        else:
            cursor.execute("INSERT INTO users (username, password, first_name, last_name) VALUES (?, ?, ?, ?)", 
                           (username, password, first_name, last_name))
            ulanish.commit()
            cursor.execute("SELECT id, username FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/products")
        
        ulanish.close()

    return render_template("register.html", error=error)


#Login


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ''  

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        ulanish = sqlite3.connect("users.db")
        cursor = ulanish.cursor()
        cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        ulanish.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/products")
        else:
            error = "Login yoki parol noto‘g‘ri!"  

    return render_template("login.html", error=error)


#Logout


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect("/")







# Akkount


@app.route("/account")
def account():
    if "user_id" not in session:
        return redirect("/login")

    ulanish = sqlite3.connect("users.db")
    cursor = ulanish.cursor()
    cursor.execute("SELECT first_name, last_name FROM users WHERE id = ?", 
                   (session["user_id"],))
    user_info = cursor.fetchone()
    cursor.execute("SELECT id, product_name, image_path FROM products WHERE user_id = ?", 
                   (session["user_id"],))
    user_products = cursor.fetchall()
    ulanish.close()

    return render_template(
        "account.html", 
        first_name=user_info[0] 
        if user_info 
        else "",  
        last_name=user_info[1] 
        if user_info 
        else "",  
        products=user_products
    )



if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(host="0.0.0.0", port=5000)
