import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options as opt
import personalized_information as pi

opt.define("port", default = 9000, help = "Server Port Number", type = int)

class Display(object):

    def __init__(self, _type):
        self._type = _type
        self.devices = set()
        self.update_queue = []

    def has_device(self, device_id):
        return device_id in self.devices

    def add_device(self, dev_id):
        self.devices.add(dev_id)
        if self._type == "airport":
            print("Adding airport cards for {0}".format(dev_id))
            self.update_queue += self.get_airport_data(dev_id)
        elif self._type == "mall":
            print("Adding mall cards for {0}".format(dev_id))
            self.update_queue += self.get_mall_data(dev_id)

    def remove_device(self, dev_id):
        print("Removing all cards for {0}".format(dev_id))
        self.devices.remove(dev_id)
        self.update_queue.append(
            {"op": "-", "user_name": pi.get_username(dev_id)})

    def get_update(self):
        if self.update_queue:
            return self.update_queue.pop(0)
        return {"op": "0"}

    def get_airport_data(self, device_id):
        return pi.get_airport_data(device_id)

    def get_mall_data(self, device_id):
        #return pi.get_mall_data(device_id)
        return "Test"


class CurlHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):
        dev_id = self.get_argument("device_id")
        disp_id = self.get_argument("display_id")
        curr_connection = get_connected_display(dev_id)
        if curr_connection:
            if disp_id and curr_connection != disp_id:
                DISPLAYS[disp_id].add_device(dev_id)
                DISPLAYS[curr_connection].remove_device(dev_id)
            elif not disp_id:
                DISPLAYS[curr_connection].remove_device(dev_id)
        elif disp_id:
            DISPLAYS[disp_id].add_device(dev_id)
        self.finish()


class AndroidHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("Connection with Android established")

    def on_message(self, message):
        dev_id, disp_id = message.split("|")
        curr_connection = get_connected_display(dev_id)
        if curr_connection:
            if disp_id and curr_connection != disp_id:
                DISPLAYS[disp_id].add_device(dev_id)
                DISPLAYS[curr_connection].remove_device(dev_id)
            elif not disp_id:
                DISPLAYS[curr_connection].remove_device(dev_id)
        elif disp_id:
            DISPLAYS[disp_id].add_device(dev_id)
        self.finish()

    def on_close(self):
        print("Connection with Android terminated")


DISPLAYS = {"Jifi": Display("airport"), "Jifi2": Display("mall")}


def get_connected_display(device_id):
    for disp_id in DISPLAYS:
        if DISPLAYS[disp_id].has_device(device_id):
            return disp_id


class AirportUpdateHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("Connection with airport display established")

    def on_message(self, message):
        update = DISPLAYS["Jifi"].get_update()
        print("Sending message to airport: {0}".format(update))
        self.write_message(json.dumps(update))

    def on_close(self):
        print("Connection with airport display terminated")


class MallUpdateHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("Connection with mall display established")

    def on_message(self, message):
        update = DISPLAYS["Jifi2"].get_update()
        print("Sending message to mall: {0}".format(update))
        self.write_message(json.dumps(update))

    def on_close(self):
        print("Connection with mall display terminated")


application = tornado.web.Application([
    (r"/push_updates", AndroidHandler),
    (r"/curl_updates", CurlHandler),
    (r"/get_airport_updates", AirportUpdateHandler),
    (r"/get_mall_updates", MallUpdateHandler),
])

if __name__ == "__main__":
    print("Server running on port {0}".format(opt.options.port))
    application.listen(opt.options.port)
    tornado.ioloop.IOLoop.instance().start()
