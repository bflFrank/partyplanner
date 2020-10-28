from django.contrib import admin

from .models import Person, Availability

# Register your models here.

admin.site.register(Person)
admin.site.register(Availability)