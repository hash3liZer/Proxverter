import configparser
import os
import pathlib
from pull import PULL

pull = PULL()

class CONFIG:
    BASEPATH = os.path.join(pathlib.Path(__file__).resolve().parent.parent, 'config.ini')

    def get_fresh_config(self):
        cf = configparser.ConfigParser()
        cf.read(self.BASEPATH)
        return cf

    def save_fresh_config(self, config_obj):
        fl = open(self.BASEPATH, 'w')
        config_obj.write(fl)

class CONFIGWRITER(CONFIG):

    def create_config(self, _prototypes):
        obj = configparser.ConfigParser()
        obj['configuration'] = {
            'domain': '',
            'ipaddress': '',
            'certificates_path': '/usr/share/proxverter/',
            'prototypes_path': '/usr/share/proxverter/prototypes',
            'debug': False,
            'port': 443,
        }

        obj['prototypes'] = {}

        for prototype in _prototypes:
            obj['prototypes'][prototype.get('name')] = 'stopped'

        self.save_fresh_config(obj)

    def update_config(self, _prototypes):
        obj = self.get_fresh_config()
        prototypes = list(obj['prototypes'].keys())
        for prototype in _prototypes:
            if prototype.get('name') not in prototypes:
                obj['prototypes'][prototype.get('name')] = 'stopped'

        self.save_fresh_config(obj)

class CONFIGREADER(CONFIG):

    def exists(self):
        if os.path.isfile(self.BASEPATH):
            return True
        return False

    def get_state(self, _prototype):
        config_obj = self.get_fresh_config()
        for (prototype, state) in config_obj['prototypes'].items():
            if prototype == _prototype:
                return state

        return ''

class CONFIGURATION:

    def __init__(self, prs):
        self.parser = prs

    def invalid(self):
        pull.session(
            ('#d9ce0b bold', '~ '),
            ('', 'Invalid Syntax'),
        )

    def write_debug(self, _val):
        if _val:
            cf = configparser.ConfigParser()
            cf.read(os.path.join(pull.BASE_DIR, 'config.ini'))

            if _val[0] == "on":
                cf['configuration']['debug'] = 'True'
            elif _val[0] == "off":
                cf['configuration']['debug'] = 'False'
            else:
                self.invalid()

            fl = open(os.path.join(pull.BASE_DIR, 'config.ini'), 'w')
            cf.write(fl)
        else:
            self.invalid()

    def write_domain(self, _val):
        if _val:
            cf = configparser.ConfigParser()
            cf.read(os.path.join(pull.BASE_DIR, 'config.ini'))

            cf['configuration']['domain'] = _val[0]

            fl = open(os.path.join(pull.BASE_DIR, 'config.ini'), 'w')
            cf.write(fl)
        else:
            self.invalid()

    def write_ipaddress(self, _val):
        if _val:
            cf = configparser.ConfigParser()
            cf.read(os.path.join(pull.BASE_DIR, 'config.ini'))

            cf['configuration']['ipaddress'] = _val[0]

            fl = open(os.path.join(pull.BASE_DIR, 'config.ini'), 'w')
            cf.write(fl)
        else:
            self.invalid()

    def write_prototypes_path(self, _val):
        if _val:
            cf = configparser.ConfigParser()
            cf.read(os.path.join(pull.BASE_DIR, 'config.ini'))

            cf['configuration']['prototypes_path'] = _val[0]

            fl = open(os.path.join(pull.BASE_DIR, 'config.ini'), 'w')
            cf.write(fl)
        else:
            self.invalid()

    def write_certificates_path(self, _val):
        if _val:
            cf = configparser.ConfigParser()
            cf.read(os.path.join(pull.BASE_DIR, 'config.ini'))

            cf['configuration']['certificates_path'] = _val[0]

            fl = open(os.path.join(pull.BASE_DIR, 'config.ini'), 'w')
            cf.write(fl)
        else:
            self.invalid()

    def write_port(self, _val):
        if _val:
            cf = configparser.ConfigParser()
            cf.read(os.path.join(pull.BASE_DIR, 'config.ini'))

            cf['configuration']['port'] = _val[0]

            fl = open(os.path.join(pull.BASE_DIR, 'config.ini'), 'w')
            cf.write(fl)
        else:
            self.invalid()

    def list_config(self):
        cf = configparser.ConfigParser()
        cf.read(os.path.join(pull.BASE_DIR, 'config.ini'))

        keys = list(cf['configuration'].keys())

        for key in keys:
            print(key)

    def execute(self):
        if self.parser.subcommand == "domain":
            self.write_domain(self.parser.args)
        elif self.parser.subcommand == "ipaddress":
            self.write_ipaddress(self.parser.args)
        elif self.parser.subcommand == "prototypes_path":
            self.write_prototypes_path(self.parser.args)
        elif self.parser.subcommand == "certificates_path":
            self.write_certificates_path(self.parser.args)
        elif self.parser.subcommand == "debug":
            self.write_debug(self.parser.args)
        elif self.parser.subcommand == "port":
            self.write_port(self.parser.args)
        elif self.parser.subcommand == "list":
            self.list_config()
        else:
            self.invalid()
