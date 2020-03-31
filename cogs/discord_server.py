import json

from discord.ext import commands


class Discord_Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['banni', 'aadva'])
    async def yodhare(self, ctx):
        await ctx.send('''**Aadlikke banni!!**
        Click and Connect-
        steam://connect/173.199.107.90:27045/munichabc
        ''')

    # @commands.command()
    # async def kick(self, ctx, member : discord.Member, *, reason=None):
    #     await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        print(prefixes)
        prefixes[str(ctx.guild.id)] = prefix

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix changed to {prefix}')


def setup(client):
    client.add_cog(Discord_Server(client))
