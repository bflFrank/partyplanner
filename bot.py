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

MEGA_DAYS_LIST = {
    0: 'Sunday     ',
    1: 'Monday     ',
    2: 'Tuesday    ',
    3: 'Wednesday  ',
    4: 'Thursday   ',
    5: 'Friday     ',
    6: 'Saturday   ',
    'sunday': 0,
    'monday': 1,
    'tuesday': 2,
    'wednesday': 3,
    'thursday': 4,
    'friday': 5,
    'saturday': 6,
  }

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

@bot.command('list_times', help='!list_times', brief='Show all times in DB.')
async def list_times(ctx, name):
  sql = 'select * from people where name = ?'
  row = db.get(sql, name)

  if row == None:
    return await ctx.send('User {} not found'.format(name))
  
  sql_two = 'select * from times where id_person = ?'
  sql_checker = db.all(sql_two,row['id'])

  if sql_checker == None:
    return await ctx.send('No times found for {}'.format(name))
  
  await ctx.send ('```All times for {}:\n'.format(name) + '\n'.join(['{day} \t\t{start} - {end}'.format(day=MEGA_DAYS_LIST[row['day']], start=row['start'], end=row['end']) for row in sql_checker])+'```')

@bot.command('delete_time', help='Use this to remove a time scheduled on a day for a specific user', brief='Remove time for a specific person.')
async def delete_time(ctx, name, day):
  sql = 'select * from people where name = ? collate nocase'
  row = db.get(sql, name)
  if row == None:
    return await ctx.send('User {} not found.'.format(name))
  id_person = row['id']

  if day.lower() not in MEGA_DAYS_LIST:
    return await ctx.send('Day incorrect, use one of the following: ' + ', '.join(MEGA_DAYS_LIST.keys()))
  day_string, day = day, MEGA_DAYS_LIST[day.lower()]

  sql_two = 'select * from times where id_person = ? and day = ?'
  row_two = db.get(sql_two, [id_person, day])

  if row_two == None:
    return await ctx.send('{name} does not have time set on {day}.'.format(name=name, day=day_string))
  
  sql_three = 'delete from times where id_person = ? and day = ?'
  db.run(sql_three, [id_person, day])
  return await ctx.send('Time for {name} on {day} has been removed'.format(name=name, day=day_string))

@bot.command('add_time', help='Used to add a time for a person on a specific day.', brief='Add a time for one person.')
async def add_time(ctx, name=None, day=None, start=None, end=None):
  if name == None or day == None or start == None or end == None:
    return await ctx.send('Incomplete parameters, use !help add_time for list of requirements')

  #make sure users spell days correctly
  if day.lower() not in MEGA_DAYS_LIST:
    return await ctx.send('Day incorrect, use one of the following: ' + ', '.join(MEGA_DAYS_LIST.keys()))
  day_string, day = day, MEGA_DAYS_LIST[day.lower()]

  #make sure users spell names correctly
  sql = 'select * from people where name = ? collate nocase'
  row = db.get(sql, name)
  if row == None:
    return await ctx.send('Error, {} not found.'.format(name))
  id_person = row['id']
  #todo: make sure start/end is proper time format

  sql = 'select * from times where id_person = ? and day = ?'
  row = db.get(sql, [row['id'], day])
  sql, inputs = None, None
  if row == None:
    sql = 'insert into times (id_person, day, start, end) values (?, ?, ?, ?)'
    inputs = [id_person, day, start, end]
  else:
    sql = 'update times set start = ?, end = ? where id = ?'
    inputs = [start, end, row['id']]
  db.run(sql,inputs)
  await ctx.send('Time for {name} on {day} set to {start} - {end}'.format(name=name, day=day_string, start=start, end=end))
bot.run(TOKEN)