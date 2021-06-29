import discord
from datetime import *
from time import *
from discord.ext import commands

#For more information about this bot: https://www.youtube.com/watch?v=dQw4w9WgXcQ

key_file  = open("./media/txt/key.txt", "r")
#récuperation du token dans key.txt
default_intents = discord.Intents.default()
default_intents.members = True

#================================================================================
bot = commands.Bot(command_prefix="py!", intents=default_intents, help_command=None)
#================================================================================
bot.load_extension("cogs.command")

bot.load_extension("cogs.event")

bot.load_extension("cogs.help")

#================================================================================
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="In dev"))
    print("main_two.py Ready!")
    print('Logged in as ---->', bot.user)
    print('ID:', bot.user.id)


bot.run(key_file.readline())
key_file.close()

#FIN ============================================================================