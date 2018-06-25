import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

#Removes DB if needed
#c.execute('DROP TABLE Server')

#Makes the DB
c.execute('CREATE TABLE IF NOT EXISTS Server(serverName TEXT, serverID TEXT PRIMARY KEY)')
conn.commit()

#Inserts a server into the DB
c.execute("INSERT INTO Server VALUES('MaxEHP-orDie',457716077984481290))")
conn.commit()

#creates the table for User
c.execute('CREATE TABLE IF NOT EXISTS User(discordID TEXT, runescapeUsername TEXT, serverID TEXT, PRIMARY KEY(discordID, serverID))')
conn.commit()
#c.close()
conn.close()