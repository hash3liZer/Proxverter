from hyper import HTTP11Connection
from hyper import HTTP20Connection
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from functools import partial
from handlers import CONFIGREADER

import socket

class PROXY(BaseHTTPRequestHandler):

    def __init__(self, ip, port, proxverter, *args, **kwargs):
        self.param_ip   = ip
        self.param_port = port
        self.proxverter = proxverter
        self.config_reader = CONFIGREADER()
        super().__init__(*args, **kwargs)

    def get_prototype(self, _name):
        for _prototype in self.proxverter.prototypes:
            if _prototype['name'] == _name:
                return _prototype

    def custom_connection(self, target, protocol, http_version, method, url, headers):
        host = '{}:{}'.format(target, ('443' if protocol == 'https' else '80'))
        conn = HTTP11Connection(host)
        
        try:
            conn.request(method, url, headers=dict(headers))
        except socket.gaierror:
            return None

        resp = conn.get_response()
        return resp

    def do_GET(self):
        host = self.headers.get('Host')
        domain = self.config_reader.get_domain()
        hostnames = self.config_reader.get_hostnames()

        if not host or not domain:
            self.send_response(404); return

        host = host.split(":")
        if len(host) == 2:
            port = int(host[1])
            host = host[0]
        else:
            port = 80
            host = host[0]

        if port != self.param_port:
            self.send_response(404); return

        if not host.endswith(domain):
            self.send_response(404); return

        for (prototype, hostname) in hostnames.items():
            if host.endswith(hostname):
                _param_prototype = self.get_prototype(prototype)
                _param_domain = host.replace(".{}".format(hostname), "")
                for _param_prototype_domain in _param_prototype["domains"]:
                    if _param_domain.endswith(_param_prototype_domain):
                        prototype = self.get_prototype(prototype)
                        response = self.custom_connection(
                            _param_domain,
                            prototype.get("proto"),
                            prototype.get("http_version"),
                            self.command,
                            self.path,
                            self.headers
                        )
                        if response:
                            self.send_response(response.status, response.reason)
                            for (header, value) in response.headers.items():
                                self.send_header(header, value)
                            self.wfile.write(response.read())
                        else:
                            self.send_response(404)
                        return

        self.send_response(404)
        return

class PROXYRUNNER:

    SERVER = None

    def __init__(self, ip, port, proxverter):
        self.ip = ip
        self.port = port
        self.proxverter = proxverter

    def kickoff(self):
        pp = partial(PROXY, self.ip, self.port, self.proxverter)
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
