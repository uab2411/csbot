import json
from itertools import cycle

import discord
from discord.ext import commands, tasks


def get_prefix(client, message):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)
status = cycle(['Monitoring the yuddha!', 'Aham Brahmasmi', 'Oota aaytha?', 'Boda seera?'])


@client.event
async def on_ready():
    change_status.start()
    print('Bot ready!')


@client.event
async def on_guild_join(guild):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# Runs for all the errors. Including the ones that have custom errors.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter all the required arguments')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command encountered!')


@tasks.loop(minutes=2)
async def change_status():
    # print('Hi')
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
    if amount > 0:
        await ctx.channel.purge(limit=(amount + 1))
    else:
        await ctx.send('Enter number of messages to be deleted.\nExample : .clear 5')


def custom_check(ctx):
    return ctx.author.id == 544631825968922644


@client.command()
@commands.check(custom_check)
async def love(ctx):
    await ctx.send(f'Hi Dayanayak! I LOVE YOU!')


@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


# Error catching only for the Load command.
@load.error
async def clear_error(ctx, error):
    await ctx.send('Please specify the Cog to be loaded!')


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


def get_bot_secret():
    with open('data/config.json', 'r') as f:
        config = json.load(f)

    return config['bot_secret']


client.load_extension('cogs.discord_server')
client.load_extension('cogs.cs_server')
client.load_extension('cogs.coronavirus')
client.run(get_bot_secret())
