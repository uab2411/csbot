import json

from discord.ext import commands

from lib.cs_server_connector import CS_Server_Connector


class CS_Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setserverip(self, ctx, ip, port=None):
        with open('data/serverips.json', 'r') as f:
            serverip = json.load(f)

        print(serverip)
        serverip[str(ctx.guild.id)] = [ip, int(port)]

        with open('data/serverips.json', 'w') as f:
            json.dump(serverip, f, indent=4)

        await ctx.send(f'Ip changed to {[ip, port]}')

    @commands.command()
    async def cscheck(self, ctx):
        with open('data/serverips.json', 'r') as f:
            serverips = json.load(f)

        if str(ctx.guild.id) in serverips:
            serverip = serverips[str(ctx.guild.id)]
            cscon = CS_Server_Connector(serverip)
            info = cscon.get_game_info()
            await ctx.send(f'Server Name : {info["serv_name"]}\tCurrent Map : {info["map"]}\nPlayer Count : '
                           f'{info["player_count"]}\tMax Players : {info["max_players"]}\nBot Count : '
                           f'{info["bot_count"]}\tPing : {round(float(info["ping"]), 3)}')


def setup(client):
    client.add_cog(CS_Server(client))
