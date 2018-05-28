from bs4 import BeautifulSoup
from urllib.request import urlopen

#Gets the information for a person
#################################
sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=Diet%20Conk")
soup = BeautifulSoup(sauce,'lxml')
#file = open("rsdata.txt","w")
#file.write(soup.get_text())
#file.close()
data = soup.get_text().split("\n")

book = {'overall':0, 'attack':1, 'defence':2, 'strength':3, 'hitpoints':4, 'ranged':5, 'prayer':6, 'magic':7, 'cooking':8, 'woodcutting':9, 'fletching':10, 'fishing':11, 'firemaking':12, 'crafting':13, 'smithing':14, 'mining':15, 'herblore':16, 'agility':17, 'theiving':18, 'slayer':19, 'farming':20, 'runecrafting':21, 'hunter':22, 'construction':23}

level = data[book['defence']].split(",")
print(level[0])
#print(soup.get_text())
#print(file.read())