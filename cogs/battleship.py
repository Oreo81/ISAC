import discord
import os.path
from datetime import *
from time import *
from discord.ext import commands
import random

abc = ["A","B","C","D","E","F","G","H","I","J"]
secret_code = ""
code_for_role = ""
main_message = None

#================================================================================
#Class bot discord
class bats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_p1_1 = None
        self.message_p1_2 = None
        self.message_p2_1 = None
        self.message_p2_2 = None
        self.info_p1 = None
        self.info_p2 = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog BS Ready!')

    @commands.command(name="battleship",aliases=['bs'],pass_context=True)
    @commands.guild_only()
    async def battleship(self,ctx,*input):
        if not input:
            await ctx.send("> \U000026A0 Pour plus d'information: py!h bs \n > La commande n'est pas encore documenté !")

#=---------------- CREATE
        elif input[0] == 'create' or input[0] == 'c':
            #création de la partie est de tout le nécéssaire pour sauvegarder la partie si le bot devient off
            if os.path.exists("./media/battleship/{}".format(ctx.author.id)):
                await ctx.send("> \U000026D4 Une partie est deja en créer pour vous. Pour l'arréter: `py!bs d`")
            else:
                # secret_code = random.randint(1000,9999)
                secret_code = 1
                code_for_role = random.randint(1000,9999)

                overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),}

                #creation du role P1_[code_role], P2_[code_role] et la category
                await ctx.guild.create_role(name="P1_{}".format(code_for_role))
                await ctx.guild.create_role(name="P2_{}".format(code_for_role))
                await ctx.guild.create_category("game_{}".format(code_for_role))

                
                category = discord.utils.get(ctx.guild.categories, name = "game_{}".format(code_for_role))
                role_p1 = discord.utils.get(ctx.guild.roles, name="P1_{}".format(code_for_role))
                role_p2 = discord.utils.get(ctx.guild.roles, name="P2_{}".format(code_for_role))

                await ctx.guild.create_text_channel("game_P1_{}".format(code_for_role), category = category, overwrites=overwrites)
                await ctx.guild.create_text_channel("game_P2_{}".format(code_for_role), category = category, overwrites=overwrites)

                salon_p1 = discord.utils.get(ctx.guild.channels, name="game_p1_{}".format(code_for_role))
                salon_p2 = discord.utils.get(ctx.guild.channels, name="game_p2_{}".format(code_for_role))

                await salon_p1.set_permissions(role_p1, read_messages=True)
                await salon_p1.set_permissions(role_p2, read_messages=False)
                await salon_p2.set_permissions(role_p1, read_messages=False)
                await salon_p2.set_permissions(role_p2, read_messages=True)

                await ctx.author.add_roles(role_p1)

                os.makedirs("./media/battleship/{}".format(ctx.author.id))
                creation("player1",ctx.author.id)
                write_txt("./media/battleship/{}/info.txt".format(ctx.author.id),"[]")
                write_txt("./media/battleship/{}/next.txt".format(ctx.author.id),"['p1']")
                edit = read_txt("./media/battleship/{}/info.txt".format(ctx.author.id))
                edit.append('{}'.format(code_for_role))
                edit.append('{}'.format(secret_code))
                edit.append('{}'.format(ctx.author.id))
                edit.append('None')
                edit.append('F')
                edit.append('{}'.format(salon_p1.id))
                edit.append('{}'.format(salon_p2.id))
                edit.append('{}'.format(ctx.message.guild.id))
                edit.append('v_p1_F')
                edit.append('v_p2_F')

                write_txt("./media/battleship/{}/info.txt".format(ctx.author.id),str(edit))

                await ctx.send("> \U00002705 Code pour rejoindre la partie envoyer en message privé. Vous êtes maintenant le joueur 1 ! (id de la partie: {})".format(code_for_role))
                await ctx.author.send("> \U00002755 Voici le code de votre partie `{}`".format(secret_code))

                know_game_with_code = read_txt("./media/battleship/link.txt")
                know_game_with_code.append(["{}".format(ctx.author.id),"{}".format(secret_code),"{}".format(ctx.message.guild.id)])

                write_txt("./media/battleship/link.txt",str(know_game_with_code))

#=---------------- JOIN
        elif input[0] == 'join' or input[0] == 'j':
            #permet de rejoindre une partie `py!bs j [secret_code]`
            mylist = read_txt("./media/battleship/link.txt")
            if mylist == []:
                 await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs j [code]`")
            else:
                for k in mylist:
                    game = read_txt(("./media/battleship/{}/info.txt".format(k[0])))
                    try:
                        if input[1] == k[1]:
                            try:
                                if str(k[0]) != str(ctx.author.id):
                                    try:
                                        if str(ctx.message.guild.id) == str(k[2]):
                                            if game[4] == 'T':
                                                await ctx.send("> \U000026D4 Il y a déjà un deuxième joureur dans cette partie !\n <@{}> P1 et <@{}> P2".format(game[2],game[3]))
                                            else:
                                                salon_p1 = discord.utils.get(ctx.guild.channels, name="game_p1_{}".format(game[0]))
                                                salon_p2 = discord.utils.get(ctx.guild.channels, name="game_p2_{}".format(game[0]))
                                                role_p2 = discord.utils.get(ctx.guild.roles, name="P2_{}".format(game[0]))
                                                game[4] = 'T'
                                                game[3] = '{}'.format(ctx.author.id)
                                                write_txt("./media/battleship/{}/info.txt".format(k[0]),str(game))
                                                await ctx.author.add_roles(role_p2)
                                                creation("player2",k[0])
                                                await ctx.send("> \U00002705 Vous êtes maintenant le joueur 2 ! (id de la partie: {}) \n> <@{}> est premier joueur et <@{}> le deuxième.".format(game[0],game[2],game[3]))
                                                
                                                #---Salon Player 1 ---
                                                await salon_p1.send("> \U00002755 <@{}> Vous pouvez jouer ici dès maintenant. `py!bs p` [bateau + info] pour plus d'info `py!h bs` \n ───────────────────────".format(game[2]))
                                                map = see(look_map("player1",game[2]))
                                                map_2 = see(look_map_enemy("player1",game[2]))
                                                self.message_p1_1 = await salon_p1.send("{} \n  ───────────────────────".format(map_2))
                                                self.message_p1_2 = await salon_p1.send("{} \n  ───────────────────────".format(map))
                                                await salon_p1.send("> > Information sur la dernière commande effectué: ")
                                                self.info_p1 = await salon_p1.send("> None")
                                                
                                                #---Salon Player 2 ---
                                                await salon_p2.send("> \U00002755 <@{}> Vous pouvez jouer ici dès maintenant. `py!bs p` [bateau + info] pour plus d'info `py!h bs` \n ───────────────────────".format(game[3]))
                                                map2 = see(look_map("player2",k[0]))
                                                map2_2 = see(look_map_enemy("player2",k[0]))
                                                self.message_p2_1 = await salon_p2.send("{} \n  ───────────────────────".format(map2_2))
                                                self.message_p2_2 = await salon_p2.send("{} \n  ───────────────────────".format(map2))
                                                await salon_p2.send("> > Information sur la dernière commande effectué: ")
                                                self.info_p2 = await salon_p2.send("> None")
                                        
                     
                                        else:
                                            await ctx.send("> \U000026D4 La partie n'est pas sur ce server, réessayer sur le bon server.")
                                    except:
                                        await ctx.send("> \U000026D4 Vous n'êtes pas la personnes")
                                else: await ctx.send("> \U000026D4 Le créateur de la partie ne peux pas etre le deuxième joueur")
                            except:
                                print("erreur code join 01")
                        else: 
                            await ctx.send("> \U000026D4 Il ce peut que le code ne correspond à aucune partie.")
                    except:
                        await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs j [code]`")

