import os
import sqlite3
from flask import Flask, request, render_template, session, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", login_state="1")


@app.route("/login", methods=("POST",))
def login():
    user_name = request.form["user-name"]
    password = request.form["password"]

    usersDB = sqlite3.connect("users.db")
    cur = usersDB.execute("select password from users where name='"+user_name+"'")
    DBpwd = cur.fetchone()
    if DBpwd is None:
        return render_template("index.html", login_state="user-not-exist")
    if password != DBpwd[0]:
        return render_template("index.html", login_state="password-error")
    session["userName"]=user_name
    return redirect("/chat")


@app.route("/chat")
def chat():
    return app.send_static_file("chat.html")


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", port=80, debug=True)
