import click
import sys


def success(text):
    click.echo(click.style("SUCCESS: ", fg="green", bold=True) + text)


def warn(text):
    click.echo(click.style("WARN: ", fg="yellow", bold=True) + text)


def error(text, exit=False):
    click.echo(click.style("ERROR: ", fg="red", bold=True) + text)
    if exit:
        sys.exit(1)
