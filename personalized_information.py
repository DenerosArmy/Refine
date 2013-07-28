from yelp import *

USER_DICT = {}
FLIGHT_DICT = {}

def add_user(device_id, display_name, profile_image_url):
    USER_DICT[device_id] = {}
    USER_DICT[device_id]["display_name"] = display_name
    USER_DICT[device_id]["profile_image_url"] = profile_image_url

def add_flight(device_id, flight_number, flight_gate, flight_time, arrival_time, destination):
    FLIGHT_DICT[device_id] = {}
    FLIGHT_DICT[device_id]["flight_number"] = flight_number
    FLIGHT_DICT[device_id]["flight_gate"] = flight_gate
    FLIGHT_DICT[device_id]["flight_time"] = flight_time
    FLIGHT_DICT[device_id]["arrival_time"] = arrival_time
    FLIGHT_DICT[device_id]["destination"] = destination

def get_username(device_id):
    return get_displayname(device_id).replace(" ", "_").replace(".", "_").lower()

def get_displayname(device_id):
    return USER_DICT[device_id]["display_name"]

def get_airport_data(device_id):
    data = []
    user_name = get_username(device_id)
    display_name = get_displayname(device_id)
    pic_url = USER_DICT[device_id]["profile_image_url"]
    flight = FLIGHT_DICT[device_id]
    return [{"op":"+",
             "type": "flight_info",
             "display_name": display_name,
             "user_name": user_name,
             "profile_image_url": pic_url,
             "flight_number": flight["flight_number"],
             "flight_gate": flight["flight_gate"],
             "flight_time": flight["flight_time"],
             "arrival_time": flight["arrival_time"],
             "destination": flight["destination"]},]

def get_destination_info():
    #returns an array of places of interest, hotels, cab companies
    return("Golden Gate Park", "The Hilton", "Hertz Car Rental")

def get_restaurant_data(location, search_term):
    #returns dictionary of restaurants and food rating
    return locate_food(location, search_term)


def get_movie_info():
    #returns dictionary of movies and personalized ratings
    return{"Despicable Me 2":5.0, "Lone Ranger":2.7, "Monsters University":4.5}

def get_store_info():
    #returns dictionary of stores and rating/distance from current location
    return{"GAP":(4.5, 13), "Abercrombie&Fitch":(2.1, 2)}


add_user("1", "Richie Z.", "https://fbcdn-sphotos-c-a.akamaihd.net/hphotos-ak-ash4/215356_10151641982947594_144941694_n.jpg")
add_flight("1", "UA 456", "G45", "11:45 AM", "6:55 PM", "Miami, FL")
add_user("kevid", "Jian L.", "https://lh6.googleusercontent.com/-TpuvTBw3vx8/UQM7IOmkmBI/AAAAAAAAAbI/DzNehhnVEWE/w256-h257-no/375563_10151168765508994_657905193_n.jpeg")
add_flight("kevid", "UA 456", "G45", "11:45 AM", "6:55 PM", "Miami, FL")
