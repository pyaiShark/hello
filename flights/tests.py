from django.test import Client, TestCase
from django.db.models import Max


from .models import Airport, Flights, Passengers

# Create your tests here.
class FlightsTestCase(TestCase):

    def setUp(self):
        # Create Airport
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # create flights
        Flights.objects.create(origin=a1, destination=a2, duration=100)
        Flights.objects.create(origin=a1, destination=a1, duration=200)
        Flights.objects.create(origin=a1, destination=a2, duration=-110)

    def test_departure_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)
    
    def test_arrival_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flights(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")

        f = Flights.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flights())

    def test_invalid_flights(self):
        a1 = Airport.objects.get(code="AAA")

        f = Flights.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flights())
    
    def test_invalid_flights_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")

        f = Flights.objects.get(origin=a1, destination=a2, duration=-110)
        self.assertFalse(f.is_valid_flights())

    def testIndex(self):
        c = Client()
        response = c.get("/flights/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flights.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.pk}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flights.objects.all().aggregate(Max("pk"))["pk__max"]

        c = Client()
        invalid_id = (max_id + 1) if max_id is not None else 1
        response = c.get(f"/flights/{invalid_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f = Flights.objects.get(pk=1)
        p = Passengers.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flights.objects.get(pk=1)
        p = Passengers.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)

