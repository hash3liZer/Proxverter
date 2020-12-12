import configparser
import os
from pull import PULL

pull = PULL()

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

    def execute(self):
        if self.parser.subcommand == "domain":
            return
        elif self.parser.subcommand == "ipaddress":
            return
        elif self.parser.subcommand == "prototypes_path":
            return
        elif self.parser.subcommand == "certificates_path":
            return
        elif self.parser.subcommand == "debug":
            self.write_debug(self.parser.args)
        elif self.parser.subcommand == "port":
            return
        elif self.parser.subcommand == "list":
            return
        else:
            self.invalid()
