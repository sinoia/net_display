#!/usr/bin/env python
import tornado.websocket
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import os
import json
import datetime
import socket

clients = []
root = os.path.dirname(__file__)
hostname = socket.gethostname()
# can be started on a different port using --port=9999 on when starting
define("port", default="8888", help="Bind to port number")
tornado.options.parse_command_line()

def sendMsg(message):
    for client in clients:
        if not client.ws_connection.stream.socket:
            print("client disconnected\n")
            clients.remove(client)
        else:
            client.write_message(message)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
      self.render('index.html', host=hostname, port=options.port)

class MsgHandler(tornado.web.RequestHandler):
    def put(self):
      # msg = json.loads(self.request.body)
      msg = self.request.body
      sendMsg(msg)

class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('new client connected.\n')
        if self not in clients:
            clients.append(self)
    def on_close(self):
        print('connection closed\n')
        if self in clients:
            clients.remove(self)

def make_app():
    return tornado.web.Application([
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {'path': ''}),
        (r'/images/(.*)', tornado.web.StaticFileHandler, {'path': './images'}),
        (r'/socket', SocketHandler),
        (r'/msg', MsgHandler),
        (r'/', MainHandler),
    ], template_path=root)

if __name__ == "__main__":
    print("Starting display; visit http://"+hostname+":"+str(options.port)
         +" to see the display.")
    print("Try: curl http://"+hostname+":"+options.port
         +"/msg -XPUT -d '{\"id\": \"message\", \"message\": \"Hello World\"}'")
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
