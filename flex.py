#Author: Nathan Fernandes
#Program: A bot to flex your Runescape stats with
from bs4 import BeautifulSoup
from urllib.request import urlopen


#Gets the text off of the link supplied with BeautifulSoup4. Separates the values by line, and finds the level of the skill provided
#--------------------------------------
#sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=Diet%20Conk")
#soup = BeautifulSoup(sauce,'lxml')
#data = soup.get_text().split("\n")
#book = {'overall':0, 'attack':1, 'defence':2, 'strength':3, 'hitpoints':4, 'ranged':5, 'prayer':6, 'magic':7, 'cooking':8, 'woodcutting':9, 'fletching':10, 'fishing':11, 'firemaking':12, 'crafting':13, 'smithing':14, 'mining':15, 'herblore':16, 'agility':17, 'theiving':18, 'slayer':19, 'farming':20, 'runecrafting':21, 'hunter':22, 'construction':23}
#level = data[book['defence']].split(",")
#print(level[0])
#----------------------------------------
#Test to see if we can detect 404's, and we can
#----------------------------------------
#username = input("Please enter the name of the account you would like to check: ")
#try:
#    sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + username)
#except:
#    print("we must be having a problem")

skillNames = {0:'Overall', 1:'Attack', 2:'Defence', 
            3:'Strength', 4:'Hitpoints', 5:'Ranged', 
            6:'prayer', 7:'magic', 8:'cooking', 
            9:'Woodcutting', 10:'Fletching', 11:'Fishing', 
            12:'Firemaking', 13:'Crafting', 14:'Smithing', 
            15:'Mining', 16:'Herblore', 17:'Agility', 
            18:'Theiving', 19:'Slayer', 20:'Farming', 
            21:'Runecrafting', 22:'Hunter', 23:'Construction'}
book = {'overall':0, 'attack':1, 'defence':2, 
        'strength':3, 'hitpoints':4, 'ranged':5, 
        'prayer':6, 'magic':7, 'cooking':8, 
        'woodcutting':9, 'fletching':10, 'fishing':11, 
        'firemaking':12, 'crafting':13, 'smithing':14, 
        'mining':15, 'herblore':16, 'agility':17, 
        'theiving':18, 'slayer':19, 'farming':20, 
        'runecrafting':21, 'hunter':22, 'construction':23}

unCaller = input("Please enter the name of the account you would like to check: ")
unCaller = unCaller.replace(" ","%20")
try:
    sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + unCaller)
    soup = BeautifulSoup(sauce,'lxml')
    dataCaller = soup.get_text().split("\n")
except:
    print("That is not a valid username")
    exit

unRec = input("Please enter the name of the person to flex on: ")
unRec = unRec.replace(" ","%20")
try:
    ranch = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player="  + unRec)
    stew = BeautifulSoup(ranch,'lxml')
    dataRec = stew.get_text().split("\n")
except:
    print("That is not a valid username")
    exit

unRec = unRec.replace("%20"," ")
skill = input("What skill do you want to compare?")
try:
    lvlCaller = dataCaller[book[skill]].split(",") 
    lvlRec = dataRec[book[skill]].split(",")
    if lvlCaller[1] > lvlRec[1]:
       print("Your %s is better than %s's %s by %d levels" %(skill,unRec,skill,(int(lvlCaller[1]) - int(lvlRec[1]))))
except:
    print("That skill dowes not exist")
    exit



