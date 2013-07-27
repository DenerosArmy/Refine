import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options as opt

opt.define("port", default = 9000, help = "Server Port Number", type = int)


class AndroidHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):
        user_id = self.get_argument("user_id")
        router_id = self.get_argument("router_id")
        self.write("0")
        self.finish()


class BrowserHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Connection established")

    def on_message(self, message):
        print("Message received")
        self.write_message("Server Response: " + message)

    def on_close(self):
        print("Connection terminated")


application = tornado.web.Application([
    (r"/push_updates", AndroidHandler),
    (r"/get_updates", BrowserHandler),
])

if __name__ == "__main__":
    print("Server running on port {0}".format(opt.options.port))
    application.listen(opt.options.port)
    tornado.ioloop.IOLoop.instance().start()
