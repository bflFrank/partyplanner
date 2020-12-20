from django.shortcuts import render
from .models import Person, Availability
from .utils import gather_all_data, fuzzy_determinizer
import json

# Create your views here.
def index(request):
  context = {'peoples': Person.objects.all()}
  return render(request, 'index.html', context)

def get_best(request):
  best_time = fuzzy_determinizer(gather_all_data())
  data = {'best': str(best_time)}
  discord_bot.send(json.dumps(data))
  return request.send("ok")