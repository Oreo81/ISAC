import discord
import os.path
from datetime import *
from time import *
from discord.ext import commands
import random

abc = ["A","B","C","D","E","F","G","H","I","J"]

class bs():
    def __init__(self,id):
        write_txt("./media/battleship/{}_bs".format(id),"[[],[]]")
        self.if_player = id
        self.sea = []
        self.sea_enemy = []

    def cr_land(self):
        map = read_txt("./media/battleship/{}_bs".format(self.if_player))
        for a in range(10):
            map[0].append([])
            map[1].append([])
            map.append('patrol_F')
            map.append('submarine_F')
            map.append('destroyer_F')
            map.append('battleship_F')
            map.append('aircraft_F')

        for a in range(10):
            for b in range(10):
                map[0][a].append(":blue_square:")
                map[1][a].append(":purple_square:")

        write_txt("./media/battleship/{}_bs".format(self.if_player),str(map))

    def reset(self):
        self.sea = []
        self.sea.append([])

    # def look_land(self):
    #     for a in range(10):
    #         print(self.sea[a], end="\n")

    # def look_land_enemy(self):
    #     for a in range(10):
    #         print(self.sea_enemy[a], end="\n")

    def look(self):
        map = read_txt("./media/battleship/{}_bs".format(self.if_player))
        return map[0]

    def look_enemy(self):
        map = read_txt("./media/battleship/{}_bs".format(self.if_player))
        return map[1]

    def tir(self,where1,where2,map_enemy):
        try:
            p1 = abc.index(where1)
        except:
            return "Karim tu veux vraiment aller dans la cuisinière ?"
        
        if where2 >= 0 and where2 <= 9:
                p2= where2
        else:
            return "Nope"

        if self.sea_enemy[p1][p2] != ':purple_square:':
            return "déjà tiré ici"
        elif map_enemy[p1][p2] == ':blue_square:':
            self.sea_enemy[p1][p2] = ':blue_square:'
        elif map_enemy[p1][p2] != ':blue_square:':
            self.sea_enemy[p1][p2] = ':blue_square:'

    def place_ship(self,bateau,where1,where2,position):
        map_place = read_txt("./media/battleship/{}_bs".format(self.if_player))
        print(map_place)
        print('--------------------')
        if bateau == 'P':
            # print(map_place[0])
            # print('--------------------')
            if verif(where1,where2,position,2,map_place[0])[1] is False:
                place00001=place00011 = abc.index(where1) 
                place00002=place00022 = int(where2)
                if position == "U":
                    place00011 -= 1
                elif position == "R":
                    place00022 += 1
                map_place[0][place00001][place00002] = ":green_square:"
                map_place[0][place00011][place00022] = ":green_square:"
                print(map_place[0])
                write_txt("./media/battleship/{}_bs".format(self.if_player),str(map_place))
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
                write_txt("./media/battleship/{}_bs".format(self.if_player),str(map_place))
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
                write_txt("./media/battleship/{}_bs".format(self.if_player),str(map_place))
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
                write_txt("./media/battleship/{}_bs".format(self.if_player),str(map_place))
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
                elif position == "R":
                    place00022 += 1
                    place00222 += 2
                    place02222 += 3
                map_place[0][place00001][place00002] = ":white_large_square:"
                map_place[0][place00011][place00022] = ":white_large_square:"
                map_place[0][place00111][place00222] = ":white_large_square:"
                map_place[0][place01111][place02222] = ":white_large_square:"
                map_place[0][place11111][place22222] = ":white_large_square:"
                write_txt("./media/battleship/{}_bs".format(self.if_player),str(map_place))
            else:
                return verif(where1,where2,position,5,map_place[0])[0]

        else: return "Erreur majeur"


#------------------------------------------------------
    # def place_patrol(self,where1,where2,position):
    #     if verif(where1,where2,position,2,self.sea)[1] is False:
    #         place00001=place00011 = abc.index(where1) 
    #         place00002=place00022 = where2
    #         if position == "U":
    #             place00011 -= 1
    #         elif position == "R":
    #             place00022 += 1
    #         self.sea[place00001][place00002] = ":green_square:"
    #         self.sea[place00011][place00022] = ":green_square:"
    #     else:
    #         return verif(where1,where2,position,2,self.sea)[0]

