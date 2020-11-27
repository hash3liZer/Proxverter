import os
import sys
import argparse
import datetime
from tabulate import tabulate
from pull import PULL
from parser import PARSER
from termcolor import colored
from handlers import handlers_parser
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

## Declarations
pull = PULL()

class PROXVERTER:

	STYLE = Style.from_dict({
		'timer': '#0096d6 bold',
		'headers': '#d40000',
		'': '#8c8c8c'
	})

	def __init__(self, prs):
		self.prototypes = prs.prototypes

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

	def handler(self, _val):
		parser = handlers_parser(_val)

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

def main():
	pull.logo()
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--prototypes', dest="prototypes", default="", type=str, help="Path to Prototypes Folder")
	parser = parser.parse_args()
	parser = PARSER(parser)

	proxverter = PROXVERTER(parser)
	proxverter.show_prototypes()
	proxverter.start_terminal()
	pull.session(
		('#d9ce0b bold', '~ '),
		('', 'Shutting Down. Hope to see you soon sire. ')
	)

if __name__ == "__main__":
	main()
