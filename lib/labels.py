class labels:
    def __init__(self):
        self.data = ['Overall','Attack','Defence','Strength','Hitpoints',
                    'Ranged','Prayer','Magic','Cooking','Woodcutting',
                    'Fletching','Fishing','Firemaking','Crafting',
                    'Smithing','Mining','Herblore','Agility',
                    'Thieving', 'Slayer', 'Farming','Runecrafting',
                    'Hunter', 'Construction']
        #stores all of the links for the icon images
        self.icons = ['https://vignette.wikia.nocookie.net/2007scape/images/a/a3/Skills_icon.png/revision/latest?cb=20180424021510',
                    'https://vignette.wikia.nocookie.net/2007scape/images/f/fe/Attack_icon.png/revision/latest?cb=20180424002328',
                    'https://vignette.wikia.nocookie.net/2007scape/images/b/b7/Defence_icon.png/revision/latest?cb=20180424010737',
                    'https://vignette.wikia.nocookie.net/2007scape/images/1/1b/Strength_icon.png/revision/latest?cb=20180424005746',
                    'https://vignette.wikia.nocookie.net/2007scape/images/9/96/Hitpoints_icon.png/revision/latest/scale-to-width-down/21?cb=20180424005312',
                    'https://vignette.wikia.nocookie.net/2007scape/images/1/19/Ranged_icon.png/revision/latest/scale-to-width-down/21?cb=20180424010745',
                    'https://vignette.wikia.nocookie.net/2007scape/images/f/f2/Prayer_icon.png/revision/latest/scale-to-width-down/21?cb=20180424010757',
                    'https://vignette.wikia.nocookie.net/2007scape/images/5/5c/Magic_icon.png/revision/latest/scale-to-width-down/21?cb=20180424010803',
                    'https://vignette.wikia.nocookie.net/2007scape/images/d/dc/Cooking_icon.png/revision/latest?cb=20180424010923',
                    'https://vignette.wikia.nocookie.net/2007scape/images/f/f4/Woodcutting_icon.png/revision/latest/scale-to-width-down/17?cb=20180424011002',
                    'https://vignette.wikia.nocookie.net/2007scape/images/9/93/Fletching_icon.png/revision/latest/scale-to-width-down/21?cb=20180424011032',
                    'https://vignette.wikia.nocookie.net/2007scape/images/3/3b/Fishing_icon.png/revision/latest/scale-to-width-down/21?cb=20180424010912',
                    'https://vignette.wikia.nocookie.net/2007scape/images/9/9b/Firemaking_icon.png/revision/latest/scale-to-width-down/21?cb=20180424010933',
                    'https://vignette.wikia.nocookie.net/2007scape/images/c/cf/Crafting_icon.png/revision/latest/scale-to-width-down/21?cb=20180424010841',
                    'https://vignette.wikia.nocookie.net/2007scape/images/d/dd/Smithing_icon.png/revision/latest?cb=20180424010903',
                    'https://vignette.wikia.nocookie.net/2007scape/images/4/4a/Mining_icon.png/revision/latest/scale-to-width-down/21?cb=20180424005736',
                    'https://vignette.wikia.nocookie.net/2007scape/images/0/03/Herblore_icon.png/revision/latest/scale-to-width-down/21?cb=20180424011014',
                    'https://vignette.wikia.nocookie.net/2007scape/images/8/86/Agility_icon.png/revision/latest/scale-to-width-down/16?cb=20180424005727',
                    'https://vignette.wikia.nocookie.net/2007scape/images/4/4a/Thieving_icon.png/revision/latest/scale-to-width-down/21?cb=20180424011020',
                    'https://vignette.wikia.nocookie.net/2007scape/images/2/28/Slayer_icon.png/revision/latest/scale-to-width-down/20?cb=20180424011038',
                    'https://vignette.wikia.nocookie.net/2007scape/images/f/fc/Farming_icon.png/revision/latest/scale-to-width-down/21?cb=20180424011047',
                    'https://vignette.wikia.nocookie.net/2007scape/images/c/c2/Runecrafting_icon.png/revision/latest/scale-to-width-down/21?cb=20180424010809',
                    'https://vignette.wikia.nocookie.net/2007scape/images/d/dd/Hunter_icon.png/revision/latest/scale-to-width-down/20?cb=20180424011103',
                    'https://vignette.wikia.nocookie.net/2007scape/images/f/f6/Construction_icon.png/revision/latest/scale-to-width-down/21?cb=20180424011447']
    
    def index(self,word):
        return self.data.index(word)
    
    def getLabels(self):
        return self.data

    def getIcons(self):
        return self.icons