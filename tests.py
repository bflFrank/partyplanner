from db import DB
from utils import fuzzy_determinizer

db = DB(target=':memory:')
db.generate_db()

def algorithm_test():
  new_person = 'insert into people (name) values (?)'
  new_time = 'insert into times (id_person, day, start, end) values (?, ?, ?, ?)'

  test1 = db.run(new_person, 'Test1')
  db.run(new_time, [test1, 1, '17:30:00', '22:00:00'])
  db.run(new_time, [test1, 2, '17:30:00', '22:00:00'])
  db.run(new_time, [test1, 3, '17:30:00', '22:00:00'])

  test2 = db.run(new_person, 'Test2')
  db.run(new_time, [test2, 1, '19:30:00', '22:00:00'])
  db.run(new_time, [test2, 2, '19:30:00', '22:00:00'])
  db.run(new_time, [test2, 3, '17:30:00', '20:00:00'])

  test3 = db.run(new_person, 'Test3')
  db.run(new_time, [test3, 1, '14:30:00', '17:00:00'])
  db.run(new_time, [test3, 2, '17:30:00', '22:00:00'])
  db.run(new_time, [test3, 3, '17:30:00', '22:00:00'])


  sql = '''
  select *
  from people
  left join times on people.id = times.id_person
  '''
  result = fuzzy_determinizer(db.all(sql))
  print(result)
algorithm_test()