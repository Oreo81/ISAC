import discord
from datetime import *
from time import *
from discord.ext import commands

with open ("./media/txt/movie_list.txt") as movie:
    film = eval(movie.read())
    len_film = len(film)

class help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="help",aliases=['h', '?'])
    @commands.guild_only()
    async def help(self,ctx,*input):
        embed = discord.Embed(
            title = "\U0001F4CD Help [py!help / py!h / py!?]",
            color = discord.Colour.purple() 
        )
        embed.set_author(name="{} - Help menu".format(ctx.author.name),icon_url=ctx.author.avatar_url)
        if not input:
            embed.add_field(name="\U00002699〉 Commande disponible", value="Pour plus d'information par rapport a une commande, utiliser `py!h [commande]` ", inline= False)
            embed.add_field(name="\U0001F506 〉 Fun", value="`ping`,`film`", inline= True)
            embed.add_field(name="\U0001F506 〉 Outils", value="`insult`,`heure`", inline= True)
            embed.add_field(name="\U0001F506 〉 Aléatoire", value="`quote`,`cointoss`", inline= False)
            await ctx.send(embed=embed)
        elif input[0] == 'film' or input[0] == 'f' or input[0] == 'movie':
            embed.add_field(name="\U0001F3EE 〉 py!film / py!f / py!movie", value="Renvoie un film aléatoire", inline= False)
            embed.add_field(name="\U0001F3EE 〉 Information complémentaire", value="-La commande peut avoir un argument qui doit être un chiffre/nombre qui correspond au numéro du film.\n -Il y a actuellement {} films dans la liste.\n -Référence des films: https://imgur.com/gallery/LaVjhjx".format(len_film), inline= False)
            embed.add_field(name="\U0001F3EE 〉 Exemple", value="```py!film --> Renvoie un film aléatoirement \npy!film 1 --> Renvoie le premier film de la liste```", inline= False)
            await ctx.send(embed=embed)
        else:
            error = discord.Embed(
                title = "{}  La commande '{}' n'existe pas".format("\U000026D4",input[0]),
                color = discord.Colour.dark_red()
            )
            await ctx.send(embed=error)

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(help(bot))        

#FIN ============================================================================