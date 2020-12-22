#https://realpython.com/how-to-make-a-discord-bot-python/
import os
import threading
from db import DB

db = DB()
db.generate_db()

import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='pp', help='Test code checkination')
async def test_message(ctx):
  response = 'where are all the white women at'
  await ctx.send(response)

@bot.command(name='peoples')
async def peoples(ctx):
  #sends a list of all peoples to server
  await ctx.send(', '.join([row['name'] for row in db.all('select * from people')]))

bot.run(TOKEN)