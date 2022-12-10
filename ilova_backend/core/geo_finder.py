# import module
from geopy.geocoders import Nominatim

# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")

# Latitude & Longitude input
def get_location(lat, long):
    location = geolocator.reverse(lat+","+long)
    address = location.raw['address']
    city = address.get('city', '')
    county = address.get('county', '')
    return city, county