#------------------------------------------------------
    # def place_submarine(self,where1,where2,position):
    #     if verif(where1,where2,position,3,self.sea)[1] is False:
    #         place00001=place00011=place00111 = abc.index(where1)
    #         place00002=place00022=place00222 = where2
    #         if position == "U":
    #             place00011 -= 1
    #             place00111 -= 2
    #         elif position == "R":
    #             place00022 += 1
    #             place00222 += 2
    #         self.sea[place00001][place00002] = ":yellow_square:"
    #         self.sea[place00011][place00022] = ":yellow_square:"
    #         self.sea[place00111][place00222] = ":yellow_square:"
    #     else:
    #         return verif(where1,where2,position,3,self.sea)[0]

#------------------------------------------------------
    # def place_destroyer(self,where1,where2,position):
        # if verif(where1,where2,position,3,self.sea)[1] is False:
        #     place00001=place00011=place00111 = abc.index(where1)
        #     place00002=place00022=place00222 = where2
        #     if position == "U":
        #         place00011 -= 1
        #         place00111 -= 2
        #     elif position == "R":
        #         place00022 += 1
        #         place00222 += 2
        #     self.sea[place00001][place00002] = ":orange_square:"
        #     self.sea[place00011][place00022] = ":orange_square:"
        #     self.sea[place00111][place00222] = ":orange_square:"
        # else:
        #     return verif(where1,where2,position,3,self.sea)[0]

#------------------------------------------------------
#     def place_battleship(self,where1,where2,position):
#         if verif(where1,where2,position,4,self.sea)[1] is False:
#             place00001=place00011=place00111=place01111 = abc.index(where1)
#             place00002=place00022=place00222=place02222 = where2
#             if position == "U":
#                 place00011 -= 1
#                 place00111 -= 2
#                 place01111 -= 3
#             elif position == "R":
#                 place00022 += 1
#                 place00222 += 2
#                 place02222 += 3
#             self.sea[place00001][place00002] = ":black_large_square:"
#             self.sea[place00011][place00022] = ":black_large_square:"
#             self.sea[place00111][place00222] = ":black_large_square:"
#             self.sea[place01111][place02222] = ":black_large_square:"
#         else:
#             return verif(where1,where2,position,4,self.sea)[0]

# #------------------------------------------------------
#     def place_aircraft(self,where1,where2,position):
#         if verif(where1,where2,position,5,self.sea)[1] is False:
#             place00001=place00011=place00111=place01111=place11111 = abc.index(where1)
#             place00002=place00022=place00222=place02222=place22222 = where2
#             if position == "U":
#                 place00011 -= 1
#                 place00111 -= 2
#                 place01111 -= 3
#             elif position == "R":
#                 place00022 += 1
#                 place00222 += 2
#                 place02222 += 3
#             self.sea[place00001][place00002] = ":white_large_square:"
#             self.sea[place00011][place00022] = ":white_large_square:"
#             self.sea[place00111][place00222] = ":white_large_square:"
#             self.sea[place01111][place02222] = ":white_large_square:"
#             self.sea[place11111][place22222] = ":white_large_square:"
#         else:
#             return verif(where1,where2,position,5,self.sea)[0]

#------------------------------------------------------
def verif(p1,p2,direction,longueur,map):
    error = ["aucune erreur",False]
    try:
        pl1 = abc.index(p1)
    except:
        error = ["Valeur alphabétique fausse !",True]

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
            if map[int(pl1)-k][int(p2)] != ':blue_square:':
                error = ["Un bateau prend déjà cet emplacement !",True]

    elif direction == 'R':
        if int(p2) == 9:
            error = ["Hors du jeu",True]
            return error
        for k in range(0,longueur):
            if map[int(pl1)][int(p2)+k] != ':blue_square:':
                error = ["Un bateau prend déjà cet emplacement !",True]
    else:
        error = ["La direction doit etre soit 'up' soit 'right'",True]
    return error

