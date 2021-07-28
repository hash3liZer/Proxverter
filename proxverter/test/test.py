import sys
import os
import tempfile
import logging
import pydoc
import multiprocessing
import proxverter
from proxverter.plugins import PluginBase

class ProxyCheck(PluginBase):
    def before_upstream_connection(self, request):
        towrite = pydoc.render_doc(request, renderer=pydoc.plaintext)
        fl = open("/tmp/filer.txt", "w")
        fl.write(towrite)
        fl.write("\n\n\n\n")
        fl.write(str(request.url) + "\n")
        fl.write(str(request.method) + "\n")
        fl.write(str(request.code) + "\n")
        fl.write(str(request.reason) + "\n")
        fl.write(str(request.version) + "\n")
        fl.write(str(request.host) + "\n")
        fl.write(str(request.port) + "\n")
        fl.write(str(request.path) + "\n")
        fl.write(str(request.headers) + "\n\n")
        fl.write(str(request.body) + "\n")
        fl.close()

        return request

    def handle_client_request(self, request):
        towrite = pydoc.render_doc(request, renderer=pydoc.plaintext)
        fl = open("/tmp/filer2.txt", "w")
        fl.write(towrite)
        fl.write("\n\n\n\n")
        fl.write(str(request.url) + "\n")
        fl.write(str(request.method) + "\n")
        fl.write(str(request.code) + "\n")
        fl.write(str(request.reason) + "\n")
        fl.write(str(request.version) + "\n")
        fl.write(str(request.host) + "\n")
        fl.write(str(request.port) + "\n")
        fl.write(str(request.path) + "\n")
        fl.write(str(request.headers) + "\n\n")
        fl.write(str(request.body) + "\n")
        fl.close()

        return request

    def handle_upstream_chunk(self, response):
        fl = open("/tmp/filer3.txt", "w")
        fl.write(str(response.tobytes()))

        return response

if __name__ == "__main__":
    multiprocessing.freeze_support()

    p = proxverter.Proxverter(
        "127.0.0.1",
        8700,
        is_https=True,
        verbose=True,
        plugins=[
            ProxyCheck
        ]
    )

    p.fetch_cert("/home/hash3lizer/Desktop/cert.crt")
    p.fetch_pfx("/home/hash3lizer/Desktop/cert.pfx")

    p.set_sysprox()
    p.engage()
    p.del_sysprox()
