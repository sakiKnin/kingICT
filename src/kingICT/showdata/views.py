from django.http import HttpResponseRedirect

from django.shortcuts import render

from .forms import FlightForm
from .models import MyFlight

from amadeus import Client, Location, ResponseError

amadeus = Client(
    client_id='KEjaAzITmu90GQhTtqQrl66natwlBA2H',
    client_secret='449heUaYWNJOoeBI'
)

def compare(objectA, objectB):
      if objectA.originLocationCode==objectB.originLocationCode and objectA.destinationLocationCode==objectB.destinationLocationCode and objectA.departureDate==objectB.departureDate and objectA.adultNumber==objectB.adultNumber:
            return True
      return False

def home(request):

      success=False
      if request.method == 'POST':
            form = FlightForm(request.POST)
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
                        if compare(flight,myFlight):
                              return HttpResponseRedirect('/showdata?success=True')
                                       
                  try:
                        body = amadeus.shopping.flight_offers_search.get(
                               originLocationCode = originLocationCode,
                               destinationLocationCode = destinationLocationCode,
                               departureDate = departureDate,
                               adults = adultNumber).result
                        res = amadeus.shopping.flight_offers.prediction.post(body)
                              
                        myFlight.results = res.data
                        print("my data: ",res.data)
                        myFlight.save()

                        return HttpResponseRedirect('/showdata?success=True')
                  except:
                        print("Error occurred while fetching data...")
               
                  return HttpResponseRedirect('/showdata?success=False')
                  
      elif 'success' in request.GET:
            form = FlightForm()
            print("my items: ", request.GET)
            if request.GET['success']=='True':
                  success = True
                  item = MyFlight.objects.latest('id')
                  #respo = amadeus.reference_data.location('ALHR').get()
                  #print(respo.data)
            else:
                  item={"No flights found or error occurred!"}
      else:
            form = FlightForm()      
            item={}
      
      return render(request, 'showdata/index.html', {'form': form, 'item': item, 'success': success})
