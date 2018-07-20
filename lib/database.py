import sqlite3
from lib.labels import labels

class database:
    def __init__(self):
        self.conn = sqlite3.connect('./test.db')
        self.c = self.conn.cursor()
        self.labels = labels().getLabels()
    
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
        self.c.execute("SELECT DISTINCT runescapeUsername, discordID FROM User WHERE serverID = (?)",(serverID,))
        return self.c.fetchall()

    def leaderBoard(self, skillName):
        self.labels.index(skillName.capitalize())    
        self.c.execute("SELECT runescapeUsername, {}XP, {}Lvl FROM Statistic GROUP BY runescapeUsername ORDER BY {}XP DESC".format(skillName,skillName,skillName))
        return self.c.fetchall()
    
    def firstStatsXP(self, username):
        self.c.execute("""SELECT overallXP, attackXP, defenceXP, 
                                strengthXP, hitpointsXP, rangedXP, 
                                prayerXP, magicXP, cookingXP, 
                                woodcuttingXP, fletchingXP, fishingXP, 
                                firemakingXP, craftingXP, smithingXP, 
                                miningXP, herbloreXP, agilityXP, 
                                thievingXP, slayerXP, farmingXP, 
                                runecraftingXP, hunterXP, constructionXP 
                                FROM Statistic 
                                WHERE runescapeUsername = (?) 
                                ORDER BY timestamp ASC""", 
                                (username,))
        return self.c.fetchone()

    def getStatsXP(self, username, timeStamp):
        self.c.execute("""SELECT overallXP, attackXP, defenceXP, 
                                strengthXP, hitpointsXP, rangedXP, 
                                prayerXP, magicXP, cookingXP, 
                                woodcuttingXP, fletchingXP, fishingXP, 
                                firemakingXP, craftingXP, smithingXP, 
                                miningXP, herbloreXP, agilityXP, 
                                thievingXP, slayerXP, farmingXP, 
                                runecraftingXP, hunterXP, constructionXP 
                                FROM Statistic 
                                WHERE runescapeUsername = (?) AND timeStamp = (?) 
                                ORDER BY timestamp DESC""", 
                                (username,timeStamp,))
        return self.c.fetchone()
    
    def highScores(self):
        self.c.execute("SELECT runescapeUsername, {}, {} FROM Statistic GROUP BY runescapeUsername ORDER BY {} DESC".format((self.labels[0]+'XP'),(self.labels[0]+'Lvl'),(self.labels[0]+'Lvl')))
        data = self.c.fetchone()
        msg = "`Overall Lvl" + ("."*(20-len("Overall Lvl"))) + data[0] + (" "*(21-len(data[0]))) +"Lvl:" + str(data[2])  + "`\n"
        for x in range(0,24):
            self.c.execute("SELECT runescapeUsername, {}, {} FROM Statistic GROUP BY runescapeUsername ORDER BY {} DESC".format((self.labels[x]+'XP'),(self.labels[x]+'Lvl'),(self.labels[x]+'XP')))
            data = self.c.fetchone()
            msg += "`{}".format(self.labels[x])
            msg += ("."*(20-len(self.labels[x]))) + data[0] + (" "*(20-len(data[0]))) + " XP:" + "{:,}`\n".format(int(data[1]))
        return msg

    def historyGet(self, username,skill):
        self.c.execute("SELECT fishingXP FROM Statistic WHERE runescapeUsername = (?) ORDER BY timeStamp ASC", (username,))
        return self.c.fetchall()

    def timeStamp(self,username):
        self.c.execute("SELECT timeStamp FROM Statistic WHERE runescapeUsername = (?) ORDER BY timeStamp ASC",(username,))
        return self.c.fetchall()
    
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

    def newUser(self, authorID, RSUN, serverID):
        try:
            self.c.execute("INSERT INTO User VALUES(?,?,?)", (authorID, RSUN, serverID))
            self.conn.commit()
            return True
        except:
            return False
