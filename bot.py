#https://realpython.com/how-to-make-a-discord-bot-python/
import os
import threading

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='pp', help='Test code checkination')
async def test_message(ctx):
  response = 'does this bad boy respond'
  await ctx.send(response)

from .models import Person
@bot.command(name='db')
def db(ctx):
  t = threading.Thread(target=send, args=[ctx], daemon=True)
  t.start()
def send(ctx):
  ctx.send(Person.objects.all())

bot.run(TOKEN)
# def launch():
#   bot.run(TOKEN)
# t = threading.Thread(target=launch,daemon=True)
# t.start()