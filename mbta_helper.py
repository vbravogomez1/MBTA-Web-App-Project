import os
import json
import urllib.request
import pprint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")
OPENWEAHTER_API_KEY = os.getenv("OPENWEAHTER_API_KEY")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
OPENWEAHTER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """

    with urllib.request.urlopen(url) as response:
        response_text = response.read().decode("utf-8")
        data = json.loads(response_text)
        pprint.pprint(data)
    return data


def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    if "Boston" not in place_name:
        place_name = "Boston " + place_name # as you mentioned in class, we looked-up a way to make sure all places are in Boston

    place = place_name.replace(" ", "%20")
    url = f"{MAPBOX_BASE_URL}/{place}.json?access_token={MAPBOX_TOKEN}&types=poi"

    data = get_json(url)

    # print(url)
    # get_lat_lng("Boston College") # checking to see if url worked correctly

    longitude, latitude = data["features"][0]["geometry"]["coordinates"]  # for some reason in data, longitude is before latitude which it should always be the other way around
    # print("Coordinates:", latitude, longitude) # checking to see if we get the correct coordinates
    return (latitude, longitude)
# get_lat_lng("Boston College") # checking to see if we get the correct coordinates


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance"

    data = get_json(url)

    if not data["data"]:
        print("You are not close to any stations!")
        return None, None

    station_name = data["data"][0]["attributes"]["name"]
    wheelchair_accessible = (data["data"][0]["attributes"]["wheelchair_boarding"] == 1)  # if 1 then that means that it is wheelchair accessible so it will return "True"
    # print("Station:", station_name, wheelchair_accessible) # checking to see if we get the correct station and if its wheelchair accessible or not
    return (station_name, wheelchair_accessible)

# get_nearest_station("42.335866", "-71.169429") # checking to see if we get the correct station and if its wheelchair accessible or not


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    latitude, longitude = get_lat_lng(place_name)
    if latitude and longitude:
        return get_nearest_station(latitude, longitude)
    print("You are not close to any stations!")
    return (None, None)


def get_weather(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    given the latitude and longsitude, we will get the current temperature in that place

    we used Chatgpt and the internet to figure out how to correctly get the weather using coordinates instead of the city as we did in class
    """
    url = f"{OPENWEAHTER_BASE_URL}?lat={latitude}&lon={longitude}&APPID={OPENWEAHTER_API_KEY}&units=metric"

    data = get_json(url)

    temp = data["main"]["temp"]
    return temp


def main():
    """
    You should test all the above functions here
    """
    place_name = "Boston Seaport"  # testing if everything works
    station, accessible = find_stop_near(place_name)
    print(f"The closest station to {place_name} is: {station}, Wheelchair accessible: {"Yes" if accessible else "No"}")  # we didn't like that it said True or False so we looked up how to make it print Yes or No

    latitude, longitude = get_lat_lng(place_name)
    if latitude and longitude:
        temperature = get_weather(latitude, longitude)
        print(f"The current temperature in {place_name} is: {temperature}")
    else:
        print(f"Could not find weather data!")


if __name__ == "__main__":
    main()
