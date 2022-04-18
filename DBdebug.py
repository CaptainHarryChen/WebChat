
usersDB = sqlite3.connect("users.db")
usersDB.execute('''create table if not exists users
(name,
password varchar(16) not null)
''')
usersDB.execute(
    "insert into users (name,password) values('CaptainChen','12345')")
usersDB.commit()
