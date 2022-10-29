import click
from yahoofantasy import Context
import yahoofantasy.util.persistence as persistence
import sys
from .utils import error, success

RETAINED_KEYS = ["auth"]


@click.command()
def clear_cache():
    try:
        ctx = Context()
    except Exception:
        error("Could not find any cached yahoofantasy data in this directory")
        sys.exit(1)

    persistence.clear(RETAINED_KEYS, ctx._persist_key)
    success("Cache cleared")
