import platform
import socket

class mac_proxy:
    '''
    Refers to the macos version of system wide proxy. Refer to `Proxy` class for initializing system wide proxy.
    '''

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port       = port

    def join(self):
        pass

class lin_proxy:
    '''
    Refers to the linux version of system wide proxy. Refer to `Proxy` class for initializing system wide proxy.
    '''

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port       = port

    def join(self):
        pass

class win_proxy:
    '''
    Refers to the windows version of system wide proxy. Refer to `Proxy` class for initializing system wide proxy.
    '''

    def __init__(self, ip_address, port):
        self.glob_import('winreg')
        self.glob_import('ctypes')

        self.regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_ALL_ACCESS)
        self.internet_option_refresh = 37
        self.internet_option_settings_changed = 39
        self.internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

        self.ip_address = ip_address
        self.port      = port

    def glob_import(self, module_name):
        globals()[module_name] = __import__(module_name)

    def refresh(self):
        self.internet_set_option(0, self.internet_option_settings_changed, 0, 0)
        self.internet_set_option(0, self.internet_option_refresh, 0, 0)

    def set_key(self, name, value):
        try:
            _, reg_type = winreg.QueryValueEx(self.regkey, name)
            winreg.SetValueEx(self.regkey, name, 0, reg_type, value)
        except FileNotFoundError:
            winreg.SetValueEx(self.regkey, name, 0, winreg.REG_SZ, value)

    def set_proxy(self):
        try:
            self.set_key('ProxyEnable', 1)
            #self.set_key('ProxyOverride', u'*.local;<local>')
            self.set_key('ProxyServer', u'%s:%i' % (self.ip_address, self.port))
            return True
        except IndexError:
            raise ValueError(f"Unable to find the registry path for proxy")
            return False

    def del_proxy(self):
        try:
            self.set_key('ProxyEnable', 0)
        except FileNotFoundError:
            pass

    def join(self):
        if not self.set_proxy():
            raise ValueError(f"Error setting proxy credentials")

        self.refresh()

class Proxy:

    ## Gets necessary information and kill mitmproxy if already running
    def __init__(self, ip_address, port):
        '''
            Accepts two arguments:

            ip_address: The IP address for system wide proxy
            port: The port for system wide proxy
        '''
        self.ip_address = ip_address
        self.port = port

    def check_connection(self):
        '''
            Checks if the given ip and port are available to be binded on the system
        '''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(( self.ip_address, self.port ))
            s.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_prox_instance(self):
        plat = platform.system().lower()
        if plat == "windows":
            prox = win_proxy(self.ip_address, self.port)
        elif plat == "linux":
            prox = lin_proxy(self.ip_address, self.port)
        elif plat == "macos":
            prox = mac_proxy(self.ip_address, self.port)
        else:
            raise OSError("Unable to determine the underlying operating system")

        return prox

    def engage(self):
        '''
            Setup system wide proxy.
        '''

        if not self.check_connection():
            raise ValueError(f"Unable to establish connection on {self.ip_address}:{self.port}")

        prox = self.get_prox_instance()
        prox.join()

    def cleanup(self):
        '''
            Removes system wide proxy
        '''

        prox = self.get_prox_instance()
        prox.del_proxy()

        if hasattr(prox, 'refresh'):
            prox.refresh()
