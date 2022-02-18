"""Builds a map of user's Twitter friends location"""
import requests
import json
from geopy.geocoders import Nominatim
import folium


def get_id(username):
    """Gets the id of a user in Twitter

    :param username: name of the user
    :type username: str
    """
    api = <your API-key>
    resp = requests.get("https://api.twitter.com/2/users/by/username/" + \
username, headers={'Authorization': 'Bearer ' + api})
    if resp.status_code == 200:
        response = json.loads(resp.text)
        if 'data' in response.keys():
            return response['data']['id']
        else:
            print('Server has not found such user, check the spelling.')
            return False
    else:
        print('Failed to access the server, check your API-key \
and connection.')
    return False


def get_location(username):
    """Gets the location of user's friends"""
    api = <your API-key>
    user_id = get_id(username)
    if user_id:
        resp = requests.get('https://api.twitter.com/2/users/' + user_id + \
'/following?user.fields=location',
                        headers={'Authorization': 'Bearer ' + api})
        response = json.loads(resp.text)
        if 'data' in response.keys():
            locations = []
            for friend in response['data']:
                if 'location' in friend.keys():
                    locations.append([friend['location'], friend['name']])
            return locations
        else:
            return False
    return False


def find_coordinates(username):
    """Finds coordinates of user's friends if possible"""
    locations = get_location(username)
    if locations:
        coordinates = []
        for i in range(len(locations)):
            try:
                geolocator = Nominatim(user_agent="twitter_requests.py")
                location = geolocator.geocode(locations[i][0])
                coordinates.append(([location.latitude, \
location.longitude], locations[i][1]))
            except AttributeError:
                continue
        return coordinates
    return False


def build_map(username):
    """Builds a map of friend's locations"""
    coordinates = find_coordinates(username)
    if coordinates:
        map = folium.Map(location=(0, 0), zoom_start=2)
        for friend in coordinates:
            map.add_child(folium.Marker(location=friend[0],
                                        popup=friend[1],
                                        icon=folium.Icon()))
        map.save('Map_1.html')
    return map
