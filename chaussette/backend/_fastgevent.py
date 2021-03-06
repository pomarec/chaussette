from gevent import monkey

import socket
from gevent.wsgi import WSGIServer
from gevent.pywsgi import WSGIHandler

from chaussette.util import create_socket


class CustomWSGIHandler(WSGIHandler):
    def log_request(self):
        if isinstance(self.code, (int, long)) and 400 <= self.code <= 599:
            WSGIHandler.log_request(self)


class Server(WSGIServer):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    handler_class = CustomWSGIHandler

    def __init__(self, listener, application=None, backlog=None,
                 spawn='default', log='default', handler_class=None,
                 environ=None, socket_type=socket.SOCK_STREAM,
                 address_family=socket.AF_INET, **ssl_args):
        monkey.noisy = False
        monkey.patch_all()
        host, port = listener
        self.socket = create_socket(host, port, self.address_family,
                                    self.socket_type, backlog=backlog)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = self.socket.getsockname()
        super(Server, self).__init__(self.socket, application, None, spawn,
                                     log, handler_class, environ, **ssl_args)