#=---------------- LEAVE
        # elif input[0] == 'leave' or input[0] == 'l':
        #     #permet de sortir d'une partie `py!bs l [secret_code]`
        #     mylist = read_txt("./media/battleship/link.txt")
        #     if mylist == []:
        #         await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs l [code]`")
        #     else:
        #         for k in mylist:
        #             game = read_txt(("./media/battleship/{}/info.txt".format(k[0])))
        #             try:
        #                 if input[1] == k[1]:
        #                     try:
        #                         if str(k[0]) != str(ctx.author.id):
        #                             try:
        #                                 if str(game[3]) != str(ctx.author.id):
        #                                     await ctx.send("> \U000026D4 Vous n'êtes pas le deuxième joueur de cette partie.")
        #                                 else:
        #                                     role_p2 = discord.utils.get(ctx.guild.roles, name="P2_{}".format(game[0]))
        #                                     game[4] = 'F'
        #                                     game[3] = "None"
        #                                     write_txt("./media/battleship/{}/info.txt".format(k[0]),str(game))
        #                                     await ctx.author.remove_roles(role_p2)
        #                                     await ctx.send("> \U00002755 Vous n'êtes plus le joueur 2 ! (id de la partie: {})".format(game[0]))
        #                             except:
        #                                 await ctx.send("> Erreur code leave 01")
        #                         else:
        #                             await ctx.send("> \U000026D4 Le créateur de la partie ne peux pas faire cette commande, pour finir et supprimer la partie: `py!bs d`")
        #                     except: 
        #                         await ctx.send("> Erreur code leave 02")
        #                 else:
        #                     await ctx.send("> \U000026D4 Le code `{}` n'est pas valide. Il se peut que le code n'est lié à aucune partie.".format(input[1]))
        #             except: 
        #                 await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs l [code]`")

