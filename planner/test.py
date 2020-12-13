from datetime import datetime, timedelta
MINIMUM_TIME = 60 * 60 #1 hour min
MAXIMUM_TIME = 60 * 60 * 2
CHUNK_TIME = 60 * 30

def timeularize(time_string):
  h = int(time_string[0:2])
  m = int(time_string[3:5])
  s = int(time_string[6:8])
  now = datetime.now()
  return now.replace(hour=h, minute=m, second=s, microsecond=0)

#weights
PARTICIPATION_WEIGHT = 100
BEST_TIME_RANGE = [timeularize('18:00:00'), timeularize('19:00:00')]#for starts
BEST_TIME_WEIGHT = 50
PREFERRED_DAYS = [2,3,4]
PREFERRED_DAYS_WEIGHT = 50

#comes from ORM
ideal = [
  {'name': 'Frank', 'start': '17:00:00', 'end': '19:00:00'},
  {'name': 'Manny', 'start': '17:30:00', 'end': '20:00:00'},
  {'name': 'Haley', 'start': '17:00:00', 'end': '21:00:00'},
  {'name': 'Tomas', 'start': '17:00:00', 'end': '22:00:00'},
]
less_ideal = [
  {'name': 'Frank', 'start': '12:00:00', 'end': '17:30:00', 'day': 1},
  {'name': 'Manny', 'start': '12:30:00', 'end': '15:00:00', 'day': 1},
  {'name': 'Haley', 'start': '19:00:00', 'end': '21:00:00', 'day': 1},
  {'name': 'Tomas', 'start': '17:00:00', 'end': '22:00:00', 'day': 1},
  {'name': 'Fahaad', 'start': '17:00:00', 'end': '22:00:00', 'day': 1},
  {'name': 'Shonna', 'start': '17:00:00', 'end': '22:00:00', 'day': 1},

  {'name': 'Frank', 'start': '12:00:00', 'end': '17:30:00', 'day': 2},
  {'name': 'Manny', 'start': '12:30:00', 'end': '15:00:00', 'day': 2},
  {'name': 'Haley', 'start': '19:00:00', 'end': '21:00:00', 'day': 2},
  {'name': 'Tomas', 'start': '17:00:00', 'end': '22:00:00', 'day': 2},
  {'name': 'Fahaad', 'start': '17:00:00', 'end': '22:00:00', 'day': 2},
  {'name': 'Shonna', 'start': '17:00:00', 'end': '22:00:00', 'day': 2},

  {'name': 'Frank', 'start': '12:00:00', 'end': '17:30:00', 'day': 3},
  {'name': 'Manny', 'start': '12:30:00', 'end': '15:00:00', 'day': 3},
  {'name': 'Haley', 'start': '19:00:00', 'end': '21:00:00', 'day': 3},
  {'name': 'Tomas', 'start': '17:00:00', 'end': '22:00:00', 'day': 3},
  {'name': 'Fahaad', 'start': '17:00:00', 'end': '22:00:00', 'day': 3},
  {'name': 'Shonna', 'start': '17:00:00', 'end': '22:00:00', 'day': 3},
]


class Possibility:
  def __init__(self, start, end, day):
    self.start = start
    self.end = end
    self.duration = end - start
    self.day = day
    self.names = []
    self.score = 0
  def add_name(self, name):
    if name not in self.names:
      self.names.append(name)
  def calculate_score(self, party_size):
    self.score += (len(self.names) / party_size) * PARTICIPATION_WEIGHT
    if self.start >= BEST_TIME_RANGE[0] and self.start <= BEST_TIME_RANGE[1]:
      self.score += BEST_TIME_WEIGHT
    if self.day in PREFERRED_DAYS:
      self.score += PREFERRED_DAYS_WEIGHT
    return self.score
  def __str__(self):
    return self.start.strftime('%H:%M:%S') + '-' + self.end.strftime('%H:%M:%S') + ' on ' + self.day + ' with ' + ', '.join(self.names)
def ideal_determinizer(times_list):
  ideal_start = timeularize('00:00:00')
  ideal_end = timeularize('23:59:59')

  for availability in times_list:
    start = timeularize(availability['start'])
    end = timeularize(availability['end'])

    if ideal_start < start:
      ideal_start = start
    if ideal_end > end:
      ideal_end = end

  return Possibility(ideal_start, ideal_end)
def fuzzy_determinizer(times_list):
  possibilities = {}
  names = []
  #build all possibilities
  for i1, time1 in enumerate(times_list):
    if time1['name'] not in names:
      names.append(time1['name'])
    for i2, time2 in enumerate(times_list):
      if time1['day'] != time2['day']:
        continue

      if time1['start'] + '-' + time2['end'] + '-' + str(time1['day']) in possibilities:
        continue

      start = timeularize(time1['start'])
      end = timeularize(time2['end'])

      if start > end:
        continue

      duration = end - start
      if duration.seconds < MINIMUM_TIME:
        continue

      #if we're inside the max duration by default
      if duration.seconds <= MAXIMUM_TIME:
        possibilities[time1['start'] + '-' + time2['end'] + '-' + str(time1['day'])] = Possibility(time1['start'], time2['end'], str(time1['day']))
        continue

      #else lets make them chunks
      i = 0
      while True:
        chunk_start = start + timedelta(seconds=i * CHUNK_TIME)
        chunk_end = chunk_start + timedelta(seconds=MAXIMUM_TIME)
        i += 1
        if chunk_end > end:
          break

        chunk_start_pretty = chunk_start.strftime('%H:%M:%S')
        chunk_end_pretty = chunk_end.strftime('%H:%M:%S')

        if chunk_start_pretty + '-' + chunk_end_pretty in possibilities:
          continue

        possibilities[chunk_start_pretty + '-' + chunk_end_pretty + '-' + str(time1['day'])] = Possibility(chunk_start, chunk_end, str(time1['day']))
  #put everyone into each possibility they fit with
  for pos in possibilities:
    for time in times_list:
      if int(possibilities[pos].day) != int(time['day']):
        continue
      if possibilities[pos].start >= timeularize(time['start']) and possibilities[pos].end <= timeularize(time['end']):
        possibilities[pos].add_name(time['name'])

  max = 0
  biggest_pos = None
  #calculate possibility scores
  for pos in possibilities:
    current_score = possibilities[pos].calculate_score(len(names))
    if current_score > max:
      max = current_score
      biggest_pos = pos
  return possibilities[biggest_pos]

#assume we don't live in a perfect world
times_list = less_ideal
#algorithm go brrr
times = fuzzy_determinizer(times_list)
#show every possibility
print(times)