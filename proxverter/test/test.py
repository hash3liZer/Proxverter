import sys
import os
import tempfile
import logging
import pydoc
import multiprocessing
import proxverter
from proxverter.plugins import PluginBase

class ProxyCheck(PluginBase):

    def intercept_request(self, request):
        fl = open("/tmp/filer1.txt", "w")
        fl.write(str(request.url))
        fl.close()

        return request

    def interept_response(self, response):
        fl = open("/tmp/filer2.txt", "w")
        fl.write(str(response.body))
        fl.close()

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
