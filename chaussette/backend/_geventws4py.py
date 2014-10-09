from ws4py.server.geventserver import (WebSocketWSGIHandler,
                                       GEventWebSocketPool)
from chaussette.backend._gevent import Server as GeventServer


class CustomWebSocketWSGIHandler(WebSocketWSGIHandler):
    def log_request(self):
        if isinstance(self.code, (int, long)) and 400 <= self.code <= 599:
            WebSocketWSGIHandler.log_request(self)


class Server(GeventServer):
    handler_class = CustomWebSocketWSGIHandler

    def __init__(self, *args, **kwargs):
        GeventServer.__init__(self, *args, **kwargs)
        self.pool = GEventWebSocketPool()

    def stop(self, *args, **kwargs):
        self.pool.clear()
        self.pool = None
        GeventServer.stop(self, *args, **kwargs)
