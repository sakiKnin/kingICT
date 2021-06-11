from django.http import HttpResponseRedirect

from django.shortcuts import render

import logging

from .forms import FlightForm
from .models import MyFlight

from amadeus import Client, Location, ResponseError

from .credentials import AMADEUS_CREDENTIALS
from .comparer import Comparer

logger = logging.getLogger('myApp')
logger.setLevel(logging.DEBUG)

amadeus = Client(
    client_id = AMADEUS_CREDENTIALS["CLIENT_ID"],
    client_secret = AMADEUS_CREDENTIALS["CLIENT_SECRET"],
    #logger=logger
    log_level='debug'
)

def home(request):
      
      success=False
      if request.method == 'POST':
            form = FlightForm(request.POST)
            print("my request :", request.POST)
            if form.is_valid():
                  originLocationCode = form.cleaned_data.get('originLocationCode')
                  destinationLocationCode = form.cleaned_data.get('destinationLocationCode')
                  departureDate = form.cleaned_data.get('departureDate')
                  adultNumber = form.cleaned_data.get('adultNumber')
                  results = form.cleaned_data.get('results')

                  myFlight = MyFlight(
                        originLocationCode = originLocationCode,
                        destinationLocationCode = destinationLocationCode,
                        departureDate = departureDate,
                        adultNumber = adultNumber,
                        results={})

                  flightList = MyFlight.objects.all()
                            
                  for flight in flightList:
                        if Comparer.compare(flight,myFlight):
                              return HttpResponseRedirect(f'/showdata?success=True&id={flight.id}')
                                       
                  try:
                        res = amadeus.shopping.flight_offers_search.get(
                               originLocationCode = originLocationCode,
                               destinationLocationCode = destinationLocationCode,
                               departureDate = departureDate,
                               adults = adultNumber)
                        #res = amadeus.shopping.flight_offers.prediction.post(body)
                        print(body)
                        myFlight.results = res.data
                        myFlight.save()
                        
                        flightId = int(MyFlight.objects.latest('id'))
                        
                        return HttpResponseRedirect(f'/showdata?success=True&id={flightId}')
                  except:
                        print("Error occurred while fetching data...")
               
                  return HttpResponseRedirect('/showdata?success=False')
                  
      elif 'success' in request.GET:
            form = FlightForm()
            tempDict = request.GET.copy()
            if request.GET['success']=='True':
                  success = True
                  flightId = request.GET['id']
                  item = MyFlight.objects.get(id = flightId)
                  tempDict['originLocationCode'] = item.originLocationCode
                  tempDict['destinationLocationCode'] = item.destinationLocationCode
                  tempDict['departureDate'] = item.departureDate
                  tempDict['adultNumber'] = item.adultNumber
                  tempDict['currency'] = item.currency
                  form = FlightForm(tempDict)
                  #respo = amadeus.reference_data.location('AAY').get()
                  #print(respo.data)
            else:
                  item={"No flights found or error occurred!"}                
             
      else:
            form = FlightForm()      
            item={}
      
      return render(request, 'showdata/index.html', {'form': form, 'item': item, 'success': success})
