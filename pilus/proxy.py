from hyper import HTTP11Connection
from hyper import HTTP20Connection
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from functools import partial

class PROXY(BaseHTTPRequestHandler):

    def __init__(self, prototypes, *args, **kwargs):
        self.prototypes = prototypes
        super().__init__(*args, **kwargs)

    def do_GET(self):
        host = self.headers.get('Host')
        if not host:
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(self.headers['Host'].encode())

class PROXYRUNNER:

    SERVER = None

    def __init__(self, ip, port, prototypes):
        self.ip = ip
        self.port = port
        self.prototypes = prototypes

    def kickoff(self):
        pp = partial(PROXY, self.prototypes)
        try:
            self.SERVER = HTTPServer(
                (self.ip, self.port), pp
            )
            self.SERVER.serve_forever()
        except:
            self.close()

    def close(self):
        if self.SERVER:
            self.SERVER.server_close()
