from datetime import datetime, timedelta

#Algorithm dials
MINIMUM_TIME = 60 * 60 #1 hour min
MAXIMUM_TIME = 60 * 60 * 2
CHUNK_TIME = 60 * 30
#Algorithm weights
PARTICIPATION_WEIGHT = 1000
BEST_TIME_RANGE = [datetime.now().replace(hour=18), datetime.now().replace(hour=19)]#for starts only
BEST_TIME_WEIGHT = 50
PREFERRED_DAYS = [2,3,4]
PREFERRED_DAYS_WEIGHT = 50

week_days = (
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
)

class Possibility:
  def __init__(self, start, end, day):
    self.start_time = start
    self.end_time = end
    self.duration = end - start
    self.day = day
    self.names = []
    self.score = 0
  def add_name(self, name):
    if name not in self.names:
      self.names.append(name)
  def calculate_score(self, party_size):
    self.score += (len(self.names) / party_size) * PARTICIPATION_WEIGHT
    if self.start_time >= BEST_TIME_RANGE[0] and self.start_time <= BEST_TIME_RANGE[1]:
      self.score += BEST_TIME_WEIGHT
    if self.day in PREFERRED_DAYS:
      self.score += PREFERRED_DAYS_WEIGHT
    return self.score
  def __str__(self):
    return self.start_time.strftime('%H:%M:%S') + '-' + self.end_time.strftime('%H:%M:%S') + ' on ' + week_days[int(self.day)] + ' with ' + ', '.join(self.names) + '\nTotal score of ' + str(round(self.score))

def timeularize(time_string):
  h = int(time_string[0:2])
  m = int(time_string[3:5])
  s = int(time_string[6:8])
  now = datetime.now()
  return now.replace(hour=h, minute=m, second=s, microsecond=0)

def fuzzy_determinizer(data):
  possibilities = {}
  names = []
  times_list = []
  for time in data:
    if time['start'] is None or time['end'] is None:
      continue
    row = dict(zip(time.keys(), time))
    row['start_time'] = timeularize(row['start'])
    row['end_time'] = timeularize(row['end'])
    times_list.append(row)
    
  #build all possibilities
  for i1, time1 in enumerate(times_list):
    if time1['name'] not in names:
      names.append(time1['name'])
    for i2, time2 in enumerate(times_list):
      if time1['day'] != time2['day']:
        continue

      if time1['start'] + '-' + time1['end'] + '-' + str(time1['day']) in possibilities:
        continue

      if time1['start_time'] > time2['end_time']:
        continue

      duration = time2['end_time'] - time1['start_time']
      if duration.seconds < MINIMUM_TIME:
        continue

      #if we're inside the max duration by default
      if duration.seconds <= MAXIMUM_TIME:
        possibilities[time1['start'] + '-' + time2['end'] + '-' + str(time1['day'])] = Possibility(start, end, str(time1['day']))
        continue

      #else lets make them chunks
      i = 0
      while True:
        chunk_start = time1['start_time'] + timedelta(seconds=i * CHUNK_TIME)
        chunk_end = chunk_start + timedelta(seconds=MAXIMUM_TIME)
        i += 1
        if chunk_end > time2['end_time']:
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
      if possibilities[pos].start_time >= time['start_time'] and possibilities[pos].end_time <= time['end_time']:
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