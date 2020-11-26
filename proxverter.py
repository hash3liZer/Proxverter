import os
import sys
import argparse
from tabulate import tabulate
from pull import PULL
from parser import PARSER

## Declarations
pull = PULL()

class PROXVERTER:

	def __init__(self, prs):
		self.prototypes = prs.prototypes

	def show_prototypes(self):
		toprint = []
		for prototype in self.prototypes:
			toappend = [
				pull.YELLOW + prototype[0] + pull.END,
				pull.BLUE + '@hash3liZer' + pull.END,
				pull.GREEN + 'Running' + pull.END,
				pull.RED + '23' + pull.END,
				pull.BOLD + 'google.com.picker.com' + pull.END
			]
			toprint.append(toappend)

		headers = [
			pull.DARKCYAN + 'Prototype' + pull.END,
			pull.DARKCYAN + 'Author' + pull.END,
			pull.DARKCYAN + 'Status' + pull.END,
			pull.DARKCYAN + 'Urls'   + pull.END,
			pull.DARKCYAN + 'Hostname' + pull.END
		]

		sys.stdout.write('\n')
		print(tabulate(toprint, headers=headers, tablefmt='orgtbl'))
		sys.stdout.write('\n')

def main():
	pull.logo()
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--prototypes', dest="prototypes", default="", type=str, help="Path to Prototypes Folder")
	parser = parser.parse_args()
	parser = PARSER(parser)

	proxverter = PROXVERTER(parser)
	proxverter.show_prototypes()

if __name__ == "__main__":
	main()
