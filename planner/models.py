from django.db import models

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
  person = models.ForeignKey(Person, on_delete=models.CASCADE)
  day = models.IntegerField(choices=week_days)
  start = models.TimeField()
  end = models.TimeField()