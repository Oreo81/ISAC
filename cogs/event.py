from datetime import *
from time import *
import random
from discord.ext import commands

class Eve(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog Event Ready!')

    @commands.Cog.listener()
    async def on_message(self,message):
        mention = '<@!{}>'.format(self.bot.user.id)
        with open ("./media/txt/mention.txt") as rep:
            repe = eval(rep.read())
            repo = repe[random.randint(0, len(repe)-1)]
        if mention in message.content:
            await message.channel.send(repo)

    # @commands.Cog.listener()
    # async def on_command_error(self,ctx, error):
    #     if isinstance(error, commands.NoPrivateMessage):
    #         await ctx.send("> {} Cette commande ne marche pas en message privé !".format("\U000026D4"))
    #     else:
    #         await ctx.send("> {}".format(error))

def setup(bot):
    bot.add_cog(Eve(bot))


#FIN ============================================================================