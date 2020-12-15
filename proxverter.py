import os
import sys
import socket
import argparse
import datetime
import threading
import configparser
from tabulate import tabulate
from pull import PULL
from parser import PARSER
from termcolor import colored
from handlers import handlers_parser
from handlers import list_commands
from handlers import CONFIGURATION
from handlers import PROTOTYPES
from pilus import PROXY
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from pathlib import Path

## Declarations
pull = PULL()
BASE_DIR = Path(__file__).resolve().parent

class PROXVERTER:

	STYLE = Style.from_dict({
		'timer': '#0096d6 bold',
		'headers': '#d40000',
		'': '#8c8c8c'
	})

	def __init__(self, prs):
		self.prototypes = prs.prototypes

	def populate(self):
		if not os.path.isfile(os.path.join(BASE_DIR, 'config.ini')):
			pull.info("Created a new configuration file for the project")

			obj = configparser.ConfigParser()
			obj['configuration'] = {
				'domain': '',
				'ipaddress': '',
				'certificates_path': '/usr/share/proxverter/',
				'prototypes_path': '/usr/share/proxverter/prototypes',
				'debug': False,
				'port': 443,
			}

			fl = open(os.path.join(BASE_DIR, 'config.ini'), 'w')
			obj.write(fl)

	def show_prototypes(self):
		toprint = []
		for prototype in self.prototypes:
			toappend = [
				colored(prototype[0], 'yellow', attrs=['bold']),
				colored('@hash3liZer', 'cyan'),
				colored('Running', 'green'),
				colored('3', 'red'),
				colored('www.google.com', 'white')
			]
			toprint.append(toappend)

		headers = [
			colored('Prototype', 'grey', attrs=['bold']),
			colored('Author', 'grey', attrs=['bold']),
			colored('Status', 'grey', attrs=['bold']),
			colored('Urls', 'grey', attrs=['bold']),
			colored('Hostname', 'grey', attrs=['bold'])
		]

		sys.stdout.write('\n')
		print(tabulate(toprint, headers=headers, tablefmt='orgtbl'))
		sys.stdout.write('\n')

	def show_invalid_syntax(self):
		pull.session(
			('#d9ce0b bold', '~ '),
			('', 'Invalid Syntax'),
		)

	def check_ports(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.bind(( '', 80 ))
			s.close()
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(( '', 443 ))
			s.close()
		except KeyboardInterrupt:
			pull.session(
				('#d9ce0b bold', '~ '),
				('', 'Unable to Bind to Ports 80 and 443')
			)
			sys.exit(-1)

	def handler(self, _val):
		parser = handlers_parser(_val)

		if parser.command not in list_commands():
			return self.show_invalid_syntax()

		if parser.command == 'configuration':
			configuration = CONFIGURATION(parser)
			configuration.execute()
		elif parser.command == 'prototypes':
			prototypes    = PROTOTYPES(parser, self)
			prototypes.execute()

	def start_terminal(self):
		session = PromptSession()

		while 1:
			mss = [
				('class:timer', '[{}] '.format(str(datetime.datetime.now().time()).split(".")[0])),
				('class:headers', '$~ '),
			]

			try:
				resp = session.prompt(mss, style=self.STYLE)
				if resp:
					if resp == "exit": break
					self.handler(resp)
			except KeyboardInterrupt:
				pull.session(
					('#d9ce0b bold', '~ '),
					('', 'Press'),
					('#d9ce0b bold', ' CTRL+D '),
					('', 'or enter'),
					('#d9ce0b bold', ' \'exit\' '),
					('', 'to exit from Proxverter'),
				)
			except EOFError:
				break

	def start_proxy_server(self):
		proxy = PROXY()
		proxy.kickoff()

def main():
	pull.logo()
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--prototypes', dest="prototypes", default="", type=str, help="Path to Prototypes Folder")
	parser = parser.parse_args()
	parser = PARSER(parser)

	proxverter = PROXVERTER(parser)
	proxverter.populate()
	proxverter.show_prototypes()
	proxverter.check_ports()

	t = threading.Thread(target=proxverter.start_proxy_server)
	t.daemon = True
	t.start()

	proxverter.start_terminal()
	pull.session(
		('#d9ce0b bold', '~ '),
		('', 'Shutting Down. Hope to see you soon sire. ')
	)

if __name__ == "__main__":
	main()
