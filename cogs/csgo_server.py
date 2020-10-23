import json
import valve.rcon

import discord
from discord.ext import commands

#from lib.cs_server_connector import CS_Server_Connector


class CS_Server(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open('data/csgo_data.json', 'r') as f:
            csgo_data = json.load(f)
            self.default_maps = csgo_data["default_maps"]
            self.workshop_maps = csgo_data["workshop_maps"]

        with open('data/serverips.json', 'r') as f:
            self.serverips = json.load(f)

    #def get_server_details(self):
    
    def get_server_details(self,guild_id):
        if str(guild_id) in self.serverips:
            serverip = self.serverips[guild_id]
            ip = serverip["ip"]
            port = serverip["port"]
            password = serverip["password"]

            server_address = (ip, int(port))
            return server_address, password
        else:
            return 0

    def console_command(self,guild_id,command):
        server_address, password = self.get_server_details(guild_id)
        if server_address:
            try:
                with valve.rcon.RCON(server_address, password) as rcon:
                    rcon.execute(command)
                    return 1, None
            except Exception as e:
                return 0, e
        else:
            return -1, None



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setserverip(self, ctx, ip, port=None):
        self.serverips[str(ctx.guild.id)] = {
            "ip": ip,
            "port": int(port),
            "password": None,
            "srv_password": None
        }

        with open('data/serverips.json', 'w') as f:
            json.dump(self.serverips, f, indent=4)

        await ctx.send(f'Ip changed to {[ip, port]}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setrconpassword(self, ctx, *, password):

        if str(ctx.guild.id) in self.serverips:
            self.serverips[str(ctx.guild.id)]["srv_password"] = password
            with open('data/serverips.json', 'w') as f:
                json.dump(self.serverips, f, indent=4)
            await ctx.send(f'Rcon password set!')
        else:
            await ctx.send(f'Set server ip first!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setsrvpassword(self, ctx, *, password):

        if str(ctx.guild.id) in self.serverips:
            self.serverips[str(ctx.guild.id)]["password"] = password
            with open('data/serverips.json', 'w') as f:
                json.dump(self.serverips, f, indent=4)
            await ctx.send(f'Server Password set!')
        else:
            await ctx.send(f'Set server ip first!')

    @commands.command()
    async def kickbots(self, ctx):
        guild_id = str(ctx.guild.id)
        command = "bot_kick"
        success, error = self.console_command(guild_id,command)
        if success == 1:
            await ctx.send(f'Bots kicked! Enjoy!')
        elif success == 0:
            print(error)
            await ctx.send(f'Something went wrong!')
        else:
            await ctx.send(f'Set server ip first!')


    @commands.command()
    async def console(self, ctx,*,command):
        guild_id = str(ctx.guild.id)
        success, error = self.console_command(guild_id, command)
        if success == 1:
            await ctx.send(f'Command Executed!')
        elif success == 0:
            print(error)
            await ctx.send(f'Something went wrong!')
        else:
            await ctx.send(f'Set server ip first!')



def setup(client):
    client.add_cog(CS_Server(client))
