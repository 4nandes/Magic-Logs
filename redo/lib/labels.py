class labels:
    def __init__(self):
        self.data = ['Overall','Attack','Defence','Strength','Hitpoints',
                    'Ranged','Prayer','Magic','Cooking','Woodcutting',
                    'Fletching','Fishing','Firemaking','Crafting',
                    'Smithing','Mining','Herblore','Agility',
                    'Thieving', 'Slayer', 'Farming','Runecrafting',
                    'Hunter', 'Construction']
    def index(self,word):
        return self.data.index(word)
    
    def getLabels(self):
        return self.data