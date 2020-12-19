import os
import sys
import datetime
from pathlib import Path
from termcolor import colored
from prompt_toolkit import print_formatted_text as print_format
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

__LOGO__ = """
 ____          __  __              _____    ____
|  _ \\ _ __ ___\\ \/ /_   _____ _ _|_   _|__|  _ \\
| |_) | '__/ _ \\\\  /\\ \ / / _ \\ '__|| |/ _ \\ |_) |
|  __/| | | (_) /  \\ \\ V /  __/ |   | |  __/  _ <
|_|   |_|  \\___/_/\\_\\ \\_/ \\___|_|   |_|\\___|_| \\_\\

                    @hash3liZer
"""

class PULL:
    BASE_DIR = Path(__file__).resolve().parent
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

    STYLE = Style.from_dict({
		'timer': '#0096d6 bold',
		'headers': '#d40000',
		'': '#d1d1d1'
	})

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

    def info(self, mss):
        print(
            colored("[*]", "blue", attrs=['bold']), mss
        )

    def session(self, *args):
        mss = [
            ('class:timer', '[{}] '.format(str(datetime.datetime.now().time()).split(".")[0])),
        ]

        for arg in args:
            mss.append(arg)

        mss = FormattedText(mss)
        print_format(mss, style=self.STYLE)

    def halt(self, mss):
        sys.exit( self.RED + "[~] " + self.END + mss )

    def logo(self):
        print(
            self.BOLD + self.YELLOW + __LOGO__ + self.END
        )
