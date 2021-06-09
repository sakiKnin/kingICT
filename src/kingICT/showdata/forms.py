from django import forms
from django.forms import ModelForm

from .models import MyFlight

class FlightForm(ModelForm):
      class Meta:
            model = MyFlight
            fields = ('originLocationCode', 'destinationLocationCode', 'departureDate', 'adultsNumber')

            labels = {
                  'originLocationCode': '',
                  'destinationLocationCode': '',
                  'departureDate': '',
                  'adultsNumber': ''

            }
            widgets = {
                  'originLocationCode': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Origin location code'}),
                  'destinationLocationCode': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Destination location code'}),
                  'departureDate': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Departure date'}),
                  'adultsNumber': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Number of adults'})
                  }