#=---------------- PLACE
#place_ship(id,player,bateau,where1,where2,position):
        elif input[0] == 'place' or input[0] == 'p':
            #permet de placer un bateau a la position choisie `py!bs p [secret_code] [bateau+emplacement]`
            mylist = read_txt("./media/battleship/link.txt")
            if mylist == []:
                await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs p [code] [type+emplacement du bateau]`")
            else:
                for k in mylist:
                    game = read_txt(("./media/battleship/{}/info.txt".format(k[0])))
                    # try:
                    if str(ctx.message.guild.id) == str(k[2]): 
                        # try:
                        if str(ctx.author.id) == game[2]:
                            map = read_txt(("./media/battleship/{}/map_player1.txt".format(k[0])))
                            if map[7] == 'done_F':
                                if str(ctx.message.channel.id) == game[5]:
                                    if input[1] == k[1]:

                                        #------------------------
                                        if input[2][0] == 'A':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':white_large_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player1.txt".format(k[0]),str(map))

                                            if verif(input[2][1],input[2][2],input[2][3],5,map[0])[1] == True:
                                                await self.info_p1.edit(content=verif(input[2][1],input[2][2],input[2][3],5,map[0])[0])
                                            else:
                                                place_ship(k[0],'player1','A',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player1.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p1.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p1.edit(content="> :grey_exclamation: Bateaux *Aircraft Carrier* placé")
                                                    await ctx.message.delete()

                                        #------------------------
                                        elif input[2][0] == 'D':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':orange_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player1.txt".format(k[0]),str(map))

                                            if verif(input[2][1],input[2][2],input[2][3],3,map[0])[1] == True:
                                                await self.info_p1.edit(content=verif(input[2][1],input[2][2],input[2][3],3,map[0])[0])
                                            else:
                                                place_ship(k[0],'player1','D',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player1.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p1.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p1.edit(content="> :grey_exclamation: Bateaux *Destroyer* placé")
                                                    await ctx.message.delete()

                                        #------------------------
                                        elif input[2][0] == 'S':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':yellow_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player1.txt".format(k[0]),str(map))
                                            if verif(input[2][1],input[2][2],input[2][3],3,map[0])[1] == True:
                                                await self.info_p1.edit(content=verif(input[2][1],input[2][2],input[2][3],3,map[0])[0])
                                            else:
                                                place_ship(k[0],'player1','S',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player1.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p1.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p1.edit(content="> :grey_exclamation: Bateaux *Submarine* placé")
                                                    await ctx.message.delete()

                                        #------------------------
                                        elif input[2][0] == 'B':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':black_large_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player1.txt".format(k[0]),str(map))
                                            if verif(input[2][1],input[2][2],input[2][3],4,map[0])[1] == True:
                                                await self.info_p1.edit(content=verif(input[2][1],input[2][2],input[2][3],4,map[0])[0])
                                            else:
                                                place_ship(k[0],'player1','B',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player1.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p1.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p1.edit(content="> :grey_exclamation: Bateaux *Battleship* placé")
                                                    await ctx.message.delete()

                                        #------------------------
                                        elif input[2][0] == 'P':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':green_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player1.txt".format(k[0]),str(map))
                                            if verif(input[2][1],input[2][2],input[2][3],2,map[0])[1] == True:
                                                await self.info_p1.edit(content=verif(input[2][1],input[2][2],input[2][3],2,map[0])[0])
                                            else:
                                                place_ship(k[0],'player1','P',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player1.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p1.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p1.edit(content="> :grey_exclamation: Bateaux *Patrol* placé")
                                                    await ctx.message.delete()
                                        else:
                                            await self.info_p1.edit(content="> \U000026D4 Le bateau demandé n'existe pas. Voici les bateaux existant: \n > :green_square: Patrol (P) Longueur 2 \n > :yellow_square: Submarine (S) Longueur 3 \n > :orange_square: Destroyer (D) Longueur 3 \n > :black_large_square: Battleship (B) Longueur 4 \n > :white_large_square: Aircraft carrier (A) Longueur 5 ")
                                    else:
                                        await self.info_p1.edit(content="> \U000026D4 Le code `{}` n'est pas valide. Il se peut que le code n'est lié à aucune partie.".format(input[1]))
                                else:
                                    await ctx.send("> \U000026D4 Vous n'êtes pas sur le bon salon! Vous devez être ici <#{}>".format(game[5]))
                            else: 
                                await self.info_p1.edit(content="> \U000026D4 Vous avez déjà validé l'emplacement des bateaux, vous ne pouvez plus les replacer !")
                        elif str(ctx.author.id) == game[3]:
                            map = read_txt(("./media/battleship/{}/map_player2.txt".format(k[0])))
                            if map[7] == 'done_F':
                                if str(ctx.message.channel.id) == game[6]:
                                    if input[1] == k[1]:

                                        #------------------------
                                        if input[2][0] == 'A':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':white_large_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player2.txt".format(k[0]),str(map))

                                            if verif(input[2][1],input[2][2],input[2][3],5,map[0])[1] == True:
                                                await self.info_p2.edit(content=verif(input[2][1],input[2][2],input[2][3],5,map[0])[0])
                                            else:
                                                place_ship(k[0],'player2','A',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player2.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p2.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p2_2.edit(content=see(look_map("player2",k[0])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p2.edit(content=see(look_map("player2",k[0])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p2.edit(content="> :grey_exclamation: Bateaux *Aircraft Carrier* placé")
                                                    await ctx.message.delete()


                                        #------------------------
                                        elif input[2][0] == 'D':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':orange_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player2.txt".format(k[0]),str(map))

                                            if verif(input[2][1],input[2][2],input[2][3],3,map[0])[1] == True:
                                                await self.info_p2.edit(content=verif(input[2][1],input[2][2],input[2][3],3,map[0])[0])
                                            else:
                                                place_ship(k[0],'player2','D',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player2.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p2.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p2_2.edit(content=see(look_map("player2",k[0])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p2.edit(content=see(look_map("player2",k[0])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p2.edit(content="> :grey_exclamation: Bateaux *Destroyer* placé")
                                                    await ctx.message.delete()

                                        #------------------------
                                        elif input[2][0] == 'S':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':yellow_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player2.txt".format(k[0]),str(map))
                                            if verif(input[2][1],input[2][2],input[2][3],3,map[0])[1] == True:
                                                await self.info_p2.edit(content=verif(input[2][1],input[2][2],input[2][3],3,map[0])[0])
                                            else:
                                                place_ship(k[0],'player2','S',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player2.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p2.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p2_2.edit(content=see(look_map("player2",k[0])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p2.edit(content=see(look_map("player2",k[0])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p2.edit(content="> :grey_exclamation: Bateaux *Submarine* placé")
                                                    await ctx.message.delete()

                                        #------------------------
                                        elif input[2][0] == 'B':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':black_large_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player2.txt".format(k[0]),str(map))
                                            if verif(input[2][1],input[2][2],input[2][3],4,map[0])[1] == True:
                                                await self.info_p2.edit(content=verif(input[2][1],input[2][2],input[2][3],4,map[0])[0])
                                            else:
                                                place_ship(k[0],'player2','B',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player2.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p2.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p2.edit(content=see(look_map("player2",k[0])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p2_2.edit(content=see(look_map("player2",k[0])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p2.edit(content="> :grey_exclamation: Bateaux *Battleship* placé")
                                                    await ctx.message.delete()

                                        #------------------------
                                        elif input[2][0] == 'P':
                                            for a in range(10):
                                                for b in range(10):
                                                    if map[0][a][b] == ':green_square:':
                                                        map[0][a][b] = ':blue_square:'
                                                        write_txt("./media/battleship/{}/map_player2.txt".format(k[0]),str(map))
                                            if verif(input[2][1],input[2][2],input[2][3],2,map[0])[1] == True:
                                                await self.info_p2.edit(content=verif(input[2][1],input[2][2],input[2][3],2,map[0])[0])
                                            else:
                                                place_ship(k[0],'player2','P',input[2][1],input[2][2],input[2][3])
                                                map_n = read_txt(("./media/battleship/{}/map_player2.txt".format(k[0])))
                                                if map_n[2] == 'patrol_T' and map_n[3] == 'submarine_T' and map_n[4] == 'destroyer_T' and map_n[5] == 'battleship_T' and map_n[6] == 'aircraft_T':
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé")
                                                    await self.info_p2.edit(content="> :grey_exclamation: Tous les bateaux on étaient placé. Pour modifier leur emplacement, refaite la commande pour les positionners comme avant. \n > Pour validé votre choix finale, faite `py!bs v [code]`")
                                                    await self.message_p2_2.edit(content=see(look_map("player2",k[0])))
                                                    await ctx.message.delete()
                                                else:
                                                    await self.message_p2.edit(content=see(look_map("player2",k[0])))
                                                    # await ctx.send("> :grey_exclamation: Bateaux placé", delete_after=2)
                                                    await self.info_p2.edit(content="> :grey_exclamation: Bateaux *Patrol* placé")
                                                    await ctx.message.delete()


                                        else:
                                            await self.info_p2.edit(content="> \U000026D4 Le bateau demandé n'existe pas. Voici les bateaux existant: \n > :green_square: Patrol (P) Longueur 2 \n > :yellow_square: Submarine (S) Longueur 3 \n > :orange_square: Destroyer (D) Longueur 3 \n > :black_large_square: Battleship (B) Longueur 4 \n > :white_large_square: Aircraft carrier (A) Longueur 5 ")
                                    else:
                                        await self.info_p2.edit(content="> \U000026D4 Le code `{}` n'est pas valide. Il se peut que le code n'est lié à aucune partie.".format(input[1]))
                                else:
                                    await ctx.send("> \U000026D4 Vous n'êtes pas sur le bon salon! Vous devez être ici <#{}>".format(game[6]),delete_after=5)
                            else: 
                                await self.info_p2.edit(content="> \U000026D4 Vous avez déjà validé l'emplacement des bateaux, vous ne pouvez plus les replacer !")
                        else: 
                            await ctx.send("> \U000026D4 Vous n'être pas la bonne personnes",delete_after=5)
                        # except:
                            print("erreur 1")
                    else:
                        await ctx.send("> \U000026D4 La partie n'est pas sur ce server, réessayer sur le bon server.",delete_after=5)
                    # except:
                        print("erreur 2")


            # await ctx.send("pas fini")

#=----------------  TIR
        elif input[0] == 'tir' or input[0] == 't':
        #permet de placer tirer sur un emplacement pour faire couller un bateaux
        #vérifie si py!bs [commande] correspond à la commande validé.
            code = read_txt("./media/battleship/link.txt")
            # code correspond a une list qui contient l'ensemble des partie qui exist. Avec [["id créateur","code secret envoyer en mp par le bot","id server ou la partie existe"]].                    
            index_game = None # correspond à une list qui contient l'id du créateur de la partie.
            for k in code:
                if input[1] == k[1]: # Partie trouver avec le bon code.
                    index_game = k
                else:
                    pass
                
            if index_game != None: 
                game = read_txt("./media/battleship/{}/info.txt".format(index_game[0])) # On récupère les informations de la partie avec l'id du créateur.
                salon_p1 = discord.utils.get(ctx.guild.channels, name="game_p1_{}".format(game[0])) # On récupère l'id du salon du joueur 1 (le créateur)
                salon_p2 = discord.utils.get(ctx.guild.channels, name="game_p2_{}".format(game[0])) # On récupère l'id du salon du joueur 2


    # def tir(self,where1,where2,map_enemy):
    #     try:
    #         p1 = abc.index(where1)
    #     except:
    #         return "Karim tu veux vraiment aller dans la cuisinière ?"
        
    #     if where2 >= 0 and where2 <= 9:
    #             p2= where2
    #     else:
    #         return "Nope"

    #     if self.sea_enemy[p1][p2] != ':purple_square:':
    #         return "déjà tiré ici"
    #     elif map_enemy[p1][p2] == ':blue_square:':
    #         self.sea_enemy[p1][p2] = ':blue_square:'
    #     elif map_enemy[p1][p2] != ':blue_square:':
    #         self.sea_enemy[p1][p2] = ':blue_square:'











#=---------------- DELETE
        elif input[0] == 'delete' or input[0] == 'd':
            #permet de supprimer une partie créer par l'autheur de la commande 
            if not os.path.isfile("./media/battleship/{}/info.txt".format(ctx.author.id)):
                await ctx.send("> \U000026D4 Vous n'avez pas créé de partie, pour en créer une `py!bs c`")
            else:
                edit = read_txt("./media/battleship/{}/info.txt".format(ctx.author.id))

                role_p1 = discord.utils.get(ctx.guild.roles, name="P1_{}".format(edit[0]))
                role_p2 = discord.utils.get(ctx.guild.roles, name="P2_{}".format(edit[0]))
                salon_p1 = discord.utils.get(ctx.guild.channels, name="game_p1_{}".format(edit[0]))
                salon_p2 = discord.utils.get(ctx.guild.channels, name="game_p2_{}".format(edit[0]))
                cat_game = discord.utils.get(ctx.guild.categories, name ="game_{}".format(edit[0]))

                await role_p1.delete()
                await role_p2.delete()
                await salon_p1.delete()
                await salon_p2.delete()
                await cat_game.delete()

                mylist = read_txt("./media/battleship/link.txt")
                for k in mylist:
                    if str(edit[1]) == k[1]:
                        mylist.remove(k)
                    else:
                        await ctx.send("> Une erreur est survenue ligne 114")
                write_txt("./media/battleship/link.txt",str(mylist))
                os.remove("./media/battleship/{}/info.txt".format(ctx.author.id))
                os.remove("./media/battleship/{}/map_player1.txt".format(ctx.author.id))
                os.remove("./media/battleship/{}/map_player2.txt".format(ctx.author.id))
                os.remove("./media/battleship/{}/next.txt".format(ctx.author.id))
                os.rmdir("./media/battleship/{}".format(ctx.author.id))
                await ctx.send("> \U00002705 Partie terminé et supprimé.")

#=---------------- VALID
# Permet de validé la position de tout les bateaux.
# Permet de confirmer le début de la partie.
        elif input[0] == 'valid' or input[0] == 'v':
        #vérifie si py!bs [commande] correspond à la commande validé.
            code = read_txt("./media/battleship/link.txt")
            # code correspond a une list qui contient l'ensemble des partie qui exist. Avec [["id créateur","code secret envoyer en mp par le bot","id server ou la partie existe"]].                    
            index_game = None # correspond à une list qui contient l'id du créateur de la partie.
            for k in code:
                if input[1] == k[1]: # Partie trouver avec le bon code.
                    index_game = k
                else:
                    pass
                
            if index_game != None: 
                game = read_txt("./media/battleship/{}/info.txt".format(index_game[0])) # On récupère les informations de la partie avec l'id du créateur.
                salon_p1 = discord.utils.get(ctx.guild.channels, name="game_p1_{}".format(game[0])) # On récupère l'id du salon du joueur 1 (le créateur)
                salon_p2 = discord.utils.get(ctx.guild.channels, name="game_p2_{}".format(game[0])) # On récupère l'id du salon du joueur 2

                if str(ctx.message.guild.id) == str(k[2]): # vérification si le message est dans le bon server
                    # --P1
                    if str(ctx.author.id) == game[2]: # vérification si la personnes correspond au joueur 1
                        if str(ctx.message.channel.id) == game[5]: # vérification si le message est dans le bon salon textuel pour le joueur 1 (game[5] correspond à l'id du salon pour le joueur 1)
                            map_p1 = read_txt("./media/battleship/{}/map_player1.txt".format(game[2])) # On charge dans la une variable, la carte du joueur 1 (game[2] correspond a l'id du créateur, donc aussi le joueur 1)
                            if map_p1[7] == 'done_F': #vérifie si la commande [py!bs v[code]] à déjà été effectué avec tout les bateaux placé.
                                if map_p1[2] == 'patrol_T' and map_p1[3] == 'submarine_T' and map_p1[4] == 'destroyer_T' and map_p1[5] == 'battleship_T' and map_p1[6] == 'aircraft_T' and map_p1[7] =='done_F': # Vérification que tout les bateaux on étaient placé pour pouvoir valider
                                    if game[9] == 'v_p2_F': # joureur 2 n'a pas encore validé sa carte
                                        map_p1[7] = 'done_T'
                                        game[8] = 'v_p1_T'
                                        write_txt("./media/battleship/{}/map_player1.txt".format(index_game[0]),str(map_p1)) # sauvegarde des modifications sur le .txt
                                        write_txt("./media/battleship/{}/info.txt".format(index_game[0]),str(game)) # sauvegarde des modifications sur le .txt
                                        await self.info_p1.edit(content = "> :white_check_mark: Carte sauvegarder, vous ne pouvez plus la modifier. \n > :grey_exclamation: L'autre joueur n'est pas encore prêt. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) # Alert type 2
                                        await ctx.message.delete()
                                    else: # joureur 2 a validé sa carte
                                        map_p1[7] = 'done_T'
                                        write_txt("./media/battleship/{}/map_player1.txt".format(index_game[0]),str(map_p1)) # sauvegarde des modifications sur le .txt
                                        await self.info_p1.edit(content = "> :white_check_mark: La partie commence. C'est à vous de jouer.".format(game[2])) # Alert type 2
                                        await self.info_p2.edit(content = "> :white_check_mark: La partie commence. Ce n'est pas encore a vous de jouer.".format(game[2])) # Alert type 2
                                        await ctx.message.delete()
                                else: # Si tout les bateaux ne sont pas placer
                                    await self.info_p1.edit(content = "> :no_entry: Tous les bateaux ne sont pas placés. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) #Erreur Type 2
                                    await ctx.message.delete()
                            else: # Si 'done_T' alors, les positions des bateaux sont déjà validé. 
                                await self.info_p1.edit(content = "> :no_entry: Vous avez déjà validé l'emplacement des différents bateaux. Vous ne pouvez plus les modifier. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) #Erreur Type 2
                                await ctx.message.delete()
                        else: # Pas le bon salon textuel
                            await ctx.send("> :no_entry: Vous n'êtes pas sur le bon salon. Pour effectuer cette commande vous devez être ici <#{}> \n > :grey_exclamation: Commande effectué: `{}`".format(game[5],ctx.message.content),delete_after=5) #Erreur Type 1 
                            await ctx.message.delete()
                    # --P2
                    elif str(ctx.author.id) == game[3]: # vérification si la personnes correspond au joueur 2
                        if str(ctx.message.channel.id) == game[6]: # vérification si le message est dans le bon salon textuel pour le joueur 2 (game[6] correspond à l'id du salon pour le joueur 1):
                            map_p2 = read_txt("./media/battleship/{}/map_player2.txt".format(game[2])) # On charge dans la une variable, la carte du joueur 2 (game[2] correspond a l'id du créateur, donc aussi le joueur 1)
                            if map_p2[7] == 'done_F': #vérifie si la commande [py!bs v[code]] à déjà été effectué avec tout les bateaux placé.
                                if map_p2[2] == 'patrol_T' and map_p2[3] == 'submarine_T' and map_p2[4] == 'destroyer_T' and map_p2[5] == 'battleship_T' and map_p2[6] == 'aircraft_T' and map_p2[7] =='done_F': # Vérification que tout les bateaux on étaient placé pour pouvoir valider
                                    if game[8] == 'v_p1_F': # joureur 1 n'a pas encore validé sa carte
                                        map_p2[7] = 'done_T'
                                        game[9] = 'v_p2_T'
                                        write_txt("./media/battleship/{}/map_player2.txt".format(index_game[0]),str(map_p2)) # sauvegarde des modifications sur le .txt
                                        write_txt("./media/battleship/{}/info.txt".format(index_game[0]),str(game)) # sauvegarde des modifications sur le .txt
                                        await self.info_p2.edit(content = "> :white_check_mark: Carte sauvegarder, vous ne pouvez plus la modifier. \n > :grey_exclamation: L'autre joueur n'est pas encore prêt. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) # Alert type 2
                                        await ctx.message.delete()
                                    else: # joureur 1 a validé sa carte
                                        map_p2[7] = 'done_T'
                                        write_txt("./media/battleship/{}/map_player1.txt".format(index_game[0]),str(map_p2)) # sauvegarde des modifications sur le .txt
                                        await self.info_p1.edit(content = "> :white_check_mark: La partie commence. C'est à vous de jouer.".format(game[2])) # Alert type 2
                                        await self.info_p2.edit(content = "> :white_check_mark: La partie commence. Ce n'est pas encore a vous de jouer.".format(game[2])) # Alert type 2
                                        await ctx.message.delete()
                                else: # Si tout les bateaux ne sont pas placer
                                    await self.info_p2.edit(content = "> :no_entry: Tous les bateaux ne sont pas placés. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) #Erreur Type 2
                                    await ctx.message.delete()
                            else: # Si 'done_T' alors, les positions des bateaux sont déjà validé. 
                                await self.info_p2.edit(content = "> :no_entry: Vous avez déjà validé l'emplacement des différents bateaux. Vous ne pouvez plus les modifier. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) #Erreur Type 2
                                await ctx.message.delete()
                        else: # Pas le bon salon textuel
                            await ctx.send("> :no_entry: Vous n'êtes pas sur le bon salon. Pour effectuer cette commande vous devez être ici <#{}> \n > :grey_exclamation: Commande effectué: `{}`".format(game[6],ctx.message.content),delete_after=5) #Erreur Type 1 
                            await ctx.message.delete()
                    # --Aucun
                    else: # La personne n'est ni le joueur 1 ni le joueur 2
                            await ctx.send("> :no_entry: Vous n'être pas la bonne personnes \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content),delete_after=5) #Erreur Type 1 
                            await ctx.message.delete() 
                else: # Pas le bon server
                    await ctx.send("> :no_entry: La partie n'est pas sur ce server, réessayer sur le bon server. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content),delete_after=5) #Erreur Type 1
                    await ctx.message.delete()
            else:
                # Le code ne correspond à aucune partie existante. 
                await ctx.send("> :no_entry: Aucune partie n'a été trouver avec ce code. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content),delete_after=5) #Erreur Type 1
                await ctx.message.delete()

#=---------------- Load (admin only)
        elif input[0] == 'load':
            mylist = read_txt("./media/battleship/link.txt")
            if mylist == []:
                await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs l [code]`")
            else:
                for k in mylist:
                    game = read_txt(("./media/battleship/{}/info.txt".format(k[0])))
                    if str(ctx.author.id) == game[2]:
                        map = [[[':white_large_square:', ':white_large_square:', ':white_large_square:', ':white_large_square:', ':white_large_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':orange_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':orange_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':orange_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':yellow_square:'], [':green_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':yellow_square:'], [':green_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':yellow_square:']], [[':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:']], 'patrol_T', 'submarine_T', 'destroyer_T', 'battleship_T', 'aircraft_T', 'done_F']
                        write_txt("./media/battleship/{}/map_player1.txt".format(k[0]),str(map))
                        await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                        await self.info_p1.edit(content="> :grey_exclamation: Map charger")
                        await ctx.message.delete()
                    elif str(ctx.author.id) == game[3]:
                        map = [[[':white_large_square:', ':white_large_square:', ':white_large_square:', ':white_large_square:', ':white_large_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':orange_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':orange_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':orange_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':yellow_square:'], [':green_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':yellow_square:'], [':green_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':yellow_square:']], [[':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:']], 'patrol_T', 'submarine_T', 'destroyer_T', 'battleship_T', 'aircraft_T', 'done_F']
                        write_txt("./media/battleship/{}/map_player2.txt".format(k[0]),str(map))
                        await self.message_p2_2.edit(content=see(look_map("player2",k[0])))
                        await self.info_p2.edit(content="> :grey_exclamation: Map charger")
                        await ctx.message.delete()
                    else:
                        pass

