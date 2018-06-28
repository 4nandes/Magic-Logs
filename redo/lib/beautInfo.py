from bs4 import BeautifulSoup
from urllib.request import urlopen

class beautInfo:
    def userStats(self, userName):
        """
        Returns the statistics from an OSRS account seperated by rows. 

        Order of the rows:
        RANK, LEVEL, XP
        """
        try:
            sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player={}".format(userName))
            soup = BeautifulSoup(sauce,'lxml')
        except:
            return ""
        return soup.get_text().split("\n")
    