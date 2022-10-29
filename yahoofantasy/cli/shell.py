import click
import code
from yahoofantasy import Context
import sys
from .utils import error

import logging

logging.basicConfig(level=logging.INFO)


@click.command()
def shell():
    try:
        ctx = Context()  # noqa
    except Exception:
        error(
            "Could not find any yahoofantasy login details, be sure to run `yahoofantasy login` from this directory first"
        )
        sys.exit(1)

    code.interact("yahoofantasy Context object available as `ctx`", local=locals())
