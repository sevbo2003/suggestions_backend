# import module
from geopy.geocoders import Nominatim

# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")

# Latitude & Longitude input
def get_location(lat, long):
    location = geolocator.reverse(lat+","+long)
    address = location.raw['address']
    city = address.get('state', '').split(' ')[0]
    county = address.get('county', '')
    if city == '':
        city = address.get('region', '').split(' ')[0]
        if city == '':
            city = address.get('city', '').split(' ')[0]
    if county == '':
        county = address.get('town', '')
    return city, county
