import os
import sys
from pull import PULL

pull = PULL()

class PARSER:

    DEF_PROTOTYPES = "/usr/share/proxverter/prototypes"

    def __init__(self, prs):
        self.prototypes = self.prototypes(prs.prototypes)

    def prototypes(self, _val):
        rtval = []
        dirnamer = ""

        if _val:
            if os.path.isdir(_val):
                dirnamer = os.path.join(os.path.dirname(__file__), _val)
            else:
                pull.halt("The provided prototypes directory doesn't exist!")
        else:
            if not os.path.isdir(self.DEF_PROTOTYPES):
                pull.halt("Unable to Locate Prototypes Directory")

            dirnamer = self.DEF_PROTOTYPES

        files = os.listdir(dirnamer)
        for file in files:
            file = os.path.join(dirnamer, file)
            if file.endswith(".yaml"):
                data = open(file, "r").read().splitlines()
                rtval.append((file.split("/")[-1].split(".")[0], tuple(data)))

        pull.info("Parsed {} Prototypes under {}".format(
            pull.GREEN + str(len(rtval)) + pull.END,
            pull.BLUE + "Prototypes" + pull.END
        ))

        return rtval
