# before running, make sure you pip install uber_rides and lyft_rides
# this is still running apis in sandbox

#for security
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


clientid_uber = os.environ['CLIENTID_UBER']
clientsecret_uber = os.environ['CLIENTSECRET_UBER']
servertoken_uber = os.environ['SERVERTOKEN_UBER']

clientid_lyft = os.environ['CLIENTID_LYFT']
clientsecret_lyft = os.environ['CLIENTSECRET_LYFT']
clienttoken_lyft = os.environ['CLIENTTOKEN_LYFT']


#for the locate function
from geopy.geocoders import Nominatim 

def locate(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    return [lat, lon]

#for Uber
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

uber_session = Session(server_token= servertoken_uber)

uber_client = UberRidesClient(uber_session)

def get_uber_pickup(origin):
    start_lat = origin[0]
    start_lon = origin[1]
    response = uber_client.get_pickup_time_estimates(
    start_latitude = start_lat,
    start_longitude= start_lon)
    return response.json.get('times')



def get_uber_cost(origin, destination):
    start_lat = origin[0]
    start_lon = origin[1]
    end_lat = destination[0]
    end_lon = destination[1]
    response = uber_client.get_price_estimates(
    start_latitude = start_lat,
    start_longitude= start_lon,
    end_latitude= end_lat,
    end_longitude= end_lon,
    seat_count= 1) 
    return response.json.get('prices') 

#forLyft
from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session
from lyft_rides.client import LyftRidesClient

lyft_auth_flow = ClientCredentialGrant(
    clientid_lyft,
    clientsecret_lyft,
    'rides.request public',) #scopes

lyft_session = lyft_auth_flow.get_session()

lyft_client = LyftRidesClient(lyft_session)

def get_lyft_pickup(origin):
    start_lat = origin[0]
    start_lon = origin[1]
    response = lyft_client.get_pickup_time_estimates(
    latitude = start_lat,
    longitude = start_lon)
    return response.json.get('eta_estimates')

def get_lyft_cost(origin, destination):
    start_lat = origin[0]
    start_lon = origin[1]
    end_lat = destination[0]
    end_lon = destination[1]
    response = lyft_client.get_cost_estimates(
    start_latitude = start_lat,
    start_longitude= start_lon,
    end_latitude= end_lat,
    end_longitude= end_lon) 
    return response.json.get('cost_estimates')

# get number of seats

#def get_seats(number):
#    try:
#        number = int(number)
#    except ValueError:
#        number = input("\nPlease input an integer between 1 & 6: ")
            #better try again... Return to the start of the loop
#    return number


#_____________________________________________________________#
#Get current location
origin = locate(input('\nWhat is your current location? '))

#Input the destination
destination = locate(input('\nWhere do you want to go? '))

#Input number of seats needed - only for Uber?

#seats = get_seats(input("\nHow many seats do you need? ")) #needs quality check...doesn't work forever

#Getting estimated time of arrival

uber_eta = get_uber_pickup(origin)
lyft_eta = get_lyft_pickup(origin)

#Getting estimated trip cost

uber_cost = get_uber_cost(origin, destination)
lyft_cost = get_lyft_cost(origin, destination)

#Create dictionary of results
uber_results = {'uberPOOL':'', 'uberX':'','uberXL':'','SUV':'','uberBLACK':''}
lyft_results = {'Lyft':'','Lyft Line':'','Lyft Plus':''}


#Printing result
print("\nThe estimated waiting times and prices for Uber are as follows: \n")
for time in uber_eta:
    for cost in uber_cost:
        ride_type = cost['display_name']
        ride_cost = cost['estimate']
        if ride_type == time['display_name']:
            ride_eta = time['estimate'] / 60
            if ride_type == "uberPOOL":
                uber_results['uberPool']={'service':'basic','sharing':'ride share','seats':'2',
                'eta':ride_eta,'cost':ride_cost}
                print("{}: {} minutes - ${} \n".format(ride_type, ride_eta, ride_cost))

            elif ride_type == "uberX":
                uber_results['uberX']={'service':'basic','sharing':'private','seats':'4',
                'eta':ride_eta,'cost':ride_cost}
                print("{}: {} minutes - ${} \n".format(ride_type, ride_eta, ride_cost))

            elif ride_type == "uberXL":
                uber_results['uberXL']={'service':'basic','sharing':'private','seats':'6',
                'eta':ride_eta,'cost':ride_cost}
                print("{}: {} minutes - ${} \n".format(ride_type, ride_eta, ride_cost))

            elif ride_type == "uberBLACK":
                uber_results['uberBLACK']={'service':'luxury','sharing':'private','seats':'4',
                'eta':ride_eta,'cost':ride_cost}
                print("{}: {} minutes - ${} \n".format(ride_type, ride_eta, ride_cost))

            elif ride_type == "SUV":
                uber_results['SUV']={'service':'luxury','sharing':'private','seats':'6',
                'eta':ride_eta,'cost':ride_cost}
                print("{}: {} minutes - ${} \n".format(ride_type, ride_eta, ride_cost))


            #print("{}: {} minutes - {} \n".format(ride_type, ride_eta, ride_cost))


print("The estimated waiting times and prices for Lyft are as follows: \n")
for time in lyft_eta:
    for cost in lyft_cost:
        ride_type = cost['display_name']
        ride_cost = cost.get('estimated_cost_cents_max') / 100
        if ride_type == time['display_name']:
            ride_eta = time['eta_seconds'] / 60
            if ride_type == "Lyft Line":
                lyft_results['Lyft']={'service':'basic','sharing':'ride share','seats':'2',
                'eta':ride_eta,'cost':ride_cost}
                print("{}: {} minutes - ${} \n".format(ride_type, ride_eta, ride_cost))

            elif ride_type == "Lyft":
                lyft_results['Lyft Line']={'service':'basic','sharing':'private','seats':'4',
                'eta':ride_eta,'cost':ride_cost}
                print("{}: {} minutes - ${} \n".format(ride_type, ride_eta, ride_cost))

            elif ride_type == "Lyft Plus":
                lyft_results['Lyft Plus']={'service':'luxury','sharing':'private','seats':'4',
                'eta':ride_eta,'cost':ride_cost}
                print("{}: {} minutes - ${} \n".format(ride_type, ride_eta, ride_cost))