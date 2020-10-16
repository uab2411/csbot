import json
import valve.rcon

import discord
from discord.ext import commands

from lib.cs_server_connector import CS_Server_Connector


class CS_Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    def get_server_details(self):


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setserverip(self, ctx, ip, port=None):
        with open('data/serverips.json', 'r') as f:
            serverip = json.load(f)

        print(serverip)
        serverip[str(ctx.guild.id)] = {
            "ip": ip,
            "port": int(port),
            "password": None
        }

        with open('data/serverips.json', 'w') as f:
            json.dump(serverip, f, indent=4)

        await ctx.send(f'Ip changed to {[ip, port]}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setserverpassword(self, ctx, *, password):
        with open('data/serverips.json', 'r') as f:
            serverip = json.load(f)

        if str(ctx.guild.id) in serverip:
            serverip[str(ctx.guild.id)]["password"] = password
            with open('data/serverips.json', 'w') as f:
                json.dump(serverip, f, indent=4)
            await ctx.send(f'Password set!')
        else:
            await ctx.send(f'Set server ip first!')

    # @commands.command()
    # async def cscheck(self, ctx):
    #     with open('data/serverips.json', 'r') as f:
    #         serverips = json.load(f)
    #
    #     if str(ctx.guild.id) in serverips:
    #         serverip = serverips[str(ctx.guild.id)]
    #
    #         steam_link = f'steam://connect/{serverip["ip"]}'
    #         steam_link = (steam_link + f':{serverip["port"]}') if serverip["port"] else steam_link
    #         steam_link = (steam_link + f'/{serverip["password"]}') if serverip["password"] else steam_link
    #
    #         embed = discord.Embed(title="Counter Strike 1.6 active server details", color=65280)
    #         embed.set_footer(
    #             text='Git : https://github.com/uab2411/csbot')
    #
    #         cscon = CS_Server_Connector(serverip)
    #         info = cscon.get_game_info()
    #         players = info["players"]
    #
    #         embed.add_field(name="Server Name", value=info["serv_name"])
    #         embed.add_field(name="Current Map", value=info["map"])
    #         embed.add_field(name="Ping", value=round(float(info["ping"]), 3))
    #         embed.add_field(name="Player Count", value=info["player_count"])
    #         embed.add_field(name="Max Players", value=info["max_players"])
    #         embed.add_field(name="Bot Count", value=info["bot_count"])
    #
    #         if len(players) > 0:
    #             name = ""
    #             score = ""
    #             time = ""
    #             for player in players:
    #                 name += player.name + '\n'
    #                 score += str(player.score) + '\n'
    #                 time += str(int(player.duration / 60)) + ' min \n'
    #             embed.add_field(name="Player Name", value=name[:-1])
    #             embed.add_field(name="Score", value=score[:-1])
    #             embed.add_field(name="Playing since", value=time[:-1])
    #
    #         embed.add_field(name="Link to connect", value=steam_link, inline=False)
    #
    #         await ctx.send(embed=embed)
    #     else:
    #         await ctx.send(f'Set server ip first!')

    @commands.command()
    async def kickbots(self, ctx):
        with open('data/serverips.json', 'r') as f:
            serverips = json.load(f)
        if str(ctx.guild.id) in serverips:

            serverip = serverips[str(ctx.guild.id)]
            ip = serverip["ip"]
            port = serverip["port"]
            password = serverip["password"]

            server_address = (ip,int(port))
            with valve.rcon.RCON(server_address, password) as rcon:
                print(rcon.connected)
                rcon.execute('bot_kick')
        else:
            await ctx.send(f'Set server ip first!')


def setup(client):
    client.add_cog(CS_Server(client))
