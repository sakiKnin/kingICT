from django import forms
from django.forms import ModelForm

from .models import MyFlight

class FlightForm(ModelForm):
      class Meta:
            model = MyFlight
            fields = ('originLocationCode', 'destinationLocationCode', 'departureDate', 'adultNumber', 'currency')

            labels = {
                  'originLocationCode': '',
                  'destinationLocationCode': '',
                  'departureDate': '',
                  'adultNumber': '',
                  'currency': ''
            }
            
            widgets = {
                  'originLocationCode': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Origin IATA location code'}),
                  'destinationLocationCode': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Destination IATA location code'}),
                  'departureDate': forms.DateInput(attrs={'class':'form-control', 'type': 'date', 'placeholder':'Departure date'}),
                  'adultNumber': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Number of adults'}),
                  'currency': forms.Select(attrs={'class':'form-control', 'placeholder':'Currency'})
                  }

          
           
