from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse

from .models import Flights, Passengers
# Create your views here.

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flights.objects.all()
    })

def flight(request, flight_id):
    try:
        flight = Flights.objects.get(pk=flight_id)
    except Flights.DoesNotExist:
        raise Http404("Flight not found.")
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(), # type:ignore
        "non_passengers": Passengers.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        try:
            flight = Flights.objects.get(pk=flight_id)
        except Flights.DoesNotExist:
            raise Http404("Flight not found.")
        passenger = Passengers.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)

        return HttpResponseRedirect(reverse("flight", args=(flight.pk,)))
    return redirect("index") 