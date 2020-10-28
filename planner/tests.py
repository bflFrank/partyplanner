from django.test import TestCase
from .models import Person, Availability
# Create your tests here.

class PersonTestCase(TestCase):
  def setUp(self):
    Person.objects.create(name='Test')

  def testPerson(self):
    self.setUp()
