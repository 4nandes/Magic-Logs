from discord.ext import commands
from discord import embeds
import requests

#add an option that will show all of the details for an item and otherwise just put what the 30 day trend is
class GrandExchange:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True, brief="Lookup item value and high alchemy profit", aliases=['ge','price','Price','value','Value'], help='Format:\n   $GE [Item Name]')
    async def GE(self, ctx):
        # Get the name of the item that they are looking for and store it in "item"
        item = " ".join(ctx.message.content.split(" ")[1:]).lower()
        try:
            sauce = requests.get("http://services.runescape.com/m=itemdb_oldschool/api/catalogue/items.json?category=1&alpha={}".format(item)).json()
            sauce = requests.get("http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={}".format(sauce['items'][0]['id'])).json()
        except IndexError:
            await self.bot.say(item + " not found")
            return
        msg = "**Current Price:**\n" + str(sauce['item']['current']['price']) + " gp\n"
        msg += "**Today's Change:**\n" + str(sauce['item']['today']['price']).replace(' ','') + " gp\n"
        msg += "**30 Day Trend:**\n" + str(sauce['item']['day30']['change']) + "\n"
        if str(sauce['item']['day30']['change']).startswith("+"):
            color = 0x2ecc71
        elif str(sauce['item']['day30']['change']).startswith("-"):
            color = 0xe74c3c
        else:
            color = 0x3498db
        emb = embeds.Embed(title=sauce['item']['name'], description=msg, color=color)
        emb.set_thumbnail(url=sauce['item']['icon'])
        emb.set_footer(text=sauce['item']['description'])
        await self.bot.say(embed=emb)
        return
    
def setup(bot):
    bot.add_cog(GrandExchange(bot))
    print("LOADED")
