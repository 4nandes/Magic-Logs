from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError

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
        except HTTPError:
            return ""
        return soup.get_text().split("\n")
    