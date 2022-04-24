import discord
import random
from datetime import *
from time import *
from discord.ext import commands
from discord.ext.commands.core import command
import requests
import praw
import feedparser

with open ("./media/txt/movie_list.txt") as movie:
    film = eval(movie.read())
    len_film = len(film)-1

with open ("./media/txt/reddit.txt") as reddit:
    red = eval(reddit.read())

reddit = praw.Reddit(client_id = red[0],
                    client_secret = red[1],
                    username = red[2],
                    password = red[3],
                    user_agent = red[4],
                    check_for_async=False)

class Com(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog Command Ready!')

#================================================================================
    @commands.command()
    @commands.guild_only()
    async def ping(self,ctx):
        await ctx.send("pong")

    @commands.command()
    async def testt(self,ctx):
        await ctx.send(ctx.message.content)
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    async def game(self,ctx):
        news_feed = feedparser.parse('https://isthereanydeal.com/rss/specials/eu1')
        print("Feed Title:", news_feed.feed.title) 

        titre = news_feed.entries[0].title
        lien = news_feed.entries[0].description

        await ctx.send("{}{}".format(titre,lien))

    @commands.command(name="heure",aliases=['hour'])
    @commands.guild_only()
    async def hour(self,ctx):
        await ctx.send("{}\n> {} Il est {}".format(ctx.author.mention,"\U0001F552",datetime.now().strftime('%Hh%M')))

    @commands.command(name="flymetothemoon")
    @commands.guild_only()
    async def fly(self,ctx):
        await ctx.send(ctx.author.mention ,file=discord.File("./media/img/rei.jpg"))

    @commands.command(name="quote",aliases=['citation'])
    @commands.guild_only()
    async def quote(self,ctx):
        url = 'https://api.quotable.io/random'
        r = requests.get(url)
        quote = r.json()
        await ctx.send("> **'**{}**'** \n > ─ **{}**".format(quote['content'],quote['author']))

    @commands.command(name="cointoss",aliases=['ct'])
    @commands.guild_only()
    async def ct(self,ctx):
        list=[['Pile','<:pile:859170464043761675>'],['Face','<:face:859170464378126336>']]
        choix = random.choice(list)
        await ctx.send("> {} {} {}".format(ctx.author.mention,choix[0],choix[1]))

    @commands.command(name="meme")
    @commands.guild_only()
    async def ct(self,ctx):
        message = await ctx.send("> \U000026A0 {} Cela peut prendre du temps !".format(ctx.author.mention))
        all_subs = []
        subreddit = reddit.subreddit("memes")
        top = subreddit.top(limit = 50)

        for submission in top:
            all_subs.append(submission)
        
        random_sub = random.choice(all_subs)
        em = discord.Embed(title = random_sub.title , colour= discord.Colour.dark_green())
        em.set_image(url= random_sub.url)
        await ctx.send(embed=em)
        await message.delete()

#================================================================================
    @commands.command(name="insult")
    @commands.guild_only()
    async def insult(self,ctx):
        id = ctx.author.id
        if is_in_list(id) == True:
            message = await ctx.send("Tu es déjà dans la liste, veux tu etre retiré ?")
        else: 
            message = await ctx.send("Tu n'es pas dans la liste, veux tu etre rajouté ?")

        await message.add_reaction("\U0001F44D")
        await message.add_reaction("🚫")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["\U0001F44D", "🚫"]

        while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=check)
                    if is_in_list(id) == False:
                        if str(reaction.emoji) == "\U0001F44D":
                            add_list(id)
                            mess_fin = "Tu es maintenant sur la liste !"
                        elif str(reaction.emoji) == "🚫":
                            mess_fin = "Aucune action n'a été fait !"
                    elif is_in_list(id) == True:
                        if str(reaction.emoji) == "\U0001F44D":
                            remove_list(id)
                            mess_fin = "Tu n'es plus sur la liste !"
                        elif str(reaction.emoji) == "🚫":
                            mess_fin = "Aucune action n'a été fait !"
                    else:
                        await message.edit(content="bug")
                        await message.remove_reaction(reaction, user)
                    
                    await message.clear_reactions()
                except:
                    await message.clear_reactions()
                    await message.edit(content=mess_fin)
                    break

