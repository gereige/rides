from flask import Flask, render_template, request
import os
from geopy.geocoders import Nominatim 
from uber_rides.session import Session
from uber_rides.client import UberRidesClient


clientid_uber = os.environ['CLIENTID_UBER']
clientsecret_uber = os.environ['CLIENTSECRET_UBER']
servertoken_uber = os.environ['SERVERTOKEN_UBER']


uber_session = Session(server_token= servertoken_uber)

uber_client = UberRidesClient(uber_session)


def locate(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    return [lat, lon]


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



app = Flask(__name__)

@app.route("/")
def index():
    origin = locate("Times square, New York")
    destination = locate("Columbia University, New York")
    uber_eta = get_uber_pickup(origin)
    uber_cost = get_uber_cost(origin, destination)
    uber_results = {'uberPOOL':'', 'uberX':'','uberXL':'','SUV':'','uberBLACK':''}
    for time in uber_eta:
        for cost in uber_cost:
            ride_type = cost['display_name']
            ride_cost = cost['estimate']
            if ride_type == time['display_name']:
                ride_eta = time['estimate'] / 60
                if ride_type == "uberPOOL":
                    uber_results['uberPool']={'service':'basic','sharing':'ride share','seats':'2',
                    'eta':ride_eta,'cost':ride_cost}

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

    return render_template('index.html', uber_results=uber_results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 500))
    app.run(host="0.0.0.0", port=port) 