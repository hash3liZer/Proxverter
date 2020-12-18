from pilus.proxy import PROXY
import logging
import click

## Disable Flask Logging completely
log = logging.getLogger('werkzeug')
log.disabled = True

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho
