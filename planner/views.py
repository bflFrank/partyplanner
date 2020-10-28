from django.shortcuts import render
from .models import Person, Availability

# Create your views here.
def index(request):
  context = {'peoples': Person.objects.all()}
  return render(request, 'index.html', context)