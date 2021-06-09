from django.db import models

import datetime

class MyFlight(models.Model):
                  originLocationCode = models.CharField('Origin location', max_length=10)
                  destinationLocationCode = models.CharField('Destination location', max_length=10)
                  departureDate = models.DateField("Departure date")
                  adultsNumber = models.IntegerField('Number of adults')
    
