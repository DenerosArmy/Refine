def get_airport_data(device_id = '12345'):
    #returns a dictionary
    return {"op":"+",
             "type": "flight_info",
            "user_name": "Richie Zeng",
            "profile_image_url": "google.com", 
            "flight_number": "UA 456", 
            "flight_gate": "G45",
            "flight_time": "2045", 
            "destination": "Miami, FL"}


def get_destination_info():
    #returns an array of places of interest, hotels, cab companies
    return('Golden Gate Park', 'The Hilton', 'Hertz Car Rental')

def get_food_info():
    #returns dictionary of restaurants and food rating
    return{'McDonalds':3.4,
           'TGIF':4.7,
           'Crepes A Go Go':5.0}

def get_movie_info():
    #returns dictionary of movies and personalized ratings
    return{'Despicable Me 2':5.0, 'Lone Ranger':2.7, 'Monsters University':4.5}

def get_store_info():
    #returns dictionary of stores and rating/distance from current location
    return{'GAP':(4.5, 13), 'Abercrombie&Fitch':(2.1, 2)}
