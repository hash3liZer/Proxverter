import sys
import socket
import proxy
import ctypes
import winreg
import certgen
import tempfile
import ipaddress
import multiprocessing

class Proxy:

    ## Registry key for modifying proxy settings
    INTERNET_SETTINGS = winreg.OpenKey(
                            winreg.HKEY_CURRENT_USER,
                            r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                            0, winreg.KEY_ALL_ACCESS
                        )

    ## Gets necessary information and kill mitmproxy if already running
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    ## Refresh setings after changing them in registry
    def refresh(self):
        INTERNET_OPTION_REFRESH = 37
        INTERNET_OPTION_SETTINGS_CHANGED = 39

        internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

        internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
        internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)

    ## Set the key in the internet settings registry as specified
    def set_key(self, name, value):
        try:
            _, reg_type = winreg.QueryValueEx(self.INTERNET_SETTINGS, name)
            winreg.SetValueEx(self.INTERNET_SETTINGS, name, 0, reg_type, value)
        except FileNotFoundError:
            winreg.SetValueEx(self.INTERNET_SETTINGS, name, 0, winreg.REG_SZ, value)

    ## Sets the proxy for whole system
    def set_proxy(self):
        try:
            self.set_key('ProxyEnable', 1)
            #self.set_key('ProxyOverride', u'*.local;<local>')
            self.set_key('ProxyServer', u'%s:%i' % (self.ip_address, self.port))
            return True
        except IndexError:
            raise ValueError(f"Unable to find the registry path for proxy")
            return False

    ## Deletes proxy for the whole system
    def del_proxy(self):
        try:
            self.set_key('ProxyEnable', 0)
        except FileNotFoundError:
            pass

    def check_connection(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(( self.ip_address, self.port ))
            s.close()
            return True
        except Exception as e:
            print(e)
            return False

    ## Engage method for the network collector
    def engage(self):
        if not self.check_connection():
            raise ValueError(f"Unable to establish connection on {self.ip_address}:{self.port}")

        if not self.set_proxy():
            raise ValueError(f"Error setting proxy credentials")

        self.refresh()

class Proxverter:

    def __init__(self, ip, port, is_https=False):
        self.ip_address = ip
        self.port       = port
        self.is_https   = is_https
        self.proxy      = Proxy(self.ip_address, self.port)

        ## Generating necessary data for certificates and private key
        if self.is_https:
            self.certgen = certgen.Generator()
            self.certgen.generate()

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

    def join(self):
        multiprocessing.freeze_support()
        self.proxy.engage()

        try:
            if not self.is_https:
                '''
                proxy.main(
                    hostname = ipaddress.IPv4Address(self.ip_address),
                    port = self.port
                )
                '''
            else:
                ktfile = tempfile.TemporaryFile()
                ctfile = tempfile.TemporaryFile()

                self.gen_key(ktfile)
                self.gen_cert(ctfile)

                '''
                proxy.main(
                    hostname = ipaddress.IPv4Address(self.ip_address),
                    port = self.port,
                    #ca_key_file = ktfile,
                    #ca_cert_file = ctfile,
                    #ca_signing_key_file = ktfile
                )
                '''

        except KeyboardInterrupt:
            pass

        self.proxy.del_proxy()
        self.proxy.refresh()
