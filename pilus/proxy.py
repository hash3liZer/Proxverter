import requests
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

    def __init__(self):
        pass

    def kickoff(self):
        app.run(
            host="0.0.0.0",
            port=8090,
            debug = False
        )
