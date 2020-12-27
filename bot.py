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

@bot.command('add', help='Add a person to the DB.')
async def help(ctx, arg):
  arg = arg.lower()
  sql = 'select * from people where name = ?'
  if db.get(sql, arg) != None:
    await ctx.send('Now hey there partner, {} already exists.'.format(arg))
  else:
    sql = 'insert into people (name) values (?)'
    db.run(sql, arg)
    await ctx.send('User {} has been added to the DB'.format(arg))

@bot.command(name='pp', help='Test code checkination')
async def test_message(ctx):
  response = 'where are all the white women at'
  await ctx.send(response)

@bot.command(name='peoples')
async def peoples(ctx):
  #sends a list of all peoples to server
  await ctx.send(', '.join([row['name'] for row in db.all('select * from people')]))

bot.run(TOKEN)