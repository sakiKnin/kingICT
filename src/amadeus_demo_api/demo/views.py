from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight
from django.http import HttpResponse

from .credentials import AMADEUS_CREDENTIALS
from .models import MyFlight
from .comparer import Comparer

#from google_currency import convert
from datetime import datetime
import json
from fastnumbers import fast_real

amadeus = Client(
    client_id = AMADEUS_CREDENTIALS['CLIENT_ID'],
    client_secret = AMADEUS_CREDENTIALS['CLIENT_SECRET']
)

def load_db():
    return MyFlight.objects.all()

def check_is_db_item(flight):
    for item in load_db():
        if Comparer.compare(item,flight):
               return item
    return None

def find_trip_purpose(kwargs):
    trip_purpose_response = amadeus.travel.predictions.trip_purpose.get(**kwargs).data
    return trip_purpose_response['result']
    

def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode'] + ', ' + data[i]['name'])
    result = list(dict.fromkeys(result))
    return json.dumps(result)

def demo(request):
    origin = request.POST.get('Origin')
    destination = request.POST.get('Destination')
    departureDate = request.POST.get('Departuredate')
    returnDate = request.POST.get('Returndate')
    adults = request.POST.get('Adults')
    currency = request.POST.get('Currency')
    
    if not adults:
        adults = 1

    kwargs = {
              'originLocationCode': origin,
              'destinationLocationCode': destination,
              'departureDate': departureDate,
              'adults': adults
              }

    myFlight = MyFlight(
                        originLocationCode = origin,
                        destinationLocationCode = destination,
                        departureDate = departureDate,
                        returnDate = returnDate,
                        adultNumber = adults,
                        currency = currency,
                        flightOffers = [],
                        predictionFlights = [],
                        tripPurpose = ''
                        )

    flight = check_is_db_item(myFlight)

    if flight and returnDate and flight.returnDate.strftime("%Y-%m-%d")!=returnDate:
        kwargs['returnDate'] = returnDate
        flight.tripPurpose = find_trip_purpose(kwargs)
    elif flight and not returnDate:
        flight.tripPurpose = ''

    if flight and flight.currency!=currency:
        flights_offers = []
        for item in flight.flightOffers:
            if flight.currency=='EUR' and currency=='USD':
                item['price'] = str(round((fast_real(item['price'])*0.83),2))
            elif flight.currency=='USD' and currency=='EUR':
                item['price'] = str(round((fast_real(item['price'])*1.21),2))
            elif flight.currency=='HRK' and currency=='USD':
                item['price'] = str(round((fast_real(item['price'])*0.16),2))
            elif flight.currency=='USD' and currency=='HRK':
                item['price'] = str(round((fast_real(item['price'])*6.19),2))
            elif flight.currency=='EUR' and currency=='HRK':
                item['price'] = str(round((fast_real(item['price'])*7.5),2))
            else:
                item['price'] = str(round((fast_real(item['price'])*0.13),2))      
            flights_offers.append(item)
            
        flight.flightOffers = flights_offers
        
        prediction_flights = []
        for item in flight.predictionFlights:
            if flight.currency=='EUR' and currency=='USD':
                item['price'] = str(round((fast_real(item['price'])*0.83),2))
            elif flight.currency=='USD' and currency=='EUR':
                item['price'] = str(round((fast_real(item['price'])*1.21),2))
            elif flight.currency=='HRK' and currency=='USD':
                item['price'] = str(round((fast_real(item['price'])*0.16),2))
            elif flight.currency=='USD' and currency=='HRK':
                item['price'] = str(round((fast_real(item['price'])*6.19),2))
            elif flight.currency=='EUR' and currency=='HRK':
                item['price'] = str(round((fast_real(item['price'])*7.5),2))
            else:
                item['price'] = str(round((fast_real(item['price'])*0.13),2))      
            prediction_flights.append(item)
            
        flight.predictionFligts = prediction_flights

        flight.currency = currency
        
    if flight:
        return render(request, 'demo/results.html', {'response': flight.flightOffers,
                                                     'prediction': flight.predictionFlights,
                                                     'origin': flight.originLocationCode,
                                                     'destination': flight.destinationLocationCode,
                                                     'departureDate': flight.departureDate,
                                                     'returnDate': flight.returnDate,
                                                     'adults': flight.adultNumber,
                                                     'currency': flight.currency,
                                                     'tripPurpose': flight.tripPurpose,
                                                     })
    tripPurpose = ''
    if returnDate:
        kwargs['returnDate'] = returnDate
        try:
            tripPurpose = find_trip_purpose(kwargs)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'demo/demo_form.html', {})
    else:
        print("No return date, freedom call!")
        myFlight.returnDate = datetime.strptime('1970-1-1','%Y-%m-%d')

    if origin and destination and departureDate:
        try:
            flight_offers = amadeus.shopping.flight_offers_search.get(**kwargs)
            prediction_flights = amadeus.shopping.flight_offers.prediction.post(flight_offers.result)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'demo/demo_form.html', {})
        
        flights_offers_returned = []
        for flight in flight_offers.data:
            offer = Flight(flight).construct_flights()
            if currency=='EUR':
                  offer['price'] = str(round((fast_real(offer['price'])*0.83),2))
            elif currency=='HRK':
                  offer['price'] = str(round((fast_real(offer['price'])*6.19),2))                  
            flights_offers_returned.append(offer)

        prediction_flights_returned = []
        for flight in prediction_flights.data:
            offer = Flight(flight).construct_flights()
            if currency=='EUR':
                  offer['price'] = str(round((fast_real(offer['price'])*0.83),2))
            elif currency=='HRK':
                  offer['price'] = str(round((fast_real(offer['price'])*6.19),2))
            prediction_flights_returned.append(offer)

        myFlight.flightOffers = flights_offers_returned
        myFlight.predictionFlights = prediction_flights_returned
        myFlight.tripPurpose = tripPurpose

        myFlight.save()

        return render(request, 'demo/results.html', {'response': flights_offers_returned,
                                                     'prediction': prediction_flights_returned,
                                                     'origin': origin,
                                                     'destination': destination,
                                                     'departureDate': departureDate,
                                                     'returnDate': returnDate,
                                                     'adults': adults,
                                                     'currency': currency,
                                                     'tripPurpose': tripPurpose,
                                                     })
    return render(request, 'demo/demo_form.html', {})


def origin_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_airport_list(data), 'application/json')


def destination_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_airport_list(data), 'application/json')
