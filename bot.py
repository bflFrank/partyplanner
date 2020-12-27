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

@bot.command('add_person', help='!add_person [name]', brief='Add a person to the DB.')
async def add_person(ctx, arg):
  sql = 'select * from people where name = ? collate nocase'
  if db.get(sql, arg) != None:
    return await ctx.send('Now hey there partner, {} already exists.'.format(arg))

  sql = 'insert into people (name) values (?)'
  db.run(sql, arg)
  await ctx.send('User {} has been added to the DB'.format(arg))

@bot.command('delete_person', help='!delete_person [name]', brief='Remove a person from the DB.')
async def delete_person(ctx, arg):
  sql = 'select * from people where name = ? collate nocase'
  row = db.get(sql, arg)
  if row == None:
    return await ctx.send('Now hey there partner, {} doesn\'t exist.'.format(arg))

  sql = 'delete from people where id = ?'
  db.run(sql, row['id'])
  await ctx.send('User {} has been deleted.'.format(arg))

@bot.command('list_people', help='!list_people', brief='Show all names in DB.')
async def list_users(ctx):
  sql = 'select * from people'
  await ctx.send('All users: ' + ', '.join([row['name'] for row in db.all(sql)]))

@bot.command('add_time', help='Used to add a time for a person on a specific day.', brief='Add a time for one person.')
async def add_time(ctx, name=None, day=None, start=None, end=None):
  if name == None or day == None or start == None or end == None:
    return await ctx.send('Incomplete parameters, use !help add_time for list of requirements')

  #make sure users spell days correctly
  days = {
    'sunday': 0,
    'monday': 1,
    'tuesday': 2,
    'wednesday': 3,
    'thursday': 4,
    'friday': 5,
    'saturday': 6,
  }
  if day.lower() not in days:
    return await ctx.send('Day incorrect, use one of the following: ' + ', '.join(days.keys()))
  day_string = day
  day = days[day]

  #make sure users spell names correctly
  sql = 'select * from people where name = ? collate nocase'
  row = db.get(sql, name)
  if row == None:
    return await ctx.send('Error, {} not found.'.format(name))
  id_person = row['id']
  #todo: make sure start/end is proper time format

  sql = 'select * from times where id_person = ? and day = ?'
  row = db.get(sql, [row['id'], day])
  if row == None:
    sql = 'insert into times (id_person, day, start, end) values (?, ?, ?, ?)'
    inputs = [id_person, day, start, end]
  else:
    sql = 'update times set start = ?, end = ? where id = ?'
    inputs = [start, end, row['id']]
  await ctx.send('Time for {name} on {day} set to {start} - {end}'.format(name=name, day=day_string, start=start, end=end))
bot.run(TOKEN)