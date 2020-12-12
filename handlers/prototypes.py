

class PROTOTYPES:

    def __init__(self, prs, _prox):
        self.parser = prs
        self.proxverter = _prox

    def invalid(self):
        pull.session(
            ('#d9ce0b bold', '~ '),
            ('', 'Invalid Syntax'),
        )

    def runner(self):
        return

    def execute(self):
        sub = self.parser.subcommand

        if sub == 'list':
            self.proxverter.show_prototypes()
        elif sub == 'run':
            self.runner(self.parser.args)
        else:
            self.invalid()
