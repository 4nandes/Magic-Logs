import sqlite3

class database:
    def __init__(self):
        self.conn = sqlite3.connect('./test.db')
        self.c = self.conn.cursor()
    
    #########
    #Getters#
    #########
    def searchDefault(self, authorID, serverID):
        self.c.execute("SELECT runescapeUsername FROM User WHERE discordID = {} AND serverID = {}".format(authorID,serverID))
        name = self.c.fetchone()
        if name:
            return name[0]
        return ""

    def userList(self, serverID):
        self.c.execute("SELECT DISTINCT runescapeUsername, discordID FROM User WHERE serverID = {}".format(serverID))
        return self.c.fetchall()

    def leaderBoard(self, skillName):
        self.c.execute("SELECT runescapeUsername, {}, {} FROM Statistic GROUP BY runescapeUsername ORDER BY {} DESC".format((skillName+'XP'),(skillName+'Lvl'),(skillName+'XP')))
        return self.c.fetchall()
    
    def lastStatsXP(self, username):
        self.c.execute("SELECT overallXP, attackXP, defenceXP, strengthXP, hitpointsXP, rangedXP, prayerXP, magicXP, cookingXP, woodcuttingXP, fletchingXP, fishingXP, firemakingXP, craftingXP, smithingXP, miningXP, herbloreXP, agilityXP, thievingXP, slayerXP, farmingXP, runecraftingXP, hunterXP, constructionXP FROM Statistic WHERE runescapeUsername = (?) ORDER BY timestamp DESC", (username,))
        return self.c.fetchone()

    def newUser(self, authorID, RSUN, serverID):
        try:
            self.c.execute("INSERT INTO User VALUES(?,?,?)", (authorID, RSUN, serverID))
            self.conn.commit()
            return True
        except:
            return False
    
    #########
    #Setters#
    #########
    def insertStats(self, inserter):
        try:
            self.c.execute("INSERT INTO Statistic VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",inserter)
            self.conn.commit()
            return True
        except:
            return False

