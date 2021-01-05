import os
import sys
import socket
import argparse
import datetime
import threading
import configparser

## From Imports
from multiprocessing import Process
from tabulate import tabulate
from pull import PULL
from parser import PARSER
from termcolor import colored
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

## Handler Imports
from handlers import handlers_parser
from handlers import list_commands
from handlers import CONFIGURATION
from handlers import CONFIGREADER
from handlers import CONFIGWRITER
from handlers import PROTOTYPES

## Pilus Imports
from pilus import PROXYRUNNER

## Declarations
pull = PULL()

## Proxverter Main Class
class PROXVERTER:
	STOPPER = False

	STYLE = Style.from_dict({
		'timer': '#0096d6 bold',
		'headers': '#d40000',
		'': '#8c8c8c'
	})

	def __init__(self, prs):
		self.debug = prs.debug
		self.prototypes_path = prs.prototypes_path
		self.prototypes = prs.prototypes
		self.config_reader = CONFIGREADER()
		self.config_writer = CONFIGWRITER()

	def populate(self):
		if not self.config_reader.exists():
			self.config_writer.create_config(self.prototypes)
		else:
			self.config_writer.update_config(self.prototypes)

	def update_prototypes(self):
		for prototype in self.prototypes:
			self.prototypes[self.prototypes.index(prototype)]['state'] = self.config_reader.get_state(prototype.get('name'))
			self.prototypes[self.prototypes.index(prototype)]['hostname'] = self.config_reader.get_hostname(prototype.get('name'))

	def show_prototypes(self):
		toprint = []
		for prototype in self.prototypes:
			toappend = [
				colored(prototype.get('name'), 'yellow'),
				colored(prototype.get('proto'), 'white'),
				colored(prototype.get('creator'), 'cyan'),
				colored(prototype.get('state'), 'green'),
				colored(str(len(prototype.get('domains'))), 'red'),
				colored(prototype.get('hostname'), 'white')
			]
			toprint.append(toappend)

		headers = [
			colored('Prototype', 'grey', attrs=['bold']),
			colored('Protocol', 'grey', attrs=['bold']),
			colored('Creator', 'grey', attrs=['bold']),
			colored('Status', 'grey', attrs=['bold']),
			colored('Domains', 'grey', attrs=['bold']),
			colored('Hostname', 'grey', attrs=['bold'])
		]

		sys.stdout.write('\n')
		print(tabulate(toprint, headers=headers, tablefmt='orgtbl'))
		sys.stdout.write('\n')

	def show_prints(self):
		pull.session(('#37adbf bold', '- '), ('', 'Running in stable mode. Phishlets detected: '), ('#37adbf', str(len(self.prototypes))))
		pull.session(('#37adbf bold', '- '), ('', 'Configuration: '), ('#37adbf', self.config_reader.BASEPATH))
		pull.session(('#37adbf bold', '- '), ('', 'Prototypes: '), ('#37adbf', self.prototypes_path))
		pull.session(('#37adbf bold', '- '), ('', 'Debug Mode: '), ('#37adbf', 'On' if self.debug else 'Off'))
		pull.session(('#37adbf bold', '- '), ('', 'Binding Port: '), ('#37adbf', str(self.config_reader.get_port())))
		sys.stdout.write('\n')

	def show_invalid_syntax(self):
		pull.session(('#bb00c2 bold', '~ '), ('', 'Invalid Syntax'))

	def check_ports(self):
		p = self.config_reader.get_port()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.bind(( '', p ))
			s.close()
		except OSError:
			pull.session(('#bb00c2 bold', '~ '), ('', 'Unable to bind to port number '), ('#bb00c2', str(p)))
			sys.exit(-1)

	def handler(self, _val):
		parser = handlers_parser(_val)

		if parser.command not in list_commands():
			return self.show_invalid_syntax()

		if parser.command == 'set' or parser.command == 'show':
			configuration = CONFIGURATION(parser)
			configuration.execute()
		elif parser.command == 'prototypes':
			prototypes    = PROTOTYPES(parser, self)
			prototypes.execute()
		self.populate()
		self.update_prototypes()

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
				pull.session(('#bb00c2 bold', '; '), ('', 'Press'), ('#bb00c2 bold', ' CTRL+D '), ('', 'or enter'), ('#bb00c2 bold', ' \'exit\' '), ('', 'to exit from Proxverter'))
			except EOFError:
				break

		self.STOPPER = True

	def start_proxy_server(self):
		self.proxy = PROXYRUNNER(self.config_reader.get_ipaddress(), self.config_reader.get_port(), self)
		self.proxy.kickoff()

def main():
	pull.logo()
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--prototypes', dest="prototypes", default="", type=str, help="Path to Prototypes Folder")
	parser.add_argument('--debug', dest="debug", default=False, action="store_true", help="Turn on Debug mode")
	parser = parser.parse_args()
	parser = PARSER(parser)
	parser.validate()

	proxverter = PROXVERTER(parser)
	proxverter.populate()
	proxverter.update_prototypes()
	proxverter.show_prototypes()
	proxverter.check_ports()
	proxverter.show_prints()

	t = threading.Thread(target=proxverter.start_terminal)
	t.daemon = True
	t.start()

	server = Process(target=proxverter.start_proxy_server)
	server.start()

	while not proxverter.STOPPER:
		pass

	server.terminate()
	server.join()

	pull.session(('#bb00c2 bold', '; '), ('', 'Shutting Down. Hope to see you soon sire. '))

if __name__ == "__main__":
	main()
