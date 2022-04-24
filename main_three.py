# import discord
from discord import Client, Intents, Embed
from datetime import *
from time import *
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

key_file  = open("./media/txt/key.txt", "r")
#récuperation du token dans key.txt
# default_intents = discord.Intents.default()
# default_intents.members = True

# bot = commands.Bot(command_prefix="py!", intents=default_intents, help_command=None)
# slash = SlashCommand(bot)

bot = Client(intents=Intents.default())
slash = SlashCommand(bot)

@slash.slash(name="test")
async def test(ctx: SlashContext):
    embed = discord.Embed(title="embed test")
    await ctx.send(content="test", embeds=[embed])

bot.run(key_file.readline())
key_file.close()