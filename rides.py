
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
