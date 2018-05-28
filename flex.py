from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas 
#Gets the information for a person
#################################
sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=Diet%20Conk")
soup = BeautifulSoup(sauce,'lxml')
#file = open("rsdata.txt","w")
#file.write(soup.get_text())
#file.close()

vals = pandas.(soup.get_text(),header=None,sep=",",encoding="ISO-8859-1")

for x in range(0,24):
    print(vals[1][x])

#print(file.read())