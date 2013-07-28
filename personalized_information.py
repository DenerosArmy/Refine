def get_username(device_id):
    return "Richie Zeng"

def get_displayname(device_id):
    return get_username(device_id).replace(" ", "_").lower()

def get_airport_data(device_id):
    #returns a dictionary
    user_name = get_username(device_id)
    display_name = get_displayname(device_id)
    return [{"op":"+",
             "type": "flight_info",
             "display_name": display_name,
             "user_name": user_name,
             "profile_image_url": "google.com",
             "flight_number": "UA 456",
             "flight_gate": "G45",
             "flight_time": "2045",
             "destination": "Miami, FL"},]


def get_destination_info():
    #returns an array of places of interest, hotels, cab companies
    return("Golden Gate Park", "The Hilton", "Hertz Car Rental")

def get_food_info():
    #returns dictionary of restaurants and food rating
    return{"McDonalds":3.4,
           "TGIF":4.7,
           "Crepes A Go Go":5.0}

def get_movie_info():
    #returns dictionary of movies and personalized ratings
    return{"Despicable Me 2":5.0, "Lone Ranger":2.7, "Monsters University":4.5}

def get_store_info():
    #returns dictionary of stores and rating/distance from current location
    return{"GAP":(4.5, 13), "Abercrombie&Fitch":(2.1, 2)}
