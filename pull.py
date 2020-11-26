import os
import sys

__LOGO__ = """
 ____          __  __              _____    ____
|  _ \\ _ __ ___\\ \/ /_   _____ _ _|_   _|__|  _ \\
| |_) | '__/ _ \\\\  /\\ \ / / _ \\ '__|| |/ _ \\ |_) |
|  __/| | | (_) /  \\ \\ V /  __/ |   | |  __/  _ <
|_|   |_|  \\___/_/\\_\\ \\_/ \\___|_|   |_|\\___|_| \\_\\

                    @hash3liZer
"""

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

    def info(self, mss):
        print(
            self.BLUE + "[*] " + self.END + mss
        )

    def halt(self, mss):
        sys.exit( self.RED + "[~] " + self.END + mss )

    def logo(self):
        print(
            self.BOLD + self.YELLOW + __LOGO__ + self.END
        )
