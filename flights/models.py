from django.db import models

# Create your models here.

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.city} ({self.code})"
    
class Flights(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.pk}: {self.origin} to {self.destination}" # pk is also called id hear bu best to use pk(Primary Key)
    
    def is_valid_flights(self):
        return self.origin != self.destination or self.duration > 0

class Passengers(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flights, blank=True, related_name="passengers")

    def __str__(self) -> str:
        return f"{self.first} {self.last}"