import sqlite3


def DB_pwd():
    usersDB = sqlite3.connect("users.db")
    usersDB.execute('''create table if not exists users
    (name primary key not null,
    password varchar(16) not null)
    ''')
    usersDB.execute(
        "insert into users (name,password) values('CaptainChen','12345')")
    usersDB.execute(
        "insert into users (name,password) values('Zhongli','12345')")
    usersDB.execute(
        "insert into users (name,password) values('Xingqiu','12345')")
    usersDB.execute(
        "insert into users (name,password) values('Xiangling','12345')")
    usersDB.execute(
        "insert into users (name,password) values('Beidou','12345')")
    usersDB.execute(
        "insert into users (name,password) values('Hu Tao','12345')")

    usersDB.commit()


def DB_CaptainChen_friends():
    DB = sqlite3.connect(".\\userdatas\\CaptainChen.db")
    DB.execute('''create table if not exists friends
    (name primary key not null)
    ''')
    DB.execute("insert into friends (name) values('Zhongli')")
    DB.execute("insert into friends (name) values('Xingqiu')")

    DB.commit()


if __name__ == "__main__":
    DB_CaptainChen_friends()
