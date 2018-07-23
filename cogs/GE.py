from discord.ext import commands
from discord import embeds
import requests
import pandas as pd


#add an option that will show all of the details for an item and otherwise just put what the 30 day trend is
class GE:
    def __init__(self, bot):
        self.bot = bot
        self.knownOffenders = ['cannonball', 'white berries',
                                'cowhide', 'maple sapling',"greenman's ale",
                                "greenman's ale(m)",'cactus spine','runite ore',
                                'law rune', 'nature rune', 'runite bar',
                                'shark']

    @commands.command(pass_context=True)
    async def test(self,ctx):
        await self.bot.say("Deez Nuts")
        return
        
    @commands.command(pass_context=True, help="Lol jack sux", brief="aylmao")
    async def GE(self, ctx):
        item = " ".join(ctx.message.content.split(" ")[1:]).lower()
        if any(item in s for s in self.knownOffenders):
            tableLoc = 1
        else:
            tableLoc = 0 
        try:
            sauce = requests.get("http://services.runescape.com/m=itemdb_oldschool/api/catalogue/items.json?category=1&alpha={}".format(item)).json()
            sauce = requests.get("http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={}".format(sauce['items'][0]['id'])).json()
            msg = "**Current Price:**\n" + str(sauce['item']['current']['price']) + " gp\n"
            msg += "**Today's Change:**\n" + str(sauce['item']['today']['price']).replace(' ','') + " gp\n"
            msg += "**30 Day Trend:**\n" + str(sauce['item']['day30']['change']) + "\n"
            if str(sauce['item']['day30']['change']).startswith("+"):
                color = 0x2ecc71
            elif str(sauce['item']['day30']['change']).startswith("-"):
                color = 0xe74c3c
            else:
                color = 0x3498db
            try:
                dfs = pd.read_html('http://oldschoolrunescape.wikia.com/wiki/{}'.format(item.replace(" ","_")))
                natRune = requests.get("http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=561").json()
                if str(sauce['item']['current']['price']).endswith('m'):
                    itemValue = float(str(sauce['item']['current']['price'])[:-1]) * 1000000
                elif str(sauce['item']['current']['price']).endswith('k'):
                    itemValue = float(str(sauce['item']['current']['price'])[:-1]) * 1000
                else:
                    itemValue = int(str(sauce['item']['current']['price']).replace(",",""))
                profit = int(dfs[tableLoc][1][7][:-5].replace(",","")) - (itemValue + int(natRune['item']['current']['price']))
                msg += "**High Alchemy Profit:**\n"  
                if profit > 0:
                    msg += "+" + "{:,}".format(profit) + " gp          :white_check_mark:"
                else:
                    msg += "{:,}".format(profit) + " gp          :no_entry_sign:"
            except ValueError:
                msg += "**High Alch 404**" 
            emb = embeds.Embed(title=sauce['item']['name'], description=msg, color=color)
            emb.set_thumbnail(url=sauce['item']['icon'])
            emb.set_footer(text=sauce['item']['description'])
            await self.bot.say(embed=emb)
        except KeyError as exc:
            await self.bot.say("Youve found an item with a floating table above it. Letting Dev know to add it to the whitelist...\n\n <@182320411718057993>\nEROR RAISED: {}".format(exc))
            return
        except IndexError:
            await self.bot.say(item + " not found")
            return
        return
    
def setup(bot):
    bot.add_cog(GE(bot))
    print("LOADED")