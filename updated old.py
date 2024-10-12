import discord
import random
import pywhatkit
import os

from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.default()
intents.members = True  # Enable member intents
intents.message_content = True
client = commands.Bot(command_prefix='', intents=intents)
status = cycle(['VALORANT', 'SHIT', 'ON UR MOM', 'UR FEELINGS'])
@client.event
async def on_ready():
    change_status.start()
    print('Nolan is alive!')


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server !')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server !')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send('PLEASE PASS IN ALL REQUIRED ARGUMENTS !!!')

    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send('INVALID COMMAND  !!!')


@tasks.loop(seconds= 5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def ping(ctx):
    await ctx.channel.send(f'Pong, {round(client.latency * 1000)}ms !')


@client.command()
async def favsong(ctx):
    pywhatkit.playonyt('https://www.youtube.com/watch?v=R9lW5WUEZbg')
    # await ctx.channel.send('just dont cry ...')


@client.command()
async def youtube(ctx, *, song):
    pywhatkit.playonyt(song)
    await ctx.channel.send(f'"{song}" is playing on youtube !')


@client.command(aliases=['8ball', 'guess'])
async def _8ball(ctx, *, question):
    responses = ['dont know',
                 'i think so',
                 'as you see ',
                 'yes',
                 'no',
                 'certain',
                 'could be ...'
                 ]
    await ctx.channel.send(f'Your question: {question}\nMy answer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send('--clear command needs the amount--')


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.send(f'{member.mention} Kicked!')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send(f'{member.mention} Banned!')


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    mem_name, mem_dis = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (mem_name, mem_dis):
            await ctx.guild.unban(user)
            await ctx.channel.send(f'{user.mention} Unbanned!')
            return
for filename in os.listdir('./'):
    if filename.endswith('.py'):
        client.load_extension(f'.{filename[:-3]}')

client.run('')

