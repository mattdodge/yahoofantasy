import click
from .login import login
from .dump import dump
from .shell import shell


@click.group()
def yahoofantasy():
    pass


yahoofantasy.add_command(login)
yahoofantasy.add_command(dump)
yahoofantasy.add_command(shell)
