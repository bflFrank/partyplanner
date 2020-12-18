from django.db import models
from datetime import datetime
def timeularize(time_string):
  h = int(time_string[0:2])
  m = int(time_string[3:5])
  s = int(time_string[6:8])
  now = datetime.now()
  return now.replace(hour=h, minute=m, second=s, microsecond=0)

week_days = (
  (0, 'Sunday'),
  (1, 'Monday'),
  (2, 'Tuesday'),
  (3, 'Wednesday'),
  (4, 'Thursday'),
  (5, 'Friday'),
  (6, 'Saturday'),
)

# Create your models here.
class Person(models.Model):
  def __str__(self):
    return self.name
  name = models.CharField(max_length=200)

class Availability(models.Model):
  def __str__(self):
    return str(self.person) + " on " + week_days[self.day][1] + " : " + str(self.start) + "-" + str(self.end)
  def as_dict(self):
    return {
    'name': str(self.person),
    'day': self.day,
    'start': timeularize(str(self.start)),
    'end': timeularize(str(self.end)),
    'start_str': str(self.start),
    'end_str': str(self.end),
    }
  person = models.ForeignKey(Person, on_delete=models.CASCADE)
  day = models.IntegerField(choices=week_days)
  start = models.TimeField()
  end = models.TimeField()