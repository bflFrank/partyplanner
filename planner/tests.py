from django.test import TestCase
from .models import Person, Availability
# Create your tests here.

class AlgorithmTestCase(TestCase):
  def setUp(self):
    test1 = Person.objects.create(name='Test1')
    test1.availability_set.create(day=1, start='17:30:00', end='22:00:00')
    test1.availability_set.create(day=2, start='17:30:00', end='22:00:00')
    test1.availability_set.create(day=3, start='17:30:00', end='22:00:00')

    test2 = Person.objects.create(name='Test2')
    # test2.availability_set.create(day=1, start='19:30:00', end='22:00:00')
    test2.availability_set.create(day=2, start='19:30:00', end='22:00:00')
    test2.availability_set.create(day=3, start='17:30:00', end='20:00:00')

    test3 = Person.objects.create(name='Test3')
    test3.availability_set.create(day=1, start='14:30:00', end='17:00:00')
    test3.availability_set.create(day=2, start='17:30:00', end='22:00:00')
    # test3.availability_set.create(day=3, start='17:30:00', end='22:00:00')

  def algorithmTest(self):
    from .utils import fuzzy_determinizer, gather_all_data
    everything = gather_all_data()
    best_time = fuzzy_determinizer(everything)
    print('\n\n\n\n\n')
    print('******************************************')
    print('Algorithm test results: ' + str(best_time))
    print('******************************************')
    print('\n\n\n\n\n')

  def testPerson(self):
    #build out availability set
    self.setUp()
    #algorithm go brrrr
    self.algorithmTest()
