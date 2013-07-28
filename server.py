import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options as opt
import personalized_information as pi

opt.define("port", default = 9000, help = "Server Port Number", type = int)

class Display(object):

    def __init__(self, place):
        self.place = place
        self.devices = set()
        self.update_queue = []

    def has_device(self, device_id):
        return device_id in self.devices

    def add_device(self, dev_id):
        self.devices.add(dev_id)
        print("Adding cards for {0} in {1}".format(dev_id, self.place))
        self.update_queue += self.get_data(dev_id, self.place)

    def remove_device(self, dev_id):
        print("Removing all cards for {0}".format(dev_id))
        self.devices.remove(dev_id)
        self.update_queue.append(
            {"op": "-", "user_name": pi.User.get_user_name(dev_id)})

    def get_update(self):
        if self.update_queue:
            return self.update_queue.pop(0)
        return {"op": "0"}

    def get_data(self, device_id, place):
        return pi.get_data(device_id, place)


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
        print("Received message {0} from Android".format(message))
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

    def on_close(self):
        print("Connection with Android terminated")


DISPLAYS = {"Jifi": Display("sf"), "NETGEAR": Display("miami")}


def get_connected_display(device_id):
    for disp_id in DISPLAYS:
        if DISPLAYS[disp_id].has_device(device_id):
            return disp_id


class SFUpdateHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("Connection with SF display established")

    def on_message(self, message):
        update = DISPLAYS["Jifi"].get_update()
        print("Sending message to SF: {0}".format(update))
        self.write_message(json.dumps(update))

    def on_close(self):
        print("Connection with SF display terminated")


class MiamiUpdateHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("Connection with Miami display established")

    def on_message(self, message):
        update = DISPLAYS["NETGEAR"].get_update()
        print("Sending message to Miami: {0}".format(update))
        self.write_message(json.dumps(update))

    def on_close(self):
        print("Connection with Miami display terminated")


application = tornado.web.Application([
    (r"/push_updates", AndroidHandler),
    (r"/curl_updates", CurlHandler),
    (r"/get_sf_updates", SFUpdateHandler),
    (r"/get_miami_updates", MiamiUpdateHandler),
])

if __name__ == "__main__":
    print("Server running on port {0}".format(opt.options.port))
    application.listen(opt.options.port)
    tornado.ioloop.IOLoop.instance().start()
