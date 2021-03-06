from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db import models
from datetime import date

from .choices import CURRENCY_CHOICES 

class MyFlight(models.Model):
        originLocationCode = models.CharField('Origin IATA location', max_length=10)
        destinationLocationCode = models.CharField('Destination IATA location', max_length=10)
        departureDate = models.DateField("Departure date", default=date.today)
        returnDate = models.DateField("Return date", default=date.today)
        adultNumber = models.PositiveIntegerField('Number of adults')
        currency = models.CharField('Currency', max_length=3, choices=CURRENCY_CHOICES, default='EUR')
        flightOffers = ArrayField(models.JSONField(null=True), default={})
        predictionFlights = ArrayField(models.JSONField(null=True), default={})
        tripPurpose = models.CharField('Trip purpose', max_length=20, default='')
