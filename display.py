#!/usr/bin/env python
import tornado.websocket
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import os
import json
import datetime
import socket
import config

root = os.path.dirname(__file__)
hostname = socket.gethostname()
# can be started on a different port using --port=9999 on when starting
define("port", default=str(config.port), help="Bind to port number")
tornado.options.parse_command_line()

clients = []
# the message history is pre-seeded with a default title and message. These
# will be the initial items displayed on the screen before any updates
msg_history = []
msg_history.append({'id': 'page_title', 'message': config.display_title})
msg_history.append({'id': 'message'
       , 'message': config.display_content.format(hostname, options.port)})

def sendMsg(message):
    """ Iterate through the list of currently connected clients and send the
    message through the open web socket. The sent message is recorded in the
    message history array. This histort is used to recreate the display
    when a new client connects or reconnects
    """
    for client in clients:
        if not client.ws_connection.stream.socket:
            print("client disconnected\n")
            clients.remove(client)
        else:
            client.write_message(message)
    # store the message in the message history array, only the last message
    # for each distinct id is stored.
    msg = json.loads(message)
    # remove any exisitng message for this id from the array
    msg_history[:] = [m for m in msg_history if m.get('id') != msg.get('id')]
    msg_history.append(msg)

def sendTime():
    """ Sends the current time to all connected clients in a time message
        clients can then put the time on the screen"""
    sendMsg(json.dumps({'id': 'time'
      , 'message': datetime.datetime.now().strftime("%d %b %H:%M")}))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
      self.render('index.html', host=hostname, port=options.port)

class ElementHandler(tornado.web.RequestHandler):
    def put(self, element_id):
      msg = self.request.body
      sendMsg(json.dumps({'id': element_id, 'message': msg.decode("utf-8")}))
    def get(self, element_id):
        try:
            msg = next((msg for msg in msg_history if msg.get('id') == element_id))
            self.write(msg['message'])
        except:
            raise tornado.web.HTTPError(404)

class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        """Called when a new client connects. Store the new client in the list
        of clients. Send any messages in the message history to the client.
        """
        print('new client connected.\n')
        if self not in clients:
            clients.append(self)
            # now send the message history to this new client
            for msg in msg_history:
                self.write_message(json.dumps(msg))

    def on_close(self):
        print('connection closed\n')
        if self in clients:
            clients.remove(self)

def make_app():
    return tornado.web.Application([
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {'path': ''}),
        (r'/images/(.*)', tornado.web.StaticFileHandler, {'path': './images'}),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(root, 'static')}),
        (r'/socket', SocketHandler),
        (r'/([^/]+)', ElementHandler),
        (r'/', MainHandler),
    ], template_path=root, autoreload=False)

if __name__ == "__main__":
    print("Starting display; visit http://"+hostname+":"+str(options.port)
         +" to see the display.")
    print("Try: "+config.example_curl_cmd.format(hostname, options.port))
    app = make_app()
    app.listen(options.port)

    main_loop = tornado.ioloop.IOLoop.current()
    time_loop = tornado.ioloop.PeriodicCallback(sendTime, 1000, io_loop = main_loop)

    time_loop.start()
    main_loop.start()
