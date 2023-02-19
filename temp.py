import sqlite3
# Open Database
conn = sqlite3.connect('users.db')
# Creation
# conn.execute('''CREATE TABLE Users 
#        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
#           NAME TEXT NOT NULL,
#        EMAIL           TEXT    NOT NULL, 
#        PASS           TEXT    NOT NULL);''')

# print("Created")
# print(conn.execute("select * from users").fetchall())

#insertion 
# conn.execute("""insert into users(email,pass) values
# ('nancypatel@gmail.com','ab1020'),
# ('aumkansara@gmail.com','ac1030'),
# ('keyurjain@gmail.com','ad9020')""")
# conn.commit()

# print(conn.execute("select * from users").fetchall())

# conn.execute('''CREATE TABLE Event_Manager
#        (EID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
#        NAME TEXT NOT NULL,
#        EVENT_NAME TEXT,
#        EMAIL            TEXT    NOT NULL, 
#        PASS           TEXT    NOT NULL,
#        event_code TEXT,
#        photos_link  TEXT
#        );''')
# print("Created")
# conn.execute('drop table users')

# conn.execute('insert into event_manager(NAME,EVENT_NAME,email,pass,event_code) values("Dean-SoCSET","ILLUMINATI","abc@gmail.com","123123123","Ix9tnh")')
# conn.commit()
print(conn.execute("select * from Event_manager").fetchall())
