from discord.ext import commands
import requests

class GE:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def GE(self, ctx):
        item = " ".join(ctx.message.content.split(" ")[1:]).lower()
        try:
            sauce = requests.get("http://services.runescape.com/m=itemdb_oldschool/api/catalogue/items.json?category=1&alpha={}".format(item)).json()
            sauce = requests.get("http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={}".format(sauce['items'][0]['id'])).json()
            msg = sauce['item']['name']  + '\n\n'
            msg += "`Current Price:........  " + str(sauce['item']['current']['price']) + " gp`"
            msg += "\n`Today's Trend:........  " + str(sauce['item']['today']['price']).replace(' ','') + " gp`"
            msg += "\n`30 Day Trend:.........  " + str(sauce['item']['day30']['change']) + "`"
            msg += "\n`90 Day Trend:.........  " + str(sauce['item']['day90']['change']) + "`"
            msg += "\n`180 Day Trend:........  " + str(sauce['item']['day180']['change']) + "`"
            await ctx.bot.say(msg)
        except:
            await ctx.bot.say(item + " not found")
            return
        return
    
def setup(bot):
    bot.add_cog(GE(bot))
    print("LOADED")