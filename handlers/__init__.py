import argparse

def list_commands():
    return (
        'configuration',
        'prototypes',
    )

def handlers_parser(toparse):
    toparse = ' '.join(toparse.split())
    toparse = toparse.lstrip().rstrip().split(" ")

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command")
    parser.add_argument("subcommand", nargs="*")

    parser = parser.parse_args(toparse)
    print(parser.command)
    print(parser.subcommand)
