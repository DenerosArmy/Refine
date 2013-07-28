import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options as opt

opt.define("port", default = 9000, help = "Server Port Number", type = int)

class AndroidHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):
        dev_id = self.get_argument("device_id")
        disp_id = self.get_argument("display_id")
        data = self.get_argument("data")
        if display_id:
            DISPLAY_MANAGER.add_device(dev_id, disp_id)
        else:
            DISPLAY_MANAGER.remove_device(dev_id)
        self.finish()


class DisplayManager(object):

    def __init__(self):
        self.displays = {}  # Mapping from display ID to a set of device IDs
        self.devices = {}  # Mapping from device ID to display ID

    def add_display(self, disp_id):
        self.displays[disp_id] = {}

    def add_device(self, dev_id, disp_id):
        self.displays[disp_id].add(dev_id)
        self.devices[dev_id] = disp_id

    def remove_device(self, dev_id):
        if dev_id in self.devices:
            self.displays[self.devices[dev_id]].remove(dev_id)
            self.devices[dev_id] = None

    def get_airport_data(self, disp_id):
        for dev_id in self.displays[disp_id]:
            #bus = get_bus(dev_id)
            pass
        return

DISPLAY_MANAGER = DisplayManager()

import random

class AirportUpdateHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("Connection established")

    def on_message(self, message):
        print("Message received")
        #DEVICE_MANAGER.get_airport_data()
        message = random.choice(("0" for _ in range(9))+("add_card",))
        self.write_message(message)

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
