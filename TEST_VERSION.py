import discord
import random
import pywhatkit
import aiohttp
import responses

from GIFs import *
import os
from res import *
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.default()
intents.members = True  # Enable member intents
intents.message_content = True
client = commands.Bot(command_prefix='', intents=intents)
status = cycle(['VALORANT', 'Fortnite',' With ur Feelings'])

# ---------------------------------------------------------------------------
def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'hey there!'
    if p_message == 'who are u':
        return 'ana el FAGER! ana el METARSHA2'
    if p_message == 'roll':
        return str(random.randint(1, 6))
    if p_message == '!help':
        return "'etfadl ya 3aslya!'"

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said: '{user_message}' ({channel})")
    print(user_message)
    print(message)

    if user_message == None:
        ctx = await client.get_context(message)
        # Process the user_message as a command
        await client.invoke(ctx)
        return

    if user_message[0] == '?':
        user_message = user_message[1:]
        await send_message(message, user_message, is_private=True)
    else:
        await send_message(message, user_message, is_private=False)


async def send_message(message, user_message, is_private):
    try:
        response = handle_response(user_message)
        if response:
            await message.author.send(response) if is_private else await message.channel.send(response)
        else:
            ctx = await client.get_context(message)
            # Process the user_message as a command
            await client.invoke(ctx)

    except Exception as e:
        ctx = await client.get_context(message)
        # Process the user_message as a command
        await client.invoke(ctx)
        print(e)
# ------------------------------------------------------------------------
@client.event
async def on_ready():
    change_status.start()
    print('Nolan is alive!')

    guild = client.guilds[0]  # Replace with the desired guild (server) object or ID
    channel = discord.utils.get(guild.text_channels, name='general')  # Replace 'general' with the desired channel name

    gif_url = random.choice(IAMBACK)  # Replace with the URL of your desired GIF

    async with aiohttp.ClientSession() as session:
        async with session.get(gif_url) as response:
            if response.status == 200:
                with open("welcome.gif", "wb") as file:
                    file.write(await response.read())

    await channel.send(file=discord.File("welcome.gif"))


@client.event
async def on_member_join(member):
    channel =client.get_channel(1106417149653815309)
    username = str(member.name)
    await channel.send("Hellooooooo, "+username)
    # print(f'{member} has joined the server !')


@client.event
async def on_member_remove(member):
    channel = client.get_channel(1106417149653815309)
    username = str(member.name)
    await channel.send("Goodbye, " + username)
    # print(f'{member} has left the server !')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send('Please Pass In All Required Arguments !!!')

    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send('Invalid Command  !!!')


@tasks.loop(seconds= 5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# @client.command(aliases=greetings)
# async def hello(ctx):
#     username = str(ctx.author)
#     await ctx.send(random.choice(greetings)+", "+username[:-5])


@client.command(aliases=greetings_franko)
async def saba7(ctx):
    username = str(ctx.author)
    await ctx.send(random.choice(greetings_franko)+" ya "+username[:-5])

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
@commands.has_permissions(administrator = True)
async def unban(ctx: commands.Context, *, member):
    banned_users = ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    async for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

for filename in os.listdir('./'):
    if filename.endswith('.py'):
        client.load_extension(f'.{filename[:-3]}')

client.run('')

