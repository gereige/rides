from flask import Flask, render_template, request
import rides 
import os
from geopy.geocoders import Nominatim 
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session
from lyft_rides.client import LyftRidesClient



app = Flask(__name__)

@app.route("/")
def index():
    origin = rides.locate("Times square, New York")
    destination = rides.locate("Columbia University, New York")
    uber_eta = rides.get_uber_pickup(origin)
    lyft_eta = rides.get_lyft_pickup(origin)
    uber_cost = rides.get_uber_cost(rides.origin, destination)
    lyft_cost = rides.get_lyft_cost(origin, destination)
    uber_results = {'uberPOOL':'', 'uberX':'','uberXL':'','SUV':'','uberBLACK':''}
    lyft_results = {'Lyft':'','Lyft Line':'','Lyft Plus':''}
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

    return render_template('index.html', uber_results=uber_results, lyft_results=lyft_results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 500))
    app.run(host="0.0.0.0", port=port) 