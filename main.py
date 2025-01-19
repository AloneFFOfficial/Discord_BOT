import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

cogs = ['Moderation', 'AloneGPT']

async def load_cogs() -> None:
    for cog in cogs:
        try:
            await bot.load_extension(f'cogs.{cog}')
            print(f'Sucessfully loaded {cog}')
        except Exception as e:
            print(f'Failed to load cog {cog}: {e}')
    print('All Cogs loaded successfully')

@bot.command()
@commands.is_owner()
async def sync_cmd(ctx):
    try:
        synced = await bot.tree.sync()
        await ctx.send('Successfully synced commands')
        print(f'Synced {len(synced)} commands ')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
        await ctx.send(f'Failed to sync {e} command')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hi(ctx):
    await ctx.send(f'Hello!, {ctx.auther.mention}')

@bot.command()
async def test(ctx):
    await ctx.send('This is a test command!')

async def main():
    await load_cogs()
    await bot.start(token)

asyncio.run(main())