#================================================================================
#Commande Film aléatoire voir ".media/txt/movie_list.txt"
#format: ['titre','date','genre (avec émoji)','rating',couleur,'lien allociné','lien cover film','lien imdb']

    # @commands.command(name="film",aliases=['f', 'movie'])
    # async def displaymod(self,ctx):
    #     chiffre = random.randint(0,len_film)
    #     embed = displaymod(chiffre)
    #     await ctx.send(f"> Information: film {chiffre + 1} sur {len_film + 1}", embed = embed)

#================================================================================
    # @commands.command(pass_context=True)
    # async def filmdemande(self,ctx):
    #     le_message = await ctx.send('> Indique le numéro du film voulu:')
    #     try:
    #         msg = await self.bot.wait_for('message',timeout=3.0)
    #         cont = msg.content
    #         if cont.isdigit() != True or int(cont) > len_film:
    #             await ctx.send("> Le film demandé n'existe pas ou la valeur demandée ne correspond pas a un chiffre.")

    #         else:
    #             embed = displaymod(int(msg.content))
    #             await ctx.send(f"> Information: film {int(cont) + 1} sur {len_film + 1}", embed = embed)
    #     except:
    #         await le_message.edit(content="> Temps de réponse dépassé !")

    # @commands.command(pass_context=True)
    # async def clear(self, ctx, number):
    #     if number.isdigit() != True or int(number) > len_film+1 or int(number) == 0:
    #         await ctx.send("> Le film demandé n'existe pas ou la valeur demandée ne correspond pas a un chiffre.")
    #     else: 
    #         embed = displaymod(int(number)-1)
    #         await ctx.send(f"> Information: film {int(number)} sur {len_film + 1}", embed = embed)

    @commands.command(name="film",aliases=['f', 'movie'])
    @commands.guild_only()
    async def film(self,ctx,*number):
        if not number:
            chiffre = random.randint(0,len_film)
            embed = displaymod(chiffre)
            await ctx.send(f"> Information: film {chiffre + 1} sur {len_film + 1}", embed = embed)
        else:
            if number[0].isdigit() != True or int(number[0]) > len_film+1 or int(number[0]) == 0:
                await ctx.send("> {} Le film demandé n'existe pas ou la valeur demandée ne correspond pas a un chiffre/nombre.".format("\U000026D4"))
            else: 
                embed = displaymod(int(number[0])-1)
                await ctx.send(f"> Information: film {int(number[0])} sur {len_film + 1}", embed = embed)

#================================================================================
def displaymod(num):
    with open ("./media/txt/movie_list.txt") as movie:
        film = eval(movie.read())
        movie = film[num]
    embed = discord.Embed(
        title = movie[0],
        color = movie[4],
        url = movie[5]
    )
    embed.set_footer(text=movie[7], icon_url = "http://ressource.lgdl.fun/img/imdb.png")
    embed.set_image(url=movie[6])
    embed.add_field(name='〉 Date', value=movie[1], inline= False)
    embed.add_field(name='〉 Genre', value=movie[2], inline= False)
    embed.add_field(name='〉 IMDB Rating/Metacritic Rating', value=movie[3], inline= True)
    return embed

#================================================================================
def is_in_list(id):
    with open("./media/txt/user_id_for_bad_word.txt") as f:
        mylist = eval(f.read())
        for k in mylist:
            if k == id:
                return True    
    return False

def add_list(id):
    with open("./media/txt/user_id_for_bad_word.txt") as f:
        mylist = eval(f.read())
        mylist.append(id)
    with open("./media/txt/user_id_for_bad_word.txt", 'w') as f:
        f.write(str(mylist))

def remove_list(id):
    with open("./media/txt/user_id_for_bad_word.txt") as f:
        mylist = eval(f.read())
        mylist.pop(mylist.index(id))
    with open("./media/txt/user_id_for_bad_word.txt", 'w') as f:
        f.write(str(mylist))
    
def setup(bot):
    bot.add_cog(Com(bot))

#FIN ============================================================================