class bats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog BS Ready!')

    @commands.command(name="battleship",aliases=['bs'])
    @commands.guild_only()
    async def battleship(self,ctx,*input):
        Player1 = bs(ctx.author.id)
        
        secret_code = ""
        secret_code_fore_role = ""
        if not input:
            await ctx.send("> \U000026A0 Pour plus d'information: py!h bs \n > /!\ Attention, la commande ne marchera pas !")
        elif input[0] == 'create' or input[0] == 'c':
            if os.path.isfile("./media/battleship/{}.txt".format(ctx.author.id)):
                await ctx.send("> \U000026D4 Une partie est deja en créer pour vous. Pour l'arréter: `py!bs d`")
            else:
                Player1.cr_land()
                secret_code_fore_role = random.randint(1000,9999)
                secret_code = random.randint(1000,9999)
                overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),}

                await ctx.guild.create_role(name="P1_{}".format(secret_code_fore_role))
                await ctx.guild.create_role(name="P2_{}".format(secret_code_fore_role))
                await ctx.guild.create_category("game_{}".format(secret_code_fore_role))

                category = discord.utils.get(ctx.guild.categories, name = "game_{}".format(secret_code_fore_role))
                role_p1 = discord.utils.get(ctx.guild.roles, name="P1_{}".format(secret_code_fore_role))
                role_p2 = discord.utils.get(ctx.guild.roles, name="P2_{}".format(secret_code_fore_role))

                await ctx.guild.create_text_channel("game_P1_{}".format(secret_code_fore_role), category = category, overwrites=overwrites)
                await ctx.guild.create_text_channel("game_P2_{}".format(secret_code_fore_role), category = category, overwrites=overwrites)

                salon_p1 = discord.utils.get(ctx.guild.channels, name="game_p1_{}".format(secret_code_fore_role))
                salon_p2 = discord.utils.get(ctx.guild.channels, name="game_p2_{}".format(secret_code_fore_role))

                await salon_p1.set_permissions(role_p1, read_messages=True)
                await salon_p1.set_permissions(role_p2, read_messages=False)
                await salon_p2.set_permissions(role_p1, read_messages=False)
                await salon_p2.set_permissions(role_p2, read_messages=True)

                await ctx.author.add_roles(role_p1)

                write_txt("./media/battleship/{}.txt".format(ctx.author.id),"[]")
                edit = read_txt("./media/battleship/{}.txt".format(ctx.author.id))

                edit.append("{}".format(secret_code))
                edit.append("{}".format(secret_code_fore_role))
                edit.append("F")
                edit.append("None")
                edit.append("{}".format(ctx.message.guild.id))

                write_txt("./media/battleship/{}.txt".format(ctx.author.id),str(edit))

                await ctx.send("> \U00002705 Code pour rejoindre la partie envoyer en message privé. Vous êtes maintenant le joueur 1 ! (id de la partie: {})".format(secret_code_fore_role))
                await ctx.author.send("> \U00002755 Voici le code de votre partie `{}`".format(secret_code))

                know_game_with_code = read_txt("./media/battleship/link.txt")
                know_game_with_code.append(["{}".format(ctx.author.id),"{}".format(secret_code),"{}".format(ctx.message.guild.id)])

                write_txt("./media/battleship/link.txt",str(know_game_with_code))

        elif input[0] == 'join' or input[0] == 'j':
            mylist = read_txt("./media/battleship/link.txt")
            if mylist == []:
                 await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs j [code]`")
            else:
                for k in mylist:        
                    try:
                        if input[1] == k[1]:
                            try:
                                if str(k[0]) != str(ctx.author.id):
                                    try:
                                        if str(ctx.message.guild.id) == str(k[2]):
                                            edit = read_txt("./media/battleship/{}.txt".format(k[0]))
                                            if edit[2] == 'T':
                                                await ctx.send("> \U000026D4 Il y a déjà un deuxième joureur dans cette partie !\n <@{}> P1 et <@{}> P2".format(k[0],edit[3]))
                                            else:
                                                salon_p1 = discord.utils.get(ctx.guild.channels, name="game_p1_{}".format(edit[1]))
                                                salon_p2 = discord.utils.get(ctx.guild.channels, name="game_p2_{}".format(edit[1]))
                                                role_p2 = discord.utils.get(ctx.guild.roles, name="P2_{}".format(edit[1]))
                                                edit[2] = 'T'
                                                edit[3] = '{}'.format(ctx.author.id)
                                                write_txt("./media/battleship/{}.txt".format(k[0]),str(edit))
                                                await ctx.author.add_roles(role_p2)
                                                await ctx.send("> \U00002705 Vous êtes maintenant le joueur 2 ! (id de la partie: {}) \n> <@{}> est premier joueur et <@{}> le deuxième.".format(edit[1],k[0],edit[3]))
                                                await salon_p1.send("> \U00002755 <@{}> Vous pouvez jouer ici dès maintenant. `py!bs p` [bateau + info] pour plus d'info `py!h bs`".format(k[0]))
                                                await salon_p2.send("> \U00002755 <@{}> Vous pouvez jouer ici dès maintenant. `py!bs p` [bateau + info] pour plus d'info `py!h bs`".format(edit[3]))
                                        else:
                                            await ctx.send("> \U000026D4 La partie n'est pas sur ce server, réessayer sur le bon server.")
                                    except:
                                        await ctx.send("> \U000026D4 Vous n'êtes pas la personnes")
                                else: await ctx.send("> \U000026D4 Le créateur de la partie ne peux pas etre le deuxième joueur")
                            except:
                                print("erreur 01")
                        else: 
                            await ctx.send("> \U000026D4 Il ce peut que le code ne correspond à aucune partie.")
                    except:
                        await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs j [code]`")

        elif input[0] == 'leave' or input[0] == 'l':
            mylist = read_txt("./media/battleship/link.txt")
            if mylist == []:
                await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs l [code]`")
            else:
                for k in mylist:
                    try:
                        if input[1] == k[1]:
                            try:
                                if str(k[0]) != str(ctx.author.id):
                                    try:
                                        edit = read_txt("./media/battleship/{}.txt".format(k[0]))
                                        if str(edit[3]) != str(ctx.author.id):
                                            await ctx.send("> \U000026D4 Vous n'êtes pas le deuxième joueur de cette partie.")
                                        else:
                                            role_p2 = discord.utils.get(ctx.guild.roles, name="P2_{}".format(edit[1]))
                                            edit[2] = 'F'
                                            edit[3] = "None"
                                            write_txt("./media/battleship/{}.txt".format(k[0]),str(edit))
                                            await ctx.author.remove_roles(role_p2)
                                            await ctx.send("> \U00002755 Vous n'êtes plus le joueur 2 ! (id de la partie: {})".format(edit[1]))
                                    except:
                                        await ctx.send("> Erreur 0")
                                else:
                                    await ctx.send("> \U000026D4 Le créateur de la partie ne peux pas faire cette commande, pour finir et supprimer la partie: `py!bs d`")
                            except: 
                                await ctx.send("> Erreur 1")
                        else:
                            await ctx.send("> \U000026D4 Le code `{}` n'est pas valide. Il se peut que le code n'est lié à aucune partie.".format(input[1]))
                    except: 
                        await ctx.send("> \U000026A0 Pour plus d'information `py!h bs`. Pour que la commande marche correctement `py!bs l [code]`")


        elif input[0] == 'delete' or input[0] == 'd':
            if not os.path.isfile("./media/battleship/{}.txt".format(ctx.author.id)):
                await ctx.send("> \U000026D4 Vous n'avez pas créé de partie, pour en créer une `py!bs c`")
            else:
                edit = read_txt("./media/battleship/{}.txt".format(ctx.author.id))

                role_p1 = discord.utils.get(ctx.guild.roles, name="P1_{}".format(edit[1]))
                role_p2 = discord.utils.get(ctx.guild.roles, name="P2_{}".format(edit[1]))
                salon_p1 = discord.utils.get(ctx.guild.channels, name="game_p1_{}".format(edit[1]))
                salon_p2 = discord.utils.get(ctx.guild.channels, name="game_p2_{}".format(edit[1]))
                cat_game = discord.utils.get(ctx.guild.categories, name ="game_{}".format(edit[1]))

                await role_p1.delete()
                await role_p2.delete()
                await salon_p1.delete()
                await salon_p2.delete()
                await cat_game.delete()

                mylist = read_txt("./media/battleship/link.txt")
                for k in mylist:
                    if str(edit[0]) == k[1]:
                        mylist.remove(k)
                    else:
                        await ctx.send("> Une erreur est survenue ligne 302")
                write_txt("./media/battleship/link.txt",str(mylist))
                os.remove("./media/battleship/{}.txt".format(ctx.author.id))
                os.remove("./media/battleship/{}_bs".format(ctx.author.id))
                await ctx.send("> \U00002705 Partie terminé et supprimé.")

        elif input[0] == 'place' or input[0] == 'p':
            print((str(input[1][0]),str(input[1][1]),int(input[1][2]),str(input[1][3])))
            erreur = Player1.place_ship(str(input[1][0]),str(input[1][1]),str(input[1][2]),str(input[1][3]))
            if erreur == True:
                err = await ctx.send("> Tu as mit: {} \n{}".format(input[1],erreur[0]))
            else:
                await ctx.send("c ok")

            await ctx.send(see(Player1.look()))
            # await ctx.send('pas fini')

        elif input[0] == 'map' or input[0] == 'm':
            mapp1 = Player1.look()
            visual_enemy = await ctx.send(see(Player1.look_enemy()))
            visual = await ctx.send(see(Player1.look()))
            

    # @commands.command(name="battleship",aliases=['bs'])
    # @commands.guild_only()
    # async def battleship(self,ctx):
    #     P1 = bs()
    #     P1.cr_land()
    #     P2 = bs()
    #     P2.cr_land()
    #     mapp2 = P2.look()

    #     patrol = "no_ok"
    #     submarine = "no_ok"
    #     destroyer = "no_ok"
    #     battleship = "no_ok"
    #     aircraft = "no_ok"
    #     validation = "no"

    #     while validation == "no":
    #         mapp1 = P1.look()
    #         patrol = "no_ok"
    #         submarine = "no_ok"
    #         destroyer = "no_ok"
    #         battleship = "no_ok"
    #         aircraft = "no_ok"
    #         while patrol == "no_ok":
    #             demande_bateau1 = await ctx.send('> Emplacement bateau 1 (10sec) format (EX: B4U)')
    #             reponse_bateau1 = await self.bot.wait_for('message')
    #             content_reponse_b1 = reponse_bateau1.content
    #             if content_reponse_b1 == "map":
    #                 visual = await ctx.send(see(P1.look()))
    #                 demande_bateau11 = await ctx.send('> Emplacement bateau 1 (10sec) format (EX: B4U)')
    #                 reponse_bateau11 = await self.bot.wait_for('message')
    #                 content_reponse_b1 = reponse_bateau11.content
    #                 erreur = verif(content_reponse_b1[0],int(content_reponse_b1[1]),content_reponse_b1[2],2,mapp1)
    #                 await visual.delete()
    #                 await demande_bateau11.delete()
    #                 await reponse_bateau11.delete()
    #             else:
    #                 erreur = verif(content_reponse_b1[0],int(content_reponse_b1[1]),content_reponse_b1[2],2,mapp1)
    #                 try:
    #                     await visual.delete()
    #                 except:
    #                     pass

    #             if erreur[1] is True:
    #                 await demande_bateau1.delete()
    #                 await reponse_bateau1.delete()
    #                 err = await ctx.send("> Tu as mit: {} \n{}".format(content_reponse_b1,erreur[0]))
    #             else:
    #                 patrol = "ok"

    #         b1 = await ctx.send("> Patrol placé case {}.".format(content_reponse_b1))
    #         await demande_bateau1.delete()
    #         await reponse_bateau1.delete()
    #         try:
    #             await err.delete()
    #         except:
    #             pass

    #         P1.place_patrol(content_reponse_b1[0],int(content_reponse_b1[1]),content_reponse_b1[2])

    #         while submarine == "no_ok":
    #             demande_bateau2 = await ctx.send('> Emplacement bateau 2 (10sec) format (EX: B4U)')
    #             reponse_bateau2 = await self.bot.wait_for('message')
    #             content_reponse_b2 = reponse_bateau2.content
    #             if content_reponse_b2 == "map":
    #                 visual = await ctx.send(see(P1.look()))
    #                 demande_bateau22 = await ctx.send('> Emplacement bateau 2 (10sec) format (EX: B4U)')
    #                 reponse_bateau22 = await self.bot.wait_for('message')
    #                 content_reponse_b2 = reponse_bateau22.content
    #                 erreur = verif(content_reponse_b2[0],int(content_reponse_b2[1]),content_reponse_b2[2],2,mapp1)
    #                 await visual.delete()
    #                 await demande_bateau22.delete()
    #                 await reponse_bateau22.delete()
    #             else:
    #                 erreur = verif(content_reponse_b2[0],int(content_reponse_b2[1]),content_reponse_b2[2],2,mapp1)
    #                 try:
    #                     await visual.delete()
    #                 except:
    #                     pass

    #             if erreur[1] is True:
    #                 await demande_bateau2.delete()
    #                 await reponse_bateau2.delete()
    #                 err = await ctx.send("> Tu as mit: {} \n{}".format(content_reponse_b2,erreur[0]))
    #             else:
    #                 submarine = "ok"

    #         b2 = await ctx.send("> Submarine placé case {}.".format(content_reponse_b2))
    #         await demande_bateau2.delete()
    #         await reponse_bateau2.delete()
    #         try:
    #             await err.delete()
    #         except:
    #             pass
    #         P1.place_submarine(content_reponse_b2[0],int(content_reponse_b2[1]),content_reponse_b2[2])

    #         while destroyer == "no_ok":
    #             demande_bateau3 = await ctx.send('> Emplacement bateau 3 (10sec) format (EX: B4U)')
    #             reponse_bateau3 = await self.bot.wait_for('message')
    #             content_reponse_b3 = reponse_bateau3.content
    #             if content_reponse_b3 == "map":
    #                 visual = await ctx.send(see(P1.look()))
    #                 demande_bateau33 = await ctx.send('> Emplacement bateau 2 (10sec) format (EX: B4U)')
    #                 reponse_bateau33 = await self.bot.wait_for('message')
    #                 content_reponse_b3 = reponse_bateau33.content
    #                 erreur = verif(content_reponse_b3[0],int(content_reponse_b3[1]),content_reponse_b3[2],2,mapp1)
    #                 await visual.delete()
    #                 await demande_bateau33.delete()
    #                 await reponse_bateau33.delete()
    #             else:
    #                 erreur = verif(content_reponse_b3[0],int(content_reponse_b3[1]),content_reponse_b3[2],2,mapp1)
    #                 try:
    #                     await visual.delete()
    #                 except:
    #                     pass

    #             if erreur[1] is True:
    #                 await demande_bateau3.delete()
    #                 await reponse_bateau3.delete()
    #                 err = await ctx.send("> Tu as mit: {} \n{}".format(content_reponse_b3,erreur[0]))
    #             else:
    #                 destroyer = "ok"

    #         b3 = await ctx.send("> Destroyer placé case {}.".format(content_reponse_b3))
    #         await demande_bateau3.delete()
    #         await reponse_bateau3.delete()
    #         try:
    #             await err.delete()
    #         except:
    #             pass
    #         P1.place_destroyer(content_reponse_b3[0],int(content_reponse_b3[1]),content_reponse_b3[2])

    #         while battleship == "no_ok":
    #             demande_bateau4 = await ctx.send('> Emplacement bateau 4 (10sec) format (EX: B4U)')
    #             reponse_bateau4 = await self.bot.wait_for('message')
    #             content_reponse_b4 = reponse_bateau4.content
    #             if content_reponse_b4 == "map":
    #                 visual = await ctx.send(see(P1.look()))
    #                 demande_bateau44 = await ctx.send('> Emplacement bateau 2 (10sec) format (EX: B4U)')
    #                 reponse_bateau44 = await self.bot.wait_for('message')
    #                 content_reponse_b4 = reponse_bateau44.content
    #                 erreur = verif(content_reponse_b4[0],int(content_reponse_b4[1]),content_reponse_b4[2],2,mapp1)
    #                 await visual.delete()
    #                 await demande_bateau44.delete()
    #                 await reponse_bateau44.delete()
    #             else:
    #                 erreur = verif(content_reponse_b4[0],int(content_reponse_b4[1]),content_reponse_b4[2],2,mapp1)
    #                 try:
    #                     await visual.delete()
    #                 except:
    #                     pass
    #             if erreur[1] is True:
    #                 await demande_bateau4.delete()
    #                 await reponse_bateau4.delete()
    #                 err = await ctx.send("> Tu as mit: {} \n{}".format(content_reponse_b4,erreur[0]))
    #             else:
    #                 battleship = "ok"

    #         b4 = await ctx.send("> Battleship placé case {}.".format(content_reponse_b4))
    #         await demande_bateau4.delete()
    #         await reponse_bateau4.delete()
    #         try:
    #             await err.delete()
    #         except:
    #             pass
    #         P1.place_battleship(content_reponse_b4[0],int(content_reponse_b4[1]),content_reponse_b4[2])

    #         while aircraft == "no_ok":
    #             demande_bateau5 = await ctx.send('> Emplacement bateau 5 (10sec) format (EX: B4U)')
    #             reponse_bateau5 = await self.bot.wait_for('message')
    #             content_reponse_b5 = reponse_bateau5.content
    #             if content_reponse_b5 == "map":
    #                 visual = await ctx.send(see(P1.look()))
    #                 demande_bateau55 = await ctx.send('> Emplacement bateau 2 (10sec) format (EX: B4U)')
    #                 reponse_bateau55 = await self.bot.wait_for('message')
    #                 content_reponse_b5 = reponse_bateau22.content
    #                 erreur = verif(content_reponse_b5[0],int(content_reponse_b5[1]),content_reponse_b5[2],2,mapp1)
    #                 await visual.delete()
    #                 await demande_bateau55.delete()
    #                 await reponse_bateau55.delete()
    #             else:
    #                 erreur = verif(content_reponse_b5[0],int(content_reponse_b5[1]),content_reponse_b5[2],2,mapp1)
    #                 try:
    #                     await visual.delete()
    #                 except:
    #                     pass

    #             if erreur[1] is True:
    #                 await demande_bateau5.delete()
    #                 await reponse_bateau5.delete()
    #                 err = await ctx.send("> Tu as mit: {} \n{}".format(content_reponse_b5,erreur[0]))
    #             else:
    #                 aircraft = "ok"

    #         b5 = await ctx.send("> Aircraft placé case {}.".format(content_reponse_b5))
    #         await demande_bateau5.delete()
    #         await reponse_bateau5.delete()
    #         try:
    #             await err.delete()
    #         except:
    #             pass
    #         P1.place_aircraft(content_reponse_b5[0],int(content_reponse_b5[1]),content_reponse_b5[2])

    #         vali = "no"
    #         while vali == "no":
    #             demande_validation = await ctx.send('> Es ce bon ? (Y ou N)')
    #             visual = await ctx.send(see(P1.look()))
    #             reponse_validation = await self.bot.wait_for('message')
    #             content_reponse = reponse_validation.content
    #             if content_reponse == "Y":
    #                 validation = "ok"
    #                 vali = "ok"
    #                 await b1.delete()
    #                 await b2.delete()
    #                 await b3.delete()
    #                 await b4.delete()
    #                 await b5.delete()
    #                 await demande_validation.delete()
    #                 await reponse_validation.delete()
    #                 await visual.delete()
    #             elif content_reponse == "N":
    #                 await b1.delete()
    #                 await b2.delete()
    #                 await b3.delete()
    #                 await b4.delete()
    #                 await b5.delete()
    #                 vali = "ok"
    #                 P1.reset
    #             else:
    #                 await ctx.send('> La réponse doit etre Y ou N')
    #                 await demande_validation.delete()
    #                 await visual.delete()


    #     # try:
    #     P2.place_patrol("B",3,"U")

    #     P1.tir("B",3,mapp2)

    #     P2.tir("A",8,mapp1)
    #     P2.tir("C",4,mapp1)

    #     await ctx.send("> P1 ───────────────────")
    #     await ctx.send(see(P1.look_enemy()))
    #     await ctx.send("> ─────────────────────")
    #     await ctx.send(see(P1.look()))

    #     # await ctx.send("> P2 ───────────────────")
    #     # await ctx.send(see(P2.look_enemy()))
    #     # await ctx.send("> ─────────────────────")
    #     # await ctx.send(see(P2.look()))

    #     # except:
    #     #     print("pass")

def see(map_arg):
    map = ""
    l = [":regional_indicator_a:",
        ":regional_indicator_b:",
        ":regional_indicator_c:",
        ":regional_indicator_d:",
        ":regional_indicator_e:",
        ":regional_indicator_f:",
        ":regional_indicator_g:",
        ":regional_indicator_h:",
        ":regional_indicator_i:",
        ":regional_indicator_j:",]

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

def read_txt(chemin):
    txt = open(chemin)
    return eval(txt.read())

def write_txt(chemin,message):
    txt = open(chemin,'w',encoding="utf-8")
    txt.write(message)


def setup(bot):
    bot.add_cog(bats(bot))





#FIN ============================================================================