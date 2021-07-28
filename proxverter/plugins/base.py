from proxy.http.proxy import HttpProxyBasePlugin

## The class to be inherited
class PluginBase(HttpProxyBasePlugin):

    def name(self):
        '''
            Returns the name of plugin
        '''
        return "Plugin Base"

    ## Returns the description of plugin
    def description(self):
        '''
            Returns the description of plugin
        '''
        return "This is base proxy plugin which is to be inherited by custom coded plugins for proxverter"

    def before_upstream_connection(self, request):
        '''
            Function to be called before the upstream connection is established.
            Remember this is the part where the connection has not yet established.
            And the data is still in manipulation phase.

            You can edit the request here
        '''
        return request

    def handle_client_request(self, request):
        '''
            Function to be called while the data is being sent to the upstream server.
            Remember this is the part where the connection has been established.
            And we are looking to modify on the ongoing request.
        '''
        return request

    def handle_upstream_chunk(self, response):
        '''
            Response received from the server
        '''
        return response

    def on_upstream_connection_close(self):
        return None
