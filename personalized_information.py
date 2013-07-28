from yelp import *
import collections as cl

USER_DICT = {}
FLIGHT_DICT = {}
PLACE_DICT = {}
RENTALCAR_DICT = cl.defaultdict(set)
RESTAURANT_DICT = {}


class User(object):

    def __init__(self, device_id, display_name, profile_image_url):
        self.device_id = device_id
        self.display_name = display_name
        self.user_name = display_name.replace(" ", "_").replace(".", "_").lower()
        self.profile_image_url = profile_image_url
        USER_DICT[device_id] = self

    @staticmethod
    def get_display_name(device_id):
        return USER_DICT[device_id].display_name

    @staticmethod
    def get_user_name(device_id):
        return USER_DICT[device_id].user_name

    @staticmethod
    def get_pic_url(device_id):
        return USER_DICT[device_id].profile_image_url


class Flight(object):

    def __init__(self, device_id, flight_number, flight_gate, departure_time, arrival_time, destination):
        self.device_id = device_id
        self.flight_number = flight_number
        self.flight_gate = flight_gate
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.destination = destination
        FLIGHT_DICT[device_id] = self

    @property
    def dict(self):
        return {"op":"+",
                "type": "flight_info",
                "display_name": User.get_display_name(self.device_id),
                "user_name": User.get_user_name(self.device_id),
                "profile_image_url": User.get_pic_url(self.device_id),
                "flight_number": self.flight_number,
                "flight_gate": self.flight_gate,
                "departure_time": self.departure_time,
                "arrival_time": self.arrival_time,
                "destination": self.destination}


class Place(object):

    def __init__(self, device_id, name, img, distance):
        self.device_id = device_id
        self.name = name
        self.img = img
        self.distance = distance
        PLACE_DICT[device_id] = self

    @property
    def dict(self):
        return {"op": "+",
                "type": "places",
                "user_name": User.get_user_name(self.device_id),
                "display_name": User.get_display_name(self.device_id),
                "user_name": User.get_user_name(self.device_id),
                "profile_image_url": User.get_pic_url(self.device_id),
                "name": self.name,
                "img": self.img,
                "distance": self.distance}


class RentalCar(object):

    def __init__(self, device_id, model, price, img, number):
        self.device_id = device_id
        self.model = model
        self.price = price
        self.img = img
        self.number = number
        RENTALCAR_DICT[device_id].add(self)

    @property
    def dict(self):
        cars = RENTALCAR_DICT[self.device_id]
        data = []
        for car in cars:
            data.append({"model": self.model,
                         "price": self.price,
                         "img": self.img,
                         "number": self.number})
        return {"op": "+",
                "type": "rentals",
                "user_name": User.get_user_name(self.device_id),
                "display_name": User.get_display_name(self.device_id),
                "user_name": User.get_user_name(self.device_id),
                "profile_image_url": User.get_pic_url(self.device_id),
                "cars": data}


class Restaurant(object):

    def __init__(self, device_id, name, rating, image_url):
        self.device_id = device_id
        self.name = name
        self.rating = rating
        self.image_url = image_url
        RESTAURANT_DICT[device_id] = self

    @property
    def dict(self):
        return {"op": "+",
                "type": "restaurants",
                "user_name": User.get_user_name(self.device_id),
                "display_name": User.get_display_name(self.device_id),
                "user_name": User.get_user_name(self.device_id),
                "profile_image_url": User.get_pic_url(self.device_id),
                "name": self.name,
                "img": self.image_url,
                "distance": self.rating}

def populate_data(data, cards):
    for card in cards:
        data.append(card.dict)

def get_data(device_id, place):
    data = []
    user_name = User.get_user_name(device_id)
    display_name = User.get_display_name(device_id)
    pic_url = USER_DICT[device_id].profile_image_url
    flight = FLIGHT_DICT[device_id]
    if place == "sf":
        if display_name == "Richie Z.":
            populate_data(data, sf_rich_data)
    if place == "miami":
        if display_name == "Richie Z.":
            populate_data(data, mia_rich_data)
        if display_name == "Jian L.":
            populate_data(data, mia_jw_data)
    return data


rich = User("518b237bef45d835", "Richie Z.", "https://fbcdn-sphotos-c-a.akamaihd.net/hphotos-ak-ash4/215356_10151641982947594_144941694_n.jpg")
jian = User("kevid", "Jian L.", "https://lh6.googleusercontent.com/-TpuvTBw3vx8/UQM7IOmkmBI/AAAAAAAAAbI/DzNehhnVEWE/w256-h257-no/375563_10151168765508994_657905193_n.jpeg")
f1 = Flight("518b237bef45d835", "UA 456", "G45", "11:45 AM", "6:55 PM", "Miami, FL")
rc1 = RentalCar("518b237bef45d835", "Honda Accord 2012", "$30.09", "../img/accord.jpg", "305-871-0300")
rc2 = RentalCar("518b237bef45d835", "Toyota Camry 2009", "$24.09", "../img/camry.jpg", "305-871-0300")
rc3 = RentalCar("518b237bef45d835", "Mitsubishi Evolution X", "$36.09", "../img/evo.jpg", "305-876-1800")
p1 = Place("518b237bef45d835", "Hollywood Beach", "../img/hollywood-beach.jpg", "21.5 mi")
r1 = Restaurant("518b237bef45d835", "People's Bar-B-Que", "6.2 mi", "http://s3-media1.ak.yelpcdn.com/bphoto/MyucYR9AxCPKRvXQSZKQNg/l.jpg")
r2 = Restaurant("kevid", "Wo Bu Che Tau", "4.1 mi", "http://s3-media2.ak.yelpcdn.com/bphoto/N2r0JV3GjbDlt5_HZS3uGQ/l.jpg")
p2 = Place("kevid", "Wo Ai Ni", "http://www.miasci.org/blog/wp-content/uploads/2010/03/MIASCI-Park-View4.jpg", "9 shingshong")

sf_rich_data = (f1, p1)
mia_rich_data = (rc1, r1)
mia_jw_data = (p2, r2)
