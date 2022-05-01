import os
import sqlite3
import json
from flask import Flask, request, render_template, session, redirect

app = Flask(__name__)

cache_msg_id = {}


@app.route("/CheckUserName", methods=("POST",))
def CheckUserName():
    user_name = request.form["user_name"]
    with sqlite3.connect("users.db") as usersDB:
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

    with sqlite3.connect(f".\\userdatas\\{user_name}.db") as userDB:
        cur = userDB.execute("select name from friends")
        names = []
        with sqlite3.connect(f".\\msglogdb\\{user_name}.db") as msglogDB:
            for name in cur.fetchall():
                name = name[0]
                msglogDB.execute(
                    f"create table if not exists {name} (id int primary key not null,username,time varchar(14),content)")
                id = msglogDB.execute(f"select MAX(id) as max_id from {name}").fetchone()
                id = id[0] if id[0] is not None else 0
                cur2 = msglogDB.execute(
                    f"select time,content from {name} where id={id}")
                cur2 = cur2.fetchone()
                if cur2 is None:
                    time = "0"
                    content = ""
                else:
                    time = cur2[0]
                    content = cur2[1]
                # print(name,time,content)
                cache_msg_id[user_name][name] = id
                names.append((name, time, content, id))

    names.sort(key=lambda x: x[1], reverse=True)
    names = [{"name": name, "time": time if time != "0" else "",
              "content": content[:20], "id": id} for name, time, content, id in names]

    jsonData = json.dumps(names, sort_keys=True,
                          indent=4, separators=(',', ': '))
    # print(jsonData)
    return jsonData


@app.route("/AddFriend", methods=("POST",))
def AddFriend():
    user_name = session["userName"]
    friend_name = request.form["user2"]

    with sqlite3.connect(".\\users.db") as usersDB:
        cur = usersDB.execute(
            "select name from users where name='"+friend_name+"'")
        if cur.fetchone() is None:
            return "not-exist"

    with sqlite3.connect(f".\\userdatas\\{user_name}.db") as DB:
        cur = DB.execute(
            f"select name from friends where name='{friend_name}'")
        if cur.fetchone() is not None:
            return "exist"
        DB.execute(f"insert into friends (name) values('{friend_name}')")
        DB.commit()

    with sqlite3.connect(f".\\userdatas\\{friend_name}.db") as DB:
        cur = DB.execute(f"select name from friends where name='{user_name}'")
        DB.execute(f"insert into friends (name) values('{user_name}')")
        DB.commit()

    cache_msg_id[user_name][friend_name] = 0

    return "success"


@app.route("/GetMsgLog", methods=("POST",))
def GetMsgLog():
    user_name = session["userName"]
    typ = request.form["class"]
    name = request.form["name"]

    with sqlite3.connect(f".\\msglogdb\\{typ}.db") as DB:
        DB.execute(
            f'''create table if not exists {name} (id int primary key not null,username,time varchar(14),content)''')
        cur = DB.execute(
            f"select id,username,time,content from {name} order by id asc")
        logs = list(cur.fetchall())

    jsonData = json.dumps(logs, sort_keys=True,
                          indent=4, separators=(',', ': '))
    # print(jsonData)
    return jsonData


@app.route("/GetNewMsg", methods=("POST",))
def GetNewMsg():
    user_name = session["userName"]
    typ = request.form["class"]
    name = request.form["name"]
    afterID = request.form["id"]

    with sqlite3.connect(f".\\msglogdb\\{typ}.db") as DB:
        DB.execute(
            f'''create table if not exists {name} (id int primary key not null,username,time varchar(14),content)''')
        cur = DB.execute(
            f"select id,username,time,content from {name} where id > {afterID} order by id asc")
        logs = list(cur.fetchall())

    jsonData = json.dumps(logs, sort_keys=True,
                          indent=4, separators=(',', ': '))
    # print(jsonData)
    return jsonData


