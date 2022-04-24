import discord
import random
from datetime import *
from time import *
from discord.ext import commands


#================================================================================
#https://discordpy.readthedocs.io/en/latest/api.html
#================================================================================
key_file  = open("./media/txt/key.txt", "r")
#récuperation du token dans key.txt
default_intents = discord.Intents.default()
default_intents.members = True


#client = discord.Client(intents=default_intents)
client = commands.Bot(command_prefix= 'py!')

#================================================================================
def get_dictionary_word_list():
    with open('./media/txt/bad_word.txt') as f:
        return f.read().split()

word_list = get_dictionary_word_list()

#================================================================================
#Lancement 
@client.event
async def on_ready():
    print("BOT OK")

#================================================================================
#event lors d'un message
@client.event
async def on_message(message: discord.Message):

    insulte = [f"Je t'aime pas {message.author.mention}",f"Tu es beau {message.author.mention}"]

    if message.content.lower() == "ping":
        await message.channel.send("pong")

    if message.content.lower() == "tg":
        await message.channel.send(file=discord.File("./media/audio/hirm_tg.wav"))

    if message.content.lower() == "ching":
        await message.channel.send(f"chong {message.author.mention}")
    if message.author.id == 235096745028091904:
        nb = random.randint(0, 100)
        nb_2 = random.randint(0, 1)
        if nb > 99:
            await message.channel.send(insulte[nb_2]) 

    contains_bad_word = False
    for k in word_list:
        if k in message.content.lower() and message.author.id != 856282502486687745:
            contains_bad_word = True

    if contains_bad_word:
        await message.channel.send(f"{message.author.mention}",file=discord.File("./media/img/derapage.png"))
    await client.process_commands(message)



#================================================================================
#commande pour le bot
@client.command()
async def ping(ctx):
    await ctx.send('Pong with command')

@client.command(name="heure")
async def hour(ctx):
    await ctx.send(f"{ctx.author.mention}\n> Il est {datetime.now().strftime('%Hh%M')}")

@client.event
async def on_member_join(member):
    channel_test:discord.TextChannel = client.get_channel(856289267348799488)
    await channel_test.send(content=f"Bienvenue {member.mention}")

client.run(key_file.readline())
key_file.close()

#================================================================================
