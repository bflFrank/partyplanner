import datetime
MINIMUM_TIME = 60 * 60 #1 hour min
MAXIMUM_TIME = 60 * 60 * 2
MINIMUM_PARTICIPATION_PERCENT = 0.50 #percent participation
MINIMUM_PARTICIPATION_COUNT = 4
#comes from ORM
ideal = [
  {'name': 'Frank', 'start': '17:00:00', 'end': '19:00:00'},
  {'name': 'Manny', 'start': '17:30:00', 'end': '20:00:00'},
  {'name': 'Haley', 'start': '17:00:00', 'end': '21:00:00'},
  {'name': 'Tomas', 'start': '17:00:00', 'end': '22:00:00'},
]
less_ideal = [
  {'name': 'Frank', 'start': '12:00:00', 'end': '17:30:00'},
  {'name': 'Manny', 'start': '12:30:00', 'end': '15:00:00'},
  {'name': 'Haley', 'start': '19:00:00', 'end': '21:00:00'},
  {'name': 'Tomas', 'start': '17:00:00', 'end': '22:00:00'},
  {'name': 'Fahaad', 'start': '17:00:00', 'end': '22:00:00'},
  {'name': 'Shonna', 'start': '17:00:00', 'end': '22:00:00'},
]

def timeularize(time_string):
  h = int(time_string[0:2])
  m = int(time_string[3:5])
  s = int(time_string[6:8])
  now = datetime.datetime.now()
  return now.replace(hour=h, minute=m, second=s)
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
  return {'ideal_start': ideal_start, 'ideal_end': ideal_end}
def fuzzy_determinizer(times_list):
  print('work needs to be did')
  pass



times_list = less_ideal
times = ideal_determinizer(times_list)
duration = times['ideal_start'] - times['ideal_end']
if duration.seconds >= MINIMUM_TIME:
  fuzzy_determinizer(times_list)#times should equal this



print(times['ideal_start'].strftime("%H:%M:%S"), ' to ', times['ideal_end'].strftime("%H:%M:%S"))