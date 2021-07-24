import sys
import socket
import proxy
import tempfile
import shutil
import ipaddress
import platform
import os
import pathlib
import logging
import multiprocessing

## Package Imports
from . import certgen
from . import sysprox as sprox

class Proxverter:
    '''
    The main Proxverter class that accepts creds, setup system wide caches and run proxy servers.
    '''

    def __init__(self, ip, port, is_https=False, new_certs=False, sysprox=False, verbose=False, suppress_errors=False):
        self.ip_address = ip
        self.port       = port
        self.is_https   = is_https
        self.new_certs  = new_certs
        self.sysprox    = sysprox
        self.verbose    = verbose
        self.suppress_errors = suppress_errors
        self.home_paths = self.__fetch_home_paths()
        self.proxy      = sprox.Proxy(self.ip_address, self.port)

        ## Generating necessary data for certificates and private key
        if self.is_https:
            self.__gen_certs()

        ## Setting system wide proxy
        if self.sysprox:
            self.set_sysprox()

        ## Setting verbose mode
        if not self.verbose:
            logging.disable(logging.DEBUG)
            logging.disable(logging.INFO)
            logging.disable(logging.WARNING)
            logging.disable(logging.CRITICAL)

        ## Suppressing errors on demand
        if self.suppress_errors:
            logging.disable(logging.ERROR)

    def __fetch_home_paths(self):
        dirname = os.path.join(pathlib.Path.home(), ".proxverter")
        rtval = {
            'dirname': dirname,
            'certname': os.path.join(dirname, "cert.pem"),
            'privname': os.path.join(dirname, "priv.pem"),
            'pfxname': os.path.join(dirname, "cert.pfx")
        }

        if not os.path.isdir(rtval['dirname']):
            os.makedirs(rtval['dirname'])

        return rtval

    def __gen_certs(self):
        if not os.path.isfile(self.home_paths['certname']) \
           or not os.path.isfile(sef.home_paths['privname']) \
           or not os.path.isfile(self.home_paths['pfxname']) \
           or self.new_certs:

           gen = certgen.Generator()
           gen.generate()
           gen.gen_key(self.home_paths['privname'])
           gen.gen_cert(self.home_paths['certname'])
           gen.gen_pfx(self.home_paths['pfxname'])

    def __clear(self):
        try:
            shutil.rmtree(
                os.path.join(pathlib.Path.home(), ".proxy")
            )
        except FileNotFoundError:
            pass

    def set_sysprox(self):
        self.proxy.engage()

    def del_sysprox(self):
        self.proxy.cleanup()

    def fetch_pkey(self, destination):
        if not self.is_https:
            raise ValueError("Private keys are only implemented in SSL Mode")

        if not os.path.isfile(self.home_paths['privname']):
            raise FileNotFoundError("No private key file was found in home directory. It has either been modified or deleted. ")

        shutil.copyfile(self.home_paths['privname'], destination)

    def fetch_cert(self, destination):
        if not self.is_https:
            raise ValueError("Certificates are only implemented in SSL Mode")

        if not os.path.isfile(self.home_paths['certname']):
            raise FileNotFoundError("No cert file was found in home directory. It has either been modified or deleted. ")

        shutil.copyfile(self.home_paths['certname'], destination)

    def fetch_pfx(self, destination):
        if not self.is_https:
            raise ValueError("PFXs are only implemented in SSL Mode")

        if not os.path.isfile(self.home_paths['certname']):
            raise FileNotFoundError("No pfx file was found in home directory. It has either been modified or deleted. ")

        shutil.copyfile(self.home_paths['pfxname'], destination)

    def engage(self):
        multiprocessing.freeze_support()
        self.__clear()

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

        if self.sysprox:
            self.del_sysprox()
