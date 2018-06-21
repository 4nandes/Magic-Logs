# FlexBot
FlexBot is a python script that runs a Discord bot. The general purpose of the bot is to retrieve and display OSRS character data.

## Commands:
### $stats
Format: `$stats [OSRS Username]`

Gets and displays the statistics for the OSRS username that was provided, if the username's statistics cannot be found then the bot will notify the user of this.

### $pie
Format: `$pie [OSRS Username]`

Gets and displays the statistics for an OSRS username in pie chart form. It seperates the pie based on XP. If the username's statistics cannot be found then the bot will notify the user of this.

### $flex
Format: `$flex [OSRS Username]`

The most complicated of the commands that the bot currently has. 
### $combat
Format: `$combat [OSRS Username]`

## Sources:
### discord.py
https://github.com/Rapptz/discord.py

This is a wonderful tool that was made by "Danny" Rapptz. It allows for the communication between a bot and Discord.
### Plotly
https://plot.ly/python/

Plotly is a python library that allows the bot to make visually pleasing graph images
### Beautiful Soup
https://www.crummy.com/software/BeautifulSoup/?

Beautiful Soup is a python library that allows the bot to get information off of the OSRS hiscore website.

## Future Plans:
- Grand exchange search function
- Ability to link a username to your Discord ID so that you can just use $stats and it will default to your account
- Daily gain leaderboard automation on Monday - Saturday, Weekly gain leaderboard Sunday
- Fixing the $combat command