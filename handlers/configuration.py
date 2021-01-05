import configparser
import os
import re
import pathlib
from pull import PULL

pull = PULL()

class CONFIG:
    BASEPATH = os.path.join(pathlib.Path(__file__).resolve().parent.parent, 'config.ini')
    REGEX_DOMAIN = r"^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$"
    REGEX_IPADDRESS = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}"

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
            'ipaddress': '0.0.0.0',
            'prototypes_path': '/usr/share/proxverter/prototypes',
            'port': 80,
        }

        obj['states'] = {}
        obj['hostnames'] = {}

        for prototype in _prototypes:
            obj['states'][prototype.get('name')] = 'stopped'

        for prototype in _prototypes:
            obj['hostnames'][prototype.get('name')] = '{}.undefined'.format(prototype.get('name'))

        self.save_fresh_config(obj)

    def update_config(self, _prototypes):
        obj = self.get_fresh_config()
        domain = obj['configuration']['domain'] if obj['configuration']['domain'] else 'undefined'
        states = list(obj['states'].keys())
        hostnames = list(obj['hostnames'].keys())
        for prototype in _prototypes:
            if prototype.get('name') not in states:
                obj['states'][prototype.get('name')] = 'stopped'

            obj['hostnames'][prototype.get('name')] = '{}.{}'.format(prototype.get('name'), domain)

        self.save_fresh_config(obj)

    def write_config(self, _name, _val):
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

    def get_hostnames(self):
        obj = self.get_fresh_config()
        return obj['hostnames']

    def get_port(self):
        obj = self.get_fresh_config()
        return int(obj['configuration']['port'])

    def get_ipaddress(self):
        obj = self.get_fresh_config()
        return obj['configuration']['ipaddress']

    def get_domain(self):
        obj = self.get_fresh_config()
        return obj['configuration']['domain']

class CONFIGURATION(CONFIG):

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
                self.config_writer.write_config('domain', _val[0])
                pull.session(
                    ('#29cc0c bold', '$ '),
                    ('', 'Domain'),
                    ('#29cc0c', ' => '),
                    ('', _val[0])
                )
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
            obj = re.match(self.REGEX_IPADDRESS, _val[0])
            if obj:
                self.config_writer.write_config('ipaddress', _val[0])
                pull.session(
                    ('#29cc0c bold', '$ '),
                    ('', 'IP Address'),
                    ('#29cc0c', ' => '),
                    ('', _val[0])
                )
                pull.session(
                    ('#bb00c2 bold', '; '),
                    ('', 'You need to restart proxverter for changes to take effect')
                )
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
            if os.path.isdir(_val[0]):
                self.config_writer.write_config('prototypes_path', _val[0])
                pull.session(
                    ('#29cc0c bold', '$ '),
                    ('', 'Prototypes Path'),
                    ('#29cc0c', ' => '),
                    ('', _val[0])
                )
                pull.session(
                    ('#bb00c2 bold', '; '),
                    ('', 'You need to restart proxverter for changes to take effect')
                )
            else:
                pull.session(
                    ('#bb00c2 bold', '; '),
                    ('', 'The provided prototypes directory does not exists: '),
                    ('#bb00c2', _val[0])
                )
        else:
            self.invalid()

    def write_port(self, _val):
        if _val:
            _p = _val[0]
            if _p.isnumeric():
                _p = int(_p)
                if _p > 0 and _p < 65536:
                    self.config_writer.write_config('port', str(_p))
                    pull.session(
                        ('#29cc0c bold', '$ '),
                        ('', 'Port Number'),
                        ('#29cc0c', ' => '),
                        ('', _val[0])
                    )
                    pull.session(
                        ('#bb00c2 bold', '; '),
                        ('', 'You need to restart proxverter for changes to take effect')
                    )
                else:
                    pull.session(
                        ('#bb00c2 bold', '; '),
                        ('', 'The provided port value must be 1-65535')
                    )
            else:
                pull.session(
                    ('#bb00c2 bold', '; '),
                    ('', 'The provided port value must be an Integer: '),
                    ('#bb00c2', _val[0])
                )
        else:
            self.invalid()

    def list_config(self):
        obj = self.get_fresh_config()
        obj = obj['configuration']

        for (key, val) in obj.items():
            pull.session(('#37adbf bold', '- '), ('', '{}: '.format(key)), ('#37adbf', val))

    def execute(self):
        if self.parser.subcommand == "DOMAIN":
            self.write_domain(self.parser.args)
        elif self.parser.subcommand == "IP_ADDRESS":
            self.write_ipaddress(self.parser.args)
        elif self.parser.subcommand == "PROTOTYPES_PATH":
            self.write_prototypes_path(self.parser.args)
        elif self.parser.subcommand == "PORT":
            self.write_port(self.parser.args)
        elif self.parser.subcommand == "options":
            self.list_config()
        else:
            self.invalid()
