import click
from .login import login
from .dump import dump


@click.group()
def yahoofantasy():
    pass


yahoofantasy.add_command(login)
yahoofantasy.add_command(dump)
