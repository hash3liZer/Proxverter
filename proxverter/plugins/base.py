from proxy.http.parser import HttpParser, httpParserTypes, httpParserStates
from proxy.http.proxy import HttpProxyBasePlugin

class PluginBase(HttpProxyBasePlugin, ABC):
    '''Modified HttpProxyBasePlugin from proxy.py. Provides more functionality'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request  = HttpParser(httpParserTypes.REQUEST_PARSER)
        self.response = HttpParser(httpParserTypes.RESPONSE_PARSER)

    def before_upstream_connection(self, connection):
        return self.intercept_connection(connection)

    def handle_client_request(self, request):
        rtval = self.intercept_request(request)
        self.request = rtval
        return rtval

    def handle_upstream_chunk(self, chunk):
        self.response.parse(response.tobytes())
        if self.response.state = httpParserStates.COMPLETE:
            self.intercept_response(self.response)
        return self.intercept_chunk(chunk)

    def on_upstream_connection_close(self):
        self.close_connection()

    def intercept_connection(self, conn):
        pass

    def intercept_request(self, request):
        pass

    def intercept_chunk(self, chunk):
        return chunk

    def intercept_response(self, response):
        pass

    def close_connection(self):
        pass
