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
    userDB.close()
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
    names = list([{"name": name[0]} for name in cur.fetchall()])
    DB.close()

    jsonData = json.dumps(names, sort_keys=True,
                          indent=4, separators=(',', ': '))
    return jsonData


@app.route("/AddFriend", methods=("POST",))
def AddFriend():
    user_name = session["userName"]
    friend_name = request.form["user2"]

    usersDB = sqlite3.connect(".\\users.db")
    cur = usersDB.execute(
        "select name from users where name='"+friend_name+"'")
    if cur.fetchone() is None:
        usersDB.close()
        return "not-exist"
    usersDB.close()

    DB = sqlite3.connect(f".\\userdatas\\{user_name}.db")
    cur = DB.execute(f"select name from friends where name='{friend_name}'")
    if cur.fetchone() is not None:
        DB.close()
        return "exist"
    DB.execute(f"insert into friends (name) values('{friend_name}')")
    DB.commit()
    DB.close()

    DB = sqlite3.connect(f".\\userdatas\\{friend_name}.db")
    cur = DB.execute(f"select name from friends where name='{user_name}'")
    DB.execute(f"insert into friends (name) values('{user_name}')")
    DB.commit()
    DB.close()

    return "success"


@app.route("/GetMsgLog", methods=("POST",))
def GetMsgLog():
    user_name = session["userName"]
    typ = request.form["class"]
    name = request.form["name"]

    DB = sqlite3.connect(f".\\msglogdb\\{typ}.db")
    DB.execute(
        f'''create table if not exists {name} (id int primary key not null,username,time varchar(14),content)''')
    cur = DB.execute(
        f"select id,username,time,content from {name} order by id asc")
    logs = list(cur.fetchall())
    DB.close()

    jsonData = json.dumps(logs, sort_keys=True,
                          indent=4, separators=(',', ': '))
    # print(jsonData)
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
    usersDB.close()
    if DBpwd is None:
        return render_template("index.html", login_state="user-not-exist")
    if password != DBpwd[0]:
        return render_template("index.html", login_state="password-error")
    session["userName"] = user_name
    return redirect("/chat")


@app.route("/logout")
def logout():
    session.pop("userName", None)
    return redirect("/")


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
        usersDB.close()
        return render_template("register.html", regis_state="user-exist")
    if pwd != pwd_rp:
        usersDB.close()
        return render_template("register.html", regis_state="password-error")
    usersDB.execute(
        f"insert into users (name,password) values('{user_name}','{pwd}')")
    usersDB.commit()
    usersDB.close()

    DB = sqlite3.connect(f".\\userdatas\\{user_name}.db")
    DB.execute('''create table if not exists friends
    (name primary key not null)
    ''')
    DB.commit()
    DB.close()

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
