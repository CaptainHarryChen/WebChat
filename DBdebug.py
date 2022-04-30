import sqlite3


def DB_pwd():
    usersDB = sqlite3.connect("users.db")
    usersDB.execute('''create table if not exists users
    (name primary key not null,
    password varchar(16) not null)
    ''')
    
    '''
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
    '''

    usersDB.commit()


def DB_CaptainChen_friends():
    DB = sqlite3.connect(".\\userdatas\\CaptainChen.db")
    DB.execute('''create table if not exists friends
    (name primary key not null)
    ''')
    DB.execute("insert into friends (name) values('Zhongli')")
    DB.execute("insert into friends (name) values('Xingqiu')")

    DB.commit()


def DB_msglog():
    DB = sqlite3.connect(".\\msglogdb\\CaptainChen.db")
    DB.execute('''create table if not exists Zhongli
    (id int primary key not null,
    username,
    time varchar(14),
    content)
    ''')
    DB.execute("insert into Zhongli (id,username,time,content) values(1,'Zhongli','20220429214800','你好，世界！')")
    DB.execute("insert into Zhongli (id,username,time,content) values(2,'CaptainChen','20220429214800','Hello, World!')")
    DB.execute("insert into Zhongli (id,username,time,content) values(3,'Zhongli','20220429214800','我是钟离。')")
    DB.execute("insert into Zhongli (id,username,time,content) values(4,'CaptainChen','20220429214800','I am CaptainChen')")
    DB.execute("insert into Zhongli (id,username,time,content) values(5,'Zhongli','20220429214800','asdfasdfasdfasda')")
    DB.execute("insert into Zhongli (id,username,time,content) values(6,'Zhongli','20220429214800','你好，世界！')")
    DB.execute("insert into Zhongli (id,username,time,content) values(7,'CaptainChen','20220429214800','Hello, World!')")
    DB.execute("insert into Zhongli (id,username,time,content) values(8,'Zhongli','20220429214800','我是钟离。')")
    DB.execute("insert into Zhongli (id,username,time,content) values(9,'CaptainChen','20220429214800','I am CaptainChen')")
    DB.execute("insert into Zhongli (id,username,time,content) values(10,'Zhongli','20220429214800','asdfasdfa\nsdfasda')")
    DB.execute("insert into Zhongli (id,username,time,content) values(11,'Zhongli','20220429214800','asdfasdfa\nsdfasda')")
    DB.execute("insert into Zhongli (id,username,time,content) values(12,'Zhongli','20220429214800','asdfasdfa\nsdfasda')")
    DB.execute("insert into Zhongli (id,username,time,content) values(13,'Zhongli','20220429214800','asdfasdfa\nsdfasda')")

    DB.commit()


if __name__ == "__main__":
    DB_pwd()
