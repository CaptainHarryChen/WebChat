import os
import sqlite3
import json
from flask import Flask, request, render_template, session, redirect

app = Flask(__name__)


@app.route("/CheckUserName", methods=("POST",))
def CheckUserName():
    user_name = request.form["user_name"]
    usersDB = sqlite3.connect("users.db")
    cur = usersDB.execute(
        "select password from users where name='"+user_name+"'")
    DBpwd = cur.fetchone()
    if DBpwd is None:
        return "1"
    return "0"


@app.route("/GetSelfName", methods=("POST",))
def GetSelfName():
    if "userName" in session.keys():
        return session["userName"]
    return ""


@app.route("/GetFriends", methods=("POST",))
def GetFriends():
    user_name = session["userName"]
    DB = sqlite3.connect(f".\\userdatas\\{user_name}.db")
    cur = DB.execute("select name from friends")
    names = list([{"name":name[0]} for name in cur.fetchall()])

    jsonData = json.dumps(names, sort_keys=True,
                          indent=4, separators=(',', ': '))
    return jsonData


@app.route("/")
def index():
    return render_template("index.html", login_state="1")


@app.route("/login", methods=("POST",))
def login():
    user_name = request.form["user-name"]
    password = request.form["password"]

    usersDB = sqlite3.connect("users.db")
    cur = usersDB.execute(
        "select password from users where name='"+user_name+"'")
    DBpwd = cur.fetchone()
    if DBpwd is None:
        return render_template("index.html", login_state="user-not-exist")
    if password != DBpwd[0]:
        return render_template("index.html", login_state="password-error")
    session["userName"] = user_name
    return redirect("/chat")


@app.route("/regis", methods=("POST",))
def regis():
    user_name = request.form["user-input"]
    pwd = request.form["pwd"]
    pwd_rp = request.form["pwd_rp"]

    usersDB = sqlite3.connect("users.db")
    cur = usersDB.execute(
        f"select password from users where name='{user_name}'")
    DBpwd = cur.fetchone()
    if DBpwd is not None:
        return render_template("register.html", regis_state="user-exist")
    if pwd != pwd_rp:
        return render_template("register.html", regis_state="password-error")
    usersDB.execute(
        f"insert into users (name,password) values('{user_name}','{pwd}')")
    usersDB.commit()
    return app.send_static_file("register_success.html")


@app.route("/register")
def register():
    return render_template("register.html", regis_state="")


@app.route("/chat")
def chat():
    return app.send_static_file("chat.html")


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", port=80, debug=True)
