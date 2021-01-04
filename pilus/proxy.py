from hyper import HTTP11Connection
from hyper import HTTP20Connection
from flask import Flask
from flask import request as flask_request

app = Flask(__name__)
app.logger.disabled = True

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy_handler(path):
    proxy = PROXY(
        flask_request.method,
        flask_request.headers,
        flask_request.cookies,
        flask_request.form,
    )
    return proxy.render()

class PROXY:

    def __init__(self, method, headers, cookies, form):
        self.method = method
        self.headers = headers
        self.cookies = cookies
        self.form    = form

    def render(self):
        return

class PROXYRUNNER:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def kickoff(self):
        app.run(
            host=self.ip,
            port=self.port,
            debug = False
        )
