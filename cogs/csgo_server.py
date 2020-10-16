import json
import valve.rcon

import discord
from discord.ext import commands

#from lib.cs_server_connector import CS_Server_Connector


class CS_Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    #def get_server_details(self):


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
            try:
                with valve.rcon.RCON(server_address, password) as rcon:
                    rcon.execute('bot_kick')
                    await ctx.send(f'Bots kicked! Enjoy!!')
            except(Exception):
                await ctx.send(f'Something went wrong!')
        else:
            await ctx.send(f'Set server ip first!')


    @commands.command()
    async def console(self, ctx,*,command):
        with open('data/serverips.json', 'r') as f:
            serverips = json.load(f)
        if str(ctx.guild.id) in serverips:

            serverip = serverips[str(ctx.guild.id)]
            ip = serverip["ip"]
            port = serverip["port"]
            password = serverip["password"]

            server_address = (ip,int(port))
            try:
                with valve.rcon.RCON(server_address, password) as rcon:
                    rcon.execute(command)
                    await ctx.send(f'Command Executed!')
            except(Exception):
                await ctx.send(f'Something went wrong!')
        else:
            await ctx.send(f'Set server ip first!')


def setup(client):
    client.add_cog(CS_Server(client))
