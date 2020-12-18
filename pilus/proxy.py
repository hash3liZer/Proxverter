import requests
from flask import Flask

app = Flask(__name__)
app.logger.disabled = True

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def request(path):
    return path

class REQUEST:

    def __init__(self):
        pass

class PROXY:

    def __init__(self):
        pass

    def kickoff(self):
        app.run(
            host="0.0.0.0",
            port=8090,
            debug = False
        )
