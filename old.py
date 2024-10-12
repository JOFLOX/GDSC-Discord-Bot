import discord
import requests
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True  # Enable member intents
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command()
async def search(ctx, *, query):
    if not query:
        await ctx.send('Please provide a search query.')
        return
    try:
        summary = await get_summary(query)
        if summary:
            await ctx.send(summary)
        else:
            await ctx.send('No results found.')
    except Exception as e:
        print(f'An error occurred: {e}')
        await ctx.send('An error occurred while fetching the information.')

async def get_summary(query):
    api_url = 'https://en.wikipedia.org/api/rest_v1/page/summary/'
    url = f'{api_url}{query}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        summary = data.get('extract')
        return summary
    else:
        return None

bot.run('')
