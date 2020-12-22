import configparser
import os
import re
import pathlib
from pull import PULL

pull = PULL()

class CONFIG:
    BASEPATH = os.path.join(pathlib.Path(__file__).resolve().parent.parent, 'config.ini')
    REGEX_DOMAIN = r"/^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/"
    REGEX_IPADDRESS = r"'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b'"

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
            'prototypes_path': '/usr/share/proxverter/prototypes',
            'port': 80,
        }

        obj['states'] = {}
        obj['hostnames'] = {}

        for prototype in _prototypes:
            obj['states'][prototype.get('name')] = 'stopped'

        for prototype in _prototypes:
            obj['hostnames'][prototype.get('name')] = ''

        self.save_fresh_config(obj)

    def update_config(self, _prototypes):
        obj = self.get_fresh_config()
        states = list(obj['states'].keys())
        hostnames = list(obj['hostnames'].keys())
        for prototype in _prototypes:
            if prototype.get('name') not in states:
                obj['states'][prototype.get('name')] = 'stopped'

            if prototype.get('name') not in hostnames:
                obj['hostnames'][prototype.get('name')] = ''

        self.save_fresh_config(obj)

    def write_conig(self, _name, _val):
        obj = self.get_fresh_config()
        obj['configuration'][_name] = _val
        self.save_fresh_config(obj)

class CONFIGREADER(CONFIG):

    def exists(self):
        if os.path.isfile(self.BASEPATH):
            return True
        return False

    def get_state(self, _prototype):
        config_obj = self.get_fresh_config()
        for (prototype, value) in config_obj['states'].items():
            if prototype == _prototype:
                return value

        return ''

    def get_hostname(self, _prototype):
        config_obj = self.get_fresh_config()
        for (prototype, value) in config_obj['hostnames'].items():
            if prototype == _prototype:
                return value

        return ''

    def get_port(self):
        obj = self.get_fresh_config()
        return int(obj['configuration']['port'])

class CONFIGURATION:

    def __init__(self, prs):
        self.parser = prs
        self.config_reader = CONFIGREADER()
        self.config_writer = CONFIGWRITER()

    def invalid(self):
        pull.session(
            ('#bb00c2 bold', '; '),
            ('', 'Invalid Syntax'),
        )

    def write_domain(self, _val):
        if _val:
            obj = re.match(self.REGEX_DOMAIN, _val[0])
            if obj:
                self.write_config('domain', _val[0])
            else:
                pull.session(
                    ('#bb00c2 bold', '; '),
                    ('', 'The provided domain value is not valid: '),
                    ('#bb00c2', _val[0])
                )
        else:
            self.invalid()

    def write_ipaddress(self, _val):
        if _val:
            obj = re.match(self.REGEX_IADDRESS, _val[0])
            if obj:
                self.write_config('ipaddress', _val[0])
            else:
                pull.session(
                    ('#bb00c2 bold', '; '),
                    ('', 'The provided ip address value is not valid: '),
                    ('#bb00c2', _val[0])
                )
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
        if self.parser.subcommand == "DOMAIN":
            self.write_domain(self.parser.args)
        elif self.parser.subcommand == "IP_ADDRESS":
            self.write_ipaddress(self.parser.args)
        elif self.parser.subcommand == "PROTOTYPES_PATH":
            self.write_prototypes_path(self.parser.args)
        elif self.parser.subcommand == "PORT":
            self.write_port(self.parser.args)
        elif self.parser.subcommand == "LIST":
            self.list_config()
        else:
            self.invalid()
