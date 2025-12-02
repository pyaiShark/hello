from django.contrib import admin

from .models import Flights, Airport, Passengers
# Register your models here.

class FlightAdmin(admin.ModelAdmin):
    list_display = ['id', 'origin', 'destination', 'duration']

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Flights, FlightAdmin) # Tell the Django admin site to load my configurations to it 
admin.site.register(Passengers, PassengerAdmin) 