

class PROTOTYPES:

    def __init__(self, prs, _prox):
        self.parser = prs
        self.proxverter = _prox

    def invalid(self):
        pull.session(
            ('#d9ce0b bold', '~ '),
            ('', 'Invalid Syntax'),
        )

    def authorize(self, _args):
        prototype_name = _args[0]

    def execute(self):
        sub = self.parser.subcommand

        if sub == 'list':
            self.proxverter.show_prototypes()
        elif sub == 'authorize':
            self.authorize(self.parser.args)
        else:
            self.invalid()
