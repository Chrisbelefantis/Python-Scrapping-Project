import sqlite3

conn = sqlite3.connect('testDatabase.db')

c = conn.cursor()


# c.execute('''CREATE TABLE peoples(
#              name TEXT,
#              lastname TEXT,
#              age    INTEGER


#             ) ''')


# c.execute("INSERT INTO peoples VALUES('Chris','Belefantis','20')")


c.execute("select * from peoples")

print(c.fetchall())

conn.commit()

c.close()
