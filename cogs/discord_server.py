import datetime
import json
import time

import pytz
from discord.ext import commands, tasks


class Discord_Server(commands.Cog):

    def __init__(self, client):
        self.client = client

        # self.send_reminder.start()

    # @commands.command(aliases=['banni', 'aadva'])
    # async def yodhare(self, ctx):
    #     await ctx.send('''**Aadlikke banni!!**
    #     Click and Connect-
    #     steam://connect/173.199.107.90:27045/munichabc
    #     ''')

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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setreminder(self, ctx, date, *, message):
        with open('data/config.json', 'r') as f:
            config = json.load(f)

        # print(prefixes)
        reminders = config["reminder"]
        date = date.split('-')
        date = [int(y) for y in date]

        x = datetime.datetime(date[2], date[1], date[0], date[3], date[4], tzinfo=pytz.timezone('Europe/Berlin'))
        stamp = time.mktime(x.timetuple())
        reminders[str(stamp)[:-2]] = message
        config['reminder'] = reminders

        with open('data/config.json', 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f'Reminder set for {x} to - {message}')

    # @tasks.loop(seconds=5)
    # async def send_reminder(self):
    #     print('Entered')
    #     with open('data/config.json', 'r') as f:
    #         config = json.load(f)
    #     reminders = config["reminder"]
    #     for reminder in reminders:
    #         pass
        # await self.client.change_presence(activity=discord.Game(next(status)))

    # @tasks.loop(seconds=5)
    # async def send_reminder(self):
    #     berlin = pytz.timezone('Europe/Berlin')
    #     with open('data/config.json', 'r') as f:
    #         config = json.load(f)
    #     reminders = config["reminder"]
    #     for reminder in reminders:
    #         alarm = datetime.datetime.utctimetuple(berlin.localize(time1))
    #         pass

def setup(client):
    client.add_cog(Discord_Server(client))
