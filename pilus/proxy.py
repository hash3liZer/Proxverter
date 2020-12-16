import requests
from twisted.web import server, resource
from twisted.internet import reactor, endpoints

class Request(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        return "<html>Hello, world!</html>"

class PROXY:

    def __init__(self):
        pass

    def kickoff(self):
        print("Running on Port 80")
        site = server.Site(Request())
        endpoint = endpoints.TCP4ServerEndpoint(reactor, 80)
        endpoint.listen(site)
        reactor.run()
