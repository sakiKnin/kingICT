from django.db import models

import datetime
from datetime import date

class MyFlight(models.Model):
                  originLocationCode = models.CharField('Origin location', max_length=10)
                  destinationLocationCode = models.CharField('Destination location', max_length=10)
                  departureDate = models.DateField("Departure date", default=date.today)
                  adultNumber = models.PositiveIntegerField('Number of adults')
                  results = models.JSONField(null=True)
    
