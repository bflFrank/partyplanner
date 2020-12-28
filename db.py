import sqlite3
import os

from dotenv import load_dotenv
load_dotenv()

class DB:
  def __init__(self, target=os.getenv('target')):
    if target == ':memory:':
      print('Generating db in memory...')
    self.conn = sqlite3.connect(target)
    self.conn.row_factory = sqlite3.Row

  def generate_db(self):
    sql = ''
    with open('create.sql', 'r') as file:
      sql = file.read().split(';')
    cursor = self.conn.cursor()
    for statement in sql:
      cursor.execute(statement)
    self.conn.commit()

  def get(self, sql, inputs=[]):
    if type(inputs) != type([]):
      inputs = [inputs]
    cursor = self.conn.cursor()
    cursor.execute(sql, inputs)
    return cursor.fetchone()

  def run(self, sql, inputs=[]):
    if type(inputs) != type([]):
      inputs = [inputs]
    cursor = self.conn.cursor()
    cursor.execute(sql, inputs)
    self.conn.commit()
    return cursor.lastrowid

  def all(self, sql, inputs=[]):
    if type(inputs) != type([]):
      inputs = [inputs]
    cursor = self.conn.cursor()
    cursor.execute(sql, inputs)
    return cursor.fetchall()
