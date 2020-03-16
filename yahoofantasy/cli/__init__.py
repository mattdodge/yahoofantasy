import click
from .login import login


@click.group()
def yahoofantasy():
    pass


yahoofantasy.add_command(login)
