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
            self.update_queue += self.get_airport_data(dev_id)
        elif self._type == "mall":
            self.update_queue += self.get_mall_data(dev_id)

    def remove_device(self, dev_id):
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
        return pi.get_mall_data(device_id)


class AndroidHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):
        dev_id = self.get_argument("device_id")
        disp_id = self.get_argument("display_id")
        data = self.get_argument("data")
        curr_connection = get_connected_display(device_id)
        if display_id and curr_connection != display_id:
            DISPLAYS[disp_id].add_device(dev_id)
            DISPLAYS[curr_connection].remove_device(dev_id)
            DISPLAY_MANAGER.add_device(dev_id, disp_id)
        elif curr_connection:
            DISPLAYS[curr_connection].remove_device(dev_id)
            DISPLAY_MANAGER.remove_device(dev_id)
        self.finish()


DISPLAYS = {"1": Display("airport"), "2": Display("mall")}


def get_connected_display(device_id):
    for disp_id, disp in DISPLAYS:
        if disp.has_device(device_id):
            return disp_id


class AirportUpdateHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("Connection established")

    def on_message(self, message):
        print("Message received")
        update = DISPLAYS[message].get_update()
        self.write_message(json.dump(update))

    def on_close(self):
        print("Connection terminated")


application = tornado.web.Application([
    (r"/push_updates", AndroidHandler),
    (r"/get_airport_updates", AirportUpdateHandler),
])

if __name__ == "__main__":
    print("Server running on port {0}".format(opt.options.port))
    application.listen(opt.options.port)
    tornado.ioloop.IOLoop.instance().start()
