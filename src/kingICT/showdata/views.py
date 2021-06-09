from django.http import HttpResponseRedirect

from django.shortcuts import render

from .forms import FlightForm
from .models import MyFlight

from amadeus import Client, Location, ResponseError

amadeus = Client(
    client_id='KEjaAzITmu90GQhTtqQrl66natwlBA2H',
    client_secret='449heUaYWNJOoeBI'
)


def home(request):

      response=""
      
      if request.method == 'POST':
            form = FlightForm(request.POST)
            
            if form.is_valid():
                  originLocationCode = form.cleaned_data.get('originLocationCode')
                  destinationLocationCode = form.cleaned_data.get('destinationLocationCode')
                  departureDate = form.cleaned_data.get('departureDate')
                  adultsNumber = form.cleaned_data.get('adults')
                  
                  try:
                        response = amadeus.shopping.flight_offers_search.get(
                                     originLocationCode = originLocationCode,
                                     destinationLocationCode = destinationLocationCode,
                                     departureDate = departureDate,
                                     adults=adultsNumber)
                  except:
                        response = ""
                  if response != "":
                        context = {'form': form, 'response': response.data}
                  else:
                        context = {'form': form, 'response': response}
                  
                  return render(request, 'showdata/index.html', {'context': context})
      else:
            form = FlightForm()
            context = {'form':form, 'response': response}
      
      return render(request, 'showdata/index.html', {'context': context})


#print(response.body) #=> The raw response, as a string
#print(response.result) #=> The body parsed as JSON, if the result was parsable
#print(response.data) #=> The list of locations, extracted from the JSON
