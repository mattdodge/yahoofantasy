import click
from .login import login
from .dump import dump
from .shell import shell
from .clear_cache import clear_cache


@click.group()
def yahoofantasy():
    pass


yahoofantasy.add_command(login)
yahoofantasy.add_command(dump)
yahoofantasy.add_command(shell)
yahoofantasy.add_command(clear_cache)
