import configparser
from pull import PULL

pull = PULL()

class CONFIGURATION:

    def __init__(self, prs):
        self.parser = prs

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
            return
        elif self.parser.subcommand == "port":
            return
        elif self.parser.subcommand == "list":
            return
        else:
            pull.session(
    			('#d9ce0b bold', '~ '),
    			('', 'Invalid Syntax'),
    		)