@app.route("/recieveMsg", methods=("POST",))
def recieveMsg():
    user_name = session["userName"]
    typ = request.form["class"]
    time = request.form["time"]
    name = request.form["name"]
    content = request.form["msg"]

    print(user_name, typ, time, name, content)

    # Add msg to own database or group database
    with sqlite3.connect(f".\\msglogdb\\{typ}.db") as DB:
        DB.execute(
            f'''create table if not exists {name} (id int primary key not null,username,time varchar(14),content)''')
        cur = DB.execute(f"select MAX(id) as max_id from {name}")
        id = cur.fetchone()
        if id[0] is None:
            id = 1
        else:
            id = id[0]+1
        DB.execute(
            f"insert into {name} (id,username,time,content) values({id},'{user_name}','{time}','{content}')")
        DB.commit()
        # print(f"set {name} id to {id}")
        cache_msg_id[user_name][name] = id

    # Add msg the other person's database
    if typ != "Group":
        with sqlite3.connect(f".\\msglogdb\\{name}.db") as DB:
            DB.execute(
                f'''create table if not exists {user_name} (id int primary key not null,username,time varchar(14),content)''')
            cur = DB.execute(f"select MAX(id) as max_id from {user_name}")
            id = cur.fetchone()
            if id[0] is None:
                id = 1
            else:
                id = id[0]+1
            DB.execute(
                f"insert into {user_name} (id,username,time,content) values({id},'{user_name}','{time}','{content}')")
            DB.commit()

    return ""


@app.route("/CheckMsgUpdate", methods=("POST",))
def CheckMsgUpdate():
    user_name = session["userName"]
    saved_id = cache_msg_id[user_name]

    ret = []
    with sqlite3.connect(f".\\msglogdb\\{user_name}.db") as msglogDB:
        for name, id in saved_id.items():
            msglogDB.execute(
                f"create table if not exists {name} (id int primary key not null,username,time varchar(14),content)")
            newid = msglogDB.execute(
                f"select MAX(id) as max_id from {name}").fetchone()
            newid = newid[0] if newid[0] is not None else 0
            #print(user_name, name, saved_id[name], newid)

            if saved_id[name] < newid:
                #print("True")
                cur2 = msglogDB.execute(
                    f"select time,content from {name} where id={newid}")
                cur2 = cur2.fetchone()
                if cur2 is None:
                    time = "0"
                    content = ""
                else:
                    time = cur2[0]
                    content = cur2[1]

                cache_msg_id[user_name][name] = newid
                #print(user_name, name, saved_id[name], newid)
                ret.append((name, time, content, newid))

    ret = [{"name": name, "time": time if time != "0" else "",
            "content": content[:20], "id": id} for name, time, content, id in ret]

    jsonData = json.dumps(ret, sort_keys=True,
                          indent=4, separators=(',', ': '))
    return jsonData


@app.route("/")
def index():
    if session.get("userName") is not None:
        return redirect("/chat")
    return render_template("index.html", login_state="1")


@app.route("/login", methods=("POST",))
def login():
    if session.get("userName") is not None:
        return app.send_static_file("repeat_login.html")

    user_name = request.form["user-name"]
    password = request.form["password"]

    with sqlite3.connect("users.db") as usersDB:
        cur = usersDB.execute(
            "select password from users where name='"+user_name+"'")
        DBpwd = cur.fetchone()

    if DBpwd is None:
        return render_template("index.html", login_state="user-not-exist")
    if password != DBpwd[0]:
        return render_template("index.html", login_state="password-error")
    
    session["userName"] = user_name
    cache_msg_id[user_name] = {}

    return redirect("/chat")


@app.route("/logout")
def logout():
    cache_msg_id.pop(session["userName"])
    session.clear()
    return redirect("/")


@app.route("/regis", methods=("POST",))
def regis():
    user_name = request.form["user-input"]
    pwd = request.form["pwd"]
    pwd_rp = request.form["pwd_rp"]

    with sqlite3.connect("users.db") as usersDB:
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

    with sqlite3.connect(f".\\userdatas\\{user_name}.db") as DB:
        DB.execute('''create table if not exists friends
        (name primary key not null)
        ''')
        DB.commit()

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
