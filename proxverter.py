import os
import sys
import argparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class PULL:

	WHITE = '\033[1m\033[0m'
	PURPLE = '\033[1m\033[95m'
	CYAN = '\033[1m\033[96m'
	DARKCYAN = '\033[1m\033[36m'
	BLUE = '\033[1m\033[94m'
	GREEN = '\033[1m\033[92m'
	YELLOW = '\033[1m\033[93m'
	RED = '\033[1m\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'
	LINEUP = '\033[F'

	def __init__(self):
		if not self.support_colors:
			self.win_colors()

	def support_colors(self):
		plat = sys.platform
		supported_platform = plat != 'Pocket PC' and (plat != 'win32' or \
														'ANSICON' in os.environ)
		is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
		if not supported_platform or not is_a_tty:
			return False
		return True

    def halt(self, mss):
        sys.exit( self.RED + "[~]" + self.END + mss )

pull = PULL()

class PARSER:

    def __init__(self, prs):
        self.templates = self.templates(prs.templates)

    def templates(self, arg):
        templates = []
        dirnamer = ""
        if arg:
            if os.path.isdir(arg):
                dirnamer = arg
            else:
                pull.halt("The provided templates directory doesn't exist!")
        else:
            dirnamer = os.path.join(os.path.dirname(__file__))

        files = os.listdir(dirnamer)
        for file in files:
            file = os.path.join(dirnamer, file)
            if file.endswith(".yaml"):
                data = open(file, "r").read().splitlines()
                templates.append(tuple(data))

        return templates

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--templates', dest="templates", default="", type=str, help="Folder containing all the proxying templates")

    parser = parser.parse_args()
    parser = PARSER(parser)

if __name__ == "__main__":
    main()
