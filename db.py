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
    sql = (
    '''
    create table if not exists people(
    id integer,
    name text not null,
    primary key(id)
    );
    ''',
    '''
    create table if not exists times(
    id integer,
    id_person integer,
    day integer check (day between 0 and 6),
    start text,
    end text,
    primary key(id),
    foreign key(id_person) references people(id)
    );
    ''',
    '''
    create table if not exists parties(
    id integer,
    day integer check (day between 0 and 6),
    start text,
    end text,
    primary key(id)
    );
    ''',
    '''
    create table if not exists attendance(
    id integer,
    id_party integer,
    id_person integer,
    primary key(id),
    foreign key(id_party) references parties(id),
    foreign key(id_person) references people(id)
    );
    '''
    )
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
