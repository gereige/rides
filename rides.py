# before running, make sure you pip install uber_rides and lyft_rides
# this is still running apis in sandbox

#for security
import os

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
