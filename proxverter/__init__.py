import sys
import socket
import proxy
import tempfile
import shutil
import ipaddress
import platform
import os
import logging
import multiprocessing

from . import certgen
from . import sysproxy

class Proxverter:

    def __init__(self, ip, port, is_https=False, verbose=False, supress_errors=False):
        self.ip_address = ip
        self.port       = port
        self.is_https   = is_https
        self.verbose    = verbose
        self.supress_errors = supress_errors
        self.proxy      = sysproxy.Proxy(self.ip_address, self.port)

        ## Generating necessary data for certificates and private key
        if self.is_https:
            self.certgen = certgen.Generator()
            self.certgen.generate()

        ## Setting verbose mode
        if not self.verbose:
            logging.disable(logging.DEBUG)
            logging.disable(logging.INFO)
            logging.disable(logging.WARNING)
            logging.disable(logging.CRITICAL)

        if self.supress_errors:
            logging.disable(logging.ERROR)

    def gen_key(self, twrapper):
        if not self.is_https:
            raise ValueError("Private key can only be generated for https mode")

        if not hasattr(self, 'certgen'):
            raise AttributeError('No certgen attribute was found for Proxverter class')

        self.certgen.gen_key(twrapper)

    def gen_cert(self, twrapper):
        if not self.is_https:
            raise ValueError("Certificate can only be generated for https mode")

        if not hasattr(self, 'certgen'):
            raise AttributeError('No certgen attribute was found for Proxverter class')

        self.certgen.gen_cert(twrapper)

    def gen_pfx(self, twrapper):
        if not self.is_https:
            raise ValueError("PFX can only be generated for https mode")

        if not hasattr(self, 'certgen'):
            raise AttributeError('No certgen attribute was found for Proxverter class')

        self.certgen.gen_pfx(twrapper)

    def clear(self):
        if platform.system().lower() == "windows":
            dirm = os.path.join(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"), ".proxy")
            if os.path.isdir(dirm):
                shutil.rmtree(dirm)
        elif platform.system().lower() == "linux":
            dirm = os.path.join(os.getenv("HOMEPATH"), ".proxy")
            if os.path.isdir(dirm):
                shutil.rmtree(dirm)

    def join(self, priv_key=None, cert_file=None, plugins=[]):
        multiprocessing.freeze_support()
        self.clear()
        self.proxy.engage()

        try:
            if not self.is_https:
                proxy.main(
                    hostname = ipaddress.IPv4Address(self.ip_address),
                    port = self.port,
                    plugins = plugins
                )
            else:
                if not priv_key or not cert_file:
                    raise ValueError("Both priv_key and cert_file are required to run in TLS Interception mode")

                if not os.path.isfile(priv_key):
                    raise FileNotFoundError("Given private key file doesn't exists")

                if not os.path.isfile(cert_file):
                    raise FileNotFoundError("Given certificate file doesn't exists")

                proxy.main(
                    hostname = ipaddress.IPv4Address(self.ip_address),
                    port = self.port,
                    ca_key_file = priv_key,
                    ca_cert_file = cert_file,
                    ca_signing_key_file = priv_key,
                    plugins = plugins
                )

        except KeyboardInterrupt:
            pass

        self.proxy.cleanup()
