import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Enable member intents
intents.message_content = True
bot = commands.Bot(command_prefix='', intents=intents)

@bot.command()
async def verify(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Verified")
    await ctx.author.add_roles(role)
    await ctx.send("You have been successfully verified.")

bot.run('')