#=---------------- RANDOM
        elif input[0] == 'random' or input[0] == 'r':
            #place de manière aléatoire les différents bateaux.
            code = read_txt("./media/battleship/link.txt")
            # code correspond a une list qui contient l'ensemble des partie qui exist. Avec [["id créateur","code secret envoyer en mp par le bot","id server ou la partie existe"]].                    
            index_game = None # correspond à une list qui contient l'id du créateur de la partie.
            for k in code:
                if input[1] == k[1]: # Partie trouver avec le bon code.
                    index_game = k
                else:
                    pass
                    
            if index_game != None: 
                game = read_txt("./media/battleship/{}/info.txt".format(index_game[0])) # On récupère les informations de la partie avec l'id du créateur.
                salon_p1 = discord.utils.get(ctx.guild.channels, name="game_p1_{}".format(game[0])) # On récupère l'id du salon du joueur 1 (le créateur)
                salon_p2 = discord.utils.get(ctx.guild.channels, name="game_p2_{}".format(game[0])) # On récupère l'id du salon du joueur 2

                if str(ctx.message.guild.id) == str(k[2]): # vérification si le message est dans le bon server
                    # --P1
                    if str(ctx.author.id) == game[2]: # vérification si la personnes correspond au joueur 1
                        if str(ctx.message.channel.id) == game[5]: # vérification si le message est dans le bon salon textuel pour le joueur 1 (game[5] correspond à l'id du salon pour le joueur 1)
                            map_p1 = [[[':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:']], [[':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:']], 'patrol_F', 'submarine_F', 'destroyer_F', 'battleship_F', 'aircraft_F', 'done_F']
                            write_txt("./media/battleship/{}/map_player1.txt".format(game[2]),"{}".format(map_p1))

                            b0 = False
                            b1 = False
                            b2 = False
                            b3 = False
                            b4 = False

                            while b0 == False:
                                position_p1_b0_1 = random.choice(abc)
                                position_p1_b0_2 = random.randint(0, 9)
                                position_p1_b0_3 = random.choice(["U","R"])
                                if verif(position_p1_b0_1,position_p1_b0_2,position_p1_b0_3,2,map_p1[0])[1] == True:
                                    b0 = False
                                else:
                                    place_ship(index_game[0],'player1','P',position_p1_b0_1,position_p1_b0_2,position_p1_b0_3)
                                    b0 = True
                            
                            while b1 == False:
                                position_p1_b1_1 = random.choice(abc)
                                position_p1_b1_2 = random.randint(0, 9)
                                position_p1_b1_3 = random.choice(["U","R"])
                                if verif(position_p1_b1_1,position_p1_b1_2,position_p1_b1_3,3,map_p1[0])[1] == True:
                                    b1 = False
                                else:
                                    place_ship(index_game[0],'player1','D',position_p1_b1_1,position_p1_b1_2,position_p1_b1_3)
                                    b1 = True

                            while b2 == False:
                                position_p1_b2_1 = random.choice(abc)
                                position_p1_b2_2 = random.randint(0, 9)
                                position_p1_b2_3 = random.choice(["U","R"])
                                if verif(position_p1_b2_1,position_p1_b2_2,position_p1_b2_3,3,map_p1[0])[1] == True:
                                    b2 = False
                                else:
                                    place_ship(index_game[0],'player1','S',position_p1_b2_1,position_p1_b2_2,position_p1_b2_3)
                                    b2 = True

                            while b3 == False:
                                position_p1_b3_1 = random.choice(abc)
                                position_p1_b3_2 = random.randint(0, 9)
                                position_p1_b3_3 = random.choice(["U","R"])
                                if verif(position_p1_b3_1,position_p1_b3_2,position_p1_b3_3,4,map_p1[0])[1] == True:
                                    b3 = False
                                else:
                                    place_ship(index_game[0],'player1','B',position_p1_b3_1,position_p1_b3_2,position_p1_b3_3)
                                    b3= True
                            
                            while b4 == False:
                                position_p1_b4_1 = random.choice(abc)
                                position_p1_b4_2 = random.randint(0, 9)
                                position_p1_b4_3 = random.choice(["U","R"])
                                if verif(position_p1_b4_1,position_p1_b4_2,position_p1_b4_3,5,map_p1[0])[1] == True:
                                    b4 = False
                                else:
                                    place_ship(index_game[0],'player1','A',position_p1_b4_1,position_p1_b4_2,position_p1_b4_3)
                                    b4 = True
                            
                            await self.message_p1_2.edit(content=see(look_map("player1",game[2])))
                            await self.info_p1.edit(content = "> :grey_exclamation: Tous les bateaux sont placés. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) #Erreur Type 2
                            await ctx.message.delete()

                    # --P2
                    elif str(ctx.author.id) == game[3]: # vérification si la personnes correspond au joueur 2
                        if str(ctx.message.channel.id) == game[6]: # vérification si le message est dans le bon salon textuel pour le joueur 2 (game[6] correspond à l'id du salon pour le joueur 1):
                            map_p2 = [[[':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:'], [':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:', ':blue_square:']], [[':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:'], [':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:', ':purple_square:']], 'patrol_F', 'submarine_F', 'destroyer_F', 'battleship_F', 'aircraft_F', 'done_F']
                            write_txt("./media/battleship/{}/map_player2.txt".format(game[2]),"{}".format(map_p2))

                            b0 = False
                            b1 = False
                            b2 = False
                            b3 = False
                            b4 = False

                            map_p2_b0 = read_txt("./media/battleship/{}/map_player2.txt".format(game[2]))
                            while map_p2_b0[2] != 'patrol_T':
                                position_p2_b0_1 = random.choice(abc)
                                position_p2_b0_2 = random.randint(0, 9)
                                position_p2_b0_3 = random.choice(["U","R"])
                                if verif(position_p2_b0_1,position_p2_b0_2,position_p2_b0_3,2,map_p2[0])[1] == True:
                                    b0 = False
                                else:
                                    place_ship(index_game[0],'player2','P',position_p2_b0_1,position_p2_b0_2,position_p2_b0_3)
                                    b0 = True
                            
                            map_p2_b1 = read_txt("./media/battleship/{}/map_player2.txt".format(game[2]))
                            while map_p2_b1[3] != 'destroyer_T':
                                position_p2_b1_1 = random.choice(abc)
                                position_p2_b1_2 = random.randint(0, 9)
                                position_p2_b1_3 = random.choice(["U","R"])
                                if verif(position_p2_b1_1,position_p2_b1_2,position_p2_b1_3,3,map_p2[0])[1] == True:
                                    b1 = False
                                else:
                                    place_ship(index_game[0],'player2','D',position_p2_b1_1,position_p2_b1_2,position_p2_b1_3)
                                    b1 = True

                            map_p2_b2 = read_txt("./media/battleship/{}/map_player2.txt".format(game[2]))
                            while map_p2_b2[4] != 'submarine_T':
                                position_p2_b2_1 = random.choice(abc)
                                position_p2_b2_2 = random.randint(0, 9)
                                position_p2_b2_3 = random.choice(["U","R"])
                                if verif(position_p2_b2_1,position_p2_b2_2,position_p2_b2_3,3,map_p2[0])[1] == True:
                                    b2 = False
                                else:
                                    place_ship(index_game[0],'player2','S',position_p2_b2_1,position_p2_b2_2,position_p2_b2_3)
                                    b2 = True

                            map_p2_b3 = read_txt("./media/battleship/{}/map_player2.txt".format(game[2]))
                            while map_p2_b3[5] != 'battleship_T':
                                position_p2_b3_1 = random.choice(abc)
                                position_p2_b3_2 = random.randint(0, 9)
                                position_p2_b3_3 = random.choice(["U","R"])
                                if verif(position_p2_b3_1,position_p2_b3_2,position_p2_b3_3,4,map_p2[0])[1] == True:
                                    b3 = False
                                else:
                                    place_ship(index_game[0],'player2','B',position_p2_b3_1,position_p2_b3_2,position_p2_b3_3)
                                    b3= True
                            
                            map_p2_b4 = read_txt("./media/battleship/{}/map_player2.txt".format(game[2]))
                            while map_p2_b4[6] != 'aircraft_T':
                                position_p2_b4_1 = random.choice(abc)
                                position_p2_b4_2 = random.randint(0, 9)
                                position_p2_b4_3 = random.choice(["U","R"])
                                if verif(position_p2_b4_1,position_p2_b4_2,position_p2_b4_3,5,map_p2[0])[1] == True:
                                    b4 = False
                                else:
                                    place_ship(index_game[0],'player2','A',position_p2_b4_1,position_p2_b4_2,position_p2_b4_3)
                                    b4= True
                                    
                            await self.message_p2_2.edit(content=see(look_map("player2",game[2])))
                            await self.info_p2.edit(content = "> :grey_exclamation: Tous les bateaux sont placés. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) #Erreur Type 2
                            await ctx.message.delete()
                    # --Aucun
                    else: # La personne n'est ni le joueur 1 ni le joueur 2
                            await ctx.send("> :no_entry: Vous n'être pas la bonne personnes \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) #Erreur Type 1 
                            await ctx.message.delete() 
                else: # Pas le bon server
                    await ctx.send("> :no_entry: La partie n'est pas sur ce server, réessayer sur le bon server. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) #Erreur Type 1
                    await ctx.message.delete()
            else:
                # Le code ne correspond à aucune partie existante. 
                await ctx.send("> :no_entry: Aucune partie n'a été trouver avec ce code. \n > :grey_exclamation: Commande effectué: `{}`".format(ctx.message.content)) #Erreur Type 1
                await ctx.message.delete()

#================================================================================
#Différente fonction pour le jeux

def creation(player,id):
    write_txt("./media/battleship/{}/map_{}.txt".format(id,player),"[[],[]]")
    map = read_txt("./media/battleship/{}/map_{}.txt".format(id,player))
    for a in range(10):
        map[0].append([])
        map[1].append([])
    map.append('patrol_F')
    map.append('submarine_F')
    map.append('destroyer_F')
    map.append('battleship_F')
    map.append('aircraft_F')
    map.append('done_F')

    for a in range(10):
        for b in range(10):
            map[0][a].append(":blue_square:")
            map[1][a].append(":purple_square:")

    write_txt("./media/battleship/{}/map_{}.txt".format(id,player),str(map))

def look_map(player,id):
    map = read_txt("./media/battleship/{}/map_{}.txt".format(id,player))
    return map[0]

def look_map_enemy(player,id):
    map = read_txt("./media/battleship/{}/map_{}.txt".format(id,player))
    return map[1]

def place_ship(id,player,bateau,where1,where2,position):
    map_place = read_txt("./media/battleship/{}/map_{}.txt".format(id,player))
    if bateau == 'P':
        if verif(where1,where2,position,2,map_place[0])[1] is False:
            place00001=place00011 = abc.index(where1) 
            place00002=place00022 = int(where2)
            if position == "U":
                place00011 -= 1
            elif position == "R":
                place00022 += 1
            map_place[0][place00001][place00002] = ":green_square:"
            map_place[0][place00011][place00022] = ":green_square:"
            map_place[2] = 'patrol_T'
            write_txt("./media/battleship/{}/map_{}.txt".format(id,player),str(map_place))
        else:
            return verif(where1,where2,position,2,map_place[0])[0]
    elif bateau == 'S':
        if verif(where1,where2,position,3,map_place[0])[1] is False:
            place00001=place00011=place00111 = abc.index(where1)
            place00002=place00022=place00222 = int(where2)
            if position == "U":
                place00011 -= 1
                place00111 -= 2
            elif position == "R":
                place00022 += 1
                place00222 += 2
            map_place[0][place00001][place00002] = ":yellow_square:"
            map_place[0][place00011][place00022] = ":yellow_square:"
            map_place[0][place00111][place00222] = ":yellow_square:"
            map_place[3] = 'submarine_T'
            write_txt("./media/battleship/{}/map_{}.txt".format(id,player),str(map_place))
        else:
            return verif(where1,where2,position,3,map_place[0])[0]

    elif bateau == 'D':
        if verif(where1,where2,position,3,map_place[0])[1] is False:
            place00001=place00011=place00111 = abc.index(where1)
            place00002=place00022=place00222 = int(where2)
            if position == "U":
                place00011 -= 1
                place00111 -= 2
            elif position == "R":
                place00022 += 1
                place00222 += 2
            map_place[0][place00001][place00002] = ":orange_square:"
            map_place[0][place00011][place00022] = ":orange_square:"
            map_place[0][place00111][place00222] = ":orange_square:"
            map_place[4] = 'destroyer_T'
            write_txt("./media/battleship/{}/map_{}.txt".format(id,player),str(map_place))
        else:
            return verif(where1,where2,position,3,map_place[0])[0]

    elif bateau == 'B':
        if verif(where1,where2,position,4,map_place[0])[1] is False:
            place00001=place00011=place00111=place01111 = abc.index(where1)
            place00002=place00022=place00222=place02222 = int(where2)
            if position == "U":
                place00011 -= 1
                place00111 -= 2
                place01111 -= 3
            elif position == "R":
                place00022 += 1
                place00222 += 2
                place02222 += 3
            map_place[0][place00001][place00002] = ":black_large_square:"
            map_place[0][place00011][place00022] = ":black_large_square:"
            map_place[0][place00111][place00222] = ":black_large_square:"
            map_place[0][place01111][place02222] = ":black_large_square:"
            map_place[5] = 'battleship_T'
            write_txt("./media/battleship/{}/map_{}.txt".format(id,player),str(map_place))
        else:
            return verif(where1,where2,position,4,map_place[0])[0]

    elif bateau == 'A':
        if verif(where1,where2,position,5,map_place[0])[1] is False:
            place00001=place00011=place00111=place01111=place11111 = abc.index(where1)
            place00002=place00022=place00222=place02222=place22222 = int(where2)
            if position == "U":
                place00011 -= 1
                place00111 -= 2
                place01111 -= 3
                place11111 -= 4
            elif position == "R":
                place00022 += 1
                place00222 += 2
                place02222 += 3
                place22222 += 4
            map_place[0][place00001][place00002] = ":white_large_square:"
            map_place[0][place00011][place00022] = ":white_large_square:"
            map_place[0][place00111][place00222] = ":white_large_square:"
            map_place[0][place01111][place02222] = ":white_large_square:"
            map_place[0][place11111][place22222] = ":white_large_square:"
            map_place[6] = 'aircraft_T'
            write_txt("./media/battleship/{}/map_{}.txt".format(id,player),str(map_place))
        else:
            return verif(where1,where2,position,5,map_place[0])[0]

    else: return "Erreur majeur"

def see(map_arg):
    #afficher la map du jeu avec les indications A-->J et 0-->9
    map = ""
    l = [":regional_indicator_a:",":regional_indicator_b:",":regional_indicator_c:",":regional_indicator_d:",":regional_indicator_e:",":regional_indicator_f:",":regional_indicator_g:",":regional_indicator_h:",":regional_indicator_i:",":regional_indicator_j:",]
    ll = [":arrow_upper_right:",":zero:",":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:"]
    ligne = "> "
    for a in range(10):
        ligne = "> {}".format(l[a])
        for b in range(10):
            ligne += map_arg[a][b]
        map += "{}\n".format(ligne)
    map += "> "
    for k in range(11):
        map += "{}".format(ll[k])
    return map

def verif(p1,p2,direction,longueur,map):
    #renvoie True si un erreur est trouver dans le positionnement du bateau et False quand il n'y a pas d'erreur
    error = ["aucune erreur",False]
    try:
        pl1 = abc.index(p1)
    except:
        error = ["Valeur alphabétique fausse !",True]
        return error

    if int(p2) < 0 or int(p2) > 9:
        error = ["Valeur numérique fausse !",True]
        return error

    if int(p2) >= 10 or int(pl1) < 0:
        error = ["le problème est ici",True]
        return error

    if direction == 'U':
        if int(pl1) == 0:
            error = ["Hors du jeu",True]
            return error
        for k in range(0,longueur):
            val = int(pl1)-k
            if val >= 0:
                if map[int(pl1)-k][int(p2)] != ':blue_square:':
                    error = ["Un bateau prend déjà cet emplacement !",True]
            else:
                error = ["Hors du jeu 2",True]

    elif direction == 'R':
        if int(p2) == 9:
            error = ["Hors du jeu",True]
            return error
        for k in range(0,longueur):
            if int(p2)+k <= 9:
                if map[int(pl1)][int(p2)+k] != ':blue_square:':
                    error = ["Un bateau prend déjà cet emplacement !",True]
            else:
                error = ["Hors du jeu 2",True]
    else:
        error = ["La direction doit etre soit 'up' soit 'right'",True]
    return error

#================================================================================
def read_txt(chemin):
    #lire un ficher .txt / retourne une list
    txt = open(chemin)
    return eval(txt.read())

def write_txt(chemin,message):
    #fonction pour écrire dans un ficher .txt au format utf-8
    txt = open(chemin,'w',encoding="utf-8")
    txt.write(message)

#================================================================================
# Fonction pour que le bot prenne en compte battleship.py
def setup(bot):
    bot.add_cog(bats(bot))

#FIN ============================================================================