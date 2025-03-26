from flask import Flask, render_template, request, redirect, session
import sqlite3


app = Flask(__name__)
app.secret_key = "supersecretkey"

# Home
@app.route("/")
def home():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
