import json
import valve.rcon

import discord
from discord.ext import commands

from lib.cs_server_connector import CS_Server_Connector


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
                    a= rcon.execute(command)
                    print(a)
                    return 1, None
            except Exception as e:
                return 0, e
        else:
            return -1, None

    async def send_status(self,ctx,success,error,success_msg,fail_msg):
        if success == 1:
            await ctx.send(success_msg)
        elif success == 0:
            print(error)
            await ctx.send(fail_msg)
        else:
            await ctx.send(f'Set server ip first!')

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
            self.serverips[str(ctx.guild.id)]["password"] = password
            with open('data/serverips.json', 'w') as f:
                json.dump(self.serverips, f, indent=4)
            await ctx.send(f'Rcon password set!')
        else:
            await ctx.send(f'Set server ip first!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setsrvpassword(self, ctx, *, password):

        if str(ctx.guild.id) in self.serverips:
            self.serverips[str(ctx.guild.id)]["srv_password"] = password
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
        success_msg = 'Bots kicked! Enjoy!'
        fail_msg = 'Something went wrong!'
        await self.send_status(ctx,success,error,success_msg,fail_msg)


    @commands.command()
    async def console(self, ctx,*,command):
        guild_id = str(ctx.guild.id)
        success, error = self.console_command(guild_id, command)
        success_msg = 'Command Executed!'
        fail_msg = 'Something went wrong!'
        await self.send_status(ctx,success,error,success_msg,fail_msg)


    @commands.command()
    async def maplist(self, ctx):
        embed = discord.Embed(title="CSGO Maps List", color=65280)
        embed.description = "To change map, send-\n.map mapname"
        embed.set_footer(
            text='Git : https://github.com/uab2411/csbot')

        for i,_map in enumerate(self.default_maps):
            embed.add_field(name=i+1,value = _map)

        # embed.add_field(name="Maps",value=map_str)
        await ctx.send(embed=embed)

    @commands.command()
    async def wsmaplist(self, ctx):
        embed = discord.Embed(title="CSGO Workshop Maps List", color=65280)
        embed.description = "To start Workshop map, send-\n.wsmap mapname"
        embed.set_footer(
            text='Git : https://github.com/uab2411/csbot')

        # for i, _map in enumerate(list(self.workshop_maps.keys())):
        #     embed.add_field(name=i + 1, value=_map)

        embed.add_field(name="Maps",value="\n".join(list(self.workshop_maps.keys())))
        await ctx.send(embed=embed)

    @commands.command()
    async def wsmap(self, ctx, mapname):
        guild_id = str(ctx.guild.id)
        map_id = self.workshop_maps.get(mapname,0)
        if map_id:
            command = "host_workshop_map " + str(map_id)
            success, error = self.console_command(guild_id, command)
            success_msg = 'Map Changed!'
            fail_msg = 'Something went wrong!'
            await self.send_status(ctx, success, error, success_msg, fail_msg)
        else:
            await ctx.send("Map not available. Send a link to the map, to add it!!")

    @commands.command()
    async def map(self, ctx, mapname):
        guild_id = str(ctx.guild.id)
        command = "changelevel " + mapname
        success, error = self.console_command(guild_id, command)
        success_msg = 'Map Changed!'
        fail_msg = 'Something went wrong!'
        await self.send_status(ctx, success, error, success_msg, fail_msg)

    @commands.command()
    async def csgocheck(self, ctx):
        with open('data/serverips.json', 'r') as f:
            serverips = json.load(f)

        if str(ctx.guild.id) in serverips:
            serverip = serverips[str(ctx.guild.id)]

            steam_link = f'steam://connect/{serverip["ip"]}'
            steam_link = (steam_link + f':{serverip["port"]}') if serverip["port"] else steam_link
            steam_link = (steam_link + f'/{serverip["srv_password"]}') if serverip["srv_password"] else steam_link

            embed = discord.Embed(title="CSGO Community server details", color=65280)
            embed.set_footer(
                text='Git : https://github.com/uab2411/csbot')

            cscon = CS_Server_Connector(serverip)
            info = cscon.get_game_info()
            players = info["players"]

            embed.add_field(name="Server Name", value=info["serv_name"])
            embed.add_field(name="Current Map", value=info["map"])
            embed.add_field(name="Ping", value=round(float(info["ping"]), 3))
            embed.add_field(name="Player Count", value=info["player_count"])
            embed.add_field(name="Max Players", value=info["max_players"])
            embed.add_field(name="Bot Count", value=info["bot_count"])

            if len(players) > 0:
                name = ""
                score = ""
                time = ""
                for player in players:
                    name += player.name + '\n'
                    score += str(player.score) + '\n'
                    time += str(int(player.duration / 60)) + ' min \n'
                embed.add_field(name="Player Name", value=name[:-1])
                embed.add_field(name="Score", value=score[:-1])
                embed.add_field(name="Playing since", value=time[:-1])

            embed.add_field(name="Link to connect", value=steam_link, inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Set server ip first!')


def setup(client):
    client.add_cog(CS_Server(client